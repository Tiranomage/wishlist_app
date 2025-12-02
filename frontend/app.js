const API_BASE = window.API_BASE || '/api';

const qs = (sel) => document.querySelector(sel);
const qsa = (sel) => Array.from(document.querySelectorAll(sel));

function showToast(message, type = 'ok') {
	const toast = qs('#toast');
	toast.textContent = message;
	toast.classList.remove('hidden');
	toast.classList.remove('ok', 'warn', 'err');
	toast.classList.add(type);
	setTimeout(() => toast.classList.add('hidden'), 2500);
}

function token() {
	return localStorage.getItem('access_token');
}

function setAuthedUI(authed) {
	qs('#nav-login').classList.toggle('hidden', authed);
	qs('#nav-logout').classList.toggle('hidden', !authed);
	qs('#auth-section').classList.toggle('hidden', authed);
	qs('#dashboard').classList.toggle('hidden', !authed);
  }

async function api(path, opts = {}) {
	const headers = Object.assign({'Content-Type': 'application/json'}, opts.headers || {});
	const t = token();
	if (t) headers['Authorization'] = `Bearer ${t}`;
	let res = await fetch(`${API_BASE}${path}`, { ...opts, headers });
	
	// ДОБАВЛЕНО: Проверка Content-Type ДО парсинга JSON
	const contentType = res.headers.get('content-type');
	
	if (!res.ok) {
		let detail = `HTTP error! status: ${res.status}`;
		try {
			// ИСПРАВЛЕНО: Проверяем тип контента перед парсингом
			if (contentType && contentType.includes('application/json')) {
				const data = await res.json();
				detail = data.detail || JSON.stringify(data);
			} else {
				// Если ответ не JSON - получаем текст
				detail = await res.text();
				// ДОБАВЛЕНО: Удаляем HTML-теги для читаемости
				if (detail.startsWith('<!DOCTYPE') || detail.includes('<html')) {
					detail = 'Server returned HTML instead of JSON. Check API endpoint.';
				}
			}
		} catch (e) {
			detail = 'Failed to parse error response';
		}

		// 401: попробовать обновить access_token по refresh_token и повторить запрос
		if (res.status === 401) {
			const rt = localStorage.getItem('refresh_token');
			if (rt) {
				try {
					const r = await fetch(`${API_BASE}/auth/refresh`, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ refresh_token: rt }) });
					if (r.ok) {
						const tokens = await r.json();
						localStorage.setItem('access_token', tokens.access_token);
						localStorage.setItem('refresh_token', tokens.refresh_token);
						headers['Authorization'] = `Bearer ${tokens.access_token}`;
						res = await fetch(`${API_BASE}${path}`, { ...opts, headers });
						if (res.ok) {
							const ct2 = res.headers.get('content-type') || '';
							return ct2.includes('application/json') ? res.json() : res.text();
						}
					}
				} catch {}
			}
			// refresh не удался — выходим из аккаунта
			localStorage.removeItem('access_token');
			localStorage.removeItem('refresh_token');
			setAuthedUI(false);
		}
		throw new Error(detail);
	}

	if (res.status === 204) return null;
	
	// ДОБАВЛЕНО: КРИТИЧЕСКАЯ ПРОВЕРКА - убеждаемся что ответ JSON
	if (!contentType || !contentType.includes('application/json')) {
		const text = await res.text();
		// ДОБАВЛЕНО: Анализируем HTML-ответ для диагностики
		const isHtml = text.startsWith('<!DOCTYPE') || text.includes('<html');
		throw new Error(
			isHtml 
				? 'Server returned HTML instead of JSON. Check API_BASE configuration.' 
				: 'Invalid JSON response received'
		);
	}

	return res.json();
}

// Auth
qs('#register-form').addEventListener('submit', async (e) => {
	e.preventDefault();
	const email = qs('#register-email').value.trim();
	const password = qs('#register-password').value;
	if (!email || password.length < 8) return showToast('Invalid email or password', 'warn');
	try {
		await api('/auth/register', { method: 'POST', body: JSON.stringify({ email, password }) });
		showToast('Registered. You can login now.');
	} catch (err) { showToast(err.message, 'err'); }
});

qs('#login-form').addEventListener('submit', async (e) => {
	e.preventDefault();
	const email = qs('#login-email').value.trim();
	const password = qs('#login-password').value;
	try {
		const data = await api('/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) });
		localStorage.setItem('access_token', data.access_token);
		localStorage.setItem('refresh_token', data.refresh_token);
		setAuthedUI(true);
		await loadDashboard();
		showToast('Logged in');
	} catch (err) { showToast(err.message, 'err'); }
});

qs('#reset-form').addEventListener('submit', async (e) => {
	e.preventDefault();
	const email = qs('#reset-email').value.trim();
	try {
		await api('/auth/password-reset', { method: 'POST', body: JSON.stringify({ email }) });
		showToast('Reset token printed to backend console');
	} catch (err) { showToast(err.message, 'err'); }
});

qs('#nav-logout').addEventListener('click', () => {
	localStorage.removeItem('access_token');
	localStorage.removeItem('refresh_token');
	setAuthedUI(false);
});

// Dashboard
async function loadDashboard() {
	try {
		const items = await api('/wishlists');
		renderWishlists(items);
	} catch (err) { showToast(err.message, 'err'); }
}

function renderWishlists(items) {
	const container = qs('#wishlists');
	container.innerHTML = '';
	for (const w of items) {
		const el = document.createElement('div');
		el.className = 'card';
		el.innerHTML = `
			<div class="row">
				<h3 style="margin:0">${w.title}</h3>
				<span class="badge ${w.is_public ? 'ok' : 'warn'}">${w.is_public ? 'Public' : 'Private'}</span>
				<span class="badge">${w.gift_count || 0} gifts</span>
			</div>
			<p>${w.description || ''}</p>
			<div class="row">
				<button class="secondary" data-act="add-gift" data-id="${w.id}">Add Gift</button>
				<button class="secondary" data-act="list-gifts" data-id="${w.id}">View Gifts</button>
			</div>
		`;
		container.appendChild(el);
	}

	container.addEventListener('click', async (e) => {
		const btn = e.target.closest('button');
		if (!btn) return;
		const id = btn.getAttribute('data-id');
		const act = btn.getAttribute('data-act');
		if (act === 'add-gift') {
			const name = prompt('Gift name');
			if (!name) return;
			const priceIn = prompt('Price (optional)');
			const price = priceIn ? Number(priceIn) : undefined;
			try {
				await api(`/gifts/wishlist/${id}`, { method: 'POST', body: JSON.stringify({ name, price }) });
				await loadDashboard();
				showToast('Gift added');
			} catch (err) { showToast(err.message, 'err'); }
		}
		if (act === 'list-gifts') {
			try {
				const gifts = await api(`/gifts/wishlist/${id}`);
				alert(gifts.map(g => `${g.name} - ${g.status}`).join('\n') || 'No gifts');
			} catch (err) { showToast(err.message, 'err'); }
		}
	});
}

// Create wishlist (minimal prompt)
qs('#create-wishlist-btn').addEventListener('click', async () => {
	const title = prompt('Wishlist title');
	if (!title) return;
	const is_public = confirm('Make it public? OK=yes, Cancel=no');
	try {
		await api('/wishlists', { method: 'POST', body: JSON.stringify({ title, is_public }) });
		await loadDashboard();
		showToast('Wishlist created');
	} catch (err) { showToast(err.message, 'err'); }
});

// Public
qs('#refresh-public').addEventListener('click', async () => {
    try {
      const q = qs('#public-search-input').value.trim();
      const params = new URLSearchParams({ public: 'true' });
      if (q) params.append('q', q);
      const items = await api(`/wishlists?${params.toString()}`);
      renderPublic(items);
    } catch (err) { 
      showToast(`Failed to load public wishlists: ${err.message}`, 'err'); 
    }
  });

function renderPublic(items) {
	const container = qs('#public-wishlists');
	container.innerHTML = '';
	for (const w of items) {
		const el = document.createElement('div');
		el.className = 'card';
		el.innerHTML = `
			<div class="row"><strong>${w.title}</strong> <span class="badge">${w.owner_email || ''}</span></div>
			<p>${w.description || ''}</p>
		`;
		container.appendChild(el);
	}
}

// Initialize
(() => {
	setAuthedUI(!!token());
	if (token()) loadDashboard();
})();



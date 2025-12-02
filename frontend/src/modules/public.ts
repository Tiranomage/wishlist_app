import { api, toast } from '../main';

export function setupPublic() {
	const refreshBtn = document.querySelector<HTMLButtonElement>('#refresh-public');
	const input = document.querySelector<HTMLInputElement>('#public-search-input');
    const tokenInput = document.querySelector<HTMLInputElement>('#token-input');
    const tokenBtn = document.querySelector<HTMLButtonElement>('#token-search');

	async function load() {
		try {
			const q = input?.value.trim() || '';
			const params = new URLSearchParams({ public: 'true' });
			if (q) params.append('q', q);
			const items = await api(`/wishlists?${params.toString()}`);
			render(items);
		} catch (e:any) { 
			toast(e.message,'err'); 
		}
	}

	function render(items: any[]) {
		const container = document.querySelector<HTMLDivElement>('#public-wishlists')!;
		container.innerHTML = '';
		
		if (items.length === 0) {
			container.innerHTML = '<div class="card"><p>No public wishlists found.</p></div>';
			return;
		}
		
		for (const w of items) {
			const el = document.createElement('div'); 
			el.className = 'card';
			el.innerHTML = `<div class="row"><strong>${w.title}</strong><span class="badge">${w.owner_email||''}</span><span class="badge public">${w.gift_count||0} gifts</span></div><p>${w.description||'<em>No description</em>'}</p>`;
			container.appendChild(el);
		}
	}

	refreshBtn?.addEventListener('click', load);

    tokenBtn?.addEventListener('click', async () => {
        const token = (tokenInput?.value || '').trim().toUpperCase();
        if (!token || token.length !== 5) {
			toast('Please enter a valid 5-character token', 'warn');
			return;
		}
        try {
            const wl = await api(`/wishlists/token/${token}`);
            const container = document.querySelector<HTMLDivElement>('#public-wishlists')!;
            container.innerHTML = '';
            const el = document.createElement('div'); 
			el.className = 'card';
            el.innerHTML = `<div class="row"><strong>${wl.title}</strong><span class="badge">share: ${wl.share_token}</span></div><p>${wl.description||'<em>No description</em>'}</p>`;
            container.appendChild(el);
        } catch (e:any) { 
			toast(e.message, 'err'); 
		}
    });
}



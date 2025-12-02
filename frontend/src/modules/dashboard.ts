import { api, toast } from '../main';

export async function loadDashboard() {
	try { const items = await api('/wishlists'); render(items); } catch (e: any) { toast(e.message, 'err'); }
}


export function render(items: any[]) {
	const container = document.querySelector<HTMLDivElement>('#wishlists')!;
	container.innerHTML = '';
	for (const w of items) {
		const el = document.createElement('div'); el.className = 'card';
		el.innerHTML = `
			<div class="row" data-act="open" data-id="${w.id}"><h3 style="margin:0">${w.title}</h3><span class="badge ${w.is_public ? 'ok':'warn'}">${w.is_public ? 'Public':'Private'}</span><span class="badge">${w.gift_count||0} gifts</span></div>
			<p>${w.description||''}</p>`;
		container.appendChild(el);
	}
}

export function setupDashboard() {
	const createBtn = document.querySelector<HTMLButtonElement>('#create-wishlist-btn');
	const createForm = document.querySelector<HTMLFormElement>('#create-wishlist-form');

	const container = document.querySelector<HTMLDivElement>('#wishlists')!;
	if (!container.dataset.bound) {
		container.addEventListener('click', async (e) => {
			const openEl = (e.target as HTMLElement).closest('[data-act="open"]');
			const btn = (e.target as HTMLElement).closest('button');
			if (!btn && !openEl) return;
			if (openEl) {
				const id = openEl.getAttribute('data-id');
				await openDetail(Number(id));
				return;
			}
			const id = btn!.getAttribute('data-id'); const act = btn!.getAttribute('data-act');
			if (act === 'add-gift') {
				const name = prompt('Gift name'); if (!name) return; const priceIn = prompt('Price (optional)'); const price = priceIn ? Number(priceIn) : undefined;
				try { await api(`/gifts/wishlist/${id}`, { method: 'POST', body: JSON.stringify({ name, price }) }); await loadDashboard(); toast('Gift added'); } catch (e:any) { toast(e.message,'err'); }
			}
		});
		container.dataset.bound = '1';
	}

	createForm?.addEventListener('submit', async (e) => {
		e.preventDefault();
		const title = (document.querySelector('#wl-title') as HTMLInputElement).value.trim();
		const description = (document.querySelector('#wl-desc') as HTMLTextAreaElement).value.trim();
		const is_public = (document.querySelector('#wl-public') as HTMLInputElement).checked;
		try { await api('/wishlists', { method: 'POST', body: JSON.stringify({ title, description, is_public }) }); (e.target as HTMLFormElement).reset(); await loadDashboard(); toast('Wishlist created'); } catch (err:any) { toast(err.message,'err'); }
	});

	// Initial load if visible
	if (document.querySelector('#dashboard') && !document.querySelector('#dashboard')!.classList.contains('hidden')) { void loadDashboard(); }
}

async function openDetail(wishlistId: number) {
	try {
		const detail = document.querySelector('#detail')!;
		const dashboard = document.querySelector('#dashboard')!;
		dashboard.classList.add('hidden'); detail.classList.remove('hidden');
		// load info
		const lists = await api('/wishlists');
		const w = (lists as any[]).find((x)=>x.id===wishlistId);
		if (!w) return;
		(document.querySelector('#detail-token') as HTMLDivElement).textContent = w.share_token ? `Token: ${w.share_token}` : '';
		const content = document.querySelector('#detail-content') as HTMLDivElement;
		const gifts = await api(`/gifts/wishlist/${wishlistId}`);
		content.innerHTML = `<h3 style="margin-top:0">${w.title}</h3><p>${w.description||''}</p>`+
			`<table class="table"><thead><tr><th>Name</th><th>Status</th><th>Price</th><th>Actions</th></tr></thead>`+
			`<tbody>${(gifts as any[]).map((g:any)=>`<tr><td>${g.name}</td><td>${g.status}</td><td>${g.price??''}</td>`+
			`<td><button class="secondary" data-act="del-gift" data-gid="${g.id}">Delete</button></td></tr>`).join('')}</tbody></table>`+
			`<div class="row"><button id="add-gift-detail" class="secondary">Add Gift</button></div>`;
		const addBtn = document.querySelector<HTMLButtonElement>('#add-gift-detail');
		addBtn?.addEventListener('click', ()=>
			openModal('Add Gift', [
				{ id:'name', label:'Name', type:'text', required:true },
				{ id:'price', label:'Price', type:'number' },
			], async (values)=>{
				const payload:any = { name: values.name };
				if (values.price) payload.price = Number(values.price);
				await api(`/gifts/wishlist/${wishlistId}`, { method:'POST', body: JSON.stringify(payload) });
				toast('Gift added');
				await openDetail(wishlistId);
			})
		);
		const back = document.querySelector<HTMLButtonElement>('#detail-back');
		back?.addEventListener('click', ()=>{ detail.classList.add('hidden'); dashboard.classList.remove('hidden'); void loadDashboard(); });
	} catch(e:any) { toast(e.message,'err'); }
}

function openModal(title: string, fields: {id:string,label:string,type:string,required?:boolean}[], onSubmit: (values: Record<string,string>)=>Promise<void>) {
	const modal = document.querySelector<HTMLDivElement>('#modal')!;
	const form = document.querySelector<HTMLFormElement>('#modal-form')!;
	(document.querySelector('#modal-title') as HTMLDivElement).textContent = title;
	form.innerHTML = fields.map(f=>`<label>${f.label}<input id="modal-${f.id}" type="${f.type}" ${f.required?'required':''} /></label><div class="spacer"></div>`).join('');
	modal.classList.remove('hidden');
	const submit = document.querySelector<HTMLButtonElement>('#modal-submit')!;
	const cancel = document.querySelector<HTMLButtonElement>('#modal-cancel')!;
	const close = ()=>{ modal.classList.add('hidden'); form.onsubmit=null; submit.onclick=null; cancel.onclick=null; };
	form.onsubmit = async (e)=>{ e.preventDefault(); const values: Record<string,string> = {}; fields.forEach(f=>{ values[f.id] = (document.querySelector(`#modal-${f.id}`) as HTMLInputElement).value; }); await onSubmit(values); close(); };
	cancel.onclick = ()=> close();
}



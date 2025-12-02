import { api, toast } from '../main';
import { loadDashboard } from './dashboard';

export function setAuthedUI(authed: boolean) {
	document.querySelector('#nav-login')?.classList.toggle('hidden', authed);
	document.querySelector('#nav-logout')?.classList.toggle('hidden', !authed);
	document.querySelector('#auth-section')?.classList.toggle('hidden', authed);
	document.querySelector('#dashboard')?.classList.toggle('hidden', !authed);
}

export function setupAuth() {
	const registerForm = document.querySelector<HTMLFormElement>('#register-form');
	const loginForm = document.querySelector<HTMLFormElement>('#login-form');
	const resetForm = document.querySelector<HTMLFormElement>('#reset-form');
	const navLogin = document.querySelector<HTMLButtonElement>('#nav-login');
	const navLogout = document.querySelector<HTMLButtonElement>('#nav-logout');

	registerForm?.addEventListener('submit', async (e) => {
		e.preventDefault();
		const email = (document.querySelector('#register-email') as HTMLInputElement).value.trim();
		const password = (document.querySelector('#register-password') as HTMLInputElement).value;
		if (!email || password.length < 8) return toast('Invalid email or password', 'warn');
    try { await api('/auth/register', { method: 'POST', body: JSON.stringify({ email, password }) }); toast('Registered. Login now.'); } catch (err: any) { toast(err.message, 'err'); }
	});

	loginForm?.addEventListener('submit', async (e) => {
		e.preventDefault();
		const email = (document.querySelector('#login-email') as HTMLInputElement).value.trim();
		const password = (document.querySelector('#login-password') as HTMLInputElement).value;
    try {
            await api('/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) });
            setAuthedUI(true);
            await loadDashboard();
            toast('Logged in');
        } catch (err: any) { toast(err.message, 'err'); }
	});

	resetForm?.addEventListener('submit', async (e) => {
		e.preventDefault();
		const email = (document.querySelector('#reset-email') as HTMLInputElement).value.trim();
		try { await api('/auth/password-reset', { method: 'POST', body: JSON.stringify({ email }) }); toast('Reset token printed to backend console'); } catch (err: any) { toast(err.message, 'err'); }
	});

    navLogout?.addEventListener('click', async () => { try { await api('/auth/logout', { method: 'POST' }); } catch {} setAuthedUI(false); });

	// Initial UI setup - authentication is handled by session cookies
	setAuthedUI(false);
}



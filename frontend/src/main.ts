import { setupAuth, setAuthedUI } from './modules/auth';
import { setupDashboard, loadDashboard } from './modules/dashboard';
import { setupPublic } from './modules/public';

declare global {
	interface Window { API_BASE?: string }
}

const API_BASE = window.API_BASE || '/api';

export type Json = Record<string, unknown>;

// Store tokens globally
let accessToken: string | null = null;

export async function api(path: string, opts: RequestInit = {}) {
	const headers: Record<string, string> = { 'Content-Type': 'application/json', ...(opts.headers as any || {}) };
	
	// Add authorization header if we have an access token
	if (accessToken) {
		headers['Authorization'] = `Bearer ${accessToken}`;
	}
	
	// Add loading state
	const loadingElement = document.querySelector('#loading');
	if (loadingElement) {
		loadingElement.classList.remove('hidden');
	}
	
	try {
		let res = await fetch(`${API_BASE}${path}`, { ...opts, headers, credentials: 'include' });
		const contentType = res.headers.get('content-type') || '';
		
		if (!res.ok) {
			// With session cookies, 401 means not logged in — bubble up
			let detail = `HTTP ${res.status}`;
			try { 
				detail = contentType.includes('application/json') ? (await res.json()).detail ?? detail : await res.text(); 
			} catch {}
			throw new Error(detail);
		}
		
		// Check if response contains new tokens (after login)
		if (path.includes('/auth/login')) {
			const responseJson = contentType.includes('application/json') ? await res.json() : {};
			if (responseJson.access_token) {
				accessToken = responseJson.access_token;
			}
			return responseJson;
		}
		
		return contentType.includes('application/json') ? res.json() : res.text();
	} finally {
		// Remove loading state
		if (loadingElement) {
			loadingElement.classList.add('hidden');
		}
	}
}

// Function to clear stored tokens
export function clearTokens() {
	accessToken = null;
}

export function toast(msg: string, type: 'ok'|'warn'|'err' = 'ok') {
	const el = document.querySelector<HTMLDivElement>('#toast')!;
	el.textContent = msg; el.classList.remove('hidden');
	el.classList.remove('ok','warn','err'); el.classList.add(type);
	setTimeout(() => el.classList.add('hidden'), 2400);
}

function init() {
	setupAuth();
	setupDashboard();
	setupPublic();
    // Check session by pinging an auth-only endpoint; if 200, show dashboard
    (async () => {
        try {
            await api('/wishlists');
            setAuthedUI(true);
            await loadDashboard();
        } catch {
            setAuthedUI(false);
        }
    })();
}

document.addEventListener('DOMContentLoaded', init);



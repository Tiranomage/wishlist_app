from fastapi.testclient import TestClient
from backend.main import app


client = TestClient(app)


def auth(email: str, password: str = "password123"):
	client.post('/auth/register', json={"email": email, "password": password})
	resp = client.post('/auth/login', json={"email": email, "password": password})
	return resp.json()['access_token']


def test_duplicate_registration_and_bad_login():
	resp = client.post('/auth/register', json={"email": "dup@example.com", "password": "password123"})
	assert resp.status_code in (200, 201)
	resp = client.post('/auth/register', json={"email": "dup@example.com", "password": "password123"})
	assert resp.status_code == 400
	assert resp.json()['detail'].lower().find('already') != -1
	# bad login
	resp = client.post('/auth/login', json={"email": "dup@example.com", "password": "wrong"})
	assert resp.status_code == 401


def test_permissions_between_users():
	# user A creates wishlist
	token_a = auth('a@example.com')
	headers_a = {"Authorization": f"Bearer {token_a}"}
	resp = client.post('/wishlists', json={"title": "A1"}, headers=headers_a)
	assert resp.status_code == 201
	wid = resp.json()['id']
	resp = client.post(f'/gifts/wishlist/{wid}', json={"name": "GiftA"}, headers=headers_a)
	assert resp.status_code == 201
	gid = resp.json()['id']
	# user B cannot modify A's wishlist/gift
	token_b = auth('b@example.com')
	headers_b = {"Authorization": f"Bearer {token_b}"}
	resp = client.patch(f'/wishlists/{wid}', json={"title": "Hacked"}, headers=headers_b)
	assert resp.status_code == 403
	resp = client.patch(f'/gifts/{gid}', json={"status": "Purchased"}, headers=headers_b)
	assert resp.status_code == 403
	resp = client.delete(f'/gifts/{gid}', headers=headers_b)
	assert resp.status_code == 403


def test_search_filters():
	token = auth('search@example.com')
	headers = {"Authorization": f"Bearer {token}"}
	resp = client.post('/wishlists', json={"title": "Travel"}, headers=headers)
	wid = resp.json()['id']
	client.post(f'/gifts/wishlist/{wid}', json={"name": "Ticket"}, headers=headers)
	client.post(f'/gifts/wishlist/{wid}', json={"name": "Backpack"}, headers=headers)
	resp = client.get('/wishlists?q=Travel', headers=headers)
	assert any(w['title'] == 'Travel' for w in resp.json())
	resp = client.get('/wishlists?q=Backpack', headers=headers)
	assert any(w['title'] == 'Travel' for w in resp.json())



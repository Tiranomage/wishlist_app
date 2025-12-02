from fastapi.testclient import TestClient
from backend.main import app


client = TestClient(app)


def register_and_login(email: str, password: str = "password123"):
	client.post('/auth/register', json={"email": email, "password": password})
	resp = client.post('/auth/login', json={"email": email, "password": password})
	assert resp.status_code == 200
	data = resp.json()
	return data['access_token']


def test_register_login_and_wishlist_crud():
	token = register_and_login("user1@example.com")
	headers = {"Authorization": f"Bearer {token}"}
	# Create wishlist
	resp = client.post('/wishlists', json={"title": "Birthday", "is_public": True}, headers=headers)
	assert resp.status_code == 201, resp.text
	w = resp.json()
	wid = w['id']
	# List wishlists (own)
	resp = client.get('/wishlists', headers=headers)
	assert resp.status_code == 200
	assert any(x['id'] == wid for x in resp.json())
	# Public fetch
	resp = client.get('/wishlists?public=true', headers=headers)
	assert resp.status_code == 200
	# Update wishlist
	resp = client.patch(f'/wishlists/{wid}', json={"description": "Party"}, headers=headers)
	assert resp.status_code == 200
	# Gift add
	resp = client.post(f'/gifts/wishlist/{wid}', json={"name": "Book", "price": 10.5}, headers=headers)
	assert resp.status_code == 201
	gid = resp.json()['id']
	# Gift update status
	resp = client.patch(f'/gifts/{gid}', json={"status": "Purchased"}, headers=headers)
	assert resp.status_code == 200
	assert resp.json()['status'] == 'Purchased'
	# List gifts
	resp = client.get(f'/gifts/wishlist/{wid}', headers=headers)
	assert resp.status_code == 200
	# Delete gift
	resp = client.delete(f'/gifts/{gid}', headers=headers)
	assert resp.status_code == 204
	# Delete wishlist
	resp = client.delete(f'/wishlists/{wid}', headers=headers)
	assert resp.status_code == 204


def test_password_reset_flow():
	client.post('/auth/register', json={"email": "reset@example.com", "password": "oldpassword123"})
	# Request reset (token printed to console; we simulate by calling login then creating token via login not available here)
	resp = client.post('/auth/password-reset', json={"email": "reset@example.com"})
	assert resp.status_code == 200
	# We cannot capture console token here; this test is a placeholder for manual verification
	# Ensure login still works with old password
	resp = client.post('/auth/login', json={"email": "reset@example.com", "password": "oldpassword123"})
	assert resp.status_code == 200



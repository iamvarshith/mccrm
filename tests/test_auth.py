def test_login(client):
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 302

def test_register(client):
    response = client.post('/register', data={
        'email': 'new@example.com',
        'password': 'password123',
        'name': 'New Agent'
    })
    assert response.status_code == 302

def test_logout(auth_client):
    response = auth_client.get('/logout')
    assert response.status_code == 302 
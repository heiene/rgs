"""
Basic application tests
"""


def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'flask-backend'


def test_api_auth_endpoints(client):
    """Test API authentication endpoints exist"""
    # Test login endpoint
    response = client.post('/api/v1/auth/login', json={})
    assert response.status_code == 200
    
    # Test register endpoint
    response = client.post('/api/v1/auth/register', json={})
    assert response.status_code == 200
    
    # Test refresh endpoint
    response = client.post('/api/v1/auth/refresh', json={})
    assert response.status_code == 200


def test_api_user_endpoints(client):
    """Test API user endpoints exist"""
    # Test get users endpoint
    response = client.get('/api/v1/users')
    assert response.status_code == 200
    
    # Test create user endpoint
    response = client.post('/api/v1/users', json={})
    assert response.status_code == 201


def test_admin_web_endpoints(client):
    """Test admin web endpoints exist"""
    # Test admin dashboard
    response = client.get('/admin/')
    assert response.status_code == 200
    assert b'Admin Dashboard' in response.data
    
    # Test admin login page
    response = client.get('/admin/login')
    assert response.status_code == 200
    assert b'Admin Login' in response.data
    
    # Test admin upload page
    response = client.get('/admin/upload')
    assert response.status_code == 200
    assert b'CSV Upload' in response.data 
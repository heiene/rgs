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


def test_api_health_endpoint(client):
    """Test API health check endpoint"""
    response = client.get('/api/v1/health')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'timestamp' in data
    assert 'version' in data


def test_api_auth_endpoints_exist(client):
    """Test that API authentication endpoints exist (not testing functionality)"""
    # Test login endpoint exists
    response = client.post('/api/v1/auth/login', json={})
    assert response.status_code in [400, 401]  # Should exist but reject empty payload
    
    # Test register endpoint exists
    response = client.post('/api/v1/auth/register', json={})
    assert response.status_code == 400  # Should exist but reject empty payload
    
    # Test forgot password endpoint exists
    response = client.post('/api/v1/auth/forgot-password', json={})
    assert response.status_code == 400  # Should exist but reject empty payload
    
    # Test reset password endpoint exists
    response = client.post('/api/v1/auth/reset-password', json={})
    assert response.status_code == 400  # Should exist but reject empty payload


def test_api_user_endpoints_exist(client, auth_headers):
    """Test that API user endpoints exist (require authentication)"""
    # Test me endpoint exists
    response = client.get('/api/v1/auth/me', headers=auth_headers)
    assert response.status_code == 200
    
    # Test users list endpoint exists (admin only, so should be 403 for regular user)
    response = client.get('/api/v1/users/', headers=auth_headers)
    assert response.status_code in [200, 403]  # Should exist


def test_api_user_endpoints_require_auth(client):
    """Test that API user endpoints require authentication"""
    # Test me endpoint requires auth
    response = client.get('/api/v1/auth/me')
    assert response.status_code == 401
    
    # Test users list endpoint requires auth
    response = client.get('/api/v1/users/')
    assert response.status_code == 401


def test_cors_headers(client):
    """Test that CORS headers are present"""
    response = client.options('/api/v1/health')
    assert response.status_code == 200
    
    # Check for CORS headers
    assert 'Access-Control-Allow-Origin' in response.headers
    assert 'Access-Control-Allow-Methods' in response.headers
    assert 'Access-Control-Allow-Headers' in response.headers


def test_404_error_handling(client):
    """Test 404 error handling for non-existent endpoints"""
    response = client.get('/api/v1/nonexistent')
    assert response.status_code == 404
    
    data = response.get_json()
    assert 'error' in data or 'message' in data


def test_method_not_allowed(client):
    """Test method not allowed handling"""
    # Health endpoint should only accept GET
    response = client.post('/api/v1/health')
    assert response.status_code == 405  # Method Not Allowed 
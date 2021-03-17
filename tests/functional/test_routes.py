def test_404(client):
    assert client.get('/test_404').status_code == 404

def test_index(client):
    response =  client.get('/')
    assert response.status_code == 200
    assert b'There will be some news' in response.data
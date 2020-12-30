from flaskr import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

# IMPORTANT !!!
# The 'client' argument here is matched to the client fixture defined in conftest.py
# In essence, the return value of the client fixture function from conftest.py will be used here as the object 'client' in the test function
# The client object here is actually app.test_client()
def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'
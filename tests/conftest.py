import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


'''
!!! IMPORTANT !!!
Pytest uses fixtures by matching their function names with the names of arguments in the test functions. For example, the test_hello function you’ll write next takes a client argument. 
Pytest matches that with the client fixture function, calls it, and passes the returned value to the test function.
'''

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


'''
For most of the views, a user needs to be logged in. The easiest way to do this in tests is to make a POST request to the login view with the client. 
Rather than writing that out every time, you can write a class with methods to do that, and use a fixture to pass it the client for each test.

In essence, this is like a dummy user, doing all the authentication actions that a real user would/could do.
'''

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


# With the auth fixture, you can call auth.login() in a test to log in as the test user, which was inserted as part of the test data in the app fixture.
@pytest.fixture
def auth(client):
    return AuthActions(client)


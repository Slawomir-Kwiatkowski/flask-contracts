from flask_contracts.auth.models import User

def test_user():
    '''
    GIVEN a User models
    WHEN a new User is created
    THEN check the username, email, admin and is_active attributes
    '''

    user = User(username='John Doe', email='jd@test.com')

    assert user.username == 'John Doe'
    assert user.email == 'jd@test.com'
    assert user.admin is None
    assert user.is_active is None

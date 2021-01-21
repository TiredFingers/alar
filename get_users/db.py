users = {
    'test@test.com': {'password': '123', 'id': '1'}
}

acl = {
    "system": True
}


def get_user(email, password, userid):

    granted = acl.get(userid, None)

    if granted:

        if email in users and password == users[email]['password']:
            return users[email]['id']
    return None


def get_summary(userid):
    granted = acl.get(userid, None)

    if granted:
        return {'created': '10', 'deleted': '3', 'authorized': '1'}

    return {}


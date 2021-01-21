
# user_id: access granted
acl = {
    '0': False,
    '1': True,
    'system': True
}

# int routeid: { route: list points ids, name: str name }
routes = {
    '0': {
        'route': [0, 1], #points id's
        'name': 'From Moscow to Paris',
        'number': 1
    },
    '1': {
        'route': [1, 0],
        'name': 'From Paris to Moscow',
        'number': 2
    }
}

# int userid: list routes id
users_routes = {
    '0': [1],
    '1': [1, 2]
}


def get_summary(userid):
    granted = acl.get(userid, None)

    if granted:
        return {'saved': '12', 'queried': '3'}
    return {}


def get_routes(userid):
    granted = acl.get(userid, None)

    if granted:
        return routes
    return None


def get_user_routes(query_user, route_owner):

    granted = acl.get(query_user, None)

    if granted:
        user_routes = users_routes.get(route_owner, None)

        res = list()

        for routeid in user_routes:
            route = routes.get(routeid, None)

            if route:
                res.append(route)

        if len(res) > 0:
            return res

        return {'error': 'no routes'}

    return {'error': 'access denied'}

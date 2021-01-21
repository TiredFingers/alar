"""
 point_id: {'x' - x coords, 'y' - y coords, 'name' - point name}
"""
points = {
    '0': {
        'l': 55.755814,
        'a': 37.617635,
        'name': 'Moscow'
    },
    '1': {
        'l': 48.856663,
        'a': 2.351556,
        'name': 'Paris'
    },
}

"""
user_id: access granted
"""
acl = {
    '0': False,
    '1': True,
    'system': True
}


def get_points(userid):

    granted = acl.get(userid, None)

    if granted:
        return points
    return None


def get_particular_points(userid, points_ids):

    granted = acl.get(userid, None)

    if granted:

        res = list()

        for point_id in points_ids:
            point = points.get(point_id, None)

            if point:
                res.append(point)

        return res

    return {'error': 'no access'}


def get_summary(userid):
    granted = acl.get(userid, None)

    if granted:
        return {'points': '1200', 'queries': '22'}
    return {}

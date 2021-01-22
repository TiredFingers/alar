import random
import json
from get_users.app import db as users_db
from get_users.models import Acl as users_acl, User as users_user

from msroutes.app import db as routes_db
from msroutes.models import Acl as routes_acl, Route as route_model

from points.app import db as points_db
from points.models import Acl as points_acl, Point as point_model


#userid: 1 for system needs
acl = users_acl(user_id=1, access_granted=True)
acl_user1 = users_acl(user_id=2, access_granted=True)
acl_user2 = users_acl(user_id=3, access_granted=True)
acl_user3 = users_acl(user_id=4, access_granted=False)

user1 = users_user(id=2, login='user1', password='123')
user2 = users_user(id=3, login='user2', password='123')
user3 = users_user(id=4, login='user3', password='123')

users_db.session.add(acl)
users_db.session.add(acl_user1)
users_db.session.add(acl_user2)
users_db.session.add(acl_user3)

users_db.session.add(user1)
users_db.session.add(user2)
users_db.session.add(user3)

users_db.session.commit()


acl = routes_acl(user_id=1, access_granted=True)
acl_user1 = routes_acl(user_id=2, access_granted=True)
acl_user2 = routes_acl(user_id=3, access_granted=True)
acl_user3 = routes_acl(user_id=4, access_granted=False)

routes_db.session.add(acl)
routes_db.session.add(acl_user1)
routes_db.session.add(acl_user2)
routes_db.session.add(acl_user3)


names = {
    0: 'Moscow',
    1: 'Saint Petersburg',
    2: 'Novgorod',
    3: 'Kazan',
    4: 'Tver',
    5: 'Krasnodar',
    6: 'Kiev',
    7: 'Minsk',
    8: 'Astrahan',
    9: 'Shpak flat =)'
}


for i in range(10):
    points = str(json.dumps([p for p in range(random.randint(1, 100))]).encode('utf-8'))
    name = str(names[random.randint(0, 9)] + ' to ' + names[random.randint(0, 9)])
    routes_db.session.add(user_id=route_model(random.randint(2, 4)), points=points, name=name)

routes_db.session.commit()

acl = points_acl(user_id=1, access_granted=True)
acl_user1 = points_acl(user_id=2, access_granted=True)
acl_user2 = points_acl(user_id=3, access_granted=True)
acl_user3 = points_acl(user_id=4, access_granted=False)

points_db.session.add(acl)
points_db.session.add(acl_user1)
points_db.session.add(acl_user2)
points_db.session.add(acl_user3)


for i in range(100):
    name = str(names[random.randint(0, 9)])
    points_db.session.add(point_model(latitude=random.randint(1, 100) * 1.12383,
                                      longtitude=random.randint(1, 100) * 1.12383, name=name))

points_db.session.commit()

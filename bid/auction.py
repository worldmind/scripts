import time
import json
import falcon
import redis
from falcon_auth import FalconAuthMiddleware, BasicAuthBackend

USERS = {
    'tester': {'id': 0, 'login': 'tester'},
    'john': {'id': 1, 'login': 'john'},
    'otto': {'id': 2, 'login': 'otto'},
}

user_loader = lambda username, password: USERS.get(username, '')
auth_backend = BasicAuthBackend(user_loader)
auth_middleware = FalconAuthMiddleware(auth_backend, exempt_routes=['/exempt'], exempt_methods=['HEAD'])

REDIS = redis.Redis(decode_responses=True)


class WinnerResource(object):
    def on_get(self, req, resp, item_id):
        bidders = REDIS.zrange(item_id, 0, 0)
        resp.body = json.dumps(bidders[0])
        resp.status = falcon.HTTP_200


class BidsResource(object):
    def on_get(self, req, resp, item_id):
        bidders = REDIS.zrange(item_id, 0, -1)
        resp.body = json.dumps(bidders)
        resp.status = falcon.HTTP_200

    def on_put(self, req, resp, item_id):
        accept_time = time.time()
        user_login = req.context['user']['login']
        save_bid(user_login, item_id, accept_time)
        resp.body = ('Bid accepted')
        resp.status = falcon.HTTP_200

class UserBidsResource(object):
    def on_get(self, req, resp, user_id):
        user_login = get_user_by_id(user_id)
        bids = REDIS.smembers('%s:bids'.format(user_login))
        resp.body = json.dumps(list(bids))
        resp.status = falcon.HTTP_200

def save_bid(user_login, item_id, accept_time):
    pipe = REDIS.pipeline()
    pipe.execute_command('ZADD', item_id, 'NX', accept_time, user_login)
    pipe.sadd('%s:bids'.format(user_login), item_id)
    pipe.execute()

def get_user_by_id(user_id):
    for login in USERS.keys():
        if USERS[login]['id'] == user_id:
            return login

app = falcon.API(middleware=[auth_middleware])
bids = BidsResource()
winner = WinnerResource()
user_bids = UserBidsResource()

app.add_route('/items/{item_id}/bids', bids)
app.add_route('/items/{item_id}/winner', winner)
app.add_route('/users/{user_id}/bids', user_bids)

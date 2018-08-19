import time
import json
import falcon
import redis
from falcon_auth import FalconAuthMiddleware, BasicAuthBackend

USERS = {
    'john': {'id': 1, 'login': 'john'},
    'otto': {'id': 2, 'login': 'otto'},
}

user_loader = lambda username, password: USERS.get(username, '')
auth_backend = BasicAuthBackend(user_loader)
auth_middleware = FalconAuthMiddleware(
    auth_backend,
    exempt_routes=['/exempt'],
    exempt_methods=['HEAD'],
)


RECONNECT_PAUSE = 0.5
REDIS = redis.Redis(decode_responses=True)


class WinnerResource(object):
    def on_get(self, req, resp, item_id):
        bidders = redis_execute(lambda: REDIS.zrange(item_id, 0, 0))
        resp.body = json.dumps(bidders[0])
        resp.status = falcon.HTTP_OK


class BidsResource(object):
    def on_get(self, req, resp, item_id):
        item_id = int(item_id)
        bidders = redis_execute(lambda: REDIS.zrange(item_id, 0, -1))
        resp.body = json.dumps(bidders)
        resp.status = falcon.HTTP_OK

    def on_put(self, req, resp, item_id):
        item_id = int(item_id)
        accept_time = time.time()
        user_login = req.context['user']['login']
        redis_execute(lambda: save_bid(user_login, item_id, accept_time))
        resp.body = json.dumps({'msg': 'Bid accepted'})
        resp.status = falcon.HTTP_CREATED


class UserBidsResource(object):
    def on_get(self, req, resp, user_id):
        user_id = int(user_id)
        user_login = get_user_by_id(user_id)
        if not user_login:
            resp.body = json.dumps({'msg': 'No such user'})
            resp.status = falcon.HTTP_404
            return
        bids = redis_execute(lambda: REDIS.smembers(user_bids_key(user_login)))
        resp.body = json.dumps([int(x) for x in bids])
        resp.status = falcon.HTTP_OK


def save_bid(user_login, item_id, accept_time):
    pipe = REDIS.pipeline()
    pipe.execute_command('ZADD', item_id, 'NX', accept_time, user_login)
    pipe.sadd(user_bids_key(user_login), item_id)
    pipe.execute()


def redis_execute(command):
    global REDIS
    while True:
        try:
            return command()
        except redis.ConnectionError:
            while True:
                try:
                    REDIS = connect2redis()
                    time.sleep(RECONNECT_PAUSE)
                    REDIS.ping()
                    break
                except:
                    pass


def user_bids_key(user_login):
    return '{0}:bids'.format(user_login)


def get_user_by_id(user_id):
    for login in USERS.keys():
        if USERS[login]['id'] == user_id:
            return login


def connect2redis():
    return redis.Redis(decode_responses=True)


app = falcon.API(middleware=[auth_middleware])
bids = BidsResource()
winner = WinnerResource()
user_bids = UserBidsResource()

app.add_route('/items/{item_id}/bids', bids)
app.add_route('/items/{item_id}/winner', winner)
app.add_route('/users/{user_id}/bids', user_bids)
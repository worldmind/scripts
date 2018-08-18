import tornado.ioloop
import tornado.web
import time
import json
import redis


REDIS = redis.Redis(decode_responses=True)


class BidHandler(tornado.web.RequestHandler):
    def put(self, item_id):
        item_id = int(item_id)
        accept_time = time.time()
        user_login = 'john'
        save_bid(user_login, item_id, accept_time)
        self.write(json.dumps({'msg': 'Bid accepted'}))
        self.set_status(201)


def save_bid(user_login, item_id, accept_time):
    pipe = REDIS.pipeline()
    pipe.execute_command('ZADD', item_id, 'NX', accept_time, user_login)
    pipe.sadd(user_bids_key(user_login), item_id)
    pipe.execute()

def user_bids_key(user_login):
    return '{0}:bids'.format(user_login)

def make_app():
    return tornado.web.Application([
        (r"/items/([0-9]+)/bids", BidHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()

from sanic import Sanic
from sanic import response
import time
import redis


app = Sanic()
REDIS = redis.Redis(decode_responses=True)


@app.route('/items/<item_id>/bids', methods=['PUT'])
def bid(request, item_id):
    item_id = int(item_id)
    accept_time = time.time()
    user_login = 'john'
    save_bid(user_login, item_id, accept_time)
    return response.json(
        {'msg': 'Bid accepted'},
        status=201,
    )


def save_bid(user_login, item_id, accept_time):
    pipe = REDIS.pipeline()
    pipe.execute_command('ZADD', item_id, 'NX', accept_time, user_login)
    pipe.sadd(user_bids_key(user_login), item_id)
    pipe.execute()


def user_bids_key(user_login):
    return '{0}:bids'.format(user_login)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, workers=4)

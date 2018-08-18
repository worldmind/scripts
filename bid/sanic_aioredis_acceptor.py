from sanic import Sanic
from sanic import response
import time
import aioredis

app = Sanic()


@app.route('/items/<item_id>/bids', methods=['PUT'])
async def bid(request, item_id):
    item_id = int(item_id)
    accept_time = time.time()
    user_login = 'john'
    await save_bid(request, user_login, item_id, accept_time)
    return response.json(
        {'msg': 'Bid accepted'},
        status=201,
    )


async def save_bid(request, user_login, item_id, accept_time):
    redis = request.app.redis
    tr = redis.multi_exec()
    tr.zadd(item_id, accept_time, user_login, exist='ZSET_IF_NOT_EXIST')
    tr.sadd(user_bids_key(user_login), item_id)
    return await tr.execute()


def user_bids_key(user_login):
    return '{0}:bids'.format(user_login)


@app.listener('before_server_start')
async def before_server_start(app, loop):
    app.redis = await aioredis.create_redis(('localhost', 6379))


@app.listener('after_server_stop')
async def after_server_stop(app, loop):
    # not correct, need to be fixed
    app.redis.close()

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, workers=4)

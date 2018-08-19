## Architecture

When I started I has next ideas:
1.  Async is not required because we have no heavy IO - I plan use local storage (Redis), framework with forks will be enough (not much memory for every process required).
2.  Redis it is a simple and fast data structure server that has all needed data structures: Sorted Set for bid requests to every item and Set for save all bids of a every user. Other plus of a Redis - you can use it from many processes.
3.  To Sorted Sets (https://redis.io/topics/data-types#sorted-sets) I put user login with unixtime of accepting request.
4.  Accepting bids is very important for this task and I think that bids acceptor must be running as separate application - other API requests did no must slow down bids accepting. Nginx can be used for routing API requests between two applications.
5.  Very important save time of a request as soon as possible.

For REST APIs I like Swagger, but heard that is not very fast and trying to search fast and stable framework, after some reading I found Falcon and use it.

After stress testing this solution, for comparing I made some alternate solutions (for bids acceptor only) with Tornado and Sanic frameworks.
I did not spend many time with Tornado, but looks that it is a little faster and I thought to try Sanic (I heard that is very fast but was, may be in past, not very stable).
Sanic acceptor is two time faster that Falcon, but I am not sure that is because it is async - version with sync and async redis client works fast. But Sanic use less processes and maybe for accepting bids async version is better.

### Some points

For simplicity:

1.  I did not add config file and logger.
2.  I use Basic Auth an did not check passwords.

For performance purposes Redis can be configured for work via unix socket.

## Files

    ├── auction
    │   └──  auction.py
    ├── sanic_acceptor.py
    ├── sanic_aioredis_acceptor.py
    ├── tests
    │   └── test.py
    └── tornado_acceptor.py

auction/auction.py - main solution based on Falcon framework
tests/test.py - simple autet for it

tornado_acceptor.py - alternate solution of a bid acceptor with Tornado framework

sanic_acceptor.py - alternate solution of a bid acceptor with Sanic framework and sync redis client
sanic_aioredis_acceptor.py - alternate solution of a bid acceptor with Sanic framework and async redis client

## Computer hardware:

Memory size: 2GiB

CPU: Intel(R) Celeron(R) CPU P4500 @ 1.87GHz, threads=2

## Computer software:

Debian GNU/Linux 9.5 (stretch), Linux 4.9.0-7-amd64

Python 3.5.3, Redis 3.2.6

## Preistall

    wajig install redis-server

## Install

For main solution:

    pip install -U -r requirements.txt

For alternate solution install tornado, sanic, aioredis via pip3

## Running

For main solution:

    uwsgi --http :8000 --lazy-apps --workers=6 --wsgi-file auction/auction.py --callable app > app.log 2>&1

For alternate solutions:

    python3 <filename.py> > app.log 2>&1

## Testing

### Cleaning storage

Clean Redis (DID NOT USE IN PRODUCTION SERVER):

    echo 'flushall' | redis-cli
    echo 'keys *' | redis-cli

### Manual functional testing

HTTPie client used, httpie.org (pip3 install httpie)

Bid item:

    http -a john:12345 PUT :8000/items/999/bids
    http -a otto:54321 PUT :8000/items/999/bids

Get winner:

    http -a john:12345 GET :8000/items/999/winner

Get item bids:

    http -a john:12345 GET :8000/items/999/bids

Get users bids:

    http -a john:12345 GET :8000/users/1/bids

### Functional autotest

    pytest -v tests/test.py

### Load testing

It is a very primitive testing because one user used, but for more sophisticated testing I need time for search more powerful tool. Hope this testing is enough.

    ab -r -k -m PUT -A john:12345 -c 500 -n 20000 127.0.0.1:8000/items/999/bids > bids_load.report 2>&1

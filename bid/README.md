# Preinstall

Python 3.5.3, Redis 3.2.6

wajig install redis-server

# Install

pip install -U -r requirements.txt

## Running

uwsgi --http :8000 --lazy-apps --workers=6 --wsgi-file auction/auction.py --callable app all> app.log

if bash used: > app.log 2>&1 

## Functional testing

### Manual

Clean Redis (DID NOT USE IN PRODUCTION SERVER)
echo 'flushall' | redis-cli
echo 'keys *' | redis-cli

Use HTTPie httpie.org (pip3 install httpie)

Bid item:
http -a john:12345 PUT :8000/items/999/bids
http -a otto:54321 PUT :8000/items/999/bids

Get winner:
http -a john:12345 GET :8000/items/999/winner

Get item bids:
http -a john:12345 GET :8000/items/999/bids

Get users bids
http -a john:12345 GET :8000/users/1/bids

### Autotests

pytest -v tests/test.py

## Load testing

ab -r -k -m PUT -A john:12345 -c 500 -n 20000 127.0.0.1:8000/items/999/bids all> bids_load.report
# Preinstall

sudo pip3 install httpie

wajig install redis-server

sudo pip3 install falcon

#sudo pip3 install ujson
#sudo pip3 install cython
#sudo pip3 install --no-binary :all: falcon

sudo pip3 install -U falcon-auth

sudo pip3 install uwsgi
sudo pip3 install redis

## Running

uwsgi --http :8000 --lazy-apps --wsgi-file auction/auction.py  --callable app

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

ab -k -m PUT -A john:12345 -c 5 -n 20 127.0.0.1:8000/items/666/bids

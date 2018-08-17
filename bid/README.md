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

uwsgi --http :8000 --lazy-apps --wsgi-file bid_acceptor.py --callable app

http -a john:12345 PUT :8000/items/666/bids
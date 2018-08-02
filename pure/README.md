# Preparing

wajig install postgresql postgresql-client libpq-dev mongodb

sudo pysed -r '(^local\s+all\s+all\s+)peer' '\\1md5' /etc/postgresql/9.6/main/pg_hba.conf --write

sudo systemctl restart postgresql

cat sql/db_and_user.sql | sudo -u postgres psql

pip install -U -r requirements.txt


# Using

cat sql/get_cars_count_by_color.sql | psql 'service=pure'

cd puretask/

python manage.py get_cars_count_by_color

cd ..

python get_images.py
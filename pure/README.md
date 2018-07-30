wajig install postgresql postgresql-client libpq-dev
sudo pysed -r '(^local\s+all\s+all\s+)peer' '\\1md5' /etc/postgresql/9.6/main/pg_hba.conf --write
sudo systemctl restart postgresql
cat sql/db_and_user.sql | sudo -u postgres psql
pip install -U -r requirements.txt
## Scraper

`cd ~ && mkdir cs4246-db`

`docker run --name db -v ~/cs4246-db:/var/lib/mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root -d mysql:latest`

Go to project root.

`docker exec -i db mysql -uroot -proot < init_db.sql`

### Setting up virtualenv

`virtualenv -p python3 venv`

`source venv/bin/activate`

`pip3 install -r requirements.txt`

### Cron



### To create db dump

`docker exec -i db mysqldump -uroot -proot --add-drop-database --opt --databases bike-gp > dump.sql`

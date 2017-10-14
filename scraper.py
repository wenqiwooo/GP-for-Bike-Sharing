import pymysql
import requests
import json
import time


class Scraper:
  def __init__(self, db_hostname, db_username, db_password, db_database):
    self.db_hostname = db_hostname
    self.db_username = db_username
    self.db_password = db_password
    self.db_database = db_database

  def connect(self):
    self.conn = pymysql.connect(host=self.db_hostname,
                                user=self.db_username,
                                passwd=self.db_password,
                                db=self.db_database)
    print('Connected to db')

  def disconnect(self):
    self.conn.close()
    print('Disconnected from db')

  def scrape_obike(self, coordinates, region):
    dt = time.strftime('%Y-%m-%d %H:%M:%S')
    for latitude, longitude, _, _ in coordinates:
      url = 'https://mobile.o.bike/api/v1/bike/list?latitude={}&longitude={}'.format(latitude, longitude)
      r = requests.get(url)
      data = r.json()['data']['list']
      self._insert_obike_data(data, region, dt)
      print('Finished 1 run! Sleeping...')
      time.sleep(5)

  def _insert_obike_data(self, data, region, dt):
    cur = self.conn.cursor()
    for d in data:
      query = """
        REPLACE INTO obike (obike_id, longitude, latitude, imei, country_id, helmet, created_at, region) 
        VALUES ('{}', {}, {}, '{}', {}, {}, '{}', '{}')
        """.format(
          d['id'],
          d['longitude'],
          d['latitude'],
          d['imei'],
          d['countryId'],
          d['helmet'],
          dt,
          region
        )
      # print(query)
      cur.execute(query)
    self.conn.commit()

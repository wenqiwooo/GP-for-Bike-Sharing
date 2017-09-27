from map_helper import MapHelper

import numpy as np
import pymysql

class DataLoader:
  def __init__(self, db_hostname, db_username, db_password, db_database):
    self.db_hostname = db_hostname
    self.db_username = db_username
    self.db_password = db_password
    self.db_database = db_database

  def connect(self):
    self.conn = pymysql.connect(
        host=self.db_hostname,
        user=self.db_username,
        passwd=self.db_password,
        db=self.db_database
    )
    print('Connected to db')

  def disconnect(self):
    self.conn.close()
    print('Disconnected from db')

  def load_region_data(self, region, box, unit_dist=0.1):
    """
    region:     'Tampines', 'Boon Lay', 'Jurong East', 'Seng Kang'
    box:        (min lat, min long, max lat, max long)
    unit_dist:  unit distance in km
    """
    cur = self.conn.cursor()
    output_data = []
    for coordinate in MapHelper.coordinates(box, unit_dist):
      min_lat, min_lng, max_lat, max_lng = MapHelper.bounding_box(coordinate, unit_dist)
      cur.execute(
          """
          SELECT created_at, COUNT(*) FROM obike
          WHERE region = '{region}'
          AND latitude >= {min_lat}
          AND latitude < {max_lat}
          AND longitude >= {min_lng}
          AND longitude > {max_lng}
          GROUP BY created_at
          """.format(
              region=region,
              min_lat=min_lat,
              min_lng=min_lng,
              max_lat=max_lat,
              max_lng=max_lng
          )
      )
      for row in cur:
        output_data.append((*coordinate, row[0].timestamp(), row[1]))
    cur.close()
    
    if output_data:
      data = np.array(output_data)
      return data[:,:3], data[:,3]

if __name__ == '__main__':
  # Sample usage
  loader = DataLoader('127.0.0.1', 'root', 'root', 'bike-gp')
  loader.connect()
  data = loader.load_region_data('Tampines', (1.344467, 103.930952, 1.360377, 103.957675))
  loader.disconnect()
  print(data)

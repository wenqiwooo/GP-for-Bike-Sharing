from map_helper import MapHelper
from constants import TAMPINES, TAMPINES_BOX, SENGKANG, SENGKANG_BOX, UNIT_DIST
import csv
import numpy as np
import pymysql
from tqdm import tqdm

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

    # Sample usage

    loader = DataLoader('127.0.0.1', 'root', 'root', 'bike-gp')
    loader.connect()
    data = loader.load_region_data('Tampines', (1.344467, 103.930952, 1.360377, 103.957675))
    loader.disconnect()
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
          AND longitude < {max_lng}
          GROUP BY created_at
          """.format(
              region=region,
              min_lat=min_lat,
              min_lng=min_lng,
              max_lat=max_lat,
              max_lng=max_lng
          )
      )
      latitude, longitude, lat_idx, long_idx = coordinate
      for row in cur:
        ts = DataLoader.round_epoch(row[0].timestamp(), 30)
        output_data.append((latitude, longitude, ts, row[1], lat_idx, long_idx))
    cur.close()
    if output_data:
      data = np.array(output_data)
      return data

  def to_csv(self, filename):
    # Read all results from database
    cur = self.conn.cursor()
    res = []
    cur.execute("SELECT * FROM obike;")
    res = [row for row in cur]
    cur.close()

    # Write to CSV
    with open(filename, 'w') as f:
      writer = csv.writer(f)
      writer.writerow([description[0] for description in cur.description]) # header
      for row in res:
        writer.writerow(row)

  @staticmethod
  def round_epoch(timestamp, m):
    """Round off timestamp to m minutes"""
    timestamp = int(timestamp)
    r = timestamp % 1800
    if r < 1800/2:
      return timestamp - r
    else:
      return timestamp - r + 1800

  @staticmethod
  def load_data(input, period, intervals=None):
    """
    Returns X, Y
    """
    data = np.load(input)
    data = data[data[:,2] % period == 0]
    if intervals is None:
      intervals = data.shape[0]
    np.save('filtered_data', data[:intervals])
    return data[:intervals]

  @staticmethod
  def dump():
    loader = DataLoader('localhost', 'root', 'root', 'bike-gp')
    loader.connect()
    print('Doing Tampines')
    tp_data = loader.load_region_data(TAMPINES, TAMPINES_BOX, unit_dist=UNIT_DIST)
    print('Doing Sengkang')
    sk_data = loader.load_region_data(SENGKANG, SENGKANG_BOX, unit_dist=UNIT_DIST)
    loader.disconnect()
    np.save('tp-data', tp_data)
    np.save('sk-data', sk_data)


if __name__ == '__main__':
  # preprocess
  DataLoader.dump()

  """
  30 min: 1800
  1 hr:   3600
  2 hr:   7200
  3 hr:   10800
  4 hr:   14400
  """
  d = DataLoader.load_data('./sk-data.npy', 3600)
  print(d)

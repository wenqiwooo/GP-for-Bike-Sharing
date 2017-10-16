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

  def load_region_data(self, region, box, unit_dist):
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
        SELECT A.created_at, COALESCE(B.bike_count, 0) as bc
        FROM (
          SELECT DISTINCT created_at FROM obike WHERE region = '{region}'
        ) AS A
        LEFT JOIN (
          SELECT created_at, COUNT(*) as bike_count FROM obike
                  WHERE region = '{region}'
                  AND latitude >= {min_lat}
                  AND latitude < {max_lat}
                  AND longitude >= {min_lng}
                  AND longitude < {max_lng}
                  GROUP BY created_at
        ) AS B
        ON A.created_at = B.created_at;
        """.format(
          region=region,
          min_lat=min_lat,
          min_lng=min_lng,
          max_lat=max_lat,
          max_lng=max_lng
        )
      )
      # cur.execute(
      #     """
      #     SELECT created_at, COUNT(*) FROM obike
      #     WHERE region = '{region}'
      #     AND latitude >= {min_lat}
      #     AND latitude < {max_lat}
      #     AND longitude >= {min_lng}
      #     AND longitude < {max_lng}
      #     GROUP BY created_at
      #     """.format(
      #         region=region,
      #         min_lat=min_lat,
      #         min_lng=min_lng,
      #         max_lat=max_lat,
      #         max_lng=max_lng
      #     )
      # )
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
  def dump(unit_dist):
    loader = DataLoader('localhost', 'root', 'root', 'bike-gp')
    loader.connect()
    print('Doing Tampines')
    tp_data = loader.load_region_data(TAMPINES, TAMPINES_BOX, unit_dist)
    print('Doing Sengkang')
    sk_data = loader.load_region_data(SENGKANG, SENGKANG_BOX, unit_dist)
    loader.disconnect()
    suffix = int(unit_dist*1000)
    np.save('./data/tp-data-{}'.format(suffix), tp_data)
    np.save('./data/sk-data-{}'.format(suffix), sk_data)

  @staticmethod
  def load_data(input, period, offset=None, intervals=None, prefix=None, suffix=None):
    """
    Returns X, Y
    """
    data = np.load(input)
    ts_start = np.amin(data[:,2])
    if offset:
        ts_start += offset * period / 2

    if intervals is not None:
      ts_end = ts_start + intervals*period
    else:
      ts_end = np.amax(data[:,2]) + period
    data = data[data[:,2] % period == 0]
    data = data[data[:,2] < ts_end]
    output = 'filtered_data'
    if suffix is not None:
      output += '-{}'.format(suffix)
    if prefix is not None:
      output = '{}-'.format(prefix) + output
    output = './data/' + output
    np.save(output, data)
    return data


if __name__ == '__main__':
  # preprocess
  # DataLoader.dump(0.1)
  # DataLoader.dump(0.2)
  # DataLoader.dump(0.4)
  # DataLoader.dump(1.0)

  """
  30 min: 1800
  1 hr:   3600
  2 hr:   7200
  3 hr:   10800
  4 hr:   14400
  """

  # Training Data
  # d = DataLoader.load_data('./data/tp-data-100.npy', 7200, suffix=100, intervals=36)
  # print(d.shape)
  d = DataLoader.load_data('./data/tp-data-200.npy', 3600, prefix='tp', suffix=200, intervals=72)
  print(d.shape)
  d = DataLoader.load_data('./data/tp-data-400.npy', 1800, prefix='tp', suffix=400)
  print(d.shape)
  # d = DataLoader.load_data('./data/sk-data-100.npy', 7200, suffix=100, intervals=36)
  # print(d.shape)
  d = DataLoader.load_data('./data/sk-data-200.npy', 7200, prefix='sk', suffix=200, intervals=24)
  print(d.shape)
  d = DataLoader.load_data('./data/sk-data-400.npy', 3600, prefix='sk', suffix=400)
  print(d.shape)

  # Test data
  # d = DataLoader.load_data('./data/tp-test-data-100.npy', 7200, suffix=100, intervals=36)
  # print(d.shape)
  d = DataLoader.load_data('./data/tp-data-200.npy', 3600, offset=1, prefix='test-tp', suffix=200, intervals=72)
  print(d.shape)
  d = DataLoader.load_data('./data/tp-data-400.npy', 1800, offset=1, prefix='test-tp', suffix=400)
  print(d.shape)
  # d = DataLoader.load_data('./data/sk-test-data-100.npy', 7200, suffix=100, intervals=36)
  # print(d.shape)
  d = DataLoader.load_data('./data/sk-data-200.npy', 7200, offset=1, prefix='test-sk', suffix=200, intervals=24)
  print(d.shape)
  d = DataLoader.load_data('./data/sk-data-400.npy', 3600, offset=1, prefix='test-sk', suffix=400)
  print(d.shape)

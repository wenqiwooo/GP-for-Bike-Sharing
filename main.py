from map_helper import MapHelper
from scraper import Scraper


HOSTNAME = '127.0.0.1'
USERNAME = 'root'
PASSWORD = 'root'
DATABASE = 'bike-gp'

# Bounding box = (min_lat, min_long, max_lat, max_long)
TAMPINES_BOX = (1.344467, 103.930952, 1.360377, 103.957675)
TAMPINES = 'Tampines'
# BOONLAY_BOX
# BOONLAY = 'Boon Lay'
# JURONG_BOX
# JURONG = 'Jurong East'
SENGKANG_BOX = (1.378823, 103.856249, 1.402076, 103.909292)
SENGKANG = 'Seng Kang'


if __name__ == '__main__':
  scraper = Scraper(HOSTNAME, USERNAME, PASSWORD, DATABASE)
  scraper.connect()
  tampines_coords = MapHelper.coordinates(box=TAMPINES_BOX, unit_dist=0.8)
  scraper.scrape_obike(coordinates=tampines_coords, region=TAMPINES)
  sengkang_coords = MapHelper.coordinates(box=SENGKANG_BOX, unit_dist=0.8)
  scraper.scrape_obike(coordinates=sengkang_coords, region=SENGKANG)
  scraper.disconnect()

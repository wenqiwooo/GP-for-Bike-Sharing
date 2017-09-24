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
# SENGKANG_BOX
# SENGKANG = 'Seng Kang'


if __name__ == '__main__':
  scraper = Scraper(HOSTNAME, USERNAME, PASSWORD, DATABASE)
  scraper.connect()
  tampines_coords = MapHelper.coordinates(box=TAMPINES_BOX, unit_dist=0.5)
  scraper.scrape_obike(coordinates=tampines_coords, region=TAMPINES)
  scraper.disconnect()

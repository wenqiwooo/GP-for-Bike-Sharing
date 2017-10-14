from map_helper import MapHelper
from scraper import Scraper
from constants import (
  HOSTNAME,
  USERNAME,
  PASSWORD,
  DATABASE,
  TAMPINES_BOX,
  TAMPINES,
  SENGKANG_BOX,
  SENGKANG,
)

if __name__ == '__main__':
  scraper = Scraper(HOSTNAME, USERNAME, PASSWORD, DATABASE)
  scraper.connect()
  tampines_coords = MapHelper.coordinates(box=TAMPINES_BOX, unit_dist=0.8)
  scraper.scrape_obike(coordinates=tampines_coords, region=TAMPINES)
  sengkang_coords = MapHelper.coordinates(box=SENGKANG_BOX, unit_dist=0.8)
  scraper.scrape_obike(coordinates=sengkang_coords, region=SENGKANG)
  scraper.disconnect()

from math import pi, cos


EARTH_RADIUS = 6378


class MapHelper:
  def __init__(self):
    pass

  @staticmethod
  def coordinates(box, unit_dist):
    """
    box: (min lat, min long, max lat, max long)
    unit_dist: unit distance in km
    """
    min_lat, min_long, max_lat, max_long = box
    curr_lat = min_lat
    curr_long = min_long
    lat_counter = 0
    while curr_lat < max_lat:
      long_counter = 0
      while curr_long < max_long:
        yield (curr_lat, curr_long, lat_counter, long_counter)
        curr_long = curr_long + (float(unit_dist) / EARTH_RADIUS) * (180 / pi) / cos(curr_lat * pi / 180)
        long_counter += 1
      curr_lat = curr_lat + (float(unit_dist) / EARTH_RADIUS) * (180 / pi)
      curr_long = min_long
      lat_counter += 1
  
  @staticmethod
  def bounding_box(center, size):
    """
    center:   lat, long
    size:     size of box
    """
    center_lat, center_lng, _, _ = center
    lng_delta = (float(size) / (2 * EARTH_RADIUS)) * (180 / pi) / cos(center_lat * pi / 180)
    lat_delta = (float(size) / (2 * EARTH_RADIUS)) * (180 / pi)
    min_lat, max_lat = map(lambda x: x * lat_delta + center_lat, [-1, 1])
    min_lng, max_lng = map(lambda x: x * lng_delta + center_lng, [-1, 1])
    return min_lat, min_lng, max_lat, max_lng

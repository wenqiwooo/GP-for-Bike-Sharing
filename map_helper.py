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
    while curr_lat < max_lat:
      while curr_long < max_long:
        yield (curr_lat, curr_long)
        curr_long = curr_long + (float(unit_dist) / EARTH_RADIUS) * (180 / pi) / cos(curr_lat * pi / 180)
      curr_lat = curr_lat + (float(unit_dist) / EARTH_RADIUS) * (180 / pi)
      curr_long = min_long

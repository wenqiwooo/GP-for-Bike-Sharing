import numpy as np

def post_process_data(data):
  """
  Converts a matrix of [[ lat, long, num_bikes ],...] to a 2D numpy array where
  the (i, j)-th entry in the array represents the i-th unique lat and j-th
  unique long from the original matrix.

  Inputs:
  - data: The data to be converted (Must be a 2d numpy array with 3 columns)
  """
  assert len(data.shape) == 2 and data.shape[1] == 3

  unique_lats = np.sort(np.unique(data[:,0]))
  unique_longs = np.sort(np.unique(data[:,1]))

  lat_map = dict([(lat, i) for i, lat in enumerate(unique_lats)])
  long_map = dict([(long, i) for i, long in enumerate(unique_longs)])

  output = np.zeros((unique_lats.size, unique_longs.size))
  for row in data:
    lat_idx, long_idx = lat_map[row[0]], long_map[row[1]]
    output[lat_idx, long_idx] = row[2]
  return output

if __name__ == '__main__':
  test_matrix = np.arange(30).reshape(10,3)
  print(post_process_data(test_matrix))

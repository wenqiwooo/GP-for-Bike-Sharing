from argparse import ArgumentParser
from matplotlib import cm
from matplotlib.animation import FuncAnimation

import numpy as np
import matplotlib.pyplot as plt

def setup_arguments():
  parser = ArgumentParser(description='Create GIFs from data')
  parser.add_argument(
    '--input',
    default=None,
    required=True,
    help='(Required) The file to visualize',
  )
  parser.add_argument(
    '--map_image',
    default=None,
    required=True,
    help='(Required) The image of the map to be rendered underneath the data visualization.',
  )
  parser.add_argument(
    '--location_name',
    default=None,
    required=True,
    help='(Required) The name of the location being visualized',
  )
  parser.add_argument(
    '--ts_col',
    default=2,
    help='The column of the timestamps. (Default 2)',
  )
  parser.add_argument(
    '--lat_idx_col',
    default=4,
    help='The column of the latitude index. (Default 4)',
  )
  parser.add_argument(
    '--long_idx_col',
    default=5,
    help='The column of the longitude index. (Default 5)',
  )
  parser.add_argument(
    '--count_col',
    default=3,
    help='The column of the bicycle counts. (Default 3)',
  )
  parser.add_argument(
    '--output',
    default='output.gif',
    help='The output GIF file. (Default output.gif)',
  )
  return parser.parse_args()


def _pad_int_string(i, desired_len):
    string = str(i)
    if len(string) >= desired_len:
        return string
    return '0' * (desired_len - len(string)) + string


def visualize_gif(data, out_file, image, ts_col, lat_col, lng_col, cnt_col, loc_name):
  """
  Requires imagemagick (and possibly yasm and ffmpeg). Visualizes data into a GIF.
  """
  fig = plt.figure()
  fig.set_tight_layout(True)

  timestamps = np.sort(np.unique(data[:, ts_col]))
  max_lat_idx = np.amax(data[:, lat_col].astype(np.int32))
  max_lng_idx = np.amax(data[:, lng_col].astype(np.int32))
  vmin = 0
  vmax = np.amax(data[:, cnt_col])
  z = np.zeros((max_lat_idx + 1, max_lng_idx + 1))

  im = plt.imshow(z, cmap=cm.coolwarm, interpolation='lanczos', vmin=vmin, vmax=vmax, animated=True)
  plt.imshow(plt.imread(image), extent=[0, max_lng_idx, 0, max_lat_idx], alpha=0.3)

  cbar = fig.colorbar(im, ticks=[0, vmax / 2, vmax])
  cbar.ax.set_yticklabels(['0', '%s' % (vmax / 2), '%s' % vmax])

  def update(timestamp):
    selected_rows = data[:, ts_col] == timestamp
    selected_data = (data[selected_rows])[:, (lat_col, lng_col, cnt_col)]
    z = np.zeros((max_lat_idx + 1, max_lng_idx + 1))

    for row in selected_data:
      lat_idx, lng_idx = row[(0, 1),].astype(np.int32)
      z[lat_idx, lng_idx] = row[2]
    
    im.set_array(z)
    fig.suptitle('%s: %s' % (loc_name, timestamp))
    return im,

  anim = FuncAnimation(fig, update, frames=timestamps, interval=50)
  anim.save(out_file, dpi=80, writer='imagemagick')
  print('GIF saved to %s' % out_file)

if __name__ == '__main__':
  args = setup_arguments()
  data = np.load(args.input)
  out_file = args.output
  image = args.map_image
  ts_col = args.ts_col
  lat_col = args.lat_idx_col
  lng_col = args.long_idx_col
  cnt_col = args.count_col
  loc_name = args.location_name

  visualize_gif(data, out_file, image, ts_col, lat_col, lng_col, cnt_col, loc_name)

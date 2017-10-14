import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

class Visualizer:
  @staticmethod
  def plot_img(img_path):
    img = mpimg.imread(img_path)
    imgplot = plt.imshow(img)


if __name__ == '__main__':
  Visualizer.plot_img('./assets/sk_map.png')
  plt.show()

# ----------------------------------------------------------------------------
# -                        Open3D: www.open3d.org                            -
# ----------------------------------------------------------------------------
# The MIT License (MIT)
#
# Copyright (c) 2018-2021 www.open3d.org
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
# ----------------------------------------------------------------------------

# examples/python/misc/color_image.py

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import os, sys
pyexample_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
test_data_path = os.path.join(os.path.dirname(pyexample_path), 'test_data')
sys.path.append(pyexample_path)

import open3d as o3d
#conda install pillow matplotlib

if __name__ == "__main__":

    print("Testing image in open3d ...")
    print("Convert an image to numpy and draw it with matplotlib.")
    x = o3d.io.read_image(os.path.join(test_data_path, 'image.PNG'))
    print(x)
    plt.imshow(np.asarray(x))
    plt.show()

    print(
        "Convet a numpy image to o3d.geometry.Image and show it with DrawGeomtries()."
    )
    y = mpimg.imread(os.path.join(test_data_path, 'lena_color.jpg'))
    print(y.shape)
    yy = o3d.geometry.Image(y)
    print(yy)
    o3d.visualization.draw_geometries([yy])

    print("Render a channel of the previous image.")
    z = np.array(y[:, :, 1])
    print(z.shape)
    print(z.strides)
    zz = o3d.geometry.Image(z)
    print(zz)
    o3d.visualization.draw_geometries([zz])

    print("Write the previous image to file then load it with matplotlib.")
    o3d.io.write_image("test.jpg", zz, quality=100)
    zzz = mpimg.imread("test.jpg")
    plt.imshow(zzz)
    plt.show()

    print("Testing basic image processing module.")
    im_raw = mpimg.imread(os.path.join(test_data_path, 'lena_color.jpg'))
    im = o3d.geometry.Image(im_raw)
    im_g3 = im.filter(o3d.geometry.ImageFilterType.Gaussian3)
    im_g5 = im.filter(o3d.geometry.ImageFilterType.Gaussian5)
    im_g7 = im.filter(o3d.geometry.ImageFilterType.Gaussian7)
    im_gaussian = [im, im_g3, im_g5, im_g7]
    pyramid_levels = 4
    pyramid_with_gaussian_filter = True
    im_pyramid = im.create_pyramid(pyramid_levels, pyramid_with_gaussian_filter)
    im_dx = im.filter(o3d.geometry.ImageFilterType.Sobel3dx)
    im_dx_pyramid = o3d.geometry.Image.filter_pyramid(
        im_pyramid, o3d.geometry.ImageFilterType.Sobel3dx)
    im_dy = im.filter(o3d.geometry.ImageFilterType.Sobel3dy)
    im_dy_pyramid = o3d.geometry.Image.filter_pyramid(
        im_pyramid, o3d.geometry.ImageFilterType.Sobel3dy)
    switcher = {
        0: im_gaussian,
        1: im_pyramid,
        2: im_dx_pyramid,
        3: im_dy_pyramid,
    }
    for i in range(4):
        for j in range(pyramid_levels):
            plt.subplot(4, pyramid_levels, i * 4 + j + 1)
            plt.imshow(switcher.get(i)[j])
    plt.show()

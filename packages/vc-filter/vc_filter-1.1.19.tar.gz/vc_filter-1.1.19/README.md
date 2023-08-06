## VC FILTER
VC filter is a new high-quality edge detector based on the Visual Cortex study

### Installation
```
pip install vc-filter
```
### About VC filter

<p align="center"><img src="https://boriskravtsov.com/pypi/hello_demo.png"/>

The well-known Sobel filter with the kernel shown below is “tuned” to detect horizontal edges. 
As the deviation from the horizontal increases, the filter’s sensitivity falls, and as a result, 
the vertical edges become invisible (image in the center). In other words, they all hide in the 
"blind zone" of the filter.
<div align="center">

```Python
 1,  2,  1
 0,  0,  0
-1, -2, -1
```
</div>

There are two ways to perform Sobel filtering:

1. **Spatial domain:** filtering is done by convolving the image with a Sobel kernel.
OpenCV has a ready-made solution for this - *cv2.Sobel(image, cv.CV_64F, 0, 1, ksize=3)*.<br><br>

2. **Frequency domain:** multiplying Fourier transform of an image with Fourier transform of Sobel kernel, 
and compute inverse Fourier transform of the resulting product:

<p align="center"><img src="https://boriskravtsov.com/pypi/pipeline_1.png"/>

We propose to upgrade the procedure above as follows:

<p align="center"><img src="https://boriskravtsov.com/pypi/pipeline_2.png"/>

Here rot(b, alpha) denotes rotation of the kernel spectrum by angle alpha. 
This rotation changes the position of the blind zone. Unfortunately, neither the Sobel filter 
nor its modifications can spare us from blind zones. However, **a set of modified Sobel filters 
acting parallel** (vc-filter) may succeed. So, let’s use a set of filters with angles equal 
to 0 degrees, 12 degrees, 24 degrees, etc. And lastly, we sum up the filters' results and get 
a perfect outline image (top right image).

The use of the vc-filter is straightforward. Unlike all known filters, the vc-filter has no parameters. 
However, the outline image obtained by vc-filter usually requires some simple contrast enhancement.

Where else can we find edge detectors tuned to different angles? D.Huebel and T.Wiesel discovered such 
detectors (orientation-selective neurons) in the visual cortex over 60 years ago, but their role 
is still unclear. We guess that **orientation-selective neurons compose outline image of 
the visible object in the same way as the set of modified Sobel filters in our method**.

### How to use:
```Python
import cv2 as cv
from vc_filter import vc_filter

def contrast_enhancement(image_in, contrast_param):

    image_out = image_in * contrast_param

    image_out[image_out > 255] = 255

    return image_out


image = cv.imread(path_in, cv.IMREAD_UNCHANGED)

image_edges = vc_filter(image)

image_edges_enh = contrast_enhancement(image_edges, 2.0)

cv.imwrite(path_out, image_edges_enh)
```

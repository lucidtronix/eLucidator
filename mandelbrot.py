import cv2
import colorsys
import numpy as np

resolution = (1024, 1024, 3)

def i_to_rgb(i):
  color = 255 * np.array(colorsys.hsv_to_rgb(i/255.0, 1.0, 0.5))
  return color.astype(int)

def mandelbrot(z,maxiter):
  c = z
  for n in range(maxiter):
      if abs(z) > 2:
          return n
      z = z*z + c
  return maxiter

def mandelbrot_set(xmin,xmax,ymin,ymax,width,height,maxiter):
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    n3 = np.empty((width,height, 3))
    for i in range(width):
        for j in range(height):
            m = mandelbrot(r1[i] + 1j*r2[j],maxiter)
            n3[i,j,:] = i_to_rgb(m)
    return n3


def run_m2():

  #img = mandelbrot_set(-2.4,0.5,-1.25,1.25,resolution[0], resolution[1], 1024)
  img = mandelbrot_set(-0.74888,-0.74877,0.06515,0.06525,resolution[0], resolution[1],1200)
  print 'got img shape:', img.shape, 'min: ', img.min(), 'max:',  img.max()
  img -= img.min()
  img *=  255.0/img.max()
  img = np.uint8(img)
  while True:
    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

run_m2()
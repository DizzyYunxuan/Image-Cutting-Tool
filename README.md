# Image-cutting-tool
Image cutting, comparison and save.

[![Demo.png](https://i.postimg.cc/8CnzjVs6/Demo.png)](https://postimg.cc/QB13ywQ8)

### Usage


python Launcher.py


### Package require

-PyQt5  (sudo apt-get install python3-pyqt5)

-numpy 

-opencv-python

-pillow

### Image Dir root hierarchy

#### HR folder is necessary and every image from each subdir should be the same name.

````
Image Dir root
    |
    --------- RealSR_SRCNN
    |           |
    |           ------------img_1.png
    |           |
    |           ------------img_2.png
    |
    --------- RealSR_EDSR
    |           |
    |           ------------img_1.png
    |           |
    |           ------------img_2.png
    |
    --------- RealSR_ESRGAN
    |
    --------- RealSR_DASR
    ......
    |
    --------- HR    # HR folder IS NECESSARY
````
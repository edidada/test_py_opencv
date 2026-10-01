import numpy as np


def test_opencv_import():
    import cv2

    assert cv2.__version__


def test_numpy_ops():
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    assert img.shape == (100, 100, 3)

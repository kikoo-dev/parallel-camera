import cv2
import numpy as np

def full_pipeline(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_f = gray.astype(np.float32)

    b1 = cv2.GaussianBlur(gray_f, (31, 31), 0)
    b2 = cv2.GaussianBlur(gray_f, (63, 63), 0)
    dog = cv2.subtract(b1, b2)

    dog_norm = cv2.normalize(dog, None, 0, 255, cv2.NORM_MINMAX)
    return cv2.cvtColor(dog_norm.astype(np.uint8), cv2.COLOR_GRAY2BGR)
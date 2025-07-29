import platform
import numpy as np
import cv2

def compute_angle(a, b, c):
    a, b, c = map(np.array, (a, b, c))
    ba, bc = a - b, c - b
    cosv = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    return np.degrees(np.arccos(np.clip(cosv, -1.0, 1.0)))

def rotate_frame(frame, mode):
    if mode == 'cw':
        return cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    if mode == 'ccw':
        return cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    if mode == '180':
        return cv2.rotate(frame, cv2.ROTATE_180)
    return frame

def select_backend():
    os_name = platform.system()
    if os_name == 'Darwin':
        return cv2.CAP_AVFOUNDATION
    if os_name == 'Windows':
        return cv2.CAP_DSHOW
    return cv2.CAP_ANY

import cv2
import numpy as np

def apply_grayscale(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def apply_blur(gray):
    return cv2.GaussianBlur(gray, (15, 15), 0)

def apply_edge_detection(blurred):
    return cv2.Canny(blurred, 50, 150)

def colorize_edges(edges):
    # Kembalikan ke 3-channel BGR agar bisa digabung
    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

def full_pipeline(frame):
    """Satu pipeline lengkap: grayscale → blur → edge → colorize"""
    gray   = apply_grayscale(frame)
    blurred = apply_blur(gray)
    edges  = apply_edge_detection(blurred)
    result = colorize_edges(edges)
    return result
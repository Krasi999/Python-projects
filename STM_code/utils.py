import cv2
import os
 
def load_image(path):
    """
    Loads an image from disk. Returns None if the file does not exist.
    """
    img = cv2.imread(path)
    if img is None:
        print(f"Error: Failed to load image at '{path}'. Please check if the file exists.")
    return img
 
 
def get_size(encoded_image):
    """
    Returns the size of the compressed image in bytes.
    """
    return len(encoded_image)
 
 
def resize_image(image, width, height):
    """
    Resizes the image to a specified width and height.
    """
    return cv2.resize(image, (width, height))
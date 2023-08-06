import cv2

def blur(image):
    blurred = cv2.blur(image, (3, 3))
    return blurred

def edge_detection(image):
    edges = cv2.Canny(image, 100, 200)
    return edges

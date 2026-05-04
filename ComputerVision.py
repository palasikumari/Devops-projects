import cv2
import numpy as np
from matplotlib import pyplot as plt
image_path = r"C:\Users\user31\Downloads\mrOrangeCat.jpg"
image = cv2.imread(image_path)
if image is None:
    print("Error: Image not found. Check the path")
    exit()
height,width,channels = image.shape
print(f"Image Dimensions:{width}*{height}")
print(f"Number of Channels:{channels}")
image_rgb = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
plt.figure(figsize=(6,6))
plt.title("Original Image")
plt.imshow(image_rgb)
plt.axis("off")
plt.show()
gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
plt.figure(figsize=(6,6))
plt.title("Grayscale Image")
plt.imshow(gray_image,cmap='gray')
plt.axis("off")
plt.show()
edges=cv2.Canny(gray_image,threshold1=100,threshold2=200)
plt.figure(figsize=(6,6))
plt.title("Edge Detection")
plt.imshow(edges,cmap='gray')
plt.axis("off")
plt.show()
color = ('b','g','r')
plt.figure(figsize=(6,4))
plt.title("Color Histogram")
for i, col in enumerate(color):
    hist = cv2.calcHist([image],[i],None,[256],[0,256])
    plt.plot(hist,color=col)
    plt.xlim([0,256])
plt.xlabel("Pixel Value")
plt.ylabel("Frequency")
plt.show()
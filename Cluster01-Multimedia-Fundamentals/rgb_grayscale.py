import cv2
import matplotlib.pyplot as plt

# Read image
img = cv2.imread("sample.jpg")

# Check whether image was loaded
if img is None:
    print("Error: sample.jpg not found!")
    exit()

# Image information
print("Shape:", img.shape)
print("Data type:", img.dtype)
print("Min/Max:", img.min(), img.max())

# Convert BGR image to Grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

print("Gray shape:", gray.shape)

# Display images
plt.figure(figsize=(8, 4))

plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title("Original RGB Image")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(gray, cmap="gray")
plt.title("Grayscale Image")
plt.axis("off")

plt.tight_layout()
plt.show()


import cv2
import os
import matplotlib.pyplot as plt

# Original image path
image_path = r"F:\multimedia lab\sample.jpg"

# Read image
img = cv2.imread(image_path)

if img is None:
    print("Error: Image not found!")
else:
    original_size = os.path.getsize(image_path)

    print("===== IMAGE COMPRESSION REPORT =====")
    print("Original Image Size:",
          round(original_size / 1024, 2), "KB")

    # Different JPEG quality levels
    qualities = [90, 70, 50, 30]

    compressed_images = []
    compressed_sizes = []

    for quality in qualities:

        output_path = (
            f"F:\\multimedia lab\\compressed_{quality}.jpg"
        )

        # Compress image
        cv2.imwrite(
            output_path,
            img,
            [cv2.IMWRITE_JPEG_QUALITY, quality]
        )

        # Calculate compressed size
        size = os.path.getsize(output_path)

        compressed_images.append(cv2.imread(output_path))
        compressed_sizes.append(size)

        print(
            f"Quality {quality}: "
            f"{round(size / 1024, 2)} KB"
        )

    # Display original and compressed images
    plt.figure(figsize=(15, 7))

    plt.subplot(1, 5, 1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title("Original")
    plt.axis("off")

    for i in range(len(qualities)):
        plt.subplot(1, 5, i + 2)

        rgb = cv2.cvtColor(
            compressed_images[i],
            cv2.COLOR_BGR2RGB
        )

        plt.imshow(rgb)
        plt.title(f"Quality {qualities[i]}")
        plt.axis("off")

    plt.tight_layout()
    plt.show()

    print("\nImage compression completed!")

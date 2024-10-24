import cv2

# Load the image
image_path = 'page_1.jpg'
image = cv2.imread(image_path)

# Check if the image was loaded successfully
if image is None:
    raise FileNotFoundError(f"Image not found at {image_path}")

# Get the dimensions of the image
height, width = image.shape[:2]

# Define the number of rows and columns to split into
num_rows = 10  # Adjust based on your needs
num_cols = 3  # Adjust based on your needs

# Calculate height and width of each piece
piece_height = height // num_rows
piece_width = width // num_cols

# Split the image into smaller pieces and save them
for row in range(num_rows):
    for col in range(num_cols):
        y_start = row * piece_height
        y_end = (row + 1) * piece_height
        x_start = col * piece_width
        x_end = (col + 1) * piece_width
        piece = image[y_start:y_end, x_start:x_end]
        
        # Save each piece
        piece_path = f'piece_{row}_{col}.jpg'
        cv2.imwrite(piece_path, piece)

print(f"Image split into {num_rows * num_cols} pieces.")

import cv2
from skimage.metrics import structural_similarity as ssim
import pyautogui as pg

# Get screen resolution
resolution = pg.size()  # Example: (1920, 1080)

# Convert resolution to string to display
resolution_text = f"Resolution: {resolution[0]}x{resolution[1]}"




# Define the function to calculate SSIM (Structural Similarity Index)
def calculate_ssim(image1, image2):
    return ssim(image1, image2, full=True)[0]  # returns the SSIM score between 0 and 1

# Capture video feed (assuming your camera is at index 0)
cap = cv2.VideoCapture("Myanmar military destroy CCTV camera on the street.mp4")

# Ensure the camera is opened
if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

# Capture the first frame and save it as the reference frame
ret, original_frame = cap.read()
if not ret:
    print("Error: Could not read frame.")
    exit()

# Save the original frame (first capture)
original_frame_gray = cv2.cvtColor(original_frame, cv2.COLOR_BGR2GRAY)

# Define boundary regions (small strips from all four boundaries)
height, width = original_frame_gray.shape
strip_height = 30  # Define the height of the boundary strips (you can adjust this)
strip_width = 30  # Define the width of the boundary strips

# Extract boundary strips from original frame
top_strip = original_frame_gray[:strip_height, :]
bottom_strip = original_frame_gray[-strip_height:, :]
left_strip = original_frame_gray[:, :strip_width]
right_strip = original_frame_gray[:, -strip_width:]

# Continuously capture frames and compare with the original frame boundaries
while True:
    ret, current_frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break
    
    # Convert current frame to grayscale
    current_frame_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    
    # Extract boundary strips from the current frame
    current_top_strip = current_frame_gray[:strip_height, :]
    current_bottom_strip = current_frame_gray[-strip_height:, :]
    current_left_strip = current_frame_gray[:, :strip_width]
    current_right_strip = current_frame_gray[:, -strip_width:]
    
    # Compare the boundary strips using SSIM
    top_ssim = calculate_ssim(top_strip, current_top_strip)
    bottom_ssim = calculate_ssim(bottom_strip, current_bottom_strip)
    left_ssim = calculate_ssim(left_strip, current_left_strip)
    right_ssim = calculate_ssim(right_strip, current_right_strip)
    
    # Define a threshold for SSIM difference to detect tampering
    ssim_threshold = 0.9 # Adjust this threshold based on your use case
    # Draw the resolution text on the frame
    # cv2.putText(current_frame, resolution_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Check if any boundary strip shows significant change
    if top_ssim < ssim_threshold and bottom_ssim < ssim_threshold and left_ssim < ssim_threshold and right_ssim < ssim_threshold:
        print("Warning: Camera tampering detected!")
        cv2.putText(current_frame, "Camera Tampering Detected!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    # Show the current frame
    new=cv2.resize(current_frame,(1920//2,1080//2))
    cv2.imshow("Camera Feed", new)

    
    # Exit on pressing 'q'
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()

import geopandas as gpd
import os
import cv2
import time


# Load the GeoDataFrame
geojson_data = gpd.read_file("C:/Users/User/Desktop/Geo sampler/Data/resultado.geojson") 
# Extract timestamps from the GeoJSON data
timestamps = geojson_data['time']
# Path to the MP4 file
video_path = 'C:/Users/User/Desktop/Geo sampler/Data/EO_1.mp4'
# Create a directory to save the extracted frames
output_dir = 'C:/Users/User/Desktop/Geo sampler/Results/frames'
os.makedirs(output_dir, exist_ok=True)

# Get the total number of timestamps
total_timestamps = len(timestamps)
print(len(timestamps))

# Open the video file
cap = cv2.VideoCapture(video_path)

# Start time
start_time = time.time()

# Loop through the timestamps and extract frames
for index, timestamp in enumerate(timestamps):
    # Convert timestamp to seconds
    time_seconds = int(timestamp)
    print(time_seconds)
    
    # Set the video position to the specific timestamp
    cap.set(cv2.CAP_PROP_POS_MSEC, time_seconds * 1000)
    
    # Read the frame
    ret, frame = cap.read()
    
    if ret:
        # Define the output frame path
        output_frame_path = os.path.join(output_dir, f'frame_{time_seconds}.png')
        print(output_frame_path)
        
        # Save the frame as an image
        cv2.imwrite(output_frame_path, frame)
        
        # Calculate the percentage of completion
        percentage = (index + 1) / total_timestamps * 100
        
        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        
        # Print progress information
        print(f"Progress: {percentage:.2f}% - Elapsed Time: {elapsed_time:.2f} seconds")
    else:
        print(f"Failed to extract frame at {time_seconds} seconds")

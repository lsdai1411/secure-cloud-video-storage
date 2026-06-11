from crypto.hash_utils import *

with open(
    "test_files/video.mp4",
    "rb"
) as f:

    video_data = f.read()

hash_value = calculate_hash(
    video_data
)

print(hash_value)
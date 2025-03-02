import instaloader
import os

# Define parameters
USERNAME = "kylewhirl"  # Your Instagram username
TARGET_PROFILE = "salonplatinumreno"  # The profile to scrape
SESSION_FILE = os.path.expanduser("~/.config/instaloader/session-kylewhirl")
OUTPUT_DIR = "instagram-images"
IMAGE_LIMIT = 3  # Only download the latest 3 images

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize Instaloader
loader = instaloader.Instaloader(download_videos=False, download_comments=False, save_metadata=False)

# Load session for authentication
loader.load_session_from_file(USERNAME, SESSION_FILE)

# Fetch profile
profile = instaloader.Profile.from_username(loader.context, TARGET_PROFILE)

# Track downloaded images
downloaded_images = 0

# Loop through profile posts and download only 3 images
for post in profile.get_posts():
    if downloaded_images >= IMAGE_LIMIT:
        break  # Stop after 3 images

    loader.download_post(post, target=OUTPUT_DIR)
    downloaded_images += 1

print(f"Downloaded {downloaded_images} images to {OUTPUT_DIR}.")

import instaloader
import os
import re

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

# Loop through profile posts (excluding pinned posts)
for post in profile.get_posts():
    if downloaded_images >= IMAGE_LIMIT:
        break  # Stop after 3 images

    # Get all image URLs in the post (handles carousel posts)
    image_urls = post.get_sidecar_nodes() if post.is_sidecar else [post]

    for index, img in enumerate(image_urls):
        if downloaded_images >= IMAGE_LIMIT:
            break  # Stop once we have 3 images

        # Define filename
        image_filename = f"{OUTPUT_DIR}/{downloaded_images + 1}.jpg"

        # Download the image
        loader.download_pic(image_filename, img.display_url, post.date_utc)
        downloaded_images += 1

print(f"Downloaded {downloaded_images} images to {OUTPUT_DIR}.")

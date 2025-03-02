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

# Collect images: first pinned, then newest regular posts
downloaded_images = 0
image_queue = []  # Stores tuples (url, filename)

# First, get pinned posts
for post in profile.get_pinned_posts():
    if downloaded_images >= IMAGE_LIMIT:
        break
    image_urls = post.get_sidecar_nodes() if post.is_sidecar else [post]
    for img in image_urls:
        if downloaded_images >= IMAGE_LIMIT:
            break
        image_queue.append((img.display_url, f"{OUTPUT_DIR}/{downloaded_images + 1}.jpg"))
        downloaded_images += 1

# Next, get regular (non-pinned) posts to fill remaining slots
for post in profile.get_posts():
    if downloaded_images >= IMAGE_LIMIT:
        break
    image_urls = post.get_sidecar_nodes() if post.is_sidecar else [post]
    for img in image_urls:
        if downloaded_images >= IMAGE_LIMIT:
            break
        image_queue.append((img.display_url, f"{OUTPUT_DIR}/{downloaded_images + 1}.jpg"))
        downloaded_images += 1

# Download the images
for url, filename in image_queue:
    loader.download_pic(filename, url, None)

print(f"Downloaded {downloaded_images} images to {OUTPUT_DIR}.")

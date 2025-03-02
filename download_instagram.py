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

# Loop through profile posts
for post in profile.get_posts():
    if downloaded_images >= IMAGE_LIMIT:
        break  # Stop after 3 images

    # If post is a carousel (multiple images), only take the first image
    if post.typename == "GraphSidecar":
        first_image = next(iter(post.get_sidecar_nodes()), None)  # Get first item from generator
        if first_image is not None:
            image_url = first_image.display_url
        else:
            continue  # Skip if no valid image found
    else:
        image_url = post.url  # Use post.url for single image posts

    # Define filename without extension so that Instaloader appends .jpg automatically
    image_filename = f"{OUTPUT_DIR}/{downloaded_images + 1}"

    # Download the image
    loader.download_pic(image_filename, image_url, post.date_utc)
    downloaded_images += 1

print(f"Downloaded {downloaded_images} images to {OUTPUT_DIR}.")

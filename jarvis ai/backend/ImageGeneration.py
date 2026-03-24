import asyncio     
from random import randint
from PIL import Image
import requests
from dotenv import load_dotenv
import os
from time import sleep

# Load environment variables
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HuggingFaceAPIKey")

# Ensure output folder exists
os.makedirs("Data", exist_ok=True)

# Hugging Face API
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

# Function to open and display images based on a given prompt
def open_images(prompt):
    folder_path = "Data"
    prompt_clean = prompt.replace(" ", "_")

    for i in range(1, 5):
        image_path = os.path.join(folder_path, f"{prompt_clean}{i}.jpg")

        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)
        except IOError:
            print(f"[ERROR] Unable to open {image_path}")

# Async function to send prompt to Hugging Face API
async def query(payload):
    try:
        response = await asyncio.to_thread(
            requests.post, API_URL, headers=headers, json=payload
        )

        if response.status_code != 200:
            print(f"[API ERROR] {response.status_code}: {response.text}")
            return None
        return response.content
    except Exception as e:
        print(f"[Exception during API call] {e}")
        return None

# Async function to generate images from a prompt
async def generate_images(prompt: str):
    tasks = []

    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4k, sharpness=maximum, ultra high detail, high resolution, seed={randint(0, 1000000)}"
        }
        tasks.append(asyncio.create_task(query(payload)))

    image_bytes_list = await asyncio.gather(*tasks)

    prompt_clean = prompt.replace(" ", "_")

    for i, image_bytes in enumerate(image_bytes_list):
        if image_bytes:
            filename = f"{prompt_clean}{i + 1}.jpg"
            with open(os.path.join("Data", filename), "wb") as f:
                f.write(image_bytes)
        else:
            print(f"[WARNING] Image {i+1} was not generated.")

# Wrapper function
def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt))
    open_images(prompt)

# Main loop to monitor the request file
while True:
    try:
        with open("frontend/Files/ImageGeneration.data", "r") as f:
            data = f.read().strip()

        if not data:
            sleep(1)
            continue

        Prompt, Status = map(str.strip, data.split(","))

        if Status == "True":
            print(f"[INFO] Generating images for: {Prompt}")
            GenerateImages(Prompt)

            with open("Frontend/Files/ImageGeneration.data", "w") as f:
                f.write("False,False")

            break

        else:
            sleep(1)

    except Exception as e:
        print(f"[ERROR] {e}")
        sleep(1)

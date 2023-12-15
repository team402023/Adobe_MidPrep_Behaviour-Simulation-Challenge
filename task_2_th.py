import torch
from transformers import pipeline, BitsAndBytesConfig
import requests
from PIL import Image
import re
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
df = pd.read_excel('./content_simulation_test_company.xlsx')
# Function to extract image links from DataFrame
def extract_link(x):
    match_ = re.search(r"previewUrl='(.*?)'|thumbnailUrl='(.*?)'", x)
    if match_:
        return match_.group(1) or match_.group(2)
    else:
        return "URL not found."

df['extracted_links'] = df['media'].apply(extract_link)

quantization_config = BitsAndBytesConfig(
         load_in_4bit=True,
         bnb_4bit_compute_dtype=torch.float16
    )

model_id = "llava-hf/llava-1.5-7b-hf"
max_new_tokens = 200
pipe = pipeline("image-to-text", model=model_id, model_kwargs={"quantization_config": quantization_config})



def tweet(link, brand, username, likes,date):
    first_image_url = link
    
    try:
        # Attempt to load the image from the URL
        image = Image.open(requests.get(first_image_url, stream=True).raw)
    except Exception as e:
        print(f"Error loading image from {first_image_url}: {e}")
        return "Image not loaded"
    
    brand_name = brand
    username = username
    likes = likes 
    date = date 
    prompt2 = f"USER: <image>\nCreate an engaging tweet caption for this image that aligns with {brand_name} style. Do consider the other name {username} . the date of the tweet is {date} , see if there is anything special on this day. Identify the place and text in the image. Also identify the objects in the image. Craft it to gather {likes} likes. Avoid direct brand mentions or like counts in the output. Incorporate relevant hashtags for maximum engagement."
    prompt = f"USER: <image>\nGenerate a tweet caption for this specific image that has brand name = {brand_name}, make a marketing tweet text in a way that it receives {likes} likes.the date of the tweet is {date}. Do not print the brand name and likes, and also provide hashtags."
    

    outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})
    text = outputs[0]['generated_text']
    original_string = text
    sentence_to_remove = "USER:this is the input image:  \nCreate a compelling tweet caption for the image featuring the brand \'pepsico\' and has twitter username \'PepsiCoAMESA\'. identify the text in the image and Craft a tweet such a way to get \'1\' likes. Avoid mentioning the likes explicitly. Include relevant hashtags to enhance visibility and appeal. Be creative and engaging in your description. Also try identifying the place in the image and also the objects present in the image. mention the place in the image. Do mention the username . Give one liner text only. \n\n"
    result_string = original_string.replace(sentence_to_remove, "")
    print(result_string)
    return result_string

    

# Function to process images in batches
def process_images(df):
    # Extract links from DataFrame
    df['extracted_links'] = df['media'].apply(extract_link)
    
    # Create a ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        futures = []
        for i, row in df.iterrows():
            link = row['extracted_links']
            brand = row['inferred company']
            username = row['username']
            likes = row['likes']
            date = row['date']
            
            # Submit tasks to the executor
            futures.append(executor.submit(tweet, link, brand, username, likes, date))

        # Gather results from the futures
        results = [future.result() for future in futures]

    return results

# Read your DataFrame (replace with your file path and logic)
df = pd.read_excel('./content_simulation_test_company.xlsx')

# Process images in batches
results = process_images(df.head(100))  # Process the first 100 rows

# Save results to a CSV file or perform further processing as needed
result_df = pd.DataFrame(results)
result_df.to_csv('processed_results.csv', index=False)

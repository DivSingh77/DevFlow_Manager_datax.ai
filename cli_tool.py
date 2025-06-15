import argparse
import requests
import json
import base64
from PIL import Image
import io
import pandas as pd
from typing import Dict, Union, List

def process_image(url: str) -> Dict[str, Union[str, int]]:
    try:
        # Download image
        response = requests.get(url)
        response.raise_for_status()
        
        # Load image and get original size
        img_data = io.BytesIO(response.content)
        img = Image.open(img_data)
        original_size = len(response.content)
        original_resolution = f"{img.width}x{img.height}"
        
        # Resize image
        target_size = (320, 568)
        img.thumbnail(target_size, Image.Resampling.LANCZOS)
        
        # Convert images to base64
        original_base64 = base64.b64encode(response.content).decode()
        
        resized_buffer = io.BytesIO()
        img.save(resized_buffer, format=img.format)
        resized_base64 = base64.b64encode(resized_buffer.getvalue()).decode()
        
        return {
            "image_url": url,
            "status": "success",
            "original_image64": original_base64,
            "resized_image64": resized_base64,
            "size": original_size,
            "resolution": original_resolution
        }
        
    except Exception as e:
        return {
            "image_url": url,
            "status": "error",
            "error_message": str(e)
        }

def main():
    parser = argparse.ArgumentParser(description='Process images from URL or CSV')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--image-url', help='Single image URL to process')
    group.add_argument('--csv-file', help='CSV file containing image URLs')
    
    args = parser.parse_args()
    results = []
    
    if args.image_url:
        results.append(process_image(args.image_url))
    else:
        df = pd.read_csv(args.csv_file)
        for url in df['url']:  # Assuming the column name is 'url'
            results.append(process_image(url))
    
    # Save results to JSON file
    output_file = 'processed_images.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    main()
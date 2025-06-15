import requests, csv, base64, json, io, os
from PIL import Image
from urllib.parse import urlparse
import argparse

OUTPUT_FILE = "image_output.json"

def download_image(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return Image.open(io.BytesIO(response.content)), response.content
    except Exception as e:
        return None, str(e)

def get_image_info(img, raw_bytes):
    width, height = img.size
    size = len(raw_bytes)
    return f"{width}x{height}", size

def resize_image(img):
    img_copy = img.copy()
    img_copy.thumbnail((320, 568))  # preserve aspect ratio
    return img_copy

def encode_image(img):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def process_url(url):
    result = {"image_url": url}
    img, content = download_image(url)
    if img is None:
        result["status"] = f"error - {content}"
        return result

    try:
        resolution, size = get_image_info(img, content)
        resized_img = resize_image(img)

        result.update({
            "status": "success",
            "resolution": resolution,
            "size": size,
            "original_image64": base64.b64encode(content).decode('utf-8'),
            "resized_image64": encode_image(resized_img),
        })
    except Exception as e:
        result["status"] = f"error - {str(e)}"

    return result

def read_csv_urls(csv_path):
    urls = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row: urls.append(row[0])
    return urls

def main():
    parser = argparse.ArgumentParser(description="Download, resize, and convert image(s) to base64.")
    parser.add_argument('--url', type=str, help='Single image URL')
    parser.add_argument('--csv', type=str, help='CSV file path with image URLs')

    args = parser.parse_args()

    results = []

    if args.url:
        results.append(process_url(args.url))

    elif args.csv:
        urls = read_csv_urls(args.csv)
        for url in urls:
            results.append(process_url(url))
    else:
        print("❌ Please provide either --url or --csv option.")
        return

    with open(OUTPUT_FILE, "w") as outfile:
        json.dump(results, outfile, indent=4)

    print(f"✅ Done! Output written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

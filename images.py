import requests

API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
headers = {"Authorization": "Bearer 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"}

# Read the image file as binary
with open("verma.jpg", "rb") as image_file:
    image_bytes = image_file.read()

# Define generation parameters as query parameters
params = {
    "max_new_tokens": 200,
    "min_length": 50,
    "num_beams": 10
}

# Send the image bytes directly as the POST body
response = requests.post(API_URL, headers=headers, params=params, data=image_bytes)
result = response.json()

if isinstance(result, list) and result:
    print(result[0].get('generated_text', 'No caption generated'))
else:
    print("Error:", result)

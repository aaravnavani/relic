import openai
import base64

openai.api_key = "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"

# Read image and encode to base64
with open("verma.jpg", "rb") as img_file:
    b64_img = base64.b64encode(img_file.read()).decode()

response = openai.ChatCompletion.create(
  model="gpt-4-vision-preview",
  messages=[
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "Describe this image in detail."},
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{b64_img}"
          },
        },
      ],
    }
  ],
  max_tokens=1000,
)

print(response['choices'][0]['message']['content'])

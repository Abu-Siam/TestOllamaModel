import time
import json
import requests
from pymupdf import pymupdf

# Start time measurement
start_time = time.time()

# Step 1: Extract text from PDF
pdf_file_path = "INV-49.xlsx - Google Sheets.pdf"
output_text_file = "output.txt"

reader = pymupdf.open(pdf_file_path)
pdf_text = ""
for page in reader:
    text = page.get_text()
    if text:
        pdf_text += text + "\n"

# Write extracted text to a file
with open(output_text_file, "w", encoding="utf-8") as file:
    file.write(pdf_text)

print(f"Extracted text has been saved to {output_text_file}")

# Step 2: Read extracted text
with open(output_text_file, "r", encoding="utf-8") as file:
    extracted_text = file.read()
# Step 3: Define API details
url = "http://localhost:11434/api/chat"
headers = {"Content-Type": "application/json"}
data = {
    "model": "phi3:latest",
    "messages": [
        {"role": "user", "content": f" Extract the following fields from the given text and return them in JSON format:\n\n"
        +"Exporter, Buyers bank, consignee, Port of loading, Invoice No. & Date, EXP NO., S/C NO."
              +
               f"freight order Content:{ extracted_text}", "context": "data collect from freight order PDF"}
    ]

    # "messages": [
    #     {"role": "user",
    #      "content": "above answer has phd degree but its wrong"}
    # ]
}

# Step 4: Make API request
response = requests.post(url, json=data, headers=headers)

# Step 5: Process the response
if response.status_code == 200:
    content = response.content.decode('utf-8')

    # Split response into individual JSON objects
    response_list = content.split('\n')

    # Parse each JSON string into a Python dictionary
    response_json = [json.loads(item) for item in response_list if item]

    # Extract the summary text from response
    paragraph = ''.join(item['message']['content'] for item in response_json)

    print("Summarized JSON Output:")
    print(paragraph)
else:
    print("Error:", response.status_code, response.text)

# End time measurement
end_time = time.time()
execution_time = end_time - start_time

print(f"\nTotal Execution Time: {execution_time:.2f} seconds")

x= "AIzaSyCvhPg1jVdJmvHN9Zlf3K5dRnOVL3TXBt0"
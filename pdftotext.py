import time
import json

import requests
from pymupdf import pymupdf
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from datetime import datetime, timedelta
import fitz
import jwt
from fastapi.security import OAuth2PasswordBearer
app = FastAPI()

# Start time measurement
start_time = time.time()
SECRET_KEY="qwerty123456"
ALGORITHM = "HS256"
ACCESS_TOKEN = jwt.encode({"exp": datetime.now() + timedelta(days=365)}, SECRET_KEY, algorithm=ALGORITHM)  # Token valid for 1 year

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Function to verify token
def verify_token(token: str = Depends(oauth2_scheme)):
    if token != ACCESS_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return token


# Route to get the static token (Share this manually)
@app.get("/get-token")
def get_static_token():
    return {"token": ACCESS_TOKEN}


@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...), token: str = Depends(verify_token)):
    # Start time measurement
    start_time = time.time()

    # Step 1: Read the uploaded PDF file
    pdf_text = ""
    pdf_file = await file.read()  # Read the file content
    reader = fitz.open(stream=pdf_file, filetype="pdf")  # Open PDF from bytes

    for page in reader:
        text = page.get_text()
        if text:
            pdf_text += text + "\n"

    # # Write extracted text to a file
    # with open(output_text_file, "w", encoding="utf-8") as file:
    #     file.write(pdf_text)
    #
    # print(f"Extracted text has been saved to {output_text_file}")
    #
    # # Step 2: Read extracted text
    # with open(output_text_file, "r", encoding="utf-8") as file:
    #     extracted_text = file.read()
    # Step 3: Define API details
    url = "http://localhost:11434/api/chat"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "gemma2:2b",
        "messages": [
            {"role": "user",
             "content": f" Extract the following fields from the given text and return them in JSON format without special characters:\n\n"
                        + "name, phone, email,graduation degree,graduation institute, graduation subject, graduation year, previous workplace, total experience"
                        +
                        f"CV Content:{pdf_text}", "context": "data collect from resume"}
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
        # print(paragraph)
        # End time measurement
        end_time = time.time()
        execution_time = end_time - start_time
        clean_response = paragraph.replace("```json", "").replace("```", "").strip()
        # print(f"\nTotal Execution Time: {execution_time:.2f} seconds")
        data = json.loads(clean_response)
        print(clean_response)
        print(data)
        return {"Response":data}
    else:
        print("Error:", response.status_code, response.text)
        return {"Response": response}



# # Step 1: Extract text from PDF
# pdf_file_path = "./cv/1d6e6b42-9182-4d42-ac9b-864cb813b98c.pdf"
# output_text_file = "output.txt"
#
# reader = pymupdf.open(pdf_file_path)
# pdf_text = ""
# for page in reader:
#     text = page.get_text()
#     if text:
#         pdf_text += text + "\n"
#
# # Write extracted text to a file
# with open(output_text_file, "w", encoding="utf-8") as file:
#     file.write(pdf_text)
#
# print(f"Extracted text has been saved to {output_text_file}")
#
# # Step 2: Read extracted text
# with open(output_text_file, "r", encoding="utf-8") as file:
#     extracted_text = file.read()
# # Step 3: Define API details
# url = "http://localhost:11434/api/chat"
# headers = {"Content-Type": "application/json"}
# data = {
#     "model": "gemma2:2b",
#     "messages": [
#         {"role": "user", "content": f" Extract the following fields from the given text and return them in JSON format:\n\n"
#         +"name, phone, email,graduation degree,graduation institute, graduation subject, graduation year, previous workplace, total experience"
#               +
#                f"CV Content:{ extracted_text}", "context": "data collect from resume"}
#     ]
#
#     # "messages": [
#     #     {"role": "user",
#     #      "content": "above answer has phd degree but its wrong"}
#     # ]
# }
#
# # Step 4: Make API request
# response = requests.post(url, json=data, headers=headers)
#
# # Step 5: Process the response
# if response.status_code == 200:
#     content = response.content.decode('utf-8')
#
#     # Split response into individual JSON objects
#     response_list = content.split('\n')
#
#     # Parse each JSON string into a Python dictionary
#     response_json = [json.loads(item) for item in response_list if item]
#
#     # Extract the summary text from response
#     paragraph = ''.join(item['message']['content'] for item in response_json)
#
#     print("Summarized JSON Output:")
#     print(paragraph)
# else:
#     print("Error:", response.status_code, response.text)
#
# # End time measurement
# end_time = time.time()
# execution_time = end_time - start_time
#
# print(f"\nTotal Execution Time: {execution_time:.2f} seconds")
#
# x= "AIzaSyCvhPg1jVdJmvHN9Zlf3K5dRnOVL3TXBt0"
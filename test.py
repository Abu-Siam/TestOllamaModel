import json

# Given response with JSON as a string
response = {
    "Response": "{\n  \"name\": \"Md. Al Arman\",\n  \"phone\": \"+8801730088195\",\n  \"email\": \"armaniutian@gmail.com\",\n  \"graduation degree\": \"Master of Business Administration (MBA)\", \n  \"graduation institute\": \"Institute of Business Administration (IBA, DU)\",\n  \"graduation subject\": null,\n  \"graduation year\": 2019, \n  \"previous workplace\": [\n    \"Software QA Manager, Nilavo Technologies Limited\",\n    \"Co-founder and CEO (Part-time), Storrea Limited\",\n    \"Software QA Lead, Nilavo Technologies Limited\", \n    \"Software QA Engineer, Nilavo Technologies Limited\",\n    \"Senior Software QA Engineer, Nilavo Technologies Limited\"\n  ],\n  \"total experienceCV\": \"14 years\"\n}"
}

# Step 1: Extract the string from "Response"
json_string = response["Response"]

# Step 2: Parse the string into a JSON object
try:
    parsed_json = json.loads(json_string)
    print(parsed_json)
    print(json.dumps(parsed_json, indent=4))  # Pretty print the JSON
except json.JSONDecodeError as e:
    print("Error in parsing JSON:", e)

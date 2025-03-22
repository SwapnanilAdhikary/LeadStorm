from search import search_links
from webscrapper import scrape_website
import json
import os
import csv
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyBjzOA-HWBjukCW6HflXNcN7PA2fdmirRE")

# Define the lead generation query parameters
URL = "Generate a list of healthcare companies with Chief Marketing Officers (CMOs) and provide their contact emails for a potential partnership"
NUM_RESULT = 5
DRIVER_PATH = "C://Users//adhik//Downloads//chromedriver-win64//chromedriver.exe"

# Get search results and scrape each website
search_result = search_links(URL, NUM_RESULT)
json_data_aggregator = []
for idx, link in enumerate(search_result):
    output_filename = f"scraped_data_{idx+1}.json"
    scrape_website(link, DRIVER_PATH, output_filename)

# Load the scraped JSON data
for idx in range(1, 6):
    filename = f"scraped_data_{idx}.json"
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            json_data_aggregator.append(json.load(file))

# Convert each JSON entry to a formatted string for the prompt
formatted_data = "\n\n".join([json.dumps(entry, indent=2) for entry in json_data_aggregator])

# Create prompt to instruct the AI with the specific lead generation requirements
prompt = f"""
I have collected JSON data from various websites about technology companies in Kolkata that are actively investing in AI solutions.
For each JSON data entry, please do the following:
1. Predict the most likely company name based on the content.
2. Generate a concise summary of the company's key offerings, strategy, and how they invest in AI.
3. Extract a contact email address if present; if none is found, leave it blank.
4. Extract the name of a decision maker (such as CEO, CTO, or another key executive) if available; if not, leave it blank.

Return your results in CSV format with exactly four columns: "Company Name", "Summary", "Email", "Decision Maker".
Do not include any extra commentary or explanation; only output valid CSV content.

Here is the raw JSON data:
{formatted_data}
"""

# Generate the CSV content using Gemini
model = genai.GenerativeModel("gemini-1.5-flash-8b")
response = model.generate_content(prompt)

# Write the CSV output to a file
csv_filename = "company_predictions.csv"
csv_data = response.text.strip().split("\n")

with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    for row in csv_data:
        writer.writerow(row.split(","))

print(f"CSV file '{csv_filename}' has been created with the predicted company names, summaries, emails, and decision maker names.")

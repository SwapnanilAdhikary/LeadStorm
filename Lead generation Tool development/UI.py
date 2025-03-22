import streamlit as st
import json
import os
import io
import csv
import pandas as pd
import google.generativeai as genai
from search import search_links
from webscrapper import scrape_website

# Configure Gemini API (replace with your actual API key)
genai.configure(api_key="AIzaSyBjzOA-HWBjukCW6HflXNcN7PA2fdmirRE")

st.title("LeadStorm: AI-Powered Lead Accelerator")
st.markdown("Generate quality leads with our AI-driven tool. Enter your search query to fetch and analyze potential leads.")

# User Input for Search Query and options
query = st.text_input(
    "Enter Lead Generation Query:", 
    "List technology companies in Kolkata that are actively investing in AI solutions, including contact emails and decision-maker names"
)
num_results = st.slider("Number of Results to Scrape", 1, 10, 5)
driver_path = st.text_input("ChromeDriver Path:", "C://Users//adhik//Downloads//chromedriver-win64//chromedriver.exe")
show_json = st.checkbox("Show scraped JSON data", value=False)

if st.button("Generate Leads"):
    st.info("Fetching search results and scraping data...")
    
    # Get search results and scrape websites
    search_result = search_links(query, num_results)
    json_data_aggregator = []
    
    for idx, link in enumerate(search_result):
        output_filename = f"scraped_data_{idx+1}.json"
        scrape_website(link, driver_path, output_filename)
    
    # Load the scraped JSON data
    for idx in range(1, num_results + 1):
        filename = f"scraped_data_{idx}.json"
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                json_data_aggregator.append(data)
    
    # Optionally display the raw JSON data
    if show_json:
        st.subheader("Scraped JSON Data")
        for idx, data in enumerate(json_data_aggregator, start=1):
            st.write(f"**File scraped_data_{idx}.json**")
            st.json(data)
    
    # Format each JSON entry to a formatted string for the prompt
    formatted_data = "\n\n".join([json.dumps(entry, indent=2) for entry in json_data_aggregator])
    
    # Build the prompt for Gemini
    prompt = f"""
    I have collected JSON data from various websites about technology companies in Kolkata that are actively investing in AI solutions.
    For each JSON data entry, please do the following:
    1. Predict the most likely company name based on the content.
    2. Generate a concise summary of the company's key offerings, strategy, and how they invest in AI.
    3. Extract a contact email address if present; if none is found, leave it blank.
    4. Extract the name of a decision maker (such as CEO, CTO, or another key executive) if available; if not, leave it blank.
    
    Return your results in CSV format with exactly four columns: "Company Name", "Summary", "Email", "Decision Maker".
    **Ensure that any field containing commas is enclosed in double quotes. Do not include any extra commentary or explanation; only output valid CSV content.**
    
    Here is the raw JSON data:
    {formatted_data}
    """
    
    # Generate CSV content using Gemini
    model = genai.GenerativeModel("gemini-1.5-flash-8b")
    response = model.generate_content(prompt)
    
    # Capture the raw CSV output as a string
    csv_content = response.text.strip()
    
    # Display the raw CSV content for debugging/inspection
    st.subheader("Raw CSV Output from AI")
    st.text_area("CSV Content", csv_content, height=200)
    
    # Use Python's csv.reader to parse the CSV string and filter rows with exactly 4 fields
    f = io.StringIO(csv_content)
    reader = csv.reader(f)
    rows = [row for row in reader if len(row) == 4]
    
    if not rows:
        st.error("No valid CSV rows found. The AI output might not be properly formatted.")
    else:
        # Create a DataFrame from the valid rows (first row is assumed as header)
        df = pd.DataFrame(rows[1:], columns=rows[0])
        
        # Save the CSV output to a file
        csv_filename = "leads.csv"
        df.to_csv(csv_filename, index=False)
        
        st.success("Lead data successfully generated!")
        st.subheader("Generated Leads CSV")
        st.dataframe(df)
        
        # Provide a download button for the CSV file
        with open(csv_filename, "rb") as file:
            st.download_button(label="Download CSV", data=file, file_name="leads.csv", mime="text/csv")

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
from extractor import extractor

def scrape_website(url, driver_path, output_file="scraped_data.json"):
    options = Options()
    options.add_argument("--headless")  # Run without opening a browser
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        html_content = driver.page_source  
        soup = BeautifulSoup(html_content, "html.parser")

        page_title = soup.title.text.strip() if soup.title else "No Title"

        headings = {f"h{i}": [h.text.strip() for h in soup.find_all(f"h{i}")] for i in range(1, 4)}
        paragraphs = [p.text.strip() for p in soup.find_all("p") if p.text.strip()]
        links = {a.text.strip(): a["href"] for a in soup.find_all("a", href=True) if a.text.strip()}

        structured_data = {
            "title": page_title,
            "headings": headings,
            "paragraphs": paragraphs[:5],  # Limit paragraphs for readability
            "links": links
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(structured_data, f, indent=4, ensure_ascii=False)

        print(f"Scraped content saved successfully in {output_file}!")
        extractor(structured_data)  # Call extractor on structured data

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        driver.quit()

# Example usage
# scrape_website("https://takeuforward.org/", "C://Users//adhik//Downloads//chromedriver-win64//chromedriver.exe")

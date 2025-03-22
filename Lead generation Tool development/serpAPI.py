import requests

api_key = "8e859272a6e77d07a69b726462aaed08b2ca80cdab44eae8b332d147028093fe"
query = "https://leetcode.com/"
url = f"https://serpapi.com/search?q={query}&api_key={api_key}"

response = requests.get(url)
data = response.json()
for result in data.get("organic_results", []):
    print(result["title"], "-", result["link"])
#print(data)
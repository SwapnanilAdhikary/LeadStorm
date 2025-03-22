from googlesearch import search

query = "https://www.sprint.dev/"
num_results=5
def search_links(query, num_results):
    results = []  # Initialize an empty list to store links
    for result in search(query, num_results=num_results):
        results.append(result)  # Append each result to the list
    return results  # Return the list of links

#print(search_links(query,num_results))        
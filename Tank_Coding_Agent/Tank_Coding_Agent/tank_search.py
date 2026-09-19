import requests

def search_web(query, num_results=5):
    url = "http://localhost:8081/search"
    params = {
        "q": query,
        "format": "json"
    }
    response = requests.get(url, params=params, timeout=10)
    data = response.json()

    results = data.get("results", [])[:num_results]

    formatted = ""
    for r in results:
        title = r.get("title", "")
        content = r.get("content", "")
        link = r.get("url", "")
        formatted += f"Title: {title}\nSnippet: {content}\nURL: {link}\n\n"

    return formatted if formatted else "No results found."


if __name__ == "__main__":
    query = input("Search query: ")
    print(search_web(query))
import requests
import textwrap

def get_wikipedia_paragraph():
    url = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        title = data["title"]
        summary = data["extract"]

        # Format the paragraph neatly for display
        formatted_text = textwrap.fill(summary, width=80)

        return title, formatted_text
    else:
        return None, "Failed to retrieve data"

# Example usage
title, paragraph = get_wikipedia_paragraph()
print(f"Title: {title}\n\n{paragraph}")
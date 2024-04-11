from bs4 import BeautifulSoup
import json

# Example HTML content

def read_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()


for i in range(15,23):
    # Parse the HTML content
    html_content = read_html_file("./static/story/story" + str(i) + ".html")

    soup = BeautifulSoup(html_content, 'html.parser')

    # Extracting data from the HTML
    data = {
        "title": soup.find(id="title").text.strip(),
        "story": soup.find('div', class_='center').p.text.strip().replace('\n', ' '),
        "name": soup.find(id="name").text.strip().split(" ")[1],  # Assuming the name always prefixed by 'BY'
        "location": soup.find(id="location").text.strip(),
        "google_map": soup.find('iframe')['src']
    }

    # Convert to JSON
    json_data = json.dumps(data, indent=4)
    print(json_data)

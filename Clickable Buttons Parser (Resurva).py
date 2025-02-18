from bs4 import BeautifulSoup

# Load HTML
file_path = 'C:\\Users\\crypt\\PycharmProjects\\pythonProject1\\Resurva HTLM code.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

# Find all clickable buttons (assuming they are 'a' tags with hrefs or 'button' tags)
clickable_elements = soup.find_all(['a', 'button'])

# Collect information about each clickable element
clickable_info = []
for element in clickable_elements:
    text = element.get_text(strip=True)
    href = element.get('href', '')
    onclick = element.get('onclick', '')
    clickable_info.append({'text': text, 'href': href, 'onclick': onclick})

# Print the clickable elements information
for info in clickable_info:
    print(info)

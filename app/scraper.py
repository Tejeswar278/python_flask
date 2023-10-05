import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

def scrape_wikipedia(url):
    # Validate and clean the URL (You may need more specific validation)
    if not url.startswith('https://en.wikipedia.org/wiki/'):
        raise ValueError('Invalid Wikipedia URL')

    # # Send an HTTP GET request
    # response = requests.get(url,timeout=10)   

    # if response.status_code != 200:
    #     raise Exception('Failed to fetch Wikipedia page')
    
    try:
        response = requests.get(url)  # Specify the timeout in seconds
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.exceptions.Timeout:
        raise TimeoutError(f"Connection to {url} timed out.")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error accessing {url}: {e}")

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    internal_urls = set()
     
    for a_tag in soup.find_all('a',href=True):
        href = a_tag['href']

        if href.startswith(('#', '/wiki/')) and not href.startswith(('/wiki/Help:', '/wiki/File:', '/wiki/Special:', '/wiki/Template:', '/wiki/Category:')):
            full_url = urljoin(url, href)
            internal_urls.add(full_url)
        
        # Stop scraping if we have reached the limit
            # if len(internal_urls) >= limit:
            #     break


    content_snippets = []
    for internal_url in internal_urls:
        # time.sleep(1)
        try:
            internal_response = requests.get(internal_url,timeout=1)
            if internal_response.status_code == 200:
                internal_soup = BeautifulSoup(internal_response.text, 'html.parser')

                # Extract the first three lines of content
                content_lines = internal_soup.text.split('\n')[:3]
                content_snippets.append({'url': internal_url, 'content': content_lines})

            internal_response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        except requests.exceptions.Timeout:
            print(f"Timeout accessing {internal_url}")
            continue  # Skip to the next URL
        except requests.exceptions.RequestException as e:
            print(f"Error accessing {internal_url}: {e}")
            continue  # Skip to the next URL
        # internal_response = requests.get(internal_url, timeout=10   )

        # if internal_response.status_code == 200:
        #     internal_soup = BeautifulSoup(internal_response.text, 'html.parser')

        #     # Extract the first three lines of content
        #     content_lines = internal_soup.text.split('\n')[:3]
        #     content_snippets.append({'url': internal_url, 'content': content_lines})
    # Extract data as needed (e.g., just the page title for this example)
    # page_title = soup.title.string

    # anchor_tags = soup.find_all('a')

    # href_values = [tag.get('href') for tag in anchor_tags if tag.get('href') is not None]

    return {'content_snippets': content_snippets}

def get_internal_urls(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        internal_urls = []

        # Extract all links (a tags) from the page
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('/wiki/'):
                # Assuming internal Wikipedia links; adjust the condition as needed
                internal_urls.append('https://en.wikipedia.org' + href)

        return internal_urls

    except requests.RequestException as e:
        return {'error': str(e)}

def scrape_url_content(url, limit=3):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')

        content_lines = []

        for paragraph in paragraphs:
            # Extract text and split into lines
            lines = paragraph.get_text().split('\n')

            # Filter out empty lines
            non_empty_lines = [line.strip() for line in lines if line.strip()]

            # Extend the content_lines list with non-empty lines
            content_lines.extend(non_empty_lines)

            # Break if we reach the desired limit
            if len(content_lines) >= limit:
                break

        return content_lines

    except requests.RequestException as e:
        return {'error': str(e)}
import xml.etree.ElementTree as ET
import requests
from datetime import datetime

def polygonParse():
    url = 'https://www.polygon.com/rss/gaming/index.xml'
    try:
        # Fetch the RSS feed
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        # Parse the XML response
        tree = ET.ElementTree(ET.fromstring(response.text))
        root = tree.getroot()

        # Define the XML namespaces to handle the Atom format
        namespaces = {
            'atom': 'http://www.w3.org/2005/Atom',
        }

        # Extract feed-level information
        title = root.find('atom:title', namespaces).text
        subtitle = root.find('atom:subtitle', namespaces).text
        link = root.find("atom:link[@rel='alternate']", namespaces).attrib['href']
        feed_id = root.find('atom:id', namespaces).text

        print(f"Feed Title: {title}")
        print(f"Feed Subtitle: {subtitle}")
        print(f"Feed Link: {link}")
        print(f"Feed ID: {feed_id}")
        print("-" * 40)
        
        articles = []
        # Iterate over entries (items in Atom feed)
        for entry in root.findall('atom:entry', namespaces):
            entry_title = entry.find('atom:title', namespaces).text
            entry_link = entry.find('atom:link[@rel="alternate"]', namespaces).attrib['href']
            entry_published = entry.find('atom:published', namespaces).text
            entry_summary = entry.find('atom:summary', namespaces).text
            entry_categories = [category.attrib['term'] for category in entry.findall('atom:category', namespaces)]

            # Convert published date to timestamp
            try:
                published_datetime = datetime.fromisoformat(entry_published.replace("Z", "+00:00"))  # Handle Z as UTC
                published_timestamp = int(published_datetime.timestamp())
            except ValueError:
                published_timestamp = None

            # Append article information to the list
            articles.append({
                'title': entry_title,
                'link': entry_link,
                'published': published_timestamp,
                'summary': entry_summary,
                'categories': entry_categories
            })

    except requests.exceptions.RequestException as e:
        print(f"Error fetching feed: {e}")
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
    
    return articles


if __name__ == "__main__":
    articles = polygonParse()
    print(articles)

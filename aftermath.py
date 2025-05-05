import re
import requests
from rss_parser import RSSParser
from datetime import datetime

def aftermathParse(parser: RSSParser):
    rss_url = 'https://aftermath.site/feed'
    response = requests.get(rss_url)
    feed = parser.parse(response.text)

    # Regex to extract the first <a href="...">link text</a>
    link_pattern = re.compile(r'<a\s+href="([^"]+)">([^<]+)</a>')

    articles = []
    for item in feed.channel.items:
        content = item.content

        # Extract categories
        categories = [cat.content for cat in content.categories] if content.categories else []

        # Extract and convert publish date to Unix timestamp
        pub_date_str = content.pub_date.content if content.pub_date else None
        pub_timestamp = None
        if pub_date_str:
            try:
                dt = datetime.strptime(pub_date_str, "%a, %d %b %Y %H:%M:%S %z")
                pub_timestamp = int(dt.timestamp())
            except ValueError as e:
                print(f"Date parsing error: {e}")

        # Extract description and parse out title and link
        description_html = content.description.content if content.description else ""
        match = link_pattern.search(description_html)
        link = match.group(1) if match else "No link found"
        title = match.group(2) if match else "No title found"

        # Get raw description text (optional)
        description_text = re.sub(r"<[^>]+>", "", description_html).strip()

        # Extract dc:creator from additional_elements
        additional = {elem.tag: elem for elem in getattr(content, "additional_elements", [])}
        creator = additional.get("dc:creator").content if "dc:creator" in additional else None

        # Append article data to the list
        articles.append({
            "title": title,
            "link": link,
            "creator": creator,
            "pub_timestamp": pub_timestamp,
            "categories": categories,
            "description": description_text
        })

        return articles


if __name__ == "__main__":
    parser = RSSParser()
    aftermathArticles = aftermathParse(parser)
    print(aftermathArticles)
#!/usr/bin/env python3

import sys
import os
import requests
from urllib.parse import urlparse
from datetime import datetime, timezone
from bs4 import BeautifulSoup
import argparse
import json

def sanitize_filename(name):
    # Replace any characters that are invalid in filenames
    valid_chars = (' ', '.', '_')

    sanitized_name = []

    for char in name:
        if char.isalnum() or char in valid_chars:
            sanitized_name.append(char)
        else:
            sanitized_name.append('_')

    return ''.join(sanitized_name)

def fetch_and_save(url, metadata_flag):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses (4XX or 5XX)

        # Parse the URL to extract the domain name
        parsed_url = urlparse(url)
        domain = parsed_url.netloc or parsed_url.path
        if not domain:
            print(f"Error: Could not extract domain from URL '{url}'")
            return

        # Sanitize filename
        safe_domain = sanitize_filename(domain)
        html_filename = f"{safe_domain}.html"
        metadata_filename = f"{safe_domain}.json"

        # Write the content to a file
        with open(html_filename, 'w', encoding=response.encoding) as f:
            f.write(response.text)

        print(f"Saved '{url}' to '{html_filename}'")

        if metadata_flag:
            # Record metadata
            last_fetch = datetime.now(timezone.utc).strftime('%a %b %d %Y %H:%M UTC')

            # Parse the HTML content to count links and images
            soup = BeautifulSoup(response.text, 'html.parser')
            num_links = len(soup.find_all('a'))
            num_images = len(soup.find_all('img'))

            # Prepare metadata dictionary
            metadata = {
                'site': domain,
                'num_links': num_links,
                'num_images': num_images,
                'last_fetch': last_fetch
            }

            # Check if metadata file exists
            if os.path.isfile(metadata_filename):
                with open(metadata_filename, 'r') as f:
                    existing_metadata = json.load(f)
                if isinstance(existing_metadata, list):
                    existing_metadata.append(metadata)
                else:
                    existing_metadata = [existing_metadata, metadata]
            else:
                existing_metadata = [metadata]

            # Save metadata to a JSON file named after the domain
            with open(metadata_filename, 'w') as f:
                json.dump(metadata, f, indent=4)

            print(f"Metadata saved to '{metadata_filename}'")

            # Print metadata
            print(f"site: {domain}")
            print(f"num_links: {num_links}")
            print(f"num_images: {num_images}")
            print(f"last_fetch: {last_fetch}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching '{url}': {e}")

def main():
    parser = argparse.ArgumentParser(description='Fetch web pages and save them to disk.')
    parser.add_argument('urls', nargs='+', help='URLs to fetch')
    parser.add_argument('--metadata', action='store_true', help='Display and save metadata about fetched pages')
    args = parser.parse_args()

    urls = args.urls
    metadata_flag = args.metadata

    for url in urls:
        # Add default scheme if missing
        if not urlparse(url).scheme:
            url = 'http://' + url
        fetch_and_save(url, metadata_flag)

if __name__ == "__main__":
    main()

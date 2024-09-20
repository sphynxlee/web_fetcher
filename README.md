## Overview

This script is a command-line utility written in Python that fetches web pages and saves them to disk for later retrieval and browsing. It accepts one or more URLs as command-line arguments, fetches each web page, and saves the content to a file named after the domain with a `.html` extension. Additionally, it can record metadata about each fetched page, including the date and time of the last fetch, the number of links on the page, and the number of images. This metadata is saved to a JSON file named after the domain.

## Features

- Fetch one or multiple web pages and save them as HTML files.
- Optionally display and save metadata about each fetched page.
- Save metadata to individual JSON files named after each URL.
- Handle errors gracefully and continue processing remaining URLs.

## Usage Instructions

### Prerequisites

- **Python 3.x**: Ensure Python 3.x is installed on your system.
- **Required Libraries**: Install the required Python libraries.

  ```bash
  pip install requests beautifulsoup4
  ```

### Running the Script

1. **Make the Script Executable** (Optional):

   ```bash
   chmod +x fetch.py
   ```

2. **Basic Usage**:

   Fetch one or more URLs and save them as HTML files.

   ```bash
   ./fetch.py https://www.example.com https://www.anotherexample.com
   ```

3. **With Metadata**:

   Use the `--metadata` flag to display and save metadata about each fetched page.

   ```bash
   ./fetch.py --metadata https://www.google.com https://autify.com/
   ```

### Example Output

```bash
Saved 'https://www.google.com' to 'www.google.com.html'
Metadata saved to 'www.google.com.json'
site: www.google.com
num_links: 19
num_images: 1
last_fetch: Fri Sep 20 2024 02:37 UTC
```

### Notes

- **Files Created**:

  - HTML content is saved to `<sanitized_domain>.html`.
  - Metadata is saved to `<sanitized_domain>.json`.


## Language and Libraries

- **Python 3.x**: Chosen for its readability, ease of use, and extensive standard library.
- **Requests**: Used for making HTTP requests due to its simplicity and reliability.
- **BeautifulSoup (bs4)**: Used for parsing HTML content to extract metadata.
- **Argparse**: Utilized for command-line argument parsing.
- **JSON**: For storing metadata in a structured and easily accessible format.

### Overall Structure

- **Main Function**: Parses command-line arguments and iterates over the provided URLs.
- **`fetch_and_save` Function**: Handles the fetching of each URL, saving the HTML content, extracting metadata, and saving the metadata to a JSON file.
- **`sanitize_filename` Function**: Ensures that filenames derived from URLs are safe for use in the file system.
- **Error Handling**: Implemented within the `fetch_and_save` function to catch exceptions without terminating the entire script.

## Code Design

- **Clear Function Names**: Functions are named descriptively (`fetch_and_save`, `sanitize_filename`).
- **Comments and Docstrings**: Inline comments explain key sections of the code.
- **Module of Concerns**: Each function has a single responsibility, making the code easier to maintain and test.
- **Exception Handling**: Uses specific exceptions (`requests.exceptions.RequestException`) for clarity.

## Error and Edge Case Handling

- **Connection Issues**: Handles exceptions raised due to network connectivity problems.
- **HTTP Errors**: Checks for unsuccessful HTTP responses and raises exceptions accordingly.
- **URL Parsing**: Uses `urlparse` to parse and validate URLs.
- **Default Scheme Addition**: Adds `http://` to URLs missing a scheme to prevent errors.
- **Filename Sanitization**: Replaces invalid filename characters to prevent file system errors.
- **Safe Writing**: Opens files using `with` statements to ensure proper closure.
- **Overwriting Files**: Overwrites existing HTML and metadata files without prompting, assuming the latest version is desired.

## Testing

### Unit Tests

- **Function Testing**: Each function can be tested individually. Test `sanitize_filename` with various test cases to ensure filenames are correctly sanitized.
- **Mock Testing**: Mock network responses to test `fetch_and_save` without making actual HTTP requests.

### Integration Tests

- **End-to-End Testing**: Run the script with a set of known URLs and verify that the HTML and metadata files are correctly created.
- **Error Conditions**: Test with invalid URLs and network failures to ensure errors are handled gracefully.

### Manual Testing

- **Valid URLs**: Test with multiple valid URLs to ensure proper functionality.
- **Invalid URLs**: Input malformed URLs to test the script's robustness.
- **No Internet Connection**: Disable the network connection to test error handling during fetch attempts.

## **Docker Support**

- **Docker Compose**: Use Docker Compose to run this script in a containerized environment. A basic `docker-compose.yml` file can be included to handle dependencies such as requests and BeautifulSoup.
- **Docker Usage**: See the `DockerUsage.md` files for more information on how to build and run the script in a Docker container.


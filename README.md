# wpdownloader
# Downloading Wordpress Content

This is a simple Python script for downloading Wordpress site content and storing it locally. The script fetches articles, pages, and media from the site, and saves them into appropriate directories.

## Usage Instructions

1. Install the required dependencies by running `pip install requests`.
2. Install tqdm `pip install tqdm`
3. Run the script as follows: `python3 wpdownloader.py <WordPress_site_URL>`.

## How the Script Works

The script operates as follows:

1. Fetches JSON-formatted data from the Wordpress site.
2. Creates necessary directories (e.g., `html`, `pictures`, `pdf`, `other`) for local storage.
3. Saves the content of Wordpress articles as HTML files in the `html` directory.
4. Saves media files (images, PDFs) into the appropriate directories.

## Notes

- Note that the script does not handle renaming in case of conflicts if files already exist with the same name.
- You can customize the script according to your needs by adding or modifying directory handling.

# Wpdownloader

This program is designed to download content from a WordPress site and save it locally.

## Usage

1. Install the required libraries with the command:

    ```bash
    pip install requests tqdm
    ```

2. Run the program with the command:

    ```bash
    python3 wpdownloader.py <WordPress_site_URL> <download_posts> <download_pages> <download_media>
    ```

    - `<WordPress_site_URL>`: The URL of the WordPress site from which content will be downloaded.
    - `<download_posts>`: 1 if you want to download posts, 0 otherwise.
    - `<download_pages>`: 1 if you want to download pages, 0 otherwise.
    - `<download_media>`: 1 if you want to download media files, 0 otherwise.

3. The program will download the requested data and save it to the local system.

## Notes

- The program saves posts as HTML files and media files in their original formats.
- Information for posts and pages is saved in the `html` directory.
- Media files are saved in directories `pictures`, `pdf`, and `other` based on their file types.

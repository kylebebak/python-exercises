"""
http://www.toptal.com/python/beginners-guide-to-concurrency-and-parallelism-in-python

Download top imgur images using concurrent execution.

IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET in ~/.virtualenvs/general/bin/activate
curl --header "Authorization: Client-ID XXX" https://api.imgur.com/3/gallery/

"""

import json
import logging
import os
import requests
from urllib.request import urlopen
from pathlib import Path

logger = logging.getLogger(__name__)

def get_links(client_id):
    """Query Imgur API to get download links as JSON."""
    headers = {'Authorization': 'Client-ID {}'.format(client_id)}
    url = 'https://api.imgur.com/3/gallery/'
    req = requests.get(url, headers=headers)
    data = json.loads(req.text)
    # extract 'link' from each 'data'->dict key-value pair in data
    return map(lambda item: item['link'], data['data'])


def download_link(directory, link):
    """Fetch the image by its URL and write it to a file."""
    logger.info('Downloading %s', link)
    download_path = directory / os.path.basename(link)
    with urlopen(link) as image, download_path.open('wb') as f:
        f.write(image.readall())


def setup_download_dir(directory):
    """Create a download destination directory if it doesn’t already exist."""
    download_dir = Path(directory)
    if not download_dir.exists():
        download_dir.mkdir()
    return download_dir


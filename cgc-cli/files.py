import requests

from helpers import get_cgc_api
from helpers import patch_cgc_api
from helpers import print_json
from helpers import download_file as download

# Files url
FILES = 'files/'

# Download file info url1
DOWNLOAD_INFO = '/download_info'


def print_file_list(token, project_id):
    """ Print all files from project

    Args:
        token: API Token for contacting CGC API
        project_id: Project ID to crawl
    """
    files = _get_project_files(token=token, project_id=project_id)
    print('CGC SevenBridges File list API')
    print('List of all files and metadata in project ' + project_id + '\n')
    print_json(files)


def print_file_details(token, file_id):
    """ Prints file details of a given file ID

    Args:
        token: API Token for contacting CGC API
        file_id: ID of the file to print details
    """
    file_details = _get_file_details(token=token, file_id=file_id)
    print('CGC Seven Bridges file info for: ' + file_id + '\n')
    print_json(file_details)


def update_file_details(token, file_id, data):
    """ Updates given file id with given data and prints modified output

    Args:
        token: API Token for contacting CGC API
        file_id: File ID to be updated
        data: Data to update file
    """
    response = patch_cgc_api(
        token=token,
        path=FILES + file_id,
        data=data
    )
    print('File with id ' + file_id + ' updated!\n')
    print_json(response.json())


def download_file(token, file_id, dest):
    """ Prints file details of a given file ID

    Args:
        token: API Token for contacting CGC API
        file_id: ID of the file to print details
    """
    print('Starting downloading file: ' + file_id + ' from CGC...')
    download(
        file_url=_get_download_url(token=token, file_id=file_id),
        dest=dest
    )
    print('File with ID: ' + file_id + ' downloaded at location: ' + dest)


def _get_file_details(token, file_id):
    """ Gets file details of a given file ID

    Args:
        token: API Token for contacting CGC API
        file_id: ID of the file that fetches details
    Returns:
        Dictionary containing file details
    """
    response = get_cgc_api(
        token=token,
        path=FILES + file_id,
    )
    return response.json()


def _get_download_url(token, file_id):
    """ Get download url for a given file

    Args:
        token: API Token for contacting CGC API
        file_id: ID of the file to download
    Returns:
        URL location of the file to be downloaded
    """
    response = get_cgc_api(
        token=token,
        path=FILES + file_id + DOWNLOAD_INFO
    )
    return response.json()['url']


def _get_folder_files(token, parent_id, folder):
    """ Recursively collects the files through folders

    Args:
        token: API Token for contacting CGC API
        parent_id: ID of the file parent
        folder: Folder to be traversed
    Returns:
        A dict containing the information of the folder data
    """
    response = get_cgc_api(
        token=token,
        path=FILES,
        params={'parent': parent_id}
    )
    folder['files'] = response.json()['items']
    for file in folder['files']:
        if file['type'] == 'folder':
            _get_folder_files(
                token=token,
                parent_id=file['id'],
                folder=file
            )


def _get_project_files(token, project_id):
    """ Collects root project files from the CGC API.

    Args:
        token: API Token for contacting CGC API
        project_id: ID of the project
    Returns:
        A dict containing the files of the project
    """
    response = get_cgc_api(
        token=token,
        path=FILES,
        params={'project': project_id}
    )
    root = response.json()['items']
    _collect_folder_files(token=token, root=root)
    return root


def _collect_folder_files(token, root):
    """ Collects files from project folders

    Args:
        token: API Token for contacting CGC API
        root: Dictionary containing root files
    """
    for file in root:
        if file['type'] == 'folder':
            _get_folder_files(
                token=token,
                parent_id=file['id'],
                folder=file
            )

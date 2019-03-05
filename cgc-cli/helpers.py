import sys
import json

import requests

# CGC SevenBridges URL
CGC_URL = 'https://cgc-api.sbgenomics.com/v2/'


def collect_update_data_args(args):
    """ Get arguments from argument list

    Function converts tag=value to list of tags.

    Args:
        args: Argument list
    Returns:
        Dictionary with arguments data 
        {
            "some_key": "some_value",
            ...
            "metadata": {
                "metadata_key": "metadata_value",
                ...
            },
            "tags": ["example_tag", "another_tag", ...]
        }
    """
    standard_args = (
        arg.split("=", 1) for arg in args
            if not arg.startswith("metadata") and not arg.startswith("tag")
    )
    data = {key: value for key, value in standard_args}

    metadata = _get_metadata(args)
    tags = _get_tags(args)
    if metadata:
        data['metadata'] = metadata
    if tags:
        data['tags'] = tags
    return data


def print_json(data):
    """ Prints dict representation as JSON

    Args:
        data: Data to print
    """
    print(json.dumps(data, indent=4, sort_keys=True))


def get_longest_string_length(dict_list, key):
    """ Returns longest string length from list of dictionaries

    Args:
        dict_list: List of dictionaries
        key: Key for value that is compared
    Returns:
        Maximum length of string in dict of given key
    """
    return max(len(s) for s in list(string[key] for string in dict_list))


def download_file(file_url, dest):
    """ Downloads file from given url to given destination

    Args:
        file_url: URL where file is located
        dest: Destination to download file
    """
    with requests.get(file_url, stream=True) as response:
        with open(dest, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)


def get_cgc_api(token, path, params={}):
    """ Creates GET request to CGC SevenBridges API

    Args:
        token: API Token for contacting CGC API
        path: URL path
        params: Query parameters
    Raises:
        HTTPError if response returns 4xx or 5xx status
    Returns:
        HTTP Response
    """
    try:
        response = requests.get(
            url=CGC_URL + path,
            params=params,
            headers={
                'X-SBG-Auth-Token': token
            }
        )
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as err:
        print('[ERROR] ' + str(err))
        print('[ERROR] ' + response.json()['message'])
        sys.exit(1)


def patch_cgc_api(token, path, data):
    """ Creates PATCH request to CGC SevenBridges API

    Args:
        token: API Token for contacting CGC API
        path: URL path
        data: JSON request body data
    Raises:
        HTTPError if response returns 4xx or 5xx status
    Returns:
        HTTP Response
    """
    try:
        response = requests.patch(
            url=CGC_URL + path,
            json=data,
            headers={
                'X-SBG-Auth-Token': token
            }
        )
        print(response.content)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as err:
        print('[ERROR] ' + str(err))
        print('[ERROR] ' + response.json()['message'])
        sys.exit(1)


def _get_metadata(args):
    """ Get metadata arguments from argument list

    Function converts metadata.key=value to appropriate dictionary format.

    Args:
        args: Argument list
    Returns:
        Dictionary containing metadata arguments with this format
        {
            "first_key": "first_value",
            "second_key": "second_value"
        }
    """
    metadata_args = [arg for arg in args if arg.startswith('metadata')]
    return {
        k: v for k,v in (arg.split('.', 1)[1].split('=', 1) for arg in metadata_args)
    }   


def _get_tags(args):
    """ Get tag arguments from argument list

    Function converts tag=value to list of tags.

    Args:
        args: Argument list
    Returns:
        List containing list of tags in the format
        ["tag_example", "another_tag_example"]
    """
    tag_args = [arg for arg in args if arg.startswith('tag')]
    return [arg.split('=',1)[1] for arg in tag_args]


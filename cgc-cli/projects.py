import requests

from helpers import get_longest_string_length, get_cgc_api

# Projects URL
PROJECTS = 'projects/'

# Table labels
NAME = 'Name'
ID = 'ID'

# Table spacing
SPACING = 5


def print_projects(token):
    """ Print list of projects from CGC API

    Args:
        token: API Token for contacting CGC API
    """
    projects = _get_projects(token=token)
    _print_project_list(
        projects=projects,
        max_name_length=get_longest_string_length(dict_list=projects, key='name'),
        max_id_length=get_longest_string_length(dict_list=projects, key='id')
    )


def _print_project(project, max_name_length, max_id_length):
    """ Print project in tabular format

    Args:
        project: Project to be printed
        max_name_length: Maximum string length of name
        max_id_length: Maximum string length of id
    """
    name_width = max_name_length - len(project['name']) + SPACING
    id_width = max_id_length - len(project['id'])
    print(
        f"{project['name']}{'':<{name_width}}| {project['id']}{'':<{id_width}}"
    )


def _print_project_list(projects, max_name_length, max_id_length):
    """ Print given list of projects in tabular format

    Args:
        projects: List of projects to be printed
        max_name_length: Maximum string length of name
        max_id_length: Maximum string length of id
    """
    name_column_width = max_name_length - len(NAME) + SPACING
    id_column_width = max_id_length - len(ID)

    print('Project list for CGC Seven Bridges:\n')
    print(f"{NAME}{'':<{name_column_width}}| {ID}{'':<{id_column_width}}")
    print(f"{'-' * (max_name_length + max_id_length + SPACING)}")
    for project in projects:
        _print_project(
            project=project,
            max_name_length=max_name_length,
            max_id_length=max_id_length
        )


def _get_projects(token):
    """ Fetch projects from the CGC

    Args:
        token: API Token for contacting CGC API
    """
    response = get_cgc_api(token=token, path=PROJECTS)
    return response.json()['items']

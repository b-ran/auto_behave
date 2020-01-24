import os
import glob
from pathlib import Path

from django.conf import settings


def paths_to_packages(paths: list) -> list:
    paths = [path for path in paths if '__init__' not in path]
    paths = [path.replace(settings.ROOT + '/', '') for path in paths]
    paths = [path.replace('.py', '') for path in paths]
    return [path.replace('/', '.') for path in paths]


def filter_underscores(items: list) -> list:
    return [item for item in items if not item.split('/')[-1].startswith('_')]


def format_rst_file(title: str, action: str, parameters: list, action_parameter='', title_style='=') -> list:
    if action_parameter != '':
        action_parameter = f'    {action_parameter}\n'
    lines = [title, title_style * len(title), '', action, action_parameter]
    for parameter in parameters:
        lines.append(f'    {parameter}')
    lines = [line + '\n' for line in lines]
    return lines


def append_to_title(title: str, append_text: str) -> str:
    if title == append_text:
        return title
    return f'{title} {append_text}'


def create_step_doc_folder(root_doc_path: str):
    Path(f'{root_doc_path}/steps').mkdir(parents=True, exist_ok=True)


def create_root_doc_index(root_path: str, root_doc_path: str):
    create_step_doc_folder(root_doc_path)
    with open(f'{root_doc_path}/steps/step-index.rst', 'w') as file:
        folder_docs_files = create_docs(root_path, root_doc_path)

        rst_lines = format_rst_file('Steps', '..  toctree::', folder_docs_files, ':maxdepth: 1')
        file.writelines(rst_lines)


def find_paths(root_path: str, sub_path: str, level=0):
    if level < 1:
        paths = glob.glob(f'{root_path}/*/', recursive=True)
        paths = [path[:-1] for path in paths]
        type = '/'
    else:
        paths = glob.glob(f'{sub_path}/**/*.py', recursive=True)
        paths = paths_to_packages(paths)
        type = '.'
    return filter_underscores(paths), type


def get_file_name(name: str, level: int) -> str:
    file_name = name.replace('_', '-')
    if level < 1:
        file_name = f'{file_name}-steps.rst'
    else:
        file_name = f'{file_name}.rst'
    return file_name


def create_docs(root_path: str, root_doc_path: str, sub_path='', level=0) -> []:
    paths, type = find_paths(root_path, sub_path, level)
    rst_files = []

    for path in paths:
        name: str = path.split(type)[-1]

        title = name.replace('_', ' ').title()
        title = append_to_title(title, 'Steps')
        file_name = get_file_name(name, level)
        rst_files.append(file_name)

        with open(f'{root_doc_path}/steps/{file_name}', 'w') as file:

            if level < 1:
                step_docs_files = create_docs(root_path, root_doc_path, path, level + 1)
                rst_lines = format_rst_file(title, '..  toctree::', step_docs_files, ':maxdepth: 1')
            else:
                rst_lines = format_rst_file(title, '..  autobehave::', [path])
            file.writelines(rst_lines)

    return rst_files

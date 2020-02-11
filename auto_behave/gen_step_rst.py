import glob
import os
from pathlib import Path


def paths_to_packages(project_path: str, paths: list) -> list:
    """
    Converts a list of paths python files to packages

    :param project_path: Absolute path to project.
    :param paths: List of paths to convert to packages
    :return: List of packages
    """
    paths = filter_underscores(paths)
    paths = [path.replace(project_path + '/', '') for path in paths]
    paths = [path.replace('.py', '') for path in paths]
    return [path.replace('/', '.') for path in paths]


def filter_underscores(items: list) -> list:
    """
    Filters all items in a list that starts with an underscore

    :param items: The items to filter.
    :return:The filtered items.
    """
    return [item for item in items if not item.split('/')[-1].startswith('_')]


def format_rst_file(title: str, action: str, parameters: list, action_parameter='', title_size='=') -> list:
    """
    Creates the text for the generated rst doc file.

    :param title: The title text for the doc.
    :param action: The action to be called i.e. '..  toctree::'.
    :param parameters: The passed in values to the action i.e. list of file names of other rst files to index.
    :param action_parameter: The action's parameter i.e. ':maxdepth: 1'.
    :param title_size: The text size of the title.
    :return: The generated text for the rst doc file, split into a list of lines.
    """
    if action_parameter != '':
        action_parameter = f'    {action_parameter}\n'
    lines = [title, title_size * len(title), '', action, action_parameter]
    for parameter in parameters:
        lines.append(f'    {parameter}')
    lines = [line + '\n' for line in lines]
    return lines


def append_to_title(title: str, append_title: str) -> str:
    """
    Append a title to a title avoiding duplication in title text, i.e. 'Steps Steps'.

    :param title: Title to append to.
    :param append_title: Other title to append to the title.
    :return: The appended title without title duplication.
    """
    if title == append_title:
        return title
    return f'{title} {append_title}'


def _find_paths(project_path: str, behave_path: str, is_step: bool):
    """
    Searches for steps folder packages and parent directories.

    :param project_path: Absolute path to project.
    :param behave_path: The root directory for behave feature files and steps.
    :param is_step: If the path is a step folder or not.
    :return: The found packages/directories and the split string.
    """
    if is_step:
        paths = glob.glob(f'{behave_path}/**/*.py', recursive=True)
        paths = paths_to_packages(project_path, paths)
        type = '.'
    else:
        paths = glob.glob(f'{behave_path}/*/', recursive=True)
        paths = [path[:-1] for path in paths]
        type = '/'

    return filter_underscores(paths), type


def _get_file_name(name: str, is_step: bool) -> str:
    """
    Gets a file name for the generated doc files.

    :param name: Name of a folder or file.
    :param is_step: If name is related to step file or not.
    :return: The file name for the doc file.
    """
    file_name = name.replace('_', '-')
    if is_step:
        file_name = f'{file_name}-steps.rst'
    else:
        file_name = f'{file_name}.rst'
    return file_name


def _create_step_doc_folder(doc_path: str):
    """
    Creates directory for the generated doc.

    :param doc_path: Output directory, location of generated rst files.
    """
    Path(f'{doc_path}/steps').mkdir(parents=True, exist_ok=True)


def generate_step_rst_files(project_path: str, behave_path: str, doc_path: str):
    """
    Generates rst files for behave step files.

    :param project_path: Absolute path to project.
    :param behave_path: Path to root behave feature files and steps.
    :param doc_path: Output directory, location of generated rst files.
    """
    behave_path = os.path.join(project_path, behave_path)
    doc_path = os.path.join(project_path, doc_path)
    _create_step_doc_folder(doc_path)
    with open(f'{doc_path}/steps/step-index.rst', 'w') as file:
        folder_docs_files = _create_docs(project_path, behave_path, doc_path)

        rst_lines = format_rst_file('Steps', '..  toctree::', folder_docs_files, ':maxdepth: 1')
        file.writelines(rst_lines)


def _create_docs(project_path: str, behave_path: str, doc_path: str, is_step=False) -> []:
    """
    Creates rst doc files for all step files

    Example uses:

    create_docs('myproject/features', 'myproject/docs'),
    creates docs for every step files indexed by a folder parent doc.

    create_docs('myproject/features/steps', 'myproject/docs', True),
    creates docs for every step without parent index doc.

    :param project_path: Absolute path to project
    :param behave_path: The root directory for behave feature files and steps.
    :param doc_path: Output directory, location of generated rst files.
    :param is_step: If path is a step folder or not.
    :return: list of names of all files created.
    """
    paths, type = _find_paths(project_path, behave_path, is_step)
    rst_files = []

    for path in paths:
        name: str = path.split(type)[-1]

        title = name.replace('_', ' ').title()
        title = append_to_title(title, 'Steps')
        file_name = _get_file_name(name, is_step)
        rst_files.append(file_name)

        with open(f'{doc_path}/steps/{file_name}', 'w') as file:

            if is_step:
                rst_lines = format_rst_file(title, '..  autobehave::', [path])
            else:
                step_docs_files = _create_docs(project_path, path, doc_path, True)
                rst_lines = format_rst_file(title, '..  toctree::', step_docs_files, ':maxdepth: 1')

            file.writelines(rst_lines)

    return rst_files

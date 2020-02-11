import importlib
import os
import re
import types
from types import FunctionType

from docutils import nodes
from docutils.nodes import document
from sphinx.application import Sphinx

from jinja2 import Template

from auto_behave.node import AutoBehave
import inspect


def process_auto_behave_nodes(app: Sphinx, doc_tree: document, from_doc_name: str):
    root = os.path.dirname(os.path.abspath(__file__))
    template_string = open(os.path.join(root, 'templates/behave.html'), 'r').read()

    template = Template(template_string)

    for node in doc_tree.traverse(AutoBehave):
        output = process_modules(node.rawsource, template)
        node.replace_self(nodes.raw('', output, format='html'))


def process_modules(modules, template: Template):
    """
    Process a list of modules, importing the module's step functions details
    and templating those details into html.

    :param modules: List of modules to import step functions from
    :param template: jinja2 template, to render to imported details
    :return: Render html string from jinja2 template
    """
    for module_name in modules:
        module = importlib.import_module(module_name)

        functions_tuples = [fn for fn in inspect.getmembers(module) if isinstance(fn[1], types.FunctionType)]
        functions = process_functions(functions_tuples)
        return template.render(functions=functions)


def process_functions(functions_tuples) -> list:
    """
    Gets details of each function for a jinja2 template

    :param functions_tuples: functions_tuples: List of functions from inspect.getmembers
    :return:  functions_tuples: List of dicts each with details about the function: title, decorators, docstring
    """
    functions = []
    for function_tuple in functions_tuples:

        function: FunctionType = function_tuple[1]
        source_lines = inspect.getsourcelines(function)[0]

        if not has_decorator(source_lines):
            continue

        docstring = inspect.getdoc(function)

        if docstring is None:
            functions.append({
                "title": function_tuple[0],
                "decorators": format_decorators(source_lines),
                "table": [],
                "docstring": ''
            })
            continue

        docstring_lines = docstring.split('\n')
        table_lines = get_table_lines(docstring_lines)
        docstring_filtered = filter_table(docstring_lines)

        functions.append({
            "title": function_tuple[0],
            "decorators": format_decorators(source_lines),
            "table": format_table(table_lines),
            "docstring": docstring_filtered
        })
    return functions


def filter_table(docstring_lines):
    for i, line in enumerate(docstring_lines):
        if re.match(r'(\+.*|\|.*)', line):
            return ' '.join(docstring_lines[0:i])
    return ' '.join(docstring_lines)


def get_table_lines(docstring_lines: list) -> list:
    docstring_lines = [line.strip() for line in docstring_lines]
    table_lines = [line for line in docstring_lines if re.match(r'\|.*', line)]
    return table_lines


def format_table(table_lines: list):
    """
    Find and format table with the docstring

    :param table_lines: Docstring containing a table within
    """
    tidy_table_lines = [line[1:-1].split('|') for line in table_lines]
    table = []
    for row in tidy_table_lines:
        cols = []
        for col in row:
            cols.append(col.strip())
        table.append(cols)
    return table


def format_decorators(source_lines: list) -> list:
    """
    Tidies up decorators, removing unneeded syntax for docs
    :param source_lines: Source code lines of a function
    :return: List of tidy decorators for doc
    """
    raw_step_decorators = [line for line in source_lines if re.match(r'@[a-z]+\(', line)]
    step_decorators = []
    for step_decorator in raw_step_decorators:
        step_decorator = step_decorator.replace("('", '  ')
        step_decorator = step_decorator.replace("')", '  ')
        step_decorator = step_decorator.replace('\\', '')
        step_decorators.append(step_decorator)
    return step_decorators


def has_decorator(source_lines: list) -> bool:
    """
    Checks if the source code for a function has a decorator or not
    :param source_lines: Source code lines of a function
    :return: True if there is a decorator else False
    """
    return '@' in source_lines[0]

import importlib
import os
import re
import types
from types import FunctionType

from docutils import nodes
from docutils.nodes import document
from docutils.statemachine import StringList
from sphinx.application import Sphinx

from jinja2 import Template


import inspect

from node import AutoBehave


def process_auto_behave_nodes(app: Sphinx, doc_tree: document, from_doc_name: str):
    root = os.path.dirname(os.path.abspath(__file__))
    template_string = open(os.path.join(root, 'templates/behave.html'), 'r').read()

    template = Template(template_string)

    for node in doc_tree.traverse(AutoBehave):
        output = process_raw_source(node.rawsource, template)
        node.replace_self(nodes.raw('', output, format='html'))


def process_raw_source(raw_source: StringList, template):
    for module_name in raw_source:
        module = importlib.import_module(module_name)

        functions_tuples = [fn for fn in inspect.getmembers(module) if isinstance(fn[1], types.FunctionType)]
        functions = process_functions(functions_tuples)

        return template.render(functions=functions)


def process_functions(functions_tuples) -> list:
    functions = []
    for function_tuple in functions_tuples:

        function: FunctionType = function_tuple[1]
        source_lines = inspect.getsourcelines(function)[0]

        if not has_decorator(source_lines):
            continue

        functions.append({
            "title": function_tuple[0],
            "decorators": format_decorator(source_lines),
            "docstring": inspect.getdoc(function)
        })
    return functions


def format_decorator(source_lines: list) -> list:
    raw_step_decorators = [line for line in source_lines if re.match(r'@[a-z]+\(', line)]
    step_decorators = []
    for step_decorator in raw_step_decorators:
        step_decorator = step_decorator.replace("('", '  ')
        step_decorator = step_decorator.replace("')", '  ')
        step_decorator = step_decorator.replace('\\', '')
        step_decorators.append(step_decorator)
    return step_decorators


def has_decorator(source_lines: list) -> bool:
    return '@' in source_lines[0]

from auto_behave.directive import AutoBehaveDirective
from auto_behave.handlers import process_auto_behave_nodes
from auto_behave.node import AutoBehave, visit_auto_behave_node, depart_auto_behave_node


def setup(app):
    app.add_node(
        AutoBehave,
        html=(visit_auto_behave_node, depart_auto_behave_node),
    )
    app.add_directive('autobehave', AutoBehaveDirective)
    app.connect('doctree-resolved', process_auto_behave_nodes)

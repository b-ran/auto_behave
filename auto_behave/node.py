from docutils.nodes import Element, Admonition


class AutoBehave(Admonition, Element):
    pass


def visit_auto_behave_node(self, node):
    self.visit_admonition(node)


def depart_auto_behave_node(self, node):
    self.depart_admonition(node)



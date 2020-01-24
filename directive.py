from docutils.parsers.rst import Directive

from auto_behave.node import AutoBehave


class AutoBehaveDirective(Directive):

    has_content = True

    def run(self):
        auto_behave_node = AutoBehave(self.content)
        self.state.nested_parse(self.content, self.content_offset, auto_behave_node)
        return [auto_behave_node]

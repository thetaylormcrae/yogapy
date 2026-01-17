from . import _native

class LayoutNode:
    def __init__(self, width=None, height=None):
        self._node = _native.Node()
        if width is not None: self._node.set_width(width)
        if height is not None: self._node.set_height(height)

    def add(self, *children):
        for i, child in enumerate(children):
            self._node.insert_child(child._node, i)
        return self

    def compute(self, width=1024, height=758):
        self._node.calculate_layout(width, height)
        return self._node.get_layout()

import _native # The compiled binary

class LayoutNode:
    def __init__(self, width=None, height=None):
        # Create the underlying C++ proxy node
        self._node = _native.Node()
        
        # Handle initial styling
        if width is not None: 
            self._node.set_width(float(width))
        if height is not None: 
            self._node.set_height(float(height))
        
        # Keep references to children to prevent Python's GC 
        # from deleting them while the C++ tree still needs them
        self._children = []

    def add(self, *children):
        for child in children:
            index = len(self._children)
            # GOTCHA: We must pass the underlying C++ object (child._node)
            self._node.insert_child(child._node, index)
            self._children.append(child)
        return self

    def compute(self, width=1024, height=758):
        # width/height must be floats for the C++ bridge
        self._node.calculate_layout(float(width), float(height))
        return self._node.get_layout()

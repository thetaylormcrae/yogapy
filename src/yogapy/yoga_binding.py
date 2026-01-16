from __future__ import annotations
import os, sys
from cffi import FFI

ffi = FFI()

ffi.cdef("""
    typedef struct YGNode* YGNodeRef;

    typedef enum { YGDirectionInherit, YGDirectionLTR, YGDirectionRTL } YGDirection;
    typedef enum { YGFlexDirectionColumn, YGFlexDirectionColumnReverse,
                   YGFlexDirectionRow, YGFlexDirectionRowReverse } YGFlexDirection;
    typedef enum { YGAlignAuto, YGAlignFlexStart, YGAlignCenter,
                   YGAlignFlexEnd, YGAlignStretch } YGAlign;
    typedef enum { YGEdgeLeft, YGEdgeTop, YGEdgeRight, YGEdgeBottom } YGEdge;

    YGNodeRef YGNodeNew(void);
    void YGNodeFree(YGNodeRef);

    void YGNodeInsertChild(YGNodeRef, YGNodeRef, unsigned int);

    void YGNodeStyleSetWidth(YGNodeRef, float);
    void YGNodeStyleSetHeight(YGNodeRef, float);
    void YGNodeStyleSetFlex(YGNodeRef, float);
    void YGNodeStyleSetFlexDirection(YGNodeRef, YGFlexDirection);
    void YGNodeStyleSetAlignItems(YGNodeRef, YGAlign);
    void YGNodeStyleSetPadding(YGNodeRef, YGEdge, float);
    void YGNodeStyleSetMargin(YGNodeRef, YGEdge, float);

    void YGNodeCalculateLayout(YGNodeRef, float, float, YGDirection);

    float YGNodeLayoutGetLeft(YGNodeRef);
    float YGNodeLayoutGetTop(YGNodeRef);
    float YGNodeLayoutGetWidth(YGNodeRef);
    float YGNodeLayoutGetHeight(YGNodeRef);
""")

def _load_lib():
    env = os.getenv("YOGAPY_LIB")
    if env:
        return ffi.dlopen(env)

    names = {
        "win32": ["yoga.dll"],
        "darwin": ["libyoga.dylib"],
        "linux": ["libyoga.so"],
    }

    for name in names.get(sys.platform, []):
        try:
            return ffi.dlopen(os.path.join(os.path.dirname(__file__), name))
        except OSError:
            pass

    raise RuntimeError("Yoga library not found")

lib = _load_lib()

YG_DIRECTION_LTR = 1
YG_FLEX_DIRECTION_ROW = 2
YG_FLEX_DIRECTION_COLUMN = 0
YG_ALIGN_FLEX_START = 1
YG_ALIGN_CENTER = 2
YG_ALIGN_FLEX_END = 3
YG_EDGE_LEFT = 0
YG_EDGE_TOP = 1
YG_EDGE_RIGHT = 2
YG_EDGE_BOTTOM = 3

class YogaNode:
    __slots__ = ("_ptr", "_children")

    def __init__(self):
        self._ptr = lib.YGNodeNew()
        self._children = []

    def __del__(self):
        if getattr(self, "_ptr", None):
            lib.YGNodeFree(self._ptr)
            self._ptr = ffi.NULL

    def set_width(self, v): lib.YGNodeStyleSetWidth(self._ptr, float(v))
    def set_height(self, v): lib.YGNodeStyleSetHeight(self._ptr, float(v))
    def set_flex(self, v): lib.YGNodeStyleSetFlex(self._ptr, float(v))
    def set_flex_direction(self, v): lib.YGNodeStyleSetFlexDirection(self._ptr, v)
    def set_align_items(self, v): lib.YGNodeStyleSetAlignItems(self._ptr, v)
    def set_padding(self, e, v): lib.YGNodeStyleSetPadding(self._ptr, e, float(v))
    def set_margin(self, e, v): lib.YGNodeStyleSetMargin(self._ptr, e, float(v))

    def insert_child(self, child, index):
        self._children.insert(index, child)
        lib.YGNodeInsertChild(self._ptr, child._ptr, index)

    def calculate_layout(self, w, h, direction=YG_DIRECTION_LTR):
        lib.YGNodeCalculateLayout(self._ptr, float(w), float(h), direction)

    @property
    def layout_left(self): return float(lib.YGNodeLayoutGetLeft(self._ptr))
    @property
    def layout_top(self): return float(lib.YGNodeLayoutGetTop(self._ptr))
    @property
    def layout_width(self): return float(lib.YGNodeLayoutGetWidth(self._ptr))
    @property
    def layout_height(self): return float(lib.YGNodeLayoutGetHeight(self._ptr))

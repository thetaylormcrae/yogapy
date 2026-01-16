import sys
import os
from importlib.resources import files
from cffi import FFI

ffi = FFI()

def _platform_dir():
    if sys.platform.startswith("linux"):
        return "linux"
    if sys.platform == "darwin":
        return "macos"
    if sys.platform.startswith("win"):
        return "windows"
    raise RuntimeError(f"Unsupported platform: {sys.platform}")

def _lib_name():
    if sys.platform.startswith("linux"):
        return "libyoga.so"
    if sys.platform == "darwin":
        return "libyoga.dylib"
    if sys.platform.startswith("win"):
        return "yoga.dll"

def _load_native_lib():
    # Allow override via environment variable
    override = os.getenv("YOGAPY_YOGA_LIB")
    if override:
        return ffi.dlopen(override)

    lib_path = files("yogapy._native").joinpath(_platform_dir(), _lib_name())
    return ffi.dlopen(str(lib_path))

lib = _load_native_lib()

# CFFI declarations (same as your current file)
ffi.cdef("""
    typedef struct YGNode* YGNodeRef;
    YGNodeRef YGNodeNew(void);
    void YGNodeFree(YGNodeRef node);
    void YGNodeInsertChild(YGNodeRef node, YGNodeRef child, unsigned int index);
    void YGNodeStyleSetWidth(YGNodeRef node, float width);
    void YGNodeStyleSetHeight(YGNodeRef node, float height);
    void YGNodeStyleSetFlex(YGNodeRef node, float flex);
    void YGNodeStyleSetFlexDirection(YGNodeRef node, int direction);
    void YGNodeStyleSetAlignItems(YGNodeRef node, int align);
    void YGNodeStyleSetPadding(YGNodeRef node, int edge, float padding);
    void YGNodeStyleSetMargin(YGNodeRef node, int edge, float margin);
    void YGNodeCalculateLayout(YGNodeRef node, float availableWidth, float availableHeight, int ownerDirection);
    float YGNodeLayoutGetLeft(YGNodeRef node);
    float YGNodeLayoutGetTop(YGNodeRef node);
    float YGNodeLayoutGetWidth(YGNodeRef node);
    float YGNodeLayoutGetHeight(YGNodeRef node);
""")

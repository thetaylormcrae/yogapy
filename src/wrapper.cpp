#include <pybind11/pybind11.h>
#include <yoga/Yoga.h>

namespace py = pybind11;
using namespace pybind11::literals;

// The "Magic Bullet": Define an empty struct. 
// This prevents every single "incomplete type" error on macOS and Windows.
struct PyNode {}; 

PYBIND11_MODULE(_native, m) {
    py::class_<PyNode>(m, "Node")
        .def(py::init([]() { 
            return reinterpret_cast<PyNode*>(YGNodeNew()); 
        }))
        .def("__del__", [](PyNode* n) { 
            YGNodeFree(reinterpret_cast<YGNode*>(n)); 
        })
        .def("calculate_layout", [](PyNode* n, float w, float h) {
            YGNodeCalculateLayout(reinterpret_cast<YGNode*>(n), w, h, YGDirectionLTR);
        })
        .def("set_width", [](PyNode* n, float w) { 
            YGNodeStyleSetWidth(reinterpret_cast<YGNode*>(n), w); 
        })
        .def("set_height", [](PyNode* n, float h) { 
            YGNodeStyleSetHeight(reinterpret_cast<YGNode*>(n), h); 
        })
        .def("insert_child", [](PyNode* n, PyNode* c, int i) {
            YGNodeInsertChild(reinterpret_cast<YGNode*>(n), reinterpret_cast<YGNode*>(c), i);
        })
        .def("get_layout", [](PyNode* n) {
            auto yn = reinterpret_cast<YGNode*>(n);
            return py::dict(
                "left"_a = YGNodeLayoutGetLeft(yn),
                "top"_a = YGNodeLayoutGetTop(yn),
                "width"_a = YGNodeLayoutGetWidth(yn),
                "height"_a = YGNodeLayoutGetHeight(yn)
            );
        });
}

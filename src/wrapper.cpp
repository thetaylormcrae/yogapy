#include <pybind11/pybind11.h>
#include <yoga/Yoga.h>

namespace py = pybind11;
using namespace pybind11::literals;

// 1. Define a dummy struct to act as our Python handle.
// This solves the "incomplete type" error permanently.
struct Node {};

PYBIND11_MODULE(_native, m) {
    m.doc() = "Native Yoga Layout Engine";

    // 2. Bind the dummy struct. We use 'YGNode*' as the underlying pointer.
    py::class_<Node>(m, "Node")
        .def(py::init([]() { 
            return reinterpret_cast<Node*>(YGNodeNew()); 
        }))
        .def("__del__", [](Node* n) { 
            YGNodeFree(reinterpret_cast<YGNode*>(n)); 
        })
        
        .def("calculate_layout", [](Node* n, float width, float height) {
            YGNodeCalculateLayout(reinterpret_cast<YGNode*>(n), width, height, YGDirectionLTR);
        })

        .def("insert_child", [](Node* n, Node* child, unsigned int index) {
            YGNodeInsertChild(reinterpret_cast<YGNode*>(n), reinterpret_cast<YGNode*>(child), index);
        })

        .def("set_width", [](Node* n, float w) { YGNodeStyleSetWidth(reinterpret_cast<YGNode*>(n), w); })
        .def("set_height", [](Node* n, float h) { YGNodeStyleSetHeight(reinterpret_cast<YGNode*>(n), h); })
        
        .def("get_layout", [](Node* n) {
            auto yn = reinterpret_cast<YGNode*>(n);
            return py::dict(
                "left"_a   = YGNodeLayoutGetLeft(yn),
                "top"_a    = YGNodeLayoutGetTop(yn),
                "width"_a  = YGNodeLayoutGetWidth(yn),
                "height"_a = YGNodeLayoutGetHeight(yn)
            );
        });

    m.attr("DIRECTION_COLUMN") = 1;
    m.attr("DIRECTION_ROW") = 2;
}

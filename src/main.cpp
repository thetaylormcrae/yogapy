#include <pybind11/pybind11.h>
#include "yoga/Yoga.h"

namespace py = pybind11;

PYBIND11_MODULE(_yogapy, m) {
    py::class_<YGNode>(m, "Node")
        .def(py::init([]() { return YGNodeNew(); }))
        .def("set_width", [](YGNode* n, float w) { YGNodeStyleSetWidth(n, w); })
        .def("set_width_percent", [](YGNode* n, float w) { YGNodeStyleSetWidthPercent(n, w); })
        .def("set_height", [](YGNode* n, float h) { YGNodeStyleSetHeight(n, h); })
        .def("set_height_percent", [](YGNode* n, float h) { YGNodeStyleSetHeightPercent(n, h); })
        .def("calculate_layout", [](YGNode* n, float w, float h) {
            YGNodeCalculateLayout(n, w, h, YGDirectionLTR);
        })
        .def_property_readonly("width", [](YGNode* n) { return YGNodeLayoutGetWidth(n); })
        .def_property_readonly("height", [](YGNode* n) { return YGNodeLayoutGetHeight(n); })
        .def_property_readonly("left", [](YGNode* n) { return YGNodeLayoutGetLeft(n); })
        .def_property_readonly("top", [](YGNode* n) { return YGNodeLayoutGetTop(n); })
        .def("insert_child", [](YGNode* n, YGNode* child, int index) {
            YGNodeInsertChild(n, child, index);
        })
        .def("__del__", [](YGNode* n) { YGNodeFree(n); });
}
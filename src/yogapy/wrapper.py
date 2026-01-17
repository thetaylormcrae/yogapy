#include <pybind11/pybind11.h>
#include <yoga/Yoga.h>

namespace py = pybind11;
using namespace pybind11::literals;

PYBIND11_MODULE(_native, m) {
    py::class_<YGNode>(m, "Node")
        .def(py::init([]() { return YGNodeNew(); }))
        .def("__del__", [](YGNode* node) { YGNodeFree(node); })
        .def("insert_child", &YGNodeInsertChild)
        .def("calculate_layout", [](YGNode* node, float width, float height) {
            YGNodeCalculateLayout(node, width, height, YGDirectionLTR);
        })
        .def("set_width", &YGNodeStyleSetWidth)
        .def("set_height", &YGNodeStyleSetHeight)
        .def("get_layout", [](YGNode* node) {
            return py::dict(
                "left"_a=YGNodeLayoutGetLeft(node),
                "top"_a=YGNodeLayoutGetTop(node),
                "width"_a=YGNodeLayoutGetWidth(node),
                "height"_a=YGNodeLayoutGetHeight(node)
            );
        });
}

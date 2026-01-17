#include <pybind11/pybind11.h>
#include <yoga/Yoga.h>

namespace py = pybind11;
using namespace pybind11::literals;

PYBIND11_MODULE(_native, m) {
    // We bind to the struct but tell pybind11 we are handling it via pointers
    py::class_<YGNode>(m, "Node")
        .def(py::init([]() { return YGNodeNew(); }))
        .def("__del__", [](YGNode* node) { YGNodeFree(node); })
        
        .def("insert_child", [](YGNode* node, YGNode* child, unsigned int index) {
            YGNodeInsertChild(node, child, index);
        })
        
        .def("calculate_layout", [](YGNode* node, float width, float height) {
            YGNodeCalculateLayout(node, width, height, YGDirectionLTR);
        })

        .def("set_width", [](YGNode* node, float width) { YGNodeStyleSetWidth(node, width); })
        .def("set_height", [](YGNode* node, float height) { YGNodeStyleSetHeight(node, height); })

        .def("get_layout", [](YGNode* node) {
            return py::dict(
                "left"_a = YGNodeLayoutGetLeft(node),
                "top"_a = YGNodeLayoutGetTop(node),
                "width"_a = YGNodeLayoutGetWidth(node),
                "height"_a = YGNodeLayoutGetHeight(node)
            );
        });
}

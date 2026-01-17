#include <pybind11/pybind11.h>
#include <yoga/Yoga.h>

namespace py = pybind11;
using namespace pybind11::literals;

// We use the C-API pointer types (YGNodeRef) for the bindings
// to ensure compatibility across all platforms and compilers.

PYBIND11_MODULE(_native, m) {
    m.doc() = "Native Yoga Layout Engine for E-Ink";

    // Defining the class as opaque via custom_type_setup prevents 
    // the "incomplete type" errors on macOS and Windows.
    py::class_<YGNode>(m, "Node", py::custom_type_setup([](py::detail::type_record& rec) {
        rec.type_size = 0; 
    }))
    .def(py::init([]() { 
        return YGNodeNew(); 
    }))
    .def("__del__", [](YGNode* node) { 
        YGNodeFree(node); 
    })
    
    // Layout Calculation
    .def("calculate_layout", [](YGNode* node, float width, float height) {
        YGNodeCalculateLayout(node, width, height, YGDirectionLTR);
    })

    // Tree Management
    .def("insert_child", [](YGNode* node, YGNode* child, unsigned int index) {
        YGNodeInsertChild(node, child, index);
    })

    // Style Setters
    .def("set_width", [](YGNode* node, float width) { YGNodeStyleSetWidth(node, width); })
    .def("set_height", [](YGNode* node, float height) { YGNodeStyleSetHeight(node, height); })
    .def("set_flex_direction", [](YGNode* node, int direction) {
        YGNodeStyleSetFlexDirection(node, static_cast<YGFlexDirection>(direction));
    })
    .def("set_padding", [](YGNode* node, int edge, float padding) {
        YGNodeStyleSetPadding(node, static_cast<YGEdge>(edge), padding);
    })
    .def("set_margin", [](YGNode* node, int edge, float margin) {
        YGNodeStyleSetMargin(node, static_cast<YGEdge>(edge), margin);
    })

    // Result Getters
    .def("get_layout", [](YGNode* node) {
        return py::dict(
            "left"_a   = YGNodeLayoutGetLeft(node),
            "top"_a    = YGNodeLayoutGetTop(node),
            "width"_a  = YGNodeLayoutGetWidth(node),
            "height"_a = YGNodeLayoutGetHeight(node)
        );
    });

    // Optional: Export Yoga Enums for Flex Direction
    m.attr("DIRECTION_COLUMN") = 1;
    m.attr("DIRECTION_ROW") = 2;
    m.attr("EDGE_ALL") = 8;
}

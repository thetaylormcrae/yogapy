from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from yogapy.yoga_binding import (
    YogaNode,
    YG_FLEX_DIRECTION_ROW,
    YG_FLEX_DIRECTION_COLUMN,
    YG_ALIGN_FLEX_START,
    YG_ALIGN_CENTER,
    YG_ALIGN_FLEX_END,
    YG_EDGE_TOP,
    YG_EDGE_RIGHT,
    YG_EDGE_BOTTOM,
    YG_EDGE_LEFT,
)

@dataclass
class Node:
    type: str = "leaf"
    style: Dict = field(default_factory=dict)
    content: Optional[Dict] = None
    children: List["Node"] = field(default_factory=list)

    x: float = 0
    y: float = 0
    width: float = 0
    height: float = 0

    def add(self, child): self.children.append(child)

def _apply_style(y, s):
    y.set_flex_direction(YG_FLEX_DIRECTION_ROW if s.get("direction") == "row" else YG_FLEX_DIRECTION_COLUMN)
    if "flex" in s: y.set_flex(s["flex"])
    if "width" in s: y.set_width(s["width"])
    if "height" in s: y.set_height(s["height"])

    if "align" in s:
        y.set_align_items({
            "start": YG_ALIGN_FLEX_START,
            "center": YG_ALIGN_CENTER,
            "end": YG_ALIGN_FLEX_END,
        }.get(s["align"], YG_ALIGN_FLEX_START))

    for edge, key in [
        (YG_EDGE_TOP, "padding_top"),
        (YG_EDGE_RIGHT, "padding_right"),
        (YG_EDGE_BOTTOM, "padding_bottom"),
        (YG_EDGE_LEFT, "padding_left"),
    ]:
        if key in s: y.set_padding(edge, s[key])

    for edge, key in [
        (YG_EDGE_TOP, "margin_top"),
        (YG_EDGE_RIGHT, "margin_right"),
        (YG_EDGE_BOTTOM, "margin_bottom"),
        (YG_EDGE_LEFT, "margin_left"),
    ]:
        if key in s: y.set_margin(edge, s[key])

def _build(node):
    y = YogaNode()
    _apply_style(y, node.style)
    for i, c in enumerate(node.children):
        y_child = _build(c)
        y.insert_child(y_child, i)
    return y

def _assign(node, y):
    node.x = y.layout_left
    node.y = y.layout_top
    node.width = y.layout_width
    node.height = y.layout_height
    for c, yc in zip(node.children, y._children):
        _assign(c, yc)

def compute_layout(root, width, height):
    y = _build(root)
    y.calculate_layout(width, height)
    _assign(root, y)
    return root

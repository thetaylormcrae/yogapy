# yogapy

**yogapy** is a cross‑platform Python binding for Facebook’s Yoga layout engine,
implemented using CFFI and bundled with prebuilt native libraries for:

- Windows (x64)
- Linux (x64, ARMv6/7/8)
- macOS (x64 + ARM64)

It provides:

- A minimal, stable CFFI wrapper around Yoga’s C API
- A Pythonic layout wrapper (`yogapy.layout`)
- Wheels that include the Yoga shared library
- Zero build requirements for end users

This package is designed to be a reliable, production‑ready layout engine for
Python UI frameworks, embedded devices, and rendering pipelines.

## Installation

```bash
pip install yogapy
```

## Example

```python
from yogapy.layout import Node, compute_layout

root = Node(style={"direction": "row"})
root.add(Node(style={"width": 100, "height": 50}))
root.add(Node(style={"flex": 1}))

compute_layout(root, 800, 480)

for child in root.children:
    print(child.x, child.y, child.width, child.height)
```

## License

MIT

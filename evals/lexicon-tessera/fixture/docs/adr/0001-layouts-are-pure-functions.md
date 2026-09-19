# 0001. Layouts are pure functions

## Status

Accepted, April 2023.

## Context

The first layouts kept their own record of which window sat where and how big the user had made it. Every window that closed, crashed or was sent to another workspace left that record out of step with reality, and most of the bugs of the first two months were of this kind: gaps where a window used to be, two windows given the same rectangle, a main tile that shrank a little more each time a dialog opened.

## Decision

A layout is a pure function of the window count, the work area, the split ratio and the gutter. It returns one rectangle per tiled window, in window order, and holds no state between calls. The `LayoutEngine` asks the layout for rectangles and hands them to the `WindowMover`, which repositions all the windows in a single batch.

The order of the windows belongs to the workspace, not to the layout.

## Consequences

- A layout can be understood, and checked, by reading one method.
- Because a layout is a pure function of the window count, the work area, the split ratio and the gutter, it cannot remember sizes, so dragging the edge of a tiled window has no lasting effect: the next arrangement puts the window back. Someone who wants one window at an odd size should float it.
- The only per-workspace adjustment a layout responds to is the split ratio. Anything richer, such as per-row heights in the stack, would need this decision revisited.
- Adding a layout means adding one class and one line where layouts are registered.

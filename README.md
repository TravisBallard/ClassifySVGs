# ClassifySVGs
Python script to traverse a folder and add CSS class names for the following elements:

- g
- path
- rect
- circle
- ellipse
- line
- polyline
- polygon

Note that multi-line SVGs with multiple elements on a single line will be classified incorrectly as the line index is used for the increment value.
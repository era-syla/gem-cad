import cadquery as cq

# Parametric dimensions
height = 100.0       # Length of the loft
octagon_radius = 30.0 # Circumradius of the octagon base
line_length = 50.0    # Length of the top edge (the "wedge" end)
line_width = 1.0     # Small width to approximate a line for lofting, or 0 for a true edge

# 1. Create the bottom octagon profile
# We sketch on the XY plane.
# cq.Workplane("XY").polygon(nSides, diameter) creates a polygon.
# diameter in CadQuery is usually the circumscribed diameter.
base_sketch = (
    cq.Workplane("XY")
    .polygon(8, octagon_radius * 2)
)

# 2. Create the top profile
# The top profile looks like a line or a very thin rectangle (a wedge tip).
# To make a robust loft in CAD, it's often better to use a very thin rectangle 
# rather than a 1D line, although CadQuery can sometimes handle points/lines.
# Looking at the geometry, the top edge is horizontal (parallel to X axis probably, 
# or Y depending on orientation). Let's align it parallel to the X-axis to match 
# the orientation relative to the octagon "flats".
top_sketch = (
    cq.Workplane("XY")
    .workplane(offset=height)
    .rect(line_length, 0.1) # Using a tiny Y-dimension to simulate a line edge
)

# 3. Perform the Loft operation
# We create a new workplane, add the bottom wire, add the top wire, and loft.
result = (
    cq.Workplane("XY")
    .polygon(8, octagon_radius * 2) # Add bottom wire
    .workplane(offset=height)       # Move to top plane
    .rect(line_length, 0.1)         # Add top wire (approximating the edge)
    .loft(combine=True)
)

# Note: If a true sharp edge is required without the tiny 0.1 thickness, 
# lofting to a line or vertices can be tricky in OpenCascade kernels via simple APIs.
# However, for visual similarity to the provided image, the tiny rectangle approximation 
# creates the flat "wedge" faces correctly.

# Alternative approach (ruled surface):
# While loft works generally, sometimes explicit ruled surfaces are preferred, 
# but loft is the most direct translation of "shape A transitions to shape B".

# Final export step is implicit in the 'result' variable requirement.
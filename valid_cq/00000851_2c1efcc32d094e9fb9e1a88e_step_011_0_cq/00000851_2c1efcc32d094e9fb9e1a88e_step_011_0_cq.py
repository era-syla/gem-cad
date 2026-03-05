import cadquery as cq

# Define parametric dimensions
# Based on visual estimation, the object is a long, thin rectangular bar.
# Let's assume some reasonable proportions.
length = 200.0  # Length of the bar
width = 5.0     # Width of the bar (thickness)
height = 10.0   # Height of the bar

# Create the solid geometry
# We create a simple box centered at the origin or starting from a corner.
# Centered is often better for symmetry.
result = cq.Workplane("XY").box(length, width, height)

# Alternatively, if "width" and "height" correspond to the cross-section
# and length corresponds to the extrusion:
# result = cq.Workplane("XY").rect(length, width).extrude(height)
# But box() is the most direct way for a simple prism.
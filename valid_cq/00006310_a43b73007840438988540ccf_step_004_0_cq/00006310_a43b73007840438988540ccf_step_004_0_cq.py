import cadquery as cq

# Parametric dimensions
length = 100.0  # Total length of the plate
width = 40.0    # Width of the plate
thickness = 5.0 # Thickness of the plate
fillet_radius = 5.0 # Radius for rounding the top edges

# Create the base rectangular plate
# We start with a box
base = cq.Workplane("XY").box(length, width, thickness)

# Apply fillets to the four vertical edges to create rounded corners
# Select vertical edges using the 'Z' selector
result = base.edges("|Z").fillet(fillet_radius)

# It's also possible the user wants the long top edges filleted, 
# or just rounded corners. The image shows a flat plate with rounded corners.
# Let's refine the interpretation. The image shows a long rectangular strip.
# The short ends are rounded. Wait, looking closely at the image:
# It looks like a standard flat bar with rounded corners.
# Or possibly the entire short edge is a semicircle? 
# No, the corners have a distinct radius, but the end is straight in the middle.
# Let's stick with the rounded rectangle interpretation.

# Re-evaluating based on typical simple parts:
# It looks like a rectangular plate with small fillets on the four corners in the XY plane.
# The top and bottom faces are flat. The sides are vertical.

# Let's adjust the parameters to match the aspect ratio better.
# Length looks about 3x the width.
# Thickness is small.

length = 150.0
width = 50.0
thickness = 5.0
corner_radius = 5.0  # Radius of the vertical corners

# Generate the geometry
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .edges("|Z")  # Select vertical edges
    .fillet(corner_radius)
)
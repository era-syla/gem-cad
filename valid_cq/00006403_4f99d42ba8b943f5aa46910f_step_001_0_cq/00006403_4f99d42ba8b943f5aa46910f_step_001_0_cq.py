import cadquery as cq

# Parametric dimensions
diameter = 50.0  # Main diameter of the puck
total_height = 15.0  # Total height of the object
top_chamfer = 2.0  # Chamfer at the top edge
bottom_fillet = 5.0  # Large fillet/rounding at the bottom
groove_width = 1.5  # Width of the circumferential groove
groove_depth = 1.0  # Depth of the groove
groove_height_ratio = 0.3  # Position of the groove from the bottom (ratio of total height)

# Derived dimensions
radius = diameter / 2.0
groove_z_pos = total_height * groove_height_ratio

# Create the main cylinder
base = cq.Workplane("XY").circle(radius).extrude(total_height)

# Create the groove
# We select the face at the calculated height, but it's cleaner to just cut a ring
# Using a sketch on the XZ plane to revolve-cut the groove is often more robust for complex profiles,
# but a simple subtractive cylinder or torus approach works for simple grooves.
# Let's use a subtractive cylinder approach by creating a ring and cutting it.
groove_cutter = (
    cq.Workplane("XY")
    .workplane(offset=groove_z_pos)
    .circle(radius + 1)  # Outer radius (larger than part)
    .circle(radius - groove_depth)  # Inner radius (cutting depth)
    .extrude(groove_width)
)

# Apply operations
result = (
    base
    # Apply the top chamfer
    .faces(">Z").chamfer(top_chamfer)
    # Apply the bottom fillet (looks like a continuous curve, likely a fillet)
    .faces("<Z").fillet(bottom_fillet)
    # Cut the groove
    .cut(groove_cutter)
)

# Optional: Adding the split line visualization is not strictly possible as "geometry" 
# in a solid model (it's likely a rendering artifact or a parting line in the image), 
# but the geometry itself is complete.

# Final Result
show_object(result) if 'show_object' in globals() else None
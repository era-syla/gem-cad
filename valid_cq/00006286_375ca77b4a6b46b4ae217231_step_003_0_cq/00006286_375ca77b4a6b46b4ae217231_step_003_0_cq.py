import cadquery as cq

# Parameters for the block dimensions
length = 200.0   # Overall length of the block
width = 200.0    # Overall width of the block
height = 200.0   # Overall height of the block
wall_thickness = 25.0  # Thickness of the walls

# Parameters for the interlocking tongue
tongue_width = 40.0
tongue_protrusion = 10.0

# Parameters for fillets
inner_fillet_radius = 15.0

# 1. Create the main outer block
# We start with a solid block
block = cq.Workplane("XY").box(length, width, height)

# 2. Add the protrusion (tongue) on one side
# We'll place this on the 'right' face relative to the initial box
tongue = (
    cq.Workplane("YZ")
    .workplane(offset=length / 2.0)  # Move to the positive X face
    .rect(tongue_width, height)      # Rectangle for the tongue profile
    .extrude(tongue_protrusion)      # Extrude outwards
)

# Combine the main block and the tongue
main_body = block.union(tongue)

# 3. Create the hollow interior
# We create a cutting shape that is smaller than the main body
# and use it to cut through the Z-axis.
cutout_length = length - (2 * wall_thickness)
cutout_width = width - (2 * wall_thickness)

# Create the cutout shape
# We use a rectangle and fillet the corners to get the rounded inner look
cutout = (
    cq.Workplane("XY")
    .rect(cutout_length, cutout_width)
    .extrude(height * 2, both=True) # Extrude long enough to cut through everything
    .edges("|Z")                    # Select the vertical edges
    .fillet(inner_fillet_radius)    # Apply fillet to the vertical edges of the cutout
)

# 4. Perform the cut
result = main_body.cut(cutout)

# Export or display result
# show_object(result)
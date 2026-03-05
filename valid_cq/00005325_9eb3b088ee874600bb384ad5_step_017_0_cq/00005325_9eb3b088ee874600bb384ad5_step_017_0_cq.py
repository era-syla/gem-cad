import cadquery as cq

# Parametric dimensions
outer_diameter = 50.0
length = 60.0
wall_thickness = 5.0
fillet_radius = 10.0  # Radius for the closed end

# Derived dimensions
inner_diameter = outer_diameter - (2 * wall_thickness)

# Create the base cylinder
# We start with a solid cylinder
base = cq.Workplane("XY").circle(outer_diameter / 2).extrude(length)

# Create the hollow interior
# We cut a cylinder from the top face, leaving the bottom solid for now
hollow_cut = (
    cq.Workplane("XY")
    .workplane(offset=wall_thickness)  # Offset from bottom to leave thickness
    .circle(inner_diameter / 2)
    .extrude(length, combine=False)    # Create the cutter object
)

# Apply the cut to the base
shell = base.cut(hollow_cut)

# Create the rounded bottom
# Select the bottom edge of the cylinder and apply a fillet
result = shell.edges("<Z").fillet(fillet_radius)

# Alternatively, if the bottom is meant to be fully spherical/domed:
# result = shell.edges("<Z").fillet(outer_diameter / 2 - 0.01) 
# Note: A fillet radius exactly equal to radius usually breaks kernels, slightly less works.
# Based on the image, it looks like a large fillet, but perhaps not a full hemisphere. 
# The generic fillet_radius variable allows adjustment.
import cadquery as cq

# Parametric dimensions based on the visual estimation
length = 150.0          # Total length of the channel
outer_radius = 40.0     # Radius of the outer surface
wall_thickness = 5.0    # Thickness of the wall
inner_radius = outer_radius - wall_thickness

# Step 1: Create a full hollow tube
# We sketch on the YZ plane so the extrusion runs along the X axis
tube = (
    cq.Workplane("YZ")
    .circle(outer_radius)   # Outer boundary
    .circle(inner_radius)   # Inner boundary (hole)
    .extrude(length)
)

# Step 2: Create a cutting box to remove the top half
# The tube is centered at (0,0,0). To create a U-shaped trough,
# we remove the material where Z > 0.
# We create a large box positioned to intersect the upper half of the tube.
cut_box = (
    cq.Workplane("XY")
    .workplane(offset=outer_radius)  # Move plane up to Z = outer_radius
    .box(length * 1.5, outer_radius * 3, outer_radius * 2)
    # The box is centered at Z=outer_radius with height 2*outer_radius,
    # effectively covering the range Z=[0, 2*outer_radius].
)

# Step 3: Perform the boolean cut operation
result = tube.cut(cut_box)
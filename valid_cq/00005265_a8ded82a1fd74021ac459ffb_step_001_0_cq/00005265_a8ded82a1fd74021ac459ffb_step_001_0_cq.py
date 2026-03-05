import cadquery as cq

# Parametric Dimensions
cylinder_radius = 20.0  # Main radius of the cylinder
cylinder_height = 20.0  # Total height of the object
groove_depth = 1.0      # Depth of the horizontal grooves
groove_height = 1.0     # Height of the cutout part of the groove
num_grooves = 8         # Number of grooves along the height

# Create the base cylinder
result = cq.Workplane("XY").circle(cylinder_radius).extrude(cylinder_height)

# Calculate spacing
# We want grooves distributed along the side.
# We need to cut rings out of the cylinder.
# Let's define the pattern for the cuts.
# The total height is partitioned into segments for ridges and grooves.

spacing = cylinder_height / (num_grooves + 1)

# Create the cutting tool (a ring) and cut multiple times
for i in range(1, num_grooves + 1):
    z_pos = i * spacing - (groove_height / 2.0)
    
    # We create a cutting shape for each groove
    # A groove is a cylinder slightly larger than the base to ensure full cut,
    # but we only care about the inner radius which is (cylinder_radius - groove_depth)
    # Actually, simpler to just cut a ring shape or revolve a rectangle.
    
    # Let's use a simple cut with a cylinder of smaller radius? No, that would hollow it.
    # We need to remove material from the outside.
    # We can create a large ring and cut, or make a smaller cylinder and intersect? No.
    # The easiest way in CadQuery to make grooves on a cylinder is to revolve a profile 
    # or to cut with a torus/cylinder.
    
    # Approach: Create a large cylinder (the negative space) and cut it away.
    # This negative space is a ring with inner radius = (cylinder_radius - groove_depth)
    # and outer radius = (cylinder_radius + extra).
    
    cutter = (
        cq.Workplane("XY")
        .workplane(offset=z_pos)
        .circle(cylinder_radius + 5.0) # Outer boundary of cut
        .circle(cylinder_radius - groove_depth) # Inner boundary of cut
        .extrude(groove_height)
    )
    
    result = result.cut(cutter)

# Optional: Add small chamfers to the top and bottom edges for a polished look
result = result.edges(">Z or <Z").chamfer(0.5)
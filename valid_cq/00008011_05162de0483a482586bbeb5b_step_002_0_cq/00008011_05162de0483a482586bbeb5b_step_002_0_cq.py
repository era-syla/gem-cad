import cadquery as cq

# Parameters
base_diameter = 100.0  # Outer diameter of the base
top_diameter = 50.0    # Diameter of the top flat circular face
total_height = 20.0    # Total height of the object
base_thickness = 2.0   # Thickness of the small vertical lip at the base
top_thickness = 5.0    # Thickness of the top cylindrical section

# Create the geometry
# We can model this using a revolution of a profile or by lofting/stacking shapes.
# Stacking primitives is often simpler for this kind of shape.

# 1. Create the base disk (the thin bottom lip)
# Note: The image shows a very thin vertical edge at the bottom.
base = cq.Workplane("XY").circle(base_diameter / 2).extrude(base_thickness)

# 2. Create the conical section
# This connects the top of the base lip to the bottom of the top cylinder.
cone_height = total_height - base_thickness - top_thickness
cone = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .circle(base_diameter / 2)
    .workplane(offset=cone_height)
    .circle(top_diameter / 2)
    .loft(combine=True)
)

# 3. Create the top cylinder
top_cylinder = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness + cone_height)
    .circle(top_diameter / 2)
    .extrude(top_thickness)
)

# Combine everything
# Since we started separate workplanes, we need to union them carefully or
# build sequentially on the same stack. The loft method above created a new solid.
# Let's rebuild sequentially for cleaner CadQuery logic.

result = (
    cq.Workplane("XY")
    # Base lip
    .circle(base_diameter / 2).extrude(base_thickness)
    # Move to top of base lip
    .faces(">Z").workplane()
    # Create the cone via lofting to the next height
    .circle(base_diameter / 2)
    .workplane(offset=total_height - base_thickness - top_thickness)
    .circle(top_diameter / 2)
    .loft(combine=True)
    # Move to top of the cone
    .faces(">Z").workplane()
    # Create the top cylinder
    .circle(top_diameter / 2)
    .extrude(top_thickness)
)
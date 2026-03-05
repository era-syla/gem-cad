import cadquery as cq

# --- Parameters ---
# Dimensions of the tube cross-section
outer_diameter = 16.0
wall_thickness = 1.5
inner_diameter = outer_diameter - (2 * wall_thickness)

# Dimensions of the path
straight_section_length = 20.0
bend_horizontal_length = 100.0
bend_vertical_drop = -40.0

# --- Modeling ---

# 1. Define the sweep path
# The path lies on the XZ plane. It starts with a straight line along the X-axis,
# followed by a smooth tangent arc curving downwards.
path = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(straight_section_length, 0)
    .tangentArcPoint(
        (straight_section_length + bend_horizontal_length, bend_vertical_drop)
    )
)

# 2. Define the cross-section profile
# The profile is an annulus (ring) defined on the YZ plane, which is perpendicular 
# to the starting direction of the path.
profile = (
    cq.Workplane("YZ")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
)

# 3. Generate the 3D geometry
# Sweep the profile along the path to create the bent tube.
result = profile.sweep(path)
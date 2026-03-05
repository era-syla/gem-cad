import cadquery as cq

# ------------------------------------------------------------------------------
# Parameters
# ------------------------------------------------------------------------------
outer_diameter = 140.0
inner_diameter = 40.0
height = 25.0
wall_thickness = 3.0
split_gap = 0.5

# Derived radii for the centerline of the profile
# We adjust by half thickness so the resulting wall is centered on these dimensions
r_start = (inner_diameter / 2.0) + (wall_thickness / 2.0)
r_end = (outer_diameter / 2.0) - (wall_thickness / 2.0)

# ------------------------------------------------------------------------------
# 1. Generate Main Body (Revolution)
# ------------------------------------------------------------------------------
# Create the cross-section profile on the XZ plane.
# The shape is a "bell" or "dome" curve, starting vertical at the top (collar)
# and becoming horizontal at the bottom (flange).
profile_wire = (
    cq.Workplane("XZ")
    .moveTo(r_start, height)
    .spline(
        [(r_end, 0)],
        tangents=[(0, -1), (1, 0)],  # Tangent down at start, horizontal at end
        includeCurrent=True
    )
)

# Thicken the wire to create the solid cross-section.
# offset2D with default kind='arc' creates the rounded lips at top and bottom edges.
profile_face = profile_wire.wire().offset2D(wall_thickness / 2.0)

# Revolve the profile 360 degrees around the Z-axis.
# In the XZ plane, the Z-axis is represented by the vector (0, 1) starting from origin.
main_body = profile_face.revolve(360, (0, 0), (0, 1))

# ------------------------------------------------------------------------------
# 2. Create the Split (Cut)
# ------------------------------------------------------------------------------
# Create a curved path on the XY plane to represent the split line.
# This mimics the "S" or curved split often seen on retrofit escutcheons.
cut_wire = (
    cq.Workplane("XY")
    .moveTo((inner_diameter / 2.0) - 5, 0)  # Start slightly inside the hole
    .spline(
        [(outer_diameter / 2.0 + 5, 15)],   # End outside the rim, offset in Y for curve
        tangents=[(1, 0), (1, 0.5)],        # Start radial, curve outwards
        includeCurrent=True
    )
)

# Create a solid tool from the wire to perform the boolean cut
cut_tool = (
    cut_wire
    .offset2D(split_gap / 2.0)      # Define the width of the cut
    .extrude(height * 2)            # Extrude tall enough to cut through the dome
    .translate((0, 0, -height))     # Position it to cover the full height
)

# ------------------------------------------------------------------------------
# 3. Final Boolean Operation
# ------------------------------------------------------------------------------
result = main_body.cut(cut_tool)
import cadquery as cq

# Parametric dimensions
outer_diameter = 40.0
inner_diameter = 20.0  # Bore size
total_height = 25.0
groove_radius = 6.0    # Radius of the concave cutout
groove_depth = 4.0     # How deep the groove cuts into the cylinder

# Derived calculations
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
rim_thickness = (outer_diameter - inner_diameter) / 2.0

# Create the base cylindrical shape with a center hole
pulley = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(total_height)
)

# Create the groove profile to revolve-cut
# The groove is centered vertically on the pulley's side
# We sketch on the XZ plane to cut into the side of the cylinder
groove_center_height = total_height / 2.0

# Create a cutter object for the groove
# We draw a profile on a plane perpendicular to the XY plane (like XZ)
# and then revolve it, or simply use a cut operation with a revolved solid.
# Alternatively, we can just sketch the cross-section and revolve it to create the main body directly.
# Let's try the direct revolve approach for cleaner geometry.

# Re-approach: Define the cross-section and revolve it 360 degrees.
# This is often more robust for rotationally symmetric parts.

# Points for the cross-section (right side of the axis)
p0 = (inner_radius, 0)
p1 = (outer_radius, 0)
p2 = (outer_radius, total_height)
p3 = (inner_radius, total_height)

# The groove will be an arc cut out of the outer edge.
# The arc center needs to be calculated or defined relative to the side.
# Let's assume a circular arc groove centered vertically.

# Using the direct revolve method:
result = (
    cq.Workplane("XZ")
    # Draw the main rectangular cross-section
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, total_height)
    .lineTo(inner_radius, total_height)
    .close()
    # Revolve to make the solid cylinder first
    .revolve()
)

# Now cut the groove.
# We'll create a torus-like shape or revolve a cutter profile to remove material.
# An arc profile on the XZ plane at the outer edge.
groove_cutter = (
    cq.Workplane("XZ")
    .moveTo(outer_radius + groove_radius - groove_depth, total_height / 2.0)
    .circle(groove_radius)
    .revolve()
)

# Combine operations
result = result.cut(groove_cutter)

# Alternatively, a more elegant single-sketch approach:
# Draw the right half cross-section with the arc cut out, then revolve.
result = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, (total_height / 2.0) - (groove_radius * 0.8)) # Go up to start of groove
    # Create the concave arc for the groove
    # We want an arc that dips in by 'groove_depth'
    .threePointArc(
        (outer_radius - groove_depth, total_height / 2.0), # Midpoint of arc (deepest point)
        (outer_radius, (total_height / 2.0) + (groove_radius * 0.8)) # End point of arc
    )
    .lineTo(outer_radius, total_height)
    .lineTo(inner_radius, total_height)
    .close()
    .revolve()
)

# The previous single-sketch approach requires calculating exact arc points which can be tricky 
# to make perfectly tangential or specific radius without constraints solver. 
# The "make cylinder then cut groove" approach is more explicit and easier to parametize 
# for a specific radius. Let's stick to the boolean operation method as it guarantees the 
# groove shape is exactly the cutter shape (a torus section).

# Final robust implementation:
# 1. Cylinder with hole
# 2. Toroidal cut

result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(total_height)
)

# Define the cutting profile for the groove on the XZ plane.
# The cutter is a circle centered outside the part radius to create a groove.
# Center of the cutter circle:
cutter_center_x = outer_radius + (groove_radius - groove_depth)
cutter_center_z = total_height / 2.0

groove_cutter = (
    cq.Workplane("XZ")
    .moveTo(cutter_center_x, cutter_center_z)
    .circle(groove_radius)
    .revolve()
)

result = result.cut(groove_cutter)
import cadquery as cq

# --- Parametric Dimensions ---
# Main Cylinder Body
body_radius = 15.0
body_length = 70.0
leg_height_under_cyl = 8.0  # Height of legs below the cylinder bottom
leg_width = 10.0            # Thickness of the legs along the X axis

# Derived vertical position: Cylinder axis Z height
# Legs go from Z=0 to Z=center_axis to cradle the cylinder
center_z = body_radius + leg_height_under_cyl

# Shaft
shaft_radius = 4.0
shaft_length = 25.0

# Large Disc
disc_radius = 28.0
disc_thickness = 5.0
disc_hole_radius = 2.5

# Target Objects (Floating)
target_distance = 40.0      # Gap between disc face and target
base_side = 16.0
base_height = 4.0
sphere_radius = 5.0
sphere_gap = 6.0            # Gap between base top and sphere bottom

# --- Geometry Construction ---

# 1. Main Housing Body
# Oriented along the X-axis, starting at X=0
housing_cyl = (
    cq.Workplane("YZ")
    .circle(body_radius)
    .extrude(body_length)
    .translate((0, 0, center_z))
)

# Support Legs
# Defined on the ground plane (XY), extruding up to the cylinder axis
# This creates a U-shaped cradle effect when unioned with the cylinder
leg_geo = (
    cq.Workplane("XY")
    .rect(leg_width, body_radius * 2)
    .extrude(center_z)
)

# Position Front Leg (at start of body)
leg_front = leg_geo.translate((leg_width / 2, 0, 0))

# Position Back Leg (at end of body)
leg_back = leg_geo.translate((body_length - leg_width / 2, 0, 0))

# Combine Body Assembly
main_assembly = housing_cyl.union(leg_front).union(leg_back)

# 2. Shaft
# Extends from the front face (X=0) in the negative X direction
shaft = (
    cq.Workplane("YZ")
    .circle(shaft_radius)
    .extrude(-shaft_length)
    .translate((0, 0, center_z))
)

# 3. Disc with Hole
# Attached to the end of the shaft
disc_pos_x = -shaft_length
disc = (
    cq.Workplane("YZ")
    .workplane(offset=disc_pos_x)
    .circle(disc_radius)
    .circle(disc_hole_radius)  # Inner circle defines the hole
    .extrude(-disc_thickness)  # Extrude outwards (negative X)
    .translate((0, 0, center_z))
)

# 4. Target Objects (Square Base + Floating Sphere)
# Positioned further along negative X
target_x = disc_pos_x - disc_thickness - target_distance

# Square Base
target_base = (
    cq.Workplane("XY")
    .rect(base_side, base_side)
    .extrude(base_height)
    .translate((target_x, 0, 0))
)

# Floating Sphere
# Calculate center Z for sphere
sphere_z = base_height + sphere_gap + sphere_radius
target_sphere = (
    cq.Workplane("XY")
    .workplane(offset=sphere_z)
    .sphere(sphere_radius)
    .translate((target_x, 0, 0))
)

# --- Final Assembly ---
result = (
    main_assembly
    .union(shaft)
    .union(disc)
    .union(target_base)
    .union(target_sphere)
)
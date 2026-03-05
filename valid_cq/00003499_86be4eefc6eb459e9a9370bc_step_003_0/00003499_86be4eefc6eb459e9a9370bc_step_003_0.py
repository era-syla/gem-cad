import cadquery as cq

# --- Parameters ---

# Component 1: Tri-Leg Spider Bracket
spider_radius = 16.0
spider_thickness = 1.2
spider_hole_dia = 4.0
leg_width = 9.0
leg_extension = 6.0
leg_drop = 9.0
leg_bend_radius = 3.0
leg_curl_radius = 2.0

# Component 2: Hinge Strap
strap_length = 80.0
strap_width = 25.0
strap_thickness = 1.2
strap_curl_radius = 2.5
notch_width = 11.0
notch_depth = 10.0  # Cutout depth into the flat section

# --- Modeling Component 1: Spider Bracket ---

# 1. Central Disk
spider_disk = (
    cq.Workplane("XY")
    .circle(spider_radius)
    .extrude(spider_thickness)
    .faces(">Z").workplane()
    .circle(spider_hole_dia / 2).cutThruAll()
)

# 2. Leg Geometry (modeled on XZ plane, extruded in Y)
# Start slightly inside the disk radius to ensure overlapping solids
leg_start_x = spider_radius - 2.0

# Define the path of the leg's centerline (Side Profile)
leg_path = (
    cq.Workplane("XZ")
    .moveTo(leg_start_x, 0)
    .lineTo(spider_radius + leg_extension, 0)
    # Bend downwards
    .tangentArcPoint((spider_radius + leg_extension + leg_bend_radius, -leg_bend_radius))
    .lineTo(spider_radius + leg_extension + leg_bend_radius, -leg_drop)
    # Curl inward (approx 180 degrees)
    .tangentArcPoint((spider_radius + leg_extension + leg_bend_radius - 2*leg_curl_radius, -leg_drop))
)

# Thicken the path (offset2D) and extrude to create the 3D leg
leg_solid = (
    leg_path
    .offset2D(spider_thickness)
    .extrude(leg_width)
    .translate((0, -leg_width / 2, 0))  # Center the leg on the Y-axis
)

# 3. Pattern the legs
# Create a union of the disk and 3 rotated copies of the leg
spider_assembly = spider_disk
for i in range(3):
    angle = i * 120
    spider_assembly = spider_assembly.union(leg_solid.rotate((0, 0, 0), (0, 0, 1), angle))


# --- Modeling Component 2: Hinge Strap ---

# 1. Main Profile (Side view on XZ plane)
half_len = strap_length / 2.0

# Define the path: Left Hook -> Flat -> Right Hook
strap_path = (
    cq.Workplane("XZ")
    # Left Hook (Start at bottom tip, arc up-right to flat start)
    .moveTo(-half_len, -2 * strap_curl_radius)
    .threePointArc((-half_len - strap_curl_radius, -strap_curl_radius), (-half_len, 0))
    # Flat section
    .lineTo(half_len, 0)
    # Right Hook (Arc down-right to bottom tip)
    .threePointArc((half_len + strap_curl_radius, -strap_curl_radius), (half_len, -2 * strap_curl_radius))
)

# Extrude profile to create the full strap width
strap_solid = (
    strap_path
    .offset2D(strap_thickness)
    .extrude(strap_width)
    .translate((0, -strap_width / 2, 0))  # Center on Y-axis
)

# 2. Cutouts (Notches at ends)
# Create a cutting tool box to remove the center material at the hinges
cutout_box = (
    cq.Workplane("XY")
    .box(notch_depth * 3, notch_width, strap_curl_radius * 6) # Size covers the curl geometry
)

strap_assembly = (
    strap_solid
    .cut(cutout_box.translate((-half_len, 0, 0))) # Cut left end
    .cut(cutout_box.translate((half_len, 0, 0)))  # Cut right end
)


# --- Final Scene ---
# Position the strap offset from the spider to mimic the image layout
result = spider_assembly.union(strap_assembly.translate((0, 50, 0)))
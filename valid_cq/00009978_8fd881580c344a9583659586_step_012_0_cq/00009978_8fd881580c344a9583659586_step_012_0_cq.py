import cadquery as cq

# --- Parameters ---

# Main Housing Dimensions
main_width = 80.0
main_depth = 50.0
main_height = 60.0

# Top Cap Dimensions
top_cap_height = 25.0
top_cap_overhang = 2.0  # Slight lip over the base

# Front Housing (Right side in image)
front_box_width = 60.0
front_box_depth = 55.0
front_box_height = 30.0

# Side Connector Block (Small protrusion on the side)
side_conn_width = 20.0
side_conn_depth = 25.0
side_conn_height = 25.0

# Cylindrical Connectors/Nozzles
nozzle_diam_outer = 12.0
nozzle_diam_inner = 8.0
nozzle_length = 25.0

# Large Circular Port (Front face)
large_port_diam = 28.0
large_port_length = 15.0
square_drive_size = 6.0

# Screw Bosses
boss_diam = 6.0
screw_head_diam = 3.5

# --- Geometry Construction ---

# 1. Base Block (Dark component)
# Creating a simple rectangular prism for the solenoid/coil housing
base_block = (
    cq.Workplane("XY")
    .box(main_width, main_depth, main_height)
    # Fillet vertical edges slightly for realism
    .edges("|Z")
    .fillet(2.0)
)

# 2. Top Cap (Main cover)
# Positioned on top of the base block
top_cap = (
    cq.Workplane("XY")
    .workplane(offset=main_height / 2 + top_cap_height / 2)
    .box(main_width + top_cap_overhang, main_depth + top_cap_overhang, top_cap_height)
)

# Add chamfer to top edges of the cap
top_cap = top_cap.edges("|Z").fillet(3.0).edges(">Z").chamfer(1.0)

# 3. Front Housing (The boxy part extending to the right)
# Positioned relative to the top cap
front_housing = (
    cq.Workplane("XY")
    .workplane(offset=main_height / 2 + top_cap_height / 2)
    .center(main_width / 2 + front_box_width / 2 - 10, 0) # Overlap slightly
    .box(front_box_width, front_box_depth, front_box_height)
)
front_housing = front_housing.edges("|Z").fillet(2.0).edges(">Z").chamfer(1.0)

# 4. Side Connector Block (Small block protruding from the front housing)
side_block = (
    cq.Workplane("XY")
    .workplane(offset=main_height / 2 + top_cap_height / 2 - 5)
    .center(main_width / 2 - 5, -front_box_depth/2 - side_conn_depth/2 + 5)
    .box(side_conn_width, side_conn_depth, side_conn_height)
    .edges("|Z").fillet(1.0)
)

# 5. Connectors (Cylindrical nozzles on the right face)
# We need to position these on the +X face of the front housing
nozzle_plane = (
    front_housing.faces(">X").workplane()
)

# Create two nozzles
nozzle1 = (
    nozzle_plane
    .center(0, front_box_depth/4)
    .circle(nozzle_diam_outer/2)
    .extrude(nozzle_length)
)

nozzle2 = (
    nozzle_plane
    .center(0, -front_box_depth/2) # Reset relative to previous center
    .center(0, -front_box_depth/4)
    .circle(nozzle_diam_outer/2)
    .extrude(nozzle_length)
)

# Hollow out the nozzles
nozzle_hole1 = (
    nozzle1.faces(">X").workplane()
    .circle(nozzle_diam_inner/2)
    .cutBlind(-nozzle_length)
)
nozzle_hole2 = (
    nozzle2.faces(">X").workplane()
    .circle(nozzle_diam_inner/2)
    .cutBlind(-nozzle_length)
)

# 6. Large Circular Control/Port
# Situated on the front face of the front housing
large_port = (
    front_housing.faces(">Y").workplane()
    .center(front_box_width/4, 0) # Offset to the right
    .circle(large_port_diam/2)
    .extrude(large_port_length)
)

# Detail on the large port (square recess)
large_port = (
    large_port.faces(">Y").workplane()
    .rect(square_drive_size, square_drive_size)
    .cutBlind(-5.0)
)

# Add side details to large port (square notches often seen on solenoids)
large_port = (
    large_port.faces(">Y").workplane(offset=-large_port_length/2)
    .transformed(rotate=(0, 90, 0))
    .rect(5, 5)
    .cutThruAll()
)


# 7. Screw Bosses and Details
# Add screw bosses to the top cap corners
boss_locations = [
    (-main_width/2 + 5, -main_depth/2 + 5),
    (-main_width/2 + 5, main_depth/2 - 5),
    (main_width/2 - 5, -main_depth/2 + 5),
    (main_width/2 - 5, main_depth/2 - 5)
]

# We need to reference the top plane of the top cap
top_cap_with_bosses = top_cap
for loc in boss_locations:
    # Create the boss geometry (subtractive for screw head recess)
    top_cap_with_bosses = (
        top_cap_with_bosses.faces(">Z").workplane()
        .center(loc[0], loc[1])
        .circle(boss_diam/2)
        .cutBlind(-3.0) # Recess
        .faces(">Z[1]").workplane() # Select the bottom of the recess
        .circle(screw_head_diam/2) # Screw shaft hole
        .cutBlind(-10.0)
    )

# Add screw bosses to the front housing
front_boss_locations = [
    (front_box_width/2 - 5, front_box_depth/2 - 5),
    (front_box_width/2 - 5, -front_box_depth/2 + 5),
    (-front_box_width/2 + 5, front_box_depth/2 - 5),
    (-front_box_width/2 + 5, -front_box_depth/2 + 5),
]
front_housing_center = (main_width / 2 + front_box_width / 2 - 10, 0) # Center X, Y relative to origin

front_housing_with_bosses = front_housing
# We approximate these locations on the top of the front housing
for loc in front_boss_locations:
     front_housing_with_bosses = (
        front_housing_with_bosses.faces(">Z").workplane()
        .center(loc[0], loc[1])
        .circle(boss_diam/2)
        .cutBlind(-2.0)
        .faces(">Z[1]").workplane()
        .circle(screw_head_diam/2)
        .cutBlind(-8.0)
    )


# 8. Bottom connectors (under the main block)
# Two small cylindrical ports coming out of the bottom
bottom_ports = (
    base_block.faces("<Z").workplane()
    .center(0, main_depth/4)
    .circle(6)
    .extrude(10)
    .center(0, -main_depth/2)
    .circle(6)
    .extrude(10)
)


# --- Assembly ---

# Combine all solid parts
result = base_block.union(top_cap_with_bosses)
result = result.union(front_housing_with_bosses)
result = result.union(side_block)
result = result.union(nozzle1).union(nozzle2) # Solid nozzles
result = result.cut(nozzle_hole1).cut(nozzle_hole2) # Apply holes
result = result.union(large_port)
result = result.union(bottom_ports)

# Cleanup: fillet intersection between main parts for 'molded' look
# (This can be computationally expensive or fragile, so we apply selectively)
try:
    result = result.edges("(>Z and >X) or (>Z and >Y)").fillet(0.5)
except:
    pass # Skip if geometric kernel fails on complex edges

# Final Result
result = result
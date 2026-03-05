import cadquery as cq

# --- Parameters ---
# Overall dimensions
total_width = 1200.0
total_depth = 400.0
tall_height = 800.0
bench_height = 450.0

# Components dimensions
tall_section_width = 450.0
bench_section_width = total_width - tall_section_width

# Material thickness (approximate for the panels)
panel_thick = 18.0

# Cushion dimensions
cushion_height = 50.0
cushion_gap = 2.0  # Gap between cushion and edges

# Leg dimensions
leg_height = 100.0
leg_top_dia = 30.0
leg_bot_dia = 15.0

# Handle/Hole dimensions
hole_dia = 35.0
hole_height_ratio = 0.6  # Height of holes relative to the door face

# --- Geometry Construction ---

# 1. Main Cabinet Body (The "L" shape)

# Create the tall section
tall_box = (
    cq.Workplane("XY")
    .box(tall_section_width, total_depth, tall_height)
    .translate((-bench_section_width / 2, 0, tall_height / 2))
)

# Create the bench section
bench_box = (
    cq.Workplane("XY")
    .box(bench_section_width, total_depth, bench_height)
    .translate((tall_section_width / 2, 0, bench_height / 2))
)

# Combine them into the main carcass
carcass = tall_box.union(bench_box)

# 2. Add Door/Front Details
# Based on the image, there are faint lines suggesting doors or drawers.
# There is a distinct horizontal line running across the bench part and maybe the tall part.
# The image shows a recessed front face or doors. Let's model a slight recess for the doors.

door_recess = 2.0
door_gap = 2.0

# Front face of the bench section
bench_door_width = bench_section_width - (2 * door_gap)
bench_door_height = bench_height - (2 * door_gap)
bench_door = (
    cq.Workplane("XZ")
    .workplane(offset=total_depth/2 + door_recess) # slightly proud or flush
    .box(bench_door_width, bench_door_height, panel_thick)
    .translate((tall_section_width / 2, bench_height / 2))
)

# Cut the holes in the bench door
hole_z_pos = bench_height * hole_height_ratio
hole_spacing = bench_section_width / 3.0

left_hole = (
    cq.Workplane("XY")
    .circle(hole_dia / 2)
    .extrude(panel_thick * 2)
    .translate((tall_section_width / 2 - hole_spacing/2, -total_depth, hole_z_pos))
    .rotate((0,0,0), (1,0,0), 90)
)

right_hole = (
    cq.Workplane("XY")
    .circle(hole_dia / 2)
    .extrude(panel_thick * 2)
    .translate((tall_section_width / 2 + hole_spacing/2, -total_depth, hole_z_pos))
    .rotate((0,0,0), (1,0,0), 90)
)

# Apply holes to the carcass/door representation
# Since we made a solid block, we'll just cut into the main block for simplicity unless we attach a separate door panel.
# Let's attach the door panel to the main block.
carcass = carcass.union(bench_door)
carcass = carcass.cut(left_hole).cut(right_hole)

# Add a subtle cut to separate the bench top from the door
reveal_cut = (
    cq.Workplane("XY")
    .box(bench_section_width, total_depth + 10, 2.0)
    .translate((tall_section_width / 2, 0, bench_height - panel_thick))
)
carcass = carcass.cut(reveal_cut)

# 3. The Cushion
# Sits on top of the bench section
cushion = (
    cq.Workplane("XY")
    .box(bench_section_width - cushion_gap*2, total_depth - cushion_gap*2, cushion_height)
    .translate((tall_section_width / 2, 0, bench_height + cushion_height / 2))
)

# 4. The Legs
# Create one leg
def create_leg():
    return (
        cq.Workplane("XY")
        .circle(leg_top_dia / 2)
        .workplane(offset=-leg_height)
        .circle(leg_bot_dia / 2)
        .loft(combine=True)
    )

leg_x_offset = total_width / 2 - 40.0
leg_y_offset = total_depth / 2 - 40.0

# Generate 4 legs positions
legs = cq.Workplane("XY")

positions = [
    (-leg_x_offset, -leg_y_offset),
    (-leg_x_offset, leg_y_offset),
    (leg_x_offset, -leg_y_offset),
    (leg_x_offset, leg_y_offset)
]

# We need to adjust leg positions because the object center isn't at (0,0) of the world, 
# but the local center of the total width.
# Current center of mass in X is roughly (bench_width/2 - tall_width/2) / 2 ... it's easier to just place absolute coordinates relative to the full assembly.

# Calculate absolute bounds
min_x = -tall_section_width
max_x = bench_section_width
min_y = -total_depth / 2
max_y = total_depth / 2

leg_inset = 40.0

leg_positions = [
    (-tall_section_width / 2 - bench_section_width / 2 + leg_inset, min_y + leg_inset), # Far Left Front
    (-tall_section_width / 2 - bench_section_width / 2 + leg_inset, max_y - leg_inset), # Far Left Back
    (tall_section_width / 2 + bench_section_width / 2 - leg_inset, min_y + leg_inset),  # Far Right Front
    (tall_section_width / 2 + bench_section_width / 2 - leg_inset, max_y - leg_inset),  # Far Right Back
]

# There might be a middle leg under the divider for support, but the image shows 4 visible corner legs (implied).
# Let's stick to 4 corners of the bounding box.
# Re-calculating proper bounding box corners based on the "L" shape construction:
# Tall box center x: -bench_section_width / 2 
# Tall box width: tall_section_width
# Left edge: -bench_section_width / 2 - tall_section_width / 2 = -(bench + tall)/2 NOT correct.
# Let's trace back:
# Tall Box X Center: -bench_section_width / 2. Width: tall_section_width.
#   Left Edge: -bench_section_width/2 - tall_section_width/2
#   Right Edge: -bench_section_width/2 + tall_section_width/2
# Bench Box X Center: tall_section_width / 2. Width: bench_section_width.
#   Left Edge: tall_section_width/2 - bench_section_width/2 (This matches the Tall Right Edge)
#   Right Edge: tall_section_width/2 + bench_section_width/2

overall_left = -bench_section_width / 2 - tall_section_width / 2
overall_right = tall_section_width / 2 + bench_section_width / 2

leg_coords = [
    (overall_left + leg_inset, -total_depth/2 + leg_inset),
    (overall_left + leg_inset, total_depth/2 - leg_inset),
    (overall_right - leg_inset, -total_depth/2 + leg_inset),
    (overall_right - leg_inset, total_depth/2 - leg_inset)
]

legs_compound = cq.Assembly()
for x, y in leg_coords:
    l = create_leg().translate((x, y, 0))
    legs_compound.add(l)

# Union legs into one object for simple boolean math later if needed, 
# but keeping them separate usually better. We will union them to the result.
all_legs = legs_compound.toCompound()


# 5. Final Assembly
# Move everything up so legs sit on Z=0
assembly_z_offset = leg_height

carcass = carcass.translate((0, 0, assembly_z_offset))
cushion = cushion.translate((0, 0, assembly_z_offset))
all_legs = all_legs.translate((0, 0, assembly_z_offset)) # Legs were built downwards from 0, so moving them up puts their bottom at 0

result = carcass.union(cushion).union(all_legs)

# Adding fillets to vertical edges for a softer look (optional but realistic)
result = result.edges("|Z").fillet(2.0)
# Adding fillets to the top edges
result = result.edges(">Z").fillet(1.0)
import cadquery as cq

# --- Parametric Dimensions ---

# Main Base Plate
base_length = 60.0
base_width = 40.0
base_thickness = 4.0
base_corner_radius = 2.5

# Side Walls
wall_height = 40.0
wall_thickness = 4.0
wall_spacing = 30.0 # Approximate distance between walls based on visual proportions

# Holes & Slots - Base
base_center_hole_d = 4.0
base_outer_hole_d = 5.0
base_outer_hole_pattern_w = 20.0 # Spacing between holes in width
base_outer_hole_pattern_l = 20.0 # Spacing between holes in length
base_slot_width = 3.0
base_slot_length = 10.0
base_slot_offset_x = 10.0 # Offset from center

# Holes - Left Wall (Shorter one with small holes)
left_wall_large_hole_d = 4.0
left_wall_small_hole_d = 2.5
left_wall_small_hole_spacing = 5.0

# Holes - Right Wall (Taller one with 4 hole pattern)
right_wall_hole_d = 3.5
right_wall_hole_spacing_x = 20.0
right_wall_hole_spacing_y = 20.0

# Cutout on front edge
front_cutout_width = 25.0
front_cutout_depth = 15.0

# --- Geometry Construction ---

# 1. Base Plate
# Create a centered rectangle, fillet corners, extrude
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
    .edges("|Z")
    .fillet(base_corner_radius)
)

# 2. Right Wall (The one with the 4-hole pattern)
# Positioned at the right edge
right_wall = (
    cq.Workplane("YZ")
    .workplane(offset=base_length/2 - wall_thickness)
    .moveTo(0, base_thickness)
    .rect(base_width, wall_height, centered=(True, False))
    .extrude(wall_thickness)
)

# 3. Left Wall (The one with the single large hole and small holes)
# Positioned inward, creating the "U" channel
left_wall_offset = (base_length/2) - wall_spacing - wall_thickness
left_wall = (
    cq.Workplane("YZ")
    .workplane(offset=left_wall_offset) 
    .moveTo(0, base_thickness)
    .rect(base_width, wall_height, centered=(True, False))
    .extrude(wall_thickness)
)

# Combine parts
main_body = base.union(right_wall).union(left_wall)

# --- Features & Cuts ---

# 4. Base Plate Holes
# Center hole
main_body = (
    main_body.faces("<Z").workplane()
    .center(0, 0)
    .circle(base_center_hole_d / 2)
    .cutThruAll()
)

# Pattern of 4 holes on base
main_body = (
    main_body.faces("<Z").workplane()
    .rect(base_outer_hole_pattern_l, base_outer_hole_pattern_w, forConstruction=True)
    .vertices()
    .circle(base_outer_hole_d / 2)
    .cutThruAll()
)

# Slot on Base (Right side of center)
main_body = (
    main_body.faces("<Z").workplane()
    .center(base_slot_offset_x, 0)
    .slot2D(base_slot_length, base_slot_width, angle=90)
    .cutThruAll()
)

# Front Cutout (creating the gap in the base)
# We need to cut a rectangular region from the front edge of the base
# positioned between the left edge and the "left wall"
cutout_center_x = -(base_length/2) + (front_cutout_depth/2) # Approximate positioning
cutout_center_y = 0 
main_body = (
    main_body.faces("<Z").workplane()
    .center(-(base_length/2) + front_cutout_depth/2, 0)
    .rect(front_cutout_depth, front_cutout_width)
    .cutThruAll()
)

# 5. Right Wall Holes (4-hole pattern)
# We need to select the inner face of the right wall
# The right wall is at X = +base_length/2
main_body = (
    main_body.faces(">X").workplane()
    .center(0, base_thickness + wall_height/2)
    .rect(right_wall_hole_spacing_x, right_wall_hole_spacing_y, forConstruction=True)
    .vertices()
    .circle(right_wall_hole_d / 2)
    .cutThruAll()
)

# 6. Left Wall Holes
# We need to select the face of the inner wall
# The wall center is at X = left_wall_offset + wall_thickness/2
main_body = (
    main_body.faces(">X").workplane(centerOption="ProjectedOrigin")
    .workplane(offset=-(base_length/2 - (left_wall_offset + wall_thickness)))
    # Center large hole
    .center(0, base_thickness + 15) # 15 is approx height
    .circle(left_wall_large_hole_d / 2)
    .cutThruAll()
)

# Small side holes on the edge of the left wall
# These look like they are on the side face (YZ plane equivalent), near the top edge
# Let's target the side edge of that wall
main_body = (
    main_body.faces("<Y").workplane(centerOption="ProjectedOrigin")
    .workplane(offset=0) 
    .moveTo(left_wall_offset + wall_thickness/2, base_thickness + wall_height - 5)
    .circle(left_wall_small_hole_d/2)
    .moveTo(left_wall_offset + wall_thickness/2 - left_wall_small_hole_spacing, base_thickness + wall_height - 5)
    .circle(left_wall_small_hole_d/2)
    .cutThruAll()
)

# 7. Add the little cutout on the side of the left wall (seen on the far left edge in image)
main_body = (
    main_body.faces("<X").workplane(centerOption="ProjectedOrigin")
    # Move to the edge of the inner wall
    .moveTo(-base_width/2, base_thickness + wall_height - 10) 
    .circle(2.0) # Small semicircular cutout
    .cutThruAll()
)

result = main_body
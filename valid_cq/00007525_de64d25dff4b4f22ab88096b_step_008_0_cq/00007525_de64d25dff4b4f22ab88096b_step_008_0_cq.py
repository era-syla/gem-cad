import cadquery as cq

# --- Parameters ---
# Overall dimensions
total_width = 100.0  # X axis
total_depth = 80.0   # Y axis
wall_height = 40.0   # Z axis
wall_thickness = 2.0
floor_thickness = 1.0

# Room layout parameters (based on visual estimation)
main_corridor_width = 30.0  # The wide section at the bottom
left_room_width = 40.0      # The room on the left
center_room_width = 30.0    # The small enclosed room in the center-back
right_room_width = 30.0     # The room on the right

# Opening dimensions
window_width = 15.0
window_height = 10.0
window_elevation = 15.0

large_door_width = 20.0
large_door_height = 25.0
interior_door_width = 12.0
interior_door_height = 25.0

# --- Geometry Construction ---

# 1. Base Floor
floor = cq.Workplane("XY").box(total_width, total_depth, floor_thickness)

# 2. Outer Shell (Extruding walls)
# We will create the outer perimeter and subtract the inner volume to make walls
outer_walls = (
    cq.Workplane("XY")
    .box(total_width, total_depth, wall_height)
    .translate((0, 0, wall_height / 2))
)

inner_volume = (
    cq.Workplane("XY")
    .box(total_width - 2 * wall_thickness, total_depth - 2 * wall_thickness, wall_height)
    .translate((0, 0, wall_height / 2))
)

shell = outer_walls.cut(inner_volume)

# 3. Internal Walls
# Wall 1: Separating left room from the rest
# Positioned at x = -total_width/2 + left_room_width
sep_wall_x_pos = -total_width/2 + left_room_width
wall_internal_1 = (
    cq.Workplane("XY")
    .box(wall_thickness, total_depth - main_corridor_width, wall_height)
    .translate((sep_wall_x_pos, (total_depth/2) - (total_depth - main_corridor_width)/2, wall_height/2))
)

# Wall 2: Separating right room from the rest
# Positioned at x = total_width/2 - right_room_width
sep_wall_x_pos_2 = total_width/2 - right_room_width
wall_internal_2 = (
    cq.Workplane("XY")
    .box(wall_thickness, total_depth - main_corridor_width, wall_height)
    .translate((sep_wall_x_pos_2, (total_depth/2) - (total_depth - main_corridor_width)/2, wall_height/2))
)

# Wall 3: Front of the center room (parallel to X axis)
# Positioned at y = total_depth/2 - (total_depth - main_corridor_width)
center_wall_y_pos = (total_depth/2) - (total_depth - main_corridor_width)
wall_internal_3 = (
    cq.Workplane("XY")
    .box(center_room_width, wall_thickness, wall_height)
    .translate((0, center_wall_y_pos, wall_height/2))
)

# Combine structure
building = shell.union(wall_internal_1).union(wall_internal_2).union(wall_internal_3)


# 4. Cuts (Windows and Doors)

# Large front door (bottom right face in image perspective)
# This is on the Y-min face, but wait, the perspective is angled. 
# Let's assume the "front" visible face with the big door is X-positive face.
# Looking at the layout, the long side is facing front-left. 
# Let's place the large door on the X-positive face (right side of image)
building = building.cut(
    cq.Workplane("YZ")
    .workplane(offset=total_width/2)
    .center(-total_depth/2 + right_room_width/2 + 5, large_door_height/2) # Approximate centering
    .rect(large_door_width, large_door_height)
    .extrude(-wall_thickness * 2)
)

# Window on X-positive face (further back)
building = building.cut(
    cq.Workplane("YZ")
    .workplane(offset=total_width/2)
    .center(total_depth/4, window_elevation + window_height/2)
    .rect(window_width, window_height)
    .extrude(-wall_thickness * 2)
)

# Window on Y-negative face (left side of image, front wall)
building = building.cut(
    cq.Workplane("XZ")
    .workplane(offset=-total_depth/2)
    .center(-total_width/2 + left_room_width/2, window_elevation + window_height/2)
    .rect(window_width, window_height)
    .extrude(wall_thickness * 2)
)

# Door into the center room
# Located on the internal wall (wall_internal_3)
building = building.cut(
    cq.Workplane("XZ")
    .workplane(offset=center_wall_y_pos - wall_thickness/2) # align with the face of the internal wall
    .center(-center_room_width/4, interior_door_height/2) # Offset slightly left
    .rect(interior_door_width, interior_door_height)
    .extrude(wall_thickness * 2)
)

# Gap/Doorway between left room and center corridor
# Located on wall_internal_1
building = building.cut(
    cq.Workplane("YZ")
    .workplane(offset=sep_wall_x_pos + wall_thickness/2)
    .center(center_wall_y_pos/2 + total_depth/4 , interior_door_height/2) # Rough positioning
    .rect(interior_door_width, interior_door_height)
    .extrude(-wall_thickness * 2)
)
# Actually, looking at the image, the left wall has a gap/opening, not a door frame.
# Let's just cut a slot out of the wall we created earlier.
# Or simpler: cut a box out of the specific location on wall_internal_1
cutout_box = (
    cq.Workplane("XY")
    .box(wall_thickness * 2, interior_door_width, interior_door_height)
    .translate((sep_wall_x_pos, center_wall_y_pos + interior_door_width, interior_door_height/2))
)
building = building.cut(cutout_box)


# Small window in the back of the center room
building = building.cut(
    cq.Workplane("XZ")
    .workplane(offset=total_depth/2)
    .center(0, window_elevation + window_height/2 + 10) # Higher up
    .rect(window_width/2, window_height/2)
    .extrude(-wall_thickness * 2)
)

# Combine floor with walls
result = building.union(floor)

# Move everything up so floor sits on Z=0
result = result.translate((0, 0, floor_thickness/2))
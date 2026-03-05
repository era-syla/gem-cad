import cadquery as cq

# --- Parametric Dimensions ---

# Overall bounding box dimensions
overall_length = 100.0  # X direction
overall_width = 80.0    # Y direction
wall_height = 40.0      # Z direction
wall_thickness = 2.0    # Thickness of all walls

# Internal Layout parameters
# The layout seems to be split roughly 60/40 along the length
split_ratio = 0.6
split_x_pos = overall_length * split_ratio

# Door parameters
door_width = 15.0
door_height = 25.0

# Window parameters
window_width = 12.0
window_height = 15.0
window_sill_height = 10.0

# Furniture / Internal Block parameters
# Large block (resembling a stove or cabinet)
block1_width = 15.0
block1_depth = 15.0
block1_height = 20.0

# Smaller adjacent block
block2_width = 10.0
block2_depth = 10.0
block2_height = 10.0

# --- Geometry Construction ---

# 1. Base Structure: Create the outer shell (floor + walls)
# Start with a solid block and shell it to create walls and floor
base = (
    cq.Workplane("XY")
    .box(overall_length, overall_width, wall_height)
    .faces("+Z")
    .shell(wall_thickness) # Positive thickness adds material outside, but here we want inside. Let's do a cut strategy instead for better control.
)

# Alternative Strategy: Extrude floor, then extrude walls.
# This gives cleaner control over wall placement relative to grid.

# Floor
floor = cq.Workplane("XY").box(overall_length, overall_width, wall_thickness)

# Outer Walls
outer_walls_outline = (
    cq.Workplane("XY")
    .rect(overall_length, overall_width)
    .rect(overall_length - 2*wall_thickness, overall_width - 2*wall_thickness)
    .extrude(wall_height)
)

# 2. Internal Wall
# A wall dividing the space along the Y axis
# Located at split_x_pos relative to the left edge? No, let's place it relative to center.
# Center of overall is (0,0). Left edge is -50. Split is at approx X = 10.
internal_wall_x_center = -overall_length/2 + split_x_pos

internal_wall = (
    cq.Workplane("XY")
    .center(internal_wall_x_center, 0)
    .rect(wall_thickness, overall_width - 2*wall_thickness)
    .extrude(wall_height)
)

# 3. Create the basic room structure
structure = floor.union(outer_walls_outline).union(internal_wall)

# 4. Cuts: Doors
# Door 1: Connecting the two main rooms (in the internal wall)
door_cutout_internal = (
    cq.Workplane("XZ")
    .center(internal_wall_x_center, wall_height/2) # Center on wall X, vertical center
    .workplane(offset=-overall_width/4) # Move to Y location of door
    .rect(wall_thickness * 3, door_height) # Width (X) needs to penetrate wall, Height (Z)
    .extrude(door_width) # Extrude along Y
)

# Door 2: Entrance (on the "front" right wall in the image view, which is likely -Y face)
# Based on image, there is an opening in the internal wall, and another "doorway" looking opening in the short wall section attached to the internal wall?
# Wait, looking closer at the image:
# There is a main internal wall.
# There is a smaller partial wall sticking out from the internal wall into the right room.
# There is a doorway in the internal wall.
# There is a window in the far right wall.

# Let's refine the layout based on closer inspection.
# Left Room: Large empty space.
# Right Room: Contains a partial wall dividing a small vestibule/entry area.

# Correction: Add the small partial wall in the right room
partial_wall_length = overall_width * 0.4
partial_wall_y_pos = -overall_width/2 + partial_wall_length/2 + 10 # Offset from bottom
partial_wall_x_pos = internal_wall_x_center + wall_thickness/2 + partial_wall_length/2 

partial_wall = (
    cq.Workplane("XY")
    .center(internal_wall_x_center + wall_thickness/2 + 15, -10) # Approx position
    .rect(30, wall_thickness) # Length 30 extending into right room
    .extrude(wall_height)
)

# Combine again
structure = structure.union(partial_wall)

# Now Cut Door in Internal Wall
# It looks like a tall archway or door
door_internal = (
    cq.Workplane("YZ")
    .center(-5, wall_height/2) # Y position (slightly off center), Z center
    .rect(door_width, door_height*2) # Cut from bottom
)
# Position the cut at the X of the internal wall
structure = structure.cut(
    door_internal.workplane(offset=internal_wall_x_center).extrude(wall_thickness*3, both=True)
)

# Cut Door/Opening in Partial Wall
door_partial = (
    cq.Workplane("XZ")
    .center(internal_wall_x_center + wall_thickness/2 + 25, wall_height/2) 
    .rect(10, door_height*2)
)
structure = structure.cut(
    door_partial.workplane(offset=-10).extrude(wall_thickness*3, both=True)
)

# Cut Window in Right Wall (+X wall)
window_cutout = (
    cq.Workplane("YZ")
    .center(10, window_sill_height + window_height/2) # Y pos, Z pos
    .rect(window_width, window_height)
)
structure = structure.cut(
    window_cutout.workplane(offset=overall_length/2).extrude(wall_thickness*3, both=True)
)

# Another Window/Door next to it?
window_cutout_2 = (
    cq.Workplane("YZ")
    .center(-5, window_sill_height + window_height/2) # Y pos, Z pos
    .rect(window_width, window_height)
)
structure = structure.cut(
    window_cutout_2.workplane(offset=overall_length/2).extrude(wall_thickness*3, both=True)
)


# 5. Furniture / Fixtures
# There is a blocky structure in the corner of the left room, against the internal wall.

# Main vertical block (Stove?)
furn_x = internal_wall_x_center - block1_width/2 - 0.1 # Against internal wall
furn_y = -overall_width/4 # Roughly centered in Y of that segment

furniture_1 = (
    cq.Workplane("XY")
    .center(furn_x, furn_y)
    .box(block1_width, block1_depth, block1_height)
    .translate((0, 0, block1_height/2)) # Sit on floor (floor is at Z=0? No, floor is centered at 0 in Z usually if box used. Adjusting.)
)

# Our floor was extruded 'wall_thickness' high. Let's assume Z=wall_thickness is the floor level.
furniture_1 = furniture_1.translate((0,0, wall_thickness - block1_height/2)) 

# Smaller block next to it
furniture_2 = (
    cq.Workplane("XY")
    .center(furn_x + block1_width/2 + block2_width/2, furn_y - block1_depth/2 + block2_depth/2) # Position relative
    .box(block2_width, block2_depth, block2_height)
    .translate((0, 0, wall_thickness + block2_height/2)) 
)
# Actually the small block is in front (lower Y) and to the right?
# Let's adjust based on the L-shape in image.
# The image shows a tall block, and a lower block attached to its side/front.

fixture_main = (
    cq.Workplane("XY")
    .center(internal_wall_x_center - 10, -10) # Position in left room, near middle wall
    .box(15, 15, 25) # W, D, H
    .translate((0,0, 12.5 + wall_thickness))
)

fixture_low = (
    cq.Workplane("XY")
    .center(internal_wall_x_center - 10 + 7.5 + 4, -10 - 7.5 + 4) # Corner offset
    .box(8, 8, 12)
    .translate((0,0, 6 + wall_thickness))
)
# There is also a small boxy thing near the front left wall?
fixture_corner = (
    cq.Workplane("XY")
    .center(internal_wall_x_center - 10, -overall_width/2 + 10)
    .box(12, 12, 10)
    .translate((0,0, 5 + wall_thickness))
    # Hollow it out to look like the bin/box in image
    .faces("+Z").shell(-1)
)


# Combine all
result = structure.union(fixture_main).union(fixture_low).union(fixture_corner)

# Final check: the floor in the original extrusions was centered on Z=0, so it went from -1 to 1.
# The walls went from 0 to 40.
# Let's move everything so bottom is at Z=0
result = result.translate((0, 0, wall_thickness/2))
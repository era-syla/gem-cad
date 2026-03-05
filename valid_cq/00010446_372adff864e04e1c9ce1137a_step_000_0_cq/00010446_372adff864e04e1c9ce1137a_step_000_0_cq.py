import cadquery as cq

# --- Parametric Dimensions ---
height = 100.0
width_outer = 50.0
depth_outer = 25.0
thickness = 3.0
fillet_radius = 2.0

# Upper Window
window_width = 30.0
window_height = 35.0
window_top_offset = 10.0

# Grid of Small Holes
grid_hole_size = 3.0
grid_rows = 7
grid_cols = 5
grid_spacing_y = 6.0
grid_spacing_x = 6.0
grid_top_margin = 55.0  # Distance from top edge to top row of grid

# Bottom Larger Holes
bottom_hole_size = 5.0
bottom_hole_offset_y = 10.0 # From bottom edge
bottom_hole_spacing_x = 30.0 # Center to center

# --- Geometry Construction ---

# 1. Base U-Shape Profile
# Create a 2D U-profile and extrude it
base_profile = (
    cq.Workplane("XY")
    .rect(width_outer, depth_outer)
    .rect(width_outer - 2 * thickness, depth_outer - 2 * thickness) # Inner cutout rect (not U-shape yet)
)

# A cleaner way for a U-channel is to draw the profile explicitly or subtract a box
# Let's start with a solid block and shell it or cut the inside.
# Given the fillets on the front face, a shell approach or straight cuts works well.
# Let's try drawing the U-shape cross-section on the XZ plane (looking from top/bottom) 
# and extruding along Y (vertical height).

# Re-orienting thinking: X = width, Y = height, Z = depth
main_body = (
    cq.Workplane("XY")
    .box(width_outer, height, depth_outer)
)

# Create the inner cut to make it a U-channel
# We want to remove material from the "back" (or inside)
# Let's assume the face with holes is on +Z or -Z. Let's make face with holes on +Z (front).
# The cut needs to go from -Z face inwards, leaving 'thickness' wall.
cutout_width = width_outer - 2 * thickness
cutout_depth = depth_outer - thickness # Leave front wall thickness

main_body = (
    main_body
    .faces("<Z") # Select back face
    .workplane()
    .rect(cutout_width, height)
    .cutBlind(-cutout_depth) # Cut towards the front
)

# 2. Fillet the front vertical edges
# Based on the image, the outer vertical edges on the front face are rounded.
main_body = main_body.edges("|Y and >Z").fillet(fillet_radius)


# 3. Create the Top Large Window
# Select the front face
front_face = main_body.faces(">Z").workplane()

# Calculate center for window
# By default workplane center is (0,0). Top of the part is at Y = height/2.
window_center_y = (height / 2) - window_top_offset - (window_height / 2)

main_body = (
    front_face
    .center(0, window_center_y)
    .rect(window_width, window_height)
    .cutBlind(-thickness * 2) # Cut through front wall
)

# 4. Create the Grid of Small Holes
# We need to position the grid below the window.
# Reset workplane to front face
front_face = main_body.faces(">Z").workplane()

# Calculate starting position for grid
# Top row Y coordinate: Top of part - grid_top_margin
start_y = (height / 2) - grid_top_margin

# Grid logic: CadQuery's rarray creates a grid centered on the current workplane center.
# We need to move the center to the middle of our desired grid area.
grid_total_height = (grid_rows - 1) * grid_spacing_y
grid_center_y = start_y - (grid_total_height / 2)

main_body = (
    front_face
    .center(0, grid_center_y)
    .rarray(grid_spacing_x, grid_spacing_y, grid_cols, grid_rows)
    .rect(grid_hole_size, grid_hole_size)
    .cutBlind(-thickness * 2)
)

# 5. Create Bottom Mounting Holes
# Reset workplane
front_face = main_body.faces(">Z").workplane()

# Y position relative to bottom edge (which is at -height/2)
bottom_hole_y = (-height / 2) + bottom_hole_offset_y

main_body = (
    front_face
    .center(0, bottom_hole_y)
    .pushPoints([(-bottom_hole_spacing_x / 2, 0), (bottom_hole_spacing_x / 2, 0)])
    .rect(bottom_hole_size, bottom_hole_size)
    .cutBlind(-thickness * 2)
)

result = main_body
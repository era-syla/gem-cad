import cadquery as cq

# --- Parameters ---
# Overall Dimensions
base_length = 150.0
base_width = 100.0
base_height = 10.0

# Recess (Pocket) Parameters
recess_depth = 3.0
wall_thickness = 5.0  # Thickness of the side walls
front_back_margin = 5.0 # Margin at front and back for the recess start

# The raised platform/strip inside the recess
strip_width = 15.0
strip_height = 2.0  # Height relative to the recess floor
strip_offset_from_side = 10.0 # Distance from the left inner wall

# Hole Grid Parameters
hole_diameter = 3.0
hole_spacing_x = 8.0
hole_spacing_y = 8.0

# Upper ledge holes (left side in image)
upper_hole_dia = 3.0
upper_hole_spacing = 10.0

# --- Geometry Construction ---

# 1. Create the main base block
base = cq.Workplane("XY").box(base_length, base_width, base_height)

# 2. Define the recess area
# The recess seems to leave a wall on the left (in image orientation, let's call it 'top' or 'left') 
# and right, but maybe open or just walled on all sides. Looking closely, it has walls on left and right ends.
# Let's assume a uniform wall thickness for simplicity, but adjust based on the visual asymmetry.
# Visually: There's a thick ledge on the "left-back" side (with a row of holes) and a thinner wall on the "right-front".
# Let's orient the model so X is the long axis, Y is the short axis.

# Re-orienting based on image:
# Long axis = X
# Short axis = Y
# Left side (thick ledge) = +Y (or -Y depending on view). Let's say +Y is the back (thick ledge).

thick_ledge_width = 20.0 # The side with the single row of holes
thin_wall_width = 5.0    # The opposing side wall
end_wall_width = 5.0     # The walls at the ends of the long axis

recess_length = base_length - (2 * end_wall_width)
recess_width = base_width - thick_ledge_width - thin_wall_width

# Calculate center offset for the cut to position it correctly
# Center of base is (0,0). 
# We want the cut to be shifted towards the thin wall side to leave the thick ledge.
y_shift = (thick_ledge_width - thin_wall_width) / 2.0 * -1

# Create the main recess
result = base.faces(">Z").workplane().center(0, y_shift).rect(recess_length, recess_width).cutBlind(-recess_depth)

# 3. Create the internal raised strip
# It runs parallel to the long axis (X), inside the recess.
# It sits on the floor of the recess.
strip_length = recess_length - 10.0 # Slightly shorter than the recess
# Position: closer to the thick ledge.
strip_y_pos = (recess_width/2.0) - strip_width/2.0 - 5.0 # Offset from the 'back' inner wall
# Adjust relative to global coords
global_strip_y = y_shift + strip_y_pos

# We need to add material back, or cut less deep initially. 
# Simplest is to boss (extrude) up from the bottom of the recess.
recess_floor_z = (base_height/2.0) - recess_depth

result = (result.faces(">Z[1]") # Select the floor of the recess (usually the second highest Z face now)
          .workplane()
          .center(0, strip_y_pos) # Relative to the center of the face we selected (which is the recess floor center)
          .rect(strip_length, strip_width)
          .extrude(strip_height))

# 4. Create the main grid of holes in the recess
# We need to define the area for the grid. It covers the rest of the recess floor.
grid_start_x = -(recess_length / 2.0) + 10.0
grid_end_x = (recess_length / 2.0) - 10.0
grid_start_y = -(recess_width / 2.0) + 10.0
# The grid stops before the raised strip
grid_end_y = strip_y_pos - (strip_width/2.0) - 5.0

# Calculate number of holes
n_holes_x = int((grid_end_x - grid_start_x) / hole_spacing_x) + 1
n_holes_y = int((grid_end_y - grid_start_y) / hole_spacing_y) + 1

# Generate points for the grid
grid_points = []
# We need to coordinate relative to the center of the cut floor
cut_center_y_global = y_shift

for i in range(n_holes_x):
    for j in range(n_holes_y):
        # Calculate local coordinates within the recess area boundaries
        lx = grid_start_x + (i * hole_spacing_x)
        ly = grid_start_y + (j * hole_spacing_y)
        grid_points.append((lx, ly))

# Drill the grid holes
# We select the floor of the recess again. 
# Note: CadQuery topological selection can be tricky. >Z[1] gets the second highest face.
# Alternatively, we can just cut from the very top but start deeper.
# Let's use the workplane on the recess floor.
result = (result.faces(">Z[1]") 
          .workplane()
          .pushPoints(grid_points)
          .hole(hole_diameter, depth=5.0)) # Blind holes

# 5. Create the single row of holes on the thick ledge
# The thick ledge is at global Y positive (based on our shift logic earlier)
ledge_y_center = (base_width/2.0) - (thick_ledge_width/2.0)
ledge_x_start = -(base_length/2.0) + 15.0
ledge_x_end = (base_length/2.0) - 15.0

n_ledge_holes = int((ledge_x_end - ledge_x_start) / upper_hole_spacing) + 1
ledge_points = []
for i in range(n_ledge_holes):
    px = ledge_x_start + (i * upper_hole_spacing)
    ledge_points.append((px, ledge_y_center))

result = (result.faces(">Z[0]") # Select the very top face
          .workplane() # Reset origin to center of top face
          .pushPoints(ledge_points)
          .hole(upper_hole_dia, depth=5.0))

# Export or Render
if 'show_object' in globals():
    show_object(result)
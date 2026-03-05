import cadquery as cq

# --- Parametric Dimensions ---

# Overall plate dimensions
plate_width = 300.0  # Estimated length based on the number of holes
plate_height = 80.0  # Estimated height
plate_thickness = 3.0 # Estimated thickness

# Central slot details
slot_length = 150.0
slot_width = 12.0 # Width of the cutout itself
slot_corner_radius = slot_width / 2.0
slot_x_offset = 10.0 # Slight offset from true center based on image

# Large hole in slot
large_hole_diameter = 16.0 
# The large hole seems to be at the left end of the slot

# Grid/Hole pattern parameters
# Small holes
small_hole_diameter = 3.5

# Top and Bottom edge mounting holes
edge_hole_spacing_x = 40.0
edge_hole_margin_y = 5.0 # From top/bottom edge

# Corner clusters (3x2 pattern)
corner_hole_pitch = 8.0 # spacing between holes in cluster

# Central grid inside/near the slot
grid_hole_pitch = 8.0

# --- Helper Functions ---

def create_corner_cluster(workplane, x_start, y_start, x_dir, y_dir):
    """Creates a 3x2 grid of points for corner holes."""
    pts = []
    for r in range(2): # 2 rows
        for c in range(3): # 3 columns
            px = x_start + (c * corner_hole_pitch * x_dir)
            py = y_start + (r * corner_hole_pitch * y_dir)
            pts.append((px, py))
    return pts

# --- Modeling ---

# 1. Base Plate
result = cq.Workplane("XY").box(plate_width, plate_height, plate_thickness)

# 2. Main Slot Cutout
# Creating the long rounded slot in the upper-middle area
result = (result.faces(">Z").workplane()
          .center(slot_x_offset, 15.0) # Shifted slightly right and up
          .slot2D(slot_length, slot_width)
          .cutThruAll())

# 3. Large Hole at the start of the slot area
# Looks like a bearing fit or cable pass-through at the left end of the slot feature
slot_left_x = slot_x_offset - (slot_length/2)
result = (result.faces(">Z").workplane()
          .center(slot_left_x, 15.0)
          .circle(large_hole_diameter / 2)
          .cutThruAll())

# 4. Patterned Holes - Central Grid (inside the slot area mostly, but looks like a separate strip)
# Looking closely, there are two rows of holes running parallel to the slot.
# Let's approximate this as a linear grid.
grid_pts = []
num_cols = 25 # approximate count
num_rows = 2
start_x = slot_left_x + 20
start_y = 15.0 - (grid_hole_pitch/2)

for r in range(num_rows):
    for c in range(num_cols):
        px = start_x + (c * grid_hole_pitch)
        py = start_y + (r * grid_hole_pitch)
        # Shift slightly to align with the visual
        py -= grid_hole_pitch/2
        grid_pts.append((px, py))

result = (result.faces(">Z").workplane()
          .pushPoints(grid_pts)
          .circle(small_hole_diameter / 2)
          .cutThruAll())

# 5. Corner Hole Clusters (3x2 grids)
# Top Left
tl_pts = create_corner_cluster(None, -plate_width/2 + 10, plate_height/2 - 10, 1, -1)
# Top Right
tr_pts = create_corner_cluster(None, plate_width/2 - 10, plate_height/2 - 10, -1, -1)
# Bottom Left
bl_pts = create_corner_cluster(None, -plate_width/2 + 10, -plate_height/2 + 10, 1, 1)
# Bottom Right
br_pts = create_corner_cluster(None, plate_width/2 - 10, -plate_height/2 + 10, -1, 1)

all_corner_pts = tl_pts + tr_pts + bl_pts + br_pts

result = (result.faces(">Z").workplane()
          .pushPoints(all_corner_pts)
          .circle(small_hole_diameter / 2)
          .cutThruAll())

# 6. Additional Distributed Mounting Holes
# There are single holes spaced along the top and bottom edges
distributed_pts = []

# Top row singles
distributed_pts.append((-50, plate_height/2 - 10))
distributed_pts.append((50, plate_height/2 - 10))

# Bottom row singles
distributed_pts.append((-80, -plate_height/2 + 10))
distributed_pts.append((0, -plate_height/2 + 10))
distributed_pts.append((80, -plate_height/2 + 10))

# Mid-section extra clusters (middle-ish area)
# There is a small cluster below the slot near the center
mid_cluster_pts = create_corner_cluster(None, 20, -15, 1, 1) # 3x2 cluster in middle
all_mid_pts = distributed_pts + mid_cluster_pts

result = (result.faces(">Z").workplane()
          .pushPoints(all_mid_pts)
          .circle(small_hole_diameter / 2)
          .cutThruAll())

# 7. Fillet the outer corners
result = result.edges("|Z").fillet(2.0)
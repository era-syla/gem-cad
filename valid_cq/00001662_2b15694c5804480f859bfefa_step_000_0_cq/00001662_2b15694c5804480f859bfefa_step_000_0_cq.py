import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions of the box
box_width = 120.0
box_depth = 80.0
front_height = 40.0
back_height = 60.0
wall_thickness = 3.0  # Assumed thickness for shell/internal
fillet_radius = 2.0   # For vertical edges and top face edges

# Perforation details (front face)
hole_diameter = 2.0
hole_spacing_x = 4.0
hole_spacing_y = 4.0
# Define the area for the holes
perf_margin_x = 5.0
perf_margin_y = 5.0

# Central Slot/Connector cutout details
slot_width = 80.0
slot_height = 8.0
slot_corner_radius = slot_height / 2.0
slot_y_offset = 0.0 # Vertical offset from center of front face

# --- Geometry Construction ---

# 1. Create the base Wedge Shape
# We will sketch the side profile and extrude it.
# The profile is a trapezoid.

# Points for the side profile (on YZ plane, extrude along X)
# Origin is at the bottom-front-left corner for convenience, then moved to center
pts = [
    (0, 0),                 # Bottom front
    (box_depth, 0),         # Bottom back
    (box_depth, back_height), # Top back
    (0, front_height)       # Top front
]

# Create the main solid block
main_body = (
    cq.Workplane("YZ")
    .polyline(pts)
    .close()
    .extrude(box_width)
    # Center the object on the origin for easier symmetry operations
    .translate((-box_width/2, -box_depth/2, 0))
    # Rotate to orient Z-up (original sketch was YZ plane, extruded X)
    # After extrude X, dimensions are: X=width, Y=depth, Z=height? No.
    # Workplane YZ extrude -> X axis is extrusion.
    # Let's re-orient carefully.
    .rotate((0,0,0), (0,1,0), -90) # Rotate to put X along Width, Y along Depth
    .rotate((0,0,0), (0,0,1), -90)
)

# Re-centering properly after rotations
# Bounding box logic helps, but let's just use the known dimensions to center it
# Current Center approx: (0, 0, height_avg/2)
main_body = main_body.translate((0, 0, 0))

# 2. Apply Fillets
# Fillet the vertical edges and the top edges.
# We select edges carefully. The "front" face is now facing -Y (based on typical orientation) or +Y depending on rotation.
# Let's inspect coordinates:
# Width is along X. Depth is along Y. Height is along Z.
main_body = main_body.edges("|Z").fillet(fillet_radius)

# Fillet the top perimeter loop.
# Select the top face (which is slanted) and fillet its edges.
# The top face is the one with the highest Z average or normal with +Z component.
top_face = main_body.faces("+Z").val()
main_body = main_body.faces("+Z").edges().fillet(fillet_radius)


# 3. Create the Front Face Features (Perforations and Slot)
# The front face is the one with the smaller height (front_height).
# Based on the wedge profile points: (0, front_height) and (0,0) were the front.
# In the extruded object, this corresponds to the face at -Y or +Y depending on the earlier setup.
# Let's assume the face at -Y (depth/2) is the front.
front_workplane = main_body.faces("<Y").workplane()

# A. Create the central slot
# Draw a slot and cut it
main_body = (
    front_workplane
    .center(0, slot_y_offset)
    .slot2D(slot_width, slot_height)
    .cutThruAll()
)

# B. Create the grid of holes
# We need to calculate how many holes fit
# Available width for holes
avail_w = box_width - (2 * perf_margin_x)
avail_h = front_height - (2 * perf_margin_y)

cols = int(avail_w // hole_spacing_x)
rows = int(avail_h // hole_spacing_y)

# We need to exclude the area where the slot is.
# Strategy: Generate points for the whole grid, then filter out points that fall inside the slot bounding box.

# Generate grid points centered on the face
grid_pts = []
slot_exclusion_width = slot_width + 4.0 # Add margin around slot
slot_exclusion_height = slot_height + 4.0

for r in range(rows):
    y_pos = -avail_h/2 + r * hole_spacing_y + (hole_spacing_y/2 if rows % 2 == 0 else 0)
    for c in range(cols):
        x_pos = -avail_w/2 + c * hole_spacing_x + (hole_spacing_x/2 if cols % 2 == 0 else 0)
        
        # Check if point is within the slot exclusion zone
        # Slot is centered at (0, slot_y_offset)
        if (abs(x_pos) < slot_exclusion_width / 2) and (abs(y_pos - slot_y_offset) < slot_exclusion_height / 2):
            continue # Skip this point
            
        grid_pts.append((x_pos, y_pos))

# Perform the hole cut operation
# We use the previous workplane
result = (
    main_body.faces("<Y").workplane()
    .pushPoints(grid_pts)
    .circle(hole_diameter / 2)
    .cutThruAll()
)

# Optional: Shelling the inside if this is an enclosure
# Not strictly requested, but makes it a realistic part.
# Removing the bottom face or back face? Usually bottom.
# result = result.faces("<Z").shell(-wall_thickness)

# For the visual match, the solid block with holes is sufficient.
# The image shows a solid-looking front, so cutThruAll suggests the holes go into the void.

# Export or Render
if 'show_object' in globals():
    show_object(result)
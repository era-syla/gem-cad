import cadquery as cq

# --- Parametric Variables ---
# Bed/Frame dimensions
bed_width = 220
bed_depth = 220
bed_thickness = 4
frame_thickness = 6  # Thickness of the Y-carriage plate

# Y-carriage plate (the horizontal one)
y_plate_width = 240
y_plate_depth = 240
y_plate_cutout_width = 150
y_plate_cutout_depth = 150
y_plate_fillet_radius = 5

# Vertical Plate (the Z-axis mount)
z_plate_width = 120
z_plate_height = 120
z_plate_thickness = 6

# Motor/Mount block dimensions
motor_block_size = 42  # NEMA 17 size
motor_length = 40
mount_extension = 20

# --- Helper Functions ---
def create_plate(width, depth, thickness, fillet_r):
    """Creates a basic rectangular plate with filleted corners."""
    plate = (
        cq.Workplane("XY")
        .rect(width, depth)
        .extrude(thickness)
        .edges("|Z")
        .fillet(fillet_r)
    )
    return plate

# --- Construction of Parts ---

# 1. Horizontal Y-Carriage Plate
# Basic shape is a large square with a large central cutout
y_plate = (
    cq.Workplane("XY")
    .rect(y_plate_width, y_plate_depth)
    .extrude(frame_thickness)
    .edges("|Z").fillet(y_plate_fillet_radius)
)

# Create the large central cutout
cutout = (
    cq.Workplane("XY")
    .rect(y_plate_cutout_width, y_plate_cutout_depth)
    .extrude(frame_thickness)
)

# Specific irregular cutout shape for the motor area on the left side
# Approximating the "stepped" cutout shape seen in the image
left_cutout_sketch = (
    cq.Workplane("XY")
    .moveTo(-y_plate_cutout_width/2, 0)
    .lineTo(-y_plate_width/2 + 20, 0) # Start from inner edge
    .lineTo(-y_plate_width/2 + 20, 40)
    .lineTo(-y_plate_cutout_width/2 - 20, 40)
    .lineTo(-y_plate_cutout_width/2 - 20, 60)
    .lineTo(-y_plate_cutout_width/2, 60)
    .close()
    .extrude(frame_thickness)
)

y_plate = y_plate.cut(cutout).cut(left_cutout_sketch)

# Add mounting holes to the Y-plate
# Corner holes
y_plate = (
    y_plate.faces(">Z")
    .workplane()
    .rect(y_plate_width - 20, y_plate_depth - 20, forConstruction=True)
    .vertices()
    .hole(3.5) # M3 screw holes
)

# Mid-span holes
y_plate = (
    y_plate.faces(">Z")
    .workplane()
    .rect(y_plate_width - 20, 0, forConstruction=True) # Holes along X axis edges
    .vertices()
    .hole(3.5)
)


# 2. Vertical Z-Axis Mounting Plate
# This plate is perpendicular to the Y-plate
z_plate = (
    cq.Workplane("XZ")
    .rect(z_plate_width, z_plate_height)
    .extrude(z_plate_thickness)
    .edges("|Y").fillet(3)
)

# Complex geometry for the Z-plate (cutouts and motor mount holes)
# Center cutout for coupling
z_center_hole = (
    cq.Workplane("XZ")
    .circle(15)
    .extrude(z_plate_thickness)
)

# Motor mounting holes (NEMA 17 spacing is 31mm)
z_motor_holes = (
    cq.Workplane("XZ")
    .rect(31, 31, forConstruction=True)
    .vertices()
    .circle(1.75) # M3 radius
    .extrude(z_plate_thickness)
)

# Structural cutouts to reduce weight (triangular/polygonal shapes)
# Top Right
cutout_tr = (
    cq.Workplane("XZ")
    .moveTo(10, 10)
    .lineTo(z_plate_width/2 - 10, 10)
    .lineTo(z_plate_width/2 - 10, z_plate_height/2 - 10)
    .close()
    .extrude(z_plate_thickness)
)
# Top Left
cutout_tl = (
    cq.Workplane("XZ")
    .moveTo(-10, 10)
    .lineTo(-z_plate_width/2 + 10, 10)
    .lineTo(-z_plate_width/2 + 10, z_plate_height/2 - 10)
    .close()
    .extrude(z_plate_thickness)
)
# Bottom Right
cutout_br = (
    cq.Workplane("XZ")
    .moveTo(10, -10)
    .lineTo(z_plate_width/2 - 10, -10)
    .lineTo(z_plate_width/2 - 10, -z_plate_height/2 + 10)
    .close()
    .extrude(z_plate_thickness)
)
# Bottom Left
cutout_bl = (
    cq.Workplane("XZ")
    .moveTo(-10, -10)
    .lineTo(-z_plate_width/2 + 10, -10)
    .lineTo(-z_plate_width/2 + 10, -z_plate_height/2 + 10)
    .close()
    .extrude(z_plate_thickness)
)

z_plate = z_plate.cut(z_center_hole).cut(z_motor_holes)
z_plate = z_plate.cut(cutout_tr).cut(cutout_tl).cut(cutout_br).cut(cutout_bl)

# Position the Z-plate relative to the Y-plate
# It sits on the edge of the irregular cutout we made earlier
z_plate_offset_x = -y_plate_width/2 + 40 # Position roughly where the mount is
z_plate_offset_y = 0
z_plate_offset_z = z_plate_height/2 - 20 # Lifted up

z_plate_positioned = z_plate.translate((z_plate_offset_x, z_plate_offset_y, z_plate_offset_z))


# 3. Connection Block / Motor Housing
# This connects the vertical plate to the horizontal frame
# It looks like a complex block housing bearings or lead nuts.

block_width = 40
block_height = 40
block_depth = 40

connector_block = (
    cq.Workplane("XY")
    .rect(block_width, block_depth)
    .extrude(block_height)
)

# Add a bore for a linear bearing
bearing_bore = (
    cq.Workplane("XY")
    .circle(10) # 20mm diameter bearing
    .extrude(block_height)
)

# Add slot for clamping
clamp_slot = (
    cq.Workplane("XY")
    .rect(2, block_depth)
    .extrude(block_height)
    .translate((10, 0, 0)) # Offset slot
)

# Machining details on the block
connector_block = connector_block.cut(bearing_bore).cut(clamp_slot)

# Add perpendicular mounting tabs
tab_geometry = (
    cq.Workplane("YZ")
    .moveTo(0,0)
    .lineTo(20, 0)
    .lineTo(0, 20)
    .close()
    .extrude(10)
    .rotate((0,0,0), (1,0,0), -90)
    .translate((-block_width/2 - 5, block_depth/2, 5))
)

connector_block = connector_block.union(tab_geometry)

# Position the connector block against the Z-plate
block_pos_x = z_plate_offset_x + z_plate_thickness/2 + block_width/2
block_pos_z = z_plate_offset_z
connector_block_positioned = connector_block.translate((block_pos_x, 0, 0))


# 4. Triangular Gussets / Brackets
# These reinforce the connection between the Z-plate and the connector block
gusset = (
    cq.Workplane("XY")
    .moveTo(0,0)
    .lineTo(20, 0)
    .lineTo(0, 20)
    .close()
    .extrude(4)
    .rotate((0,0,0), (1,0,0), 90) # Stand upright
)

gusset1 = gusset.translate((z_plate_offset_x + 5, 25, 0))
gusset2 = gusset.translate((z_plate_offset_x + 5, -25, 0))


# --- Assembly ---

# Combine Y-plate
result = y_plate

# Add Z-plate
result = result.union(z_plate_positioned)

# Add Connector Block
result = result.union(connector_block_positioned)

# Add Gussets
result = result.union(gusset1).union(gusset2)

# Add the small tensioner/screw detail on the front right corner of the Y-plate
tensioner_boss = (
    cq.Workplane("YZ")
    .circle(4)
    .extrude(15)
    .translate((y_plate_width/2 + 7.5, -y_plate_depth/2 + 20, frame_thickness/2))
)
result = result.union(tensioner_boss)

# Final cleanup / Fillets on union edges where reasonable (optional, computationally expensive)
# result = result.edges("|Z").fillet(1) 

# Export/Render
# show_object(result) # Used in CQ-editor
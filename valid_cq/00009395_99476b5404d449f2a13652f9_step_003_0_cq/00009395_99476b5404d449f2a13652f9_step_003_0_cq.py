import cadquery as cq

# --- Parameters ---

# Overall Chassis Dimensions
chassis_width = 80.0
chassis_height = 120.0
chassis_depth = 60.0
wall_thickness = 1.5

# Top I/O Panel
top_panel_depth = 40.0
top_panel_overhang = 5.0  # How much it sticks out front

# Fan Cutout
fan_diameter = 75.0
fan_center_z = -20.0  # Relative to center of vertical face

# Bottom Mesh/Shelf
shelf_depth = 50.0
shelf_z_pos = -40.0

# --- Geometry Construction ---

# 1. Main U-Shaped Chassis Body
# Create the base U-profile sketch
u_profile = (
    cq.Workplane("XY")
    .rect(chassis_width, chassis_depth)
    .extrude(chassis_height)
    # Shelling to create the U-shape (removing front, top, bottom for now, then refining)
    # Actually, simpler to build wall by wall for this complex shape
)

# Alternative approach: Build the back and side walls
back_wall = (
    cq.Workplane("XZ")
    .workplane(offset=-chassis_depth/2)
    .rect(chassis_width, chassis_height)
    .extrude(wall_thickness)
)

left_wall = (
    cq.Workplane("YZ")
    .workplane(offset=-chassis_width/2)
    .rect(chassis_depth, chassis_height)
    .extrude(wall_thickness)
    .translate((wall_thickness/2, 0, 0)) # Adjust for centering
)

right_wall = (
    cq.Workplane("YZ")
    .workplane(offset=chassis_width/2)
    .rect(chassis_depth, chassis_height)
    .extrude(-wall_thickness)
    .translate((-wall_thickness/2, 0, 0))
)

# Combine basic chassis walls
chassis = back_wall.union(left_wall).union(right_wall)


# 2. Top I/O Panel
top_panel = (
    cq.Workplane("XY")
    .workplane(offset=chassis_height/2 - wall_thickness)
    .center(0, top_panel_overhang/2)
    .rect(chassis_width, top_panel_depth + top_panel_overhang)
    .extrude(wall_thickness)
)

# Cutouts for IO ports on the top panel
# Creating a dummy shape to cut
io_cutouts = (
    cq.Workplane("XY")
    .workplane(offset=chassis_height/2 - wall_thickness)
    # Slot 1 (long)
    .center(0, 5)
    .rect(50, 8)
    # Slot 2 (smaller with notches - simplified here)
    .center(0, -15)
    .rect(45, 6)
    # RJ45-ish port
    .center(-28, 15)
    .rect(12, 12)
    .extrude(wall_thickness * 2)
)

top_panel = top_panel.cut(io_cutouts)

# Add side details to top panel (bent tabs)
top_side_tab_l = (
    cq.Workplane("YZ")
    .workplane(offset=-chassis_width/2)
    .center(top_panel_overhang/2, chassis_height/2 - 5)
    .rect(top_panel_depth, 10)
    .extrude(wall_thickness)
)
top_side_tab_r = (
    cq.Workplane("YZ")
    .workplane(offset=chassis_width/2)
    .center(top_panel_overhang/2, chassis_height/2 - 5)
    .rect(top_panel_depth, 10)
    .extrude(-wall_thickness)
)

chassis = chassis.union(top_panel).union(top_side_tab_l).union(top_side_tab_r)


# 3. Fan Mount Area (Front Face Plate)
# This sits between the side walls
fan_plate_height = 90.0
fan_plate = (
    cq.Workplane("XZ")
    .workplane(offset=chassis_depth/2 - wall_thickness) # Front of the box
    .center(0, -10)
    .rect(chassis_width - 2*wall_thickness, fan_plate_height)
    .extrude(-wall_thickness)
)

# Fan Cutout and screw holes
fan_cutout = (
    cq.Workplane("XZ")
    .workplane(offset=chassis_depth/2 + 5) # Start cut from in front
    .center(0, fan_center_z)
    .circle(fan_diameter/2)
    .extrude(-50)
)

# Add fan "spokes" or structure (simplified representation of the fan grill)
spoke_w = 4
spoke_h = fan_diameter
v_spoke = (
    cq.Workplane("XZ")
    .workplane(offset=chassis_depth/2 - wall_thickness)
    .center(0, fan_center_z)
    .rect(spoke_w, spoke_h)
    .extrude(-wall_thickness)
)
h_spoke = (
    cq.Workplane("XZ")
    .workplane(offset=chassis_depth/2 - wall_thickness)
    .center(0, fan_center_z)
    .rect(spoke_h, spoke_w)
    .extrude(-wall_thickness)
)
# Intersect spokes with the circular hole area so they only exist inside
fan_grill = v_spoke.union(h_spoke).intersect(
     cq.Workplane("XZ").workplane(offset=chassis_depth/2).center(0, fan_center_z).circle(fan_diameter/2).extrude(-10)
)

# Apply cut to plate, then add grill back
fan_plate = fan_plate.cut(fan_cutout).union(fan_grill)

# Add mounting ears for the fan (rounded tabs at corners)
mount_hole_spacing = 60.0
mount_ears = cq.Workplane("XZ").workplane(offset=chassis_depth/2 - wall_thickness)

for x in [-1, 1]:
    for y in [-1, 1]:
        ear = (
            cq.Workplane("XZ")
            .workplane(offset=chassis_depth/2 - wall_thickness)
            .center(x * mount_hole_spacing/2, fan_center_z + y * mount_hole_spacing/2)
            .circle(6)
            .extrude(-wall_thickness)
        )
        hole = (
             cq.Workplane("XZ")
            .workplane(offset=chassis_depth/2 + 1)
            .center(x * mount_hole_spacing/2, fan_center_z + y * mount_hole_spacing/2)
            .circle(2.5)
            .extrude(-20)
        )
        fan_plate = fan_plate.union(ear).cut(hole)


chassis = chassis.union(fan_plate)

# 4. Bottom Mesh Shelf
# This protrudes outwards
shelf = (
    cq.Workplane("XY")
    .workplane(offset=shelf_z_pos)
    .center(0, chassis_depth/2 + shelf_depth/2 - wall_thickness)
    .rect(chassis_width - 4, shelf_depth)
    .extrude(wall_thickness)
)

# Create the Hex Mesh pattern
# Creating a single hex and replicating is expensive, let's make a grid of holes
# To save computation time for this example, we'll use a rect grid of small circles
mesh_rect = (
    cq.Workplane("XY")
    .workplane(offset=shelf_z_pos)
    .center(0, chassis_depth/2 + shelf_depth/2 - wall_thickness)
    .rarray(3, 3, 20, 12) # x_spacing, y_spacing, x_count, y_count
    .circle(1.0)
    .extrude(wall_thickness * 2)
)

# Cutouts in the shelf (the larger squares)
shelf_cutouts = (
    cq.Workplane("XY")
    .workplane(offset=shelf_z_pos)
    .center(15, chassis_depth/2 + shelf_depth/2 - wall_thickness)
    .rect(15, 15)
    .center(-30, 0)
    .rect(10, 10)
    .extrude(wall_thickness * 2)
)

shelf = shelf.cut(mesh_rect).cut(shelf_cutouts)

# Side rails for the shelf
shelf_rail_l = (
    cq.Workplane("YZ")
    .workplane(offset=-chassis_width/2 + 2)
    .center(chassis_depth/2 + shelf_depth/2 - wall_thickness, shelf_z_pos + 5)
    .rect(shelf_depth, 10)
    .extrude(wall_thickness)
)
shelf_rail_r = (
    cq.Workplane("YZ")
    .workplane(offset=chassis_width/2 - 2 - wall_thickness)
    .center(chassis_depth/2 + shelf_depth/2 - wall_thickness, shelf_z_pos + 5)
    .rect(shelf_depth, 10)
    .extrude(wall_thickness)
)


chassis = chassis.union(shelf).union(shelf_rail_l).union(shelf_rail_r)


# 5. Side wall detailing (Indentations/Rails)
# Indentation on left wall
left_indent = (
    cq.Workplane("YZ")
    .workplane(offset=-chassis_width/2 - 1)
    .center(0, 0)
    .rect(chassis_depth/2, chassis_height + 10) # Vertical strip
    .extrude(wall_thickness * 2)
)
# We won't cut the whole wall, just create a rail effect by adding material inside
left_rail = (
    cq.Workplane("YZ")
    .workplane(offset=-chassis_width/2 + wall_thickness)
    .center(-10, 0)
    .rect(10, chassis_height - 10)
    .extrude(2)
)
chassis = chassis.union(left_rail)


# 6. Bottom Hinge/Tab detail
bottom_tab = (
    cq.Workplane("XZ")
    .workplane(offset=chassis_depth/2 - wall_thickness)
    .center(-chassis_width/2 + 5, -chassis_height/2)
    .circle(5)
    .extrude(-wall_thickness)
)
bottom_tab_hole = (
    cq.Workplane("XZ")
    .workplane(offset=chassis_depth/2 + 1)
    .center(-chassis_width/2 + 5, -chassis_height/2)
    .circle(2)
    .extrude(-20)
)
chassis = chassis.union(bottom_tab).cut(bottom_tab_hole)


# Final fillets to make it look manufactured
try:
    # Selective filleting to avoid kernel errors on complex intersections
    chassis = chassis.edges("|Z").filter_by(lambda e: e.boundingBox().min.z > -chassis_height/2 + 10).fillet(0.5)
except:
    pass # Fallback if fillet fails

result = chassis
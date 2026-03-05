import cadquery as cq

# --- Parametric Dimensions ---
# Main Conveyor Width (X direction of the main block)
width = 200.0

# Roller dimensions
roller_diam = 40.0
roller_length = width + 20.0  # Slightly wider than the frame

# Frame / Bed dimensions
bed_thickness = 10.0
bed_length = 80.0  # Distance from roller to front
front_lip_height = 20.0
front_lip_thickness = 8.0
side_wall_height = 30.0
side_wall_thickness = 10.0

# Mesh (grating) simulation parameters
# Creating actual mesh is computationally expensive and complex for a single solid.
# We will represent it as a solid plate with a grid of holes to simulate the look.
mesh_plate_thickness = 2.0
mesh_hole_size = 3.0
mesh_spacing = 5.0

# Support structure
support_arm_thickness = 10.0
support_arm_depth = 40.0 # Vertical drop

# --- Geometry Construction ---

# 1. The Roller
# Aligned along the X axis
roller = cq.Workplane("YZ").circle(roller_diam / 2).extrude(roller_length)
roller = roller.translate((-(roller_length - width)/2, 0, 0)) # Center it roughly

# 2. The Mesh Bed (represented as a plate connecting roller to front frame)
# It slopes down slightly or is flat. Let's make it flat for simplicity, tangent to roller top.
mesh_z_level = 0
mesh_start_y = 0  # Center of roller
mesh_end_y = -bed_length

mesh_plate = (
    cq.Workplane("XY")
    .workplane(offset=mesh_z_level)
    .center(width/2, (mesh_start_y + mesh_end_y)/2)
    .box(width, abs(mesh_start_y - mesh_end_y), mesh_plate_thickness)
)

# Create the grid pattern (holes) to simulate mesh
# Note: Doing a full grid cut can be slow. We will do a simplified version or just the plate 
# depending on complexity requirements. Let's do a simplified pattern.
# For robust code generation without timeouts, I'll create the plate and cut a few slots or 
# just leave it as a solid plate that represents the mesh area. 
# Looking at the image, it's a wire mesh. A solid plate is the best CAD approximation for a 
# base model unless specifically generating STL.
# Let's cut a few large rectangular pockets to suggest openness instead of 1000s of tiny holes.
mesh_cutout_width = (width / 4) - 5
mesh_cutout_length = (abs(mesh_start_y - mesh_end_y)) - 10

mesh_plate = (
    mesh_plate.faces(">Z").workplane()
    .rarray(width/4, 1, 4, 1) # distribute cutouts
    .rect(mesh_cutout_width, mesh_cutout_length)
    .cutThruAll()
)

# 3. The Front Frame Assembly
# This consists of a transverse beam and side walls.

# Transverse beam (the bottom part of the front section)
beam_y_pos = mesh_end_y - side_wall_thickness/2
beam = (
    cq.Workplane("XY")
    .workplane(offset=mesh_z_level - bed_thickness)
    .center(width/2, beam_y_pos)
    .box(width, side_wall_thickness * 3, bed_thickness)
)

# Angled front plate (ramp)
ramp_length = 30.0
ramp_angle = 45.0
ramp = (
    cq.Workplane("XY")
    .workplane(offset=mesh_z_level)
    .center(width/2, mesh_end_y)
    .box(width, 10, mesh_plate_thickness) # Small transition piece
)

# The L-shaped or U-shaped collection trough at the front
trough_base_y = beam_y_pos - 20
trough_floor = (
    cq.Workplane("XY")
    .workplane(offset=mesh_z_level - bed_thickness)
    .center(width/2, trough_base_y)
    .box(width, 40, bed_thickness)
)

front_wall = (
    cq.Workplane("XZ")
    .workplane(offset=-trough_base_y - 20)
    .center(width/2, mesh_z_level - bed_thickness + front_lip_height/2)
    .box(width, front_lip_thickness, front_lip_height)
)

# Side Walls at the front
left_wall = (
    cq.Workplane("YZ")
    .workplane(offset=0)
    .center(trough_base_y, mesh_z_level + side_wall_height/2 - bed_thickness)
    .box(60, side_wall_height, side_wall_thickness)
)

right_wall = (
    cq.Workplane("YZ")
    .workplane(offset=width - side_wall_thickness)
    .center(trough_base_y, mesh_z_level + side_wall_height/2 - bed_thickness)
    .box(60, side_wall_height, side_wall_thickness)
)

# 4. Connecting Arms (connecting roller axle area to the frame)
# Left Arm
arm_length = abs(mesh_end_y)
left_arm = (
    cq.Workplane("YZ")
    .center(mesh_end_y/2, -15)
    .box(arm_length, 10, 5)
    .translate((5,0,0)) # Offset slightly from edge
)

# Right Arm
right_arm = (
    cq.Workplane("YZ")
    .center(mesh_end_y/2, -15)
    .box(arm_length, 10, 5)
    .translate((width - 5 - 5,0,0))
)

# Vertical supports under the front
left_leg = (
    cq.Workplane("YZ")
    .center(trough_base_y, -25)
    .box(40, 40, side_wall_thickness)
    .translate((0,0,0))
)

right_leg = (
    cq.Workplane("YZ")
    .center(trough_base_y, -25)
    .box(40, 40, side_wall_thickness)
    .translate((width - side_wall_thickness,0,0))
)


# --- Combine All Parts ---

result = (
    roller
    .union(mesh_plate)
    .union(beam)
    .union(trough_floor)
    .union(front_wall)
    .union(left_wall)
    .union(right_wall)
    .union(left_arm)
    .union(right_arm)
    .union(left_leg)
    .union(right_leg)
)

# Rotate to match the isometric view orientation roughly
result = result.rotate((0,0,0), (1,0,0), -90) 
result = result.rotate((0,0,0), (0,0,1), 180) 
result = result.translate((-width/2, 0, 50))
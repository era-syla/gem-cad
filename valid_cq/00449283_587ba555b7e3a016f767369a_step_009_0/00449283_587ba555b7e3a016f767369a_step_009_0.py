import cadquery as cq

# --- Dimensions & Parameters ---
# Housing
housing_depth = 40.0
housing_main_width = 45.0
housing_main_height = 30.0
housing_step_width = 15.0
housing_step_height = 12.0

# Features on Front Face
sq_hole_size = 3.5
sq_hole_z = 22.0
sq_hole_y_start = 10.0
sq_hole_spacing = 8.0

top_pipe_diam = 8.0
top_pipe_len = 45.0
top_pipe_y = 36.0
top_pipe_z = 22.0

# Curved Pipes Array
num_pipes = 4
pipe_od = 6.0
pipe_spacing = 10.0
pipe_z_level = 8.0
pipe_y_start = 9.0  # Y position of the first (innermost) pipe
pipe_straight_len = 15.0
pipe_inner_bend_radius = 20.0
pipe_exit_len = 30.0  # Length after the bend
sleeve_od_offset = 1.0  # Extra diameter for the connector sleeve
sleeve_len = 10.0

# --- Geometry Construction ---

# 1. Create Housing Body
# We build the housing so the front face is at X=0, extending into negative X.
# Main block (holds the features)
main_body = (
    cq.Workplane("XY")
    .box(housing_depth, housing_main_width, housing_main_height, centered=(False, False, False))
    .translate((-housing_depth, 0, 0))
)

# Step block (flange at the back/side)
# Attached to the -Y side of the main block
step_body = (
    cq.Workplane("XY")
    .box(housing_depth, housing_step_width, housing_step_height, centered=(False, False, False))
    .translate((-housing_depth, -housing_step_width, 0))
)

housing = main_body.union(step_body)

# 2. Cut Square Holes
housing = (
    housing.faces(">X").workplane()
    .moveTo(sq_hole_y_start, sq_hole_z)
    .rect(sq_hole_size, sq_hole_size)
    .moveTo(sq_hole_y_start + sq_hole_spacing, sq_hole_z)
    .rect(sq_hole_size, sq_hole_size)
    .cutBlind(-15.0)
)

# 3. Create Top Straight Pipe
top_pipe = (
    cq.Workplane("YZ").workplane(offset=0)
    .moveTo(top_pipe_y, top_pipe_z)
    .circle(top_pipe_diam / 2.0)
    .extrude(top_pipe_len)
)

result = housing.union(top_pipe)

# 4. Create Curved Pipes Array
for i in range(num_pipes):
    # Calculate position and radius for concentric bends
    y_pos = pipe_y_start + (i * pipe_spacing)
    # The radius increases by the pitch to keep pipes parallel
    bend_radius = pipe_inner_bend_radius + (i * pipe_spacing)
    
    # Define the sweep path
    # 1. Start at the face (X=0)
    # 2. Straight segment
    # 3. 90-degree turn towards -Y (Right relative to X view)
    # 4. Straight extension after bend
    path = (
        cq.Workplane("XY").workplane(offset=pipe_z_level)
        .moveTo(0, y_pos)
        .lineTo(pipe_straight_len, y_pos)
        .tangentArcPoint((bend_radius, -bend_radius)) # Turns -90 deg
        .line(0, -pipe_exit_len) # Extend in -Y direction
    )
    
    # Create the pipe solid
    pipe = (
        cq.Workplane("YZ").workplane(offset=0)
        .moveTo(y_pos, pipe_z_level)
        .circle(pipe_od / 2.0)
        .sweep(path)
    )
    
    # Create the connector sleeve (thicker section at base)
    sleeve = (
        cq.Workplane("YZ").workplane(offset=0)
        .moveTo(y_pos, pipe_z_level)
        .circle((pipe_od / 2.0) + (sleeve_od_offset / 2.0))
        .extrude(sleeve_len)
    )
    
    result = result.union(pipe).union(sleeve)

# 'result' now contains the complete model
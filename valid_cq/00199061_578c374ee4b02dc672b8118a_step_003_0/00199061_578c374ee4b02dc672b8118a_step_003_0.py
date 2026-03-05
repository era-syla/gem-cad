import cadquery as cq

# Dimensions
frame_width = 32.0
frame_height = 24.0
thickness = 4.0
rim_width = 3.5
fillet_radius = 2.0
notch_width = 5.0
notch_depth = 1.0

# Array Parameters
arc_radius = 100.0
num_frames = 5
total_angle = 60.0  # Degrees

def create_master_frame():
    # Define frame on YZ plane so its normal aligns with X axis (Radial in array)
    
    # 1. Create the main body
    outer = (
        cq.Workplane("YZ")
        .rect(frame_width, frame_height)
        .extrude(thickness)
        .edges("|X")
        .fillet(fillet_radius)
    )
    
    # 2. Create the inner cutout
    inner_w = frame_width - 2 * rim_width
    inner_h = frame_height - 2 * rim_width
    # Ensure inner fillet is physically possible
    inner_r = max(0.2, fillet_radius - 0.5) 
    
    inner = (
        cq.Workplane("YZ")
        .rect(inner_w, inner_h)
        .extrude(thickness)
        .edges("|X")
        .fillet(inner_r)
    )
    
    # 3. Create the notch cutter
    # Notch is on the top inner edge (Z direction in local YZ plane)
    # Box dimensions: X=thickness, Y=notch_width, Z=notch_depth*2
    # We position it to cut into the rim from the inner edge upwards
    notch_box = (
        cq.Workplane("XY") # Use global coords relative to frame origin
        .box(thickness, notch_width, notch_depth * 2)
        # Shift X to cover thickness [0, T]
        # Shift Z to start at inner edge (inner_h/2) and go up
        .translate((thickness / 2.0, 0, (inner_h / 2.0) + notch_depth))
    )
    
    # Boolean operations
    frame = outer.cut(inner).cut(notch_box)
    return frame

# Generate the master geometry
master_frame = create_master_frame()

# Generate the polar array locations
# Center the arc on the X-axis (angle 0)
start_angle = -total_angle / 2.0
locs = (
    cq.Workplane("XY")
    .polarArray(arc_radius, start_angle, total_angle, num_frames, rotate=True)
    .vals()
)

# Place the frames at the generated locations
result = cq.Workplane("XY")
for loc in locs:
    # .val() gets the Shape object, .located() applies the transformation
    result = result.add(master_frame.val().located(loc))

# The 'result' variable now contains the final compound solid
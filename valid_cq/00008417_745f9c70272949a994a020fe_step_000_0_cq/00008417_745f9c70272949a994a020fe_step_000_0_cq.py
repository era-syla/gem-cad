import cadquery as cq

# --- Parameters ---

# Main plate dimensions
plate_width = 150.0
plate_height = 80.0
plate_thickness = 5.0
plate_corner_radius = 5.0

# Fan hole parameters
fan_hole_diameter = 60.0
fan_spacing = 70.0  # Center-to-center distance

# Mounting holes (corner holes)
mount_hole_diameter = 4.0
mount_hole_inset = 5.0 # Distance from edge to hole center

# Center mounting holes (the small ones in the middle)
center_mount_hole_diameter = 3.0
center_mount_hole_spacing_x = 20.0
center_mount_hole_spacing_y = 40.0

# Bottom clip/foot parameters
foot_width = 30.0
foot_height = 40.0
foot_depth = 15.0
foot_thickness = 4.0
foot_slot_width = 5.0  # The gap in the clip
foot_spacing = fan_spacing # Align feet with fan centers
foot_angle = 15.0 # Slight angle for the feet

# --- Geometry Construction ---

# 1. Create the main rectangular plate
plate = (
    cq.Workplane("XY")
    .rect(plate_width, plate_height)
    .extrude(plate_thickness)
    .edges("|Z")
    .fillet(plate_corner_radius)
)

# 2. Cut the large fan holes
# We position two holes symmetrically
fan_holes = (
    cq.Workplane("XY")
    .pushPoints([(-fan_spacing / 2, 0), (fan_spacing / 2, 0)])
    .circle(fan_hole_diameter / 2)
    .extrude(plate_thickness, combine=False)
)

plate = plate.cut(fan_holes)

# 3. Cut the corner mounting holes
# Calculate corner positions
mx = plate_width / 2 - mount_hole_inset
my = plate_height / 2 - mount_hole_inset
corner_pts = [(-mx, -my), (mx, -my), (mx, my), (-mx, my)]

corner_holes = (
    cq.Workplane("XY")
    .pushPoints(corner_pts)
    .circle(mount_hole_diameter / 2)
    .extrude(plate_thickness, combine=False)
)

plate = plate.cut(corner_holes)

# 4. Cut the center mounting holes (4 small holes between fans)
cx = center_mount_hole_spacing_x / 2
cy = center_mount_hole_spacing_y / 2
center_pts = [(-cx, -cy), (cx, -cy), (cx, cy), (-cx, cy)]

center_holes = (
    cq.Workplane("XY")
    .pushPoints(center_pts)
    .circle(center_mount_hole_diameter / 2)
    .extrude(plate_thickness, combine=False)
)

plate = plate.cut(center_holes)

# 5. Create the bottom feet/clips
# We will create a profile for the clip and extrude it.
# The profile looks like a U-shape or a hollow rectangle with an open top (relative to the profile plane).

def create_foot():
    # Helper to make one foot
    # Profile sketch on YZ plane (side view)
    
    # Outer profile
    outer_rect = (
        cq.Workplane("YZ")
        .rect(foot_depth, foot_height)
    )
    
    # Inner slot (cutout)
    inner_rect = (
        cq.Workplane("YZ")
        .rect(foot_slot_width, foot_height - foot_thickness) # Keep bottom closed
        .translate((0, foot_thickness/2, 0)) # Shift up to keep bottom thickness
    )
    
    # Extrude the profile to get width
    foot_solid = (
        cq.Workplane("YZ")
        .rect(foot_depth, foot_height) # Outer boundary
        .rect(foot_slot_width, foot_height - foot_thickness) # Inner cut
        .translate((0, foot_thickness/2, 0)) # Shift inner cut
        .extrude(foot_width) # Extrude along X
    )
    
    # Add fillets to the foot edges for smoothness
    foot_solid = foot_solid.edges("|X").fillet(2.0)
    
    return foot_solid

# Generate one foot
single_foot = create_foot()

# Position the left foot
# Rotate slightly to match image
foot_left = (
    single_foot
    .rotate((0,0,0), (1,0,0), -foot_angle) # Tilt it back
    .translate((-fan_spacing / 2, -plate_height/2 - foot_height/2 + 5, foot_depth/2)) 
    # Adjust Z translation to merge nicely with back of plate or front
)

# Position the right foot
foot_right = (
    single_foot
    .rotate((0,0,0), (1,0,0), -foot_angle)
    .translate((fan_spacing / 2, -plate_height/2 - foot_height/2 + 5, foot_depth/2))
)

# Combine feet with the plate
result = plate.union(foot_left).union(foot_right)

# Optional: Add a small fillet where the feet join the plate for strength
# This is tricky without selecting specific edges, so we'll rely on the overlap union.

# Export or display
if "show_object" in locals():
    show_object(result)
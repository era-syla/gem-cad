import cadquery as cq

# --- Model Parameters ---
# Dimensions approximated for an M4 Pan Head Machine Screw
thread_diameter = 4.0
total_length = 40.0  # Length of the shaft
head_diameter = 8.0
head_height = 2.8    # Height of the head including dome
head_fillet_radius = 1.4  # Creates the rounded 'pan' profile

# Phillips-style drive dimensions
drive_span = 5.0     # Total width of the cross
drive_width = 1.2    # Thickness of the cross arms
drive_depth = 2.2
drive_taper_angle = -15.0 # Negative angle to taper inwards (make hole smaller at bottom)

# --- Geometry Construction ---

# 1. Create the Shaft
# We use a cylinder to represent the threaded shank (standard CAD simplification)
shaft = (
    cq.Workplane("XY")
    .circle(thread_diameter / 2.0)
    .extrude(-total_length)
)

# Add a chamfer to the tip of the shaft
shaft = shaft.faces("<Z").edges().chamfer(thread_diameter * 0.1)

# 2. Create the Head
# Start with a cylinder at the top of the shaft
head_base = (
    cq.Workplane("XY")
    .circle(head_diameter / 2.0)
    .extrude(head_height)
)

# Apply a fillet to the top edge to achieve the Pan Head dome shape
head = head_base.faces(">Z").edges().fillet(head_fillet_radius)

# 3. Combine Head and Shaft
screw_body = head.union(shaft)

# Add a small fillet at the neck (junction of head and shaft) for realism
try:
    screw_body = screw_body.edges(cq.NearestToPointSelector((thread_diameter/2.0, 0, 0))).fillet(0.2)
except:
    pass # Proceed if edge selection is ambiguous

# 4. Create the Drive Recess (Phillips Cross)
# We create the cutter by unioning two tapered rectangular extrusions.
# We start at the top of the head and extrude downwards with a negative taper to create the wedge shape.

# Create the workplane at the top of the head
top_plane = cq.Workplane("XY").workplane(offset=head_height)

# Arm 1 of the cross
arm_1 = (
    top_plane
    .rect(drive_span, drive_width)
    .extrude(-drive_depth, taper=drive_taper_angle)
)

# Arm 2 of the cross (rotated 90 degrees conceptually, but defined by dimensions here)
arm_2 = (
    top_plane
    .rect(drive_width, drive_span)
    .extrude(-drive_depth, taper=drive_taper_angle)
)

# Combine arms to form the Phillips driver shape
drive_cutter = arm_1.union(arm_2)

# 5. Final Operation
# Cut the drive shape from the screw body
result = screw_body.cut(drive_cutter)
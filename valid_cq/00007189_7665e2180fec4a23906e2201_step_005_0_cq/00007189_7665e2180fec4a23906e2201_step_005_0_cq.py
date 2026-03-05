import cadquery as cq

# Parametric dimensions
total_length = 80.0
main_body_height = 20.0
main_body_width = 15.0
main_body_length = 40.0

# Right arm dimensions
arm_length = total_length - main_body_length
arm_height = 10.0
arm_width = main_body_width # Same width as main body

# Slot dimensions (left side)
slot_depth = 15.0
slot_height = 8.0
slot_width = main_body_width # Through cut

# Hole dimensions
hole_diameter = 3.0
hole_offset_from_right = 10.0 # From the right face of the main body
hole_height_ratio = 0.5 # Centered vertically on the main body

# Create the main block
# We will construct it by creating the main large block and then cutting/adding
main_block = cq.Workplane("XY").box(main_body_length, main_body_width, main_body_height)

# Create the right arm
# The arm is attached to the right face of the main block.
# We need to position it correctly. 
# main_block center is (0,0,0). Its x-range is [-20, 20].
# We want the arm to start at x=20 and go to x=60.
# The arm height is 10, main body is 20. Let's align the bottom faces? 
# Looking at the image, the arm seems aligned with the bottom of the main block.
# Main block z-range is [-10, 10]. Bottom is -10.
# Arm z-range should be [-10, 0]. Center at -5.
arm_center_x = (main_body_length / 2) + (arm_length / 2)
arm_center_z = -(main_body_height / 2) + (arm_height / 2)

right_arm = (
    cq.Workplane("XY")
    .center(arm_center_x, 0)
    .center(0, arm_center_z) # Adjust Z height relative to XY plane
    .box(arm_length, arm_width, arm_height)
)

# Combine main body and arm. 
# Note: box() creates centered geometry by default. 
# Let's rebuild more sequentially to be cleaner.

# Strategy 2: Sketch the profile on the XZ plane (front view) and extrude.
# This handles the height difference naturally.
# Let's orient length along X, Height along Z, Width along Y.

# Profile points (starting bottom-left, going counter-clockwise)
# Let's place the bottom-left corner at (0,0)
pts = [
    (0, 0),                           # Bottom-left of main body
    (main_body_length, 0),            # Bottom-right of main body (start of arm)
    (main_body_length + arm_length, 0), # End of arm
    (main_body_length + arm_length, arm_height), # Top of arm end
    (main_body_length, arm_height),   # Top of arm connection
    (main_body_length, main_body_height), # Top-right of main body
    (0, main_body_height),            # Top-left of main body
    (0, (main_body_height + slot_height)/2), # Top of slot start
    (slot_depth, (main_body_height + slot_height)/2), # Top-inner slot corner
    (slot_depth, (main_body_height - slot_height)/2), # Bottom-inner slot corner
    (0, (main_body_height - slot_height)/2) # Bottom of slot start
]

# Create the base shape by extruding the profile
# We center the extrusion on Y so origin is in the middle of the width
result = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .extrude(main_body_width)
)

# Create the hole
# The hole is on the main body.
# Location: Looking at image, it's roughly centered vertically on the main body
# and some distance from the step where the arm starts.
hole_x = main_body_length - hole_offset_from_right
hole_z = main_body_height / 2

result = (
    result
    .faces(">Y") # Select the front face (positive Y)
    .workplane()
    .center(hole_x - (total_length/2), hole_z - (main_body_height/2)) # Adjust coordinate system mess from extrude?
    # Actually, it's easier to just select the face and use relative coordinates or absolute if we know them.
    # The extrude centered the object on the origin in Y, but X and Z start at 0 based on my points.
    # So Global coords are: X in [0, 80], Z in [0, 20], Y in [-7.5, 7.5].
    # We want a hole at specific X, Z, through all Y.
)

# Let's do the hole using global coordinates for clarity
result = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .extrude(main_body_width) # Center is Y=0
    .faces(">Y").workplane()  # Workplane on the "front" face
    .pushPoints([(hole_x, hole_z)]) # X is along the length, Y (local) is along Z (global)
    .hole(hole_diameter)
)

if __name__ == "__main__":
    # If running in an environment that supports show_object (like CQ-editor)
    try:
        show_object(result)
    except NameError:
        pass
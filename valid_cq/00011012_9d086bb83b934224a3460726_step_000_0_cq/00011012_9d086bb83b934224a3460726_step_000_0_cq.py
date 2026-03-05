import cadquery as cq

# --- Parameter Definitions ---

# Base Plate Dimensions
base_length = 200.0
base_width = 80.0
base_thickness = 10.0

# A-Frame Support Dimensions
support_leg_thickness = 5.0
support_leg_width = 10.0
support_height = 80.0
support_spread = 60.0  # Distance between legs at the bottom
pivot_post_height = 100.0
pivot_post_width = 10.0
pivot_post_thickness = 10.0

# Linkage Arm Dimensions
arm_length = 250.0
arm_width = 8.0
arm_thickness = 4.0
arm_spacing = 20.0  # Vertical distance between parallel arms (parallelogram linkage)

# End Effector / Wall Mount Dimensions
mount_plate_size = 40.0
mount_plate_thickness = 2.0
mount_flange_depth = 20.0

# Pivot Pin Dimensions
pin_diameter = 3.0
pin_length = 15.0

# --- Helper Functions ---

def create_arm(length, width, thickness, hole_dia):
    """Creates a single linkage arm with holes at ends and center."""
    arm = (cq.Workplane("XY")
           .box(length, width, thickness)
           .faces(">Z").workplane()
           .pushPoints([(-length/2 + width, 0), (length/2 - width, 0), (0, 0)])
           .hole(hole_dia)
           )
    return arm

# --- Geometry Construction ---

# 1. Base Plate
base = cq.Workplane("XY").box(base_length, base_width, base_thickness)

# 2. A-Frame / Support Structure
# We'll create the central vertical post first
post = (cq.Workplane("XY")
        .center(0, 0)
        .box(pivot_post_width, pivot_post_thickness, pivot_post_height)
        .translate((0, 0, pivot_post_height/2 + base_thickness/2))
        )

# Add pivot holes to the post
post = (post.faces(">Y").workplane()
        .pushPoints([(0, arm_spacing/2 + 20), (0, -arm_spacing/2 + 20)]) # Offset from center somewhat
        .hole(pin_diameter)
        )

# Create the angled legs
# We calculate angles or just construct geometry bridging points
# Leg 1 (Front/Right)
leg_path = (cq.Workplane("XZ")
            .moveTo(0, base_thickness/2 + 30) # Connect partway up the post
            .lineTo(support_spread/2, -base_thickness/2) # Connect to base edge
            )
leg_right = (cq.Workplane("XY")
             .center(0, base_width/2) # Offset in Y slightly so it's not centered
             .workplane(offset=0) # Reset
             .rect(support_leg_width, support_leg_thickness) # Cross section
             .extrude(1) # Dummy extrude to init solid
             )

# Creating angled legs is cleaner by lofting or sweeping, 
# but simply rotating boxes is often more robust in parametric scripts.
# Let's use rotated boxes.
leg_angle = 30.0 # Approximate angle
leg_len = support_height / cq.selectors.math.cos(cq.selectors.math.radians(leg_angle))

leg_r = (cq.Workplane("XY")
         .box(support_leg_width, support_leg_thickness, leg_len + 20)
         .rotate((0,0,0), (0,1,0), leg_angle)
         .translate((support_spread/4, 0, base_thickness + 20))
         )

leg_l = (cq.Workplane("XY")
         .box(support_leg_width, support_leg_thickness, leg_len + 20)
         .rotate((0,0,0), (0,1,0), -leg_angle)
         .translate((-support_spread/4, 0, base_thickness + 20))
         )

# Combine Support Structure
support_structure = post.union(leg_r).union(leg_l)


# 3. Linkage Arms (Parallelogram mechanism)
# Top Arm
arm_top = create_arm(arm_length, arm_width, arm_thickness, pin_diameter)
# Position Top Arm (relative to post top hole)
arm_top_positioned = (arm_top
                      .translate((0, 0, 0)) # Center
                      .rotate((0,0,0), (0,1,0), -15) # Tilt slightly
                      .translate((-arm_length/4, pivot_post_thickness/2 + arm_thickness/2, base_thickness/2 + pivot_post_height/2 + 20 + arm_spacing/2))
                      )

# Bottom Arm
arm_bottom = create_arm(arm_length, arm_width, arm_thickness, pin_diameter)
# Position Bottom Arm (relative to post bottom hole)
arm_bottom_positioned = (arm_bottom
                         .translate((0, 0, 0))
                         .rotate((0,0,0), (0,1,0), -15) # Tilt slightly
                         .translate((-arm_length/4, pivot_post_thickness/2 + arm_thickness/2, base_thickness/2 + pivot_post_height/2 + 20 - arm_spacing/2))
                         )

# Mirror arms to the other side for stability (optional based on image interpretation, but standard practice)
# The image shows arms on one side mostly, maybe double. Let's stick to single side based on visual clutter, 
# or double if it looks like a yoke. The image looks like single bars on one side of the pivot.

# 4. End Effector / Wall Mount
# This is the "L" shaped bracket at the end of the arms
bracket_h = arm_spacing + 20
bracket = (cq.Workplane("YZ")
           .rect(mount_plate_size, bracket_h)
           .extrude(mount_plate_thickness)
           .translate((-mount_plate_thickness/2, 0, 0))
           )

# Add flange to bracket
flange = (cq.Workplane("XY")
          .box(mount_flange_depth, mount_plate_size, mount_plate_thickness)
          .translate((-mount_flange_depth/2 - mount_plate_thickness/2, 0, -bracket_h/2 + mount_plate_thickness/2))
          )

end_effector = bracket.union(flange)

# Pivot mounts on the bracket
# Just small protrusions or blocks to accept the pins
mount_block_top = (cq.Workplane("XY")
                   .box(5, 5, 5)
                   .translate((2.5, 0, arm_spacing/2))
                   )
mount_block_bot = (cq.Workplane("XY")
                   .box(5, 5, 5)
                   .translate((2.5, 0, -arm_spacing/2))
                   )

end_effector = end_effector.union(mount_block_top).union(mount_block_bot)

# Move End Effector to tip of arms
# We need to calculate the tip position based on arm length and rotation
angle_rad = cq.selectors.math.radians(-15)
# Pivot is at approx -arm_length/4 relative to center of arm. 
# So the tip is at (arm_length/2 - arm_length/4) = arm_length/4 from pivot?
# Actually, let's just approximate visually. The pivot is near the middle-ish.
# Let's say pivot index is at x=0 in global, arm center is offset.
dx = (arm_length/2 - arm_width) * cq.selectors.math.cos(angle_rad) 
dz = (arm_length/2 - arm_width) * cq.selectors.math.sin(angle_rad)

# The arms were shifted by -arm_length/4. So the long end is to the right?
# In the code: .translate((-arm_length/4 ...)) means the geometric center is shifted left.
# So the right end (positive X local) is closer to the pivot.
# The left end (negative X local) is the long reach.
# The image shows the wall bracket on the left (long reach).

# Coordinates of the "Left" end of the arm (where bracket goes)
# Local arm coord: -length/2 + width
bracket_x = (-arm_length/2 + arm_width) * cq.selectors.math.cos(angle_rad) - arm_length/4
bracket_z = (-arm_length/2 + arm_width) * cq.selectors.math.sin(angle_rad) + (base_thickness/2 + pivot_post_height/2 + 20)

end_effector_positioned = (end_effector
                           .rotate((0,0,0), (0,1,0), -15) # Match arm tilt so it stays vertical? Parallelogram keeps it vertical relative to ground usually.
                           # Actually parallelogram linkage keeps the end effector orientation constant relative to base.
                           # So if base is horizontal, end effector stays vertical/horizontal. No rotation needed on the part itself usually, just translation.
                           .rotate((0,0,0), (0,1,0), 0) 
                           .translate((bracket_x, pivot_post_thickness/2 + arm_thickness/2, bracket_z))
                           )

# 5. Connecting Pins (Cosmetic)
# Center Pivot Pin
pin_center = (cq.Workplane("YZ")
              .circle(pin_diameter/2)
              .extrude(pin_length + pivot_post_thickness + arm_thickness)
              .translate((-arm_length/4, -pivot_post_thickness/2, base_thickness/2 + pivot_post_height/2 + 20))
              )


# --- Combine All Parts ---

result = (base
          .union(support_structure)
          .union(arm_top_positioned)
          .union(arm_bottom_positioned)
          .union(end_effector_positioned)
          .union(pin_center)
          )
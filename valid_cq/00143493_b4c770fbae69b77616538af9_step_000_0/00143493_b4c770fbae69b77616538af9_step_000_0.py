import cadquery as cq

# --- Parameters ---

# Base Plate Dimensions
base_height = 60.0
base_width = 60.0
base_thickness = 8.0

# Standoff/Pin Dimensions
pin_diameter = 6.0
pin_hole_diameter = 3.5
pin_length = 22.0
pin_spacing_x = 46.0
pin_spacing_y = 46.0

# Arm Dimensions
arm_length = 240.0
arm_width = 36.0
arm_thickness = 3.0

# Feature Locations & Dimensions
cutout_size = 12.0
cutout_pos_1 = 125.0
cutout_pos_2 = 195.0

notch_width = 3.0
notch_depth = 2.0  # Depth into the arm edge

tip_notch_depth = 8.0
tip_notch_width = 12.0

bolt_pos_x = 25.0
bolt_head_dia = 10.0
bolt_head_height = 4.0

# --- Geometry Construction ---

# 1. Base Plate
# Create plate on YZ plane, centered. Translate so front face is at X=0.
base = (cq.Workplane("YZ")
        .box(base_width, base_height, base_thickness)
        .translate((-base_thickness/2, 0, 0)))

# 2. Standoffs (Pins)
# Define locations relative to center of plate
pin_locs = [
    (pin_spacing_x/2, pin_spacing_y/2),
    (pin_spacing_x/2, -pin_spacing_y/2),
    (-pin_spacing_x/2, pin_spacing_y/2),
    (-pin_spacing_x/2, -pin_spacing_y/2)
]

# Add standoffs to the front face (>X)
base_assembly = (base.faces(">X").workplane()
                 .pushPoints(pin_locs)
                 .circle(pin_diameter/2)
                 .circle(pin_hole_diameter/2) # Inner circle for hollow tube
                 .extrude(pin_length))

# Cut mounting holes through the base plate (from back face <X)
base_assembly = (base_assembly.faces("<X").workplane()
                 .pushPoints(pin_locs)
                 .circle(pin_hole_diameter/2)
                 .cutBlind(-base_thickness))

# 3. Arm
# Create arm geometry on XY plane.
# Positioned such that it starts at X=0 and extends along +X.
# Centered vertically at Z=0.
arm = (cq.Workplane("XY")
       .workplane(offset=-arm_thickness/2)
       .moveTo(arm_length/2, 0)
       .rect(arm_length, arm_width)
       .extrude(arm_thickness))

# 4. Bolt Head
# Hex bolt head on top of the arm near the base
bolt = (cq.Workplane("XY")
        .workplane(offset=arm_thickness/2)
        .moveTo(bolt_pos_x, 0)
        .polygon(6, bolt_head_dia)
        .extrude(bolt_head_height))

# Combine Arm and Bolt for cutting
arm_assembly = arm.union(bolt)

# 5. Cuts and Features on Arm
# We perform cuts by sketching on the top face of the arm assembly
# Using a fresh workplane referenced to global coordinates for easier positioning
arm_assembly = (arm_assembly.faces(">Z").workplane()
                # Square Cutout 1
                .moveTo(cutout_pos_1, 0)
                .rect(cutout_size, cutout_size)
                
                # Square Cutout 2
                .moveTo(cutout_pos_2, 0)
                .rect(cutout_size, cutout_size)
                
                # Side Notches at Cutout 1
                .moveTo(cutout_pos_1, arm_width/2).rect(notch_width, notch_depth*2)
                .moveTo(cutout_pos_1, -arm_width/2).rect(notch_width, notch_depth*2)
                
                # Side Notches at Cutout 2
                .moveTo(cutout_pos_2, arm_width/2).rect(notch_width, notch_depth*2)
                .moveTo(cutout_pos_2, -arm_width/2).rect(notch_width, notch_depth*2)
                
                # Tip Notch (at the end of the arm)
                .moveTo(arm_length, 0).rect(tip_notch_depth*2, tip_notch_width) # *2 depth to ensure cut from edge
                
                # Execute Cut
                .cutBlind(-20) # Cut deep enough to go through the arm
                )

# 6. Final Assembly
result = base_assembly.union(arm_assembly)
import cadquery as cq
import math

# --- Parameters ---
# Central Prism
prism_side = 30.0
prism_height = 40.0

# Aluminum Extrusion Profile Simulation (simplified 2020 T-slot style)
extrusion_size = 20.0
extrusion_length = 35.0  # Length sticking out from the center
slot_width = 6.0
slot_depth = 5.0

# Plates
plate_length = 150.0  # Total length from center
plate_width = 30.0
plate_thickness = 3.0
plate_offset = extrusion_size / 2.0  # To align with the bottom/top of the extrusion

# Holes in Plate
hole_diameter = 4.0
hole_spacing = 20.0
num_holes = 5
hole_start_dist = 50.0  # Distance from center to first hole

# --- Helper Functions ---

def create_extrusion_profile(length):
    """Creates a simplified 2020 extrusion profile."""
    # Base square
    base = cq.Workplane("XY").box(extrusion_size, extrusion_size, length)
    
    # Create slots on all 4 sides
    slot_shape = cq.Workplane("XY").box(slot_width, slot_depth, length)
    
    # Cut slots
    # Top
    s1 = slot_shape.translate((0, extrusion_size/2 - slot_depth/2, 0))
    # Bottom
    s2 = slot_shape.translate((0, -(extrusion_size/2 - slot_depth/2), 0))
    # Right
    s3 = slot_shape.rotate((0,0,1), (0,0,0), 90).translate((extrusion_size/2 - slot_depth/2, 0, 0))
    # Left
    s4 = slot_shape.rotate((0,0,1), (0,0,0), 90).translate((-(extrusion_size/2 - slot_depth/2), 0, 0))
    
    # Center hole
    center_hole = cq.Workplane("XY").cylinder(length, 2.5) # 5mm diameter hole
    
    final = base.cut(s1).cut(s2).cut(s3).cut(s4).cut(center_hole)
    return final

def create_arm_assembly(angle):
    """Creates one arm: extrusion + plate."""
    
    # 1. Extrusion
    # Create and orient extrusion
    ext = create_extrusion_profile(extrusion_length)
    # Rotate extrusion so length is along X (initially it's along Z)
    ext = ext.rotate((0,1,0), (0,0,0), 90)
    # Shift it so it starts from slightly outside the center
    ext = ext.translate((prism_side/2 * 0.6 + extrusion_length/2, 0, 0))
    
    # 2. Plate
    # Create basic plate
    # We construct it starting from near the center extending outwards
    p_len_actual = plate_length - (prism_side/2)
    plate = cq.Workplane("XY").box(p_len_actual, plate_width, plate_thickness)
    
    # Move plate to correct position
    # Align bottom of plate with bottom of extrusion (or top, based on image looks like bottom)
    # The image shows the plate attached to the *bottom* face of the extrusion structure.
    # Extrusion center is at Z=0. Extrusion bottom is at -10. Plate top should be at -10.
    plate_z = - (extrusion_size / 2) - (plate_thickness / 2)
    plate_x_center = (prism_side/2) + (p_len_actual / 2)
    plate = plate.translate((plate_x_center, 0, plate_z))
    
    # Add holes to plate
    for i in range(num_holes):
        h_dist = hole_start_dist + (i * hole_spacing)
        # Create a cylinder for cutting
        cutter = cq.Workplane("XY").cylinder(plate_thickness * 2, hole_diameter/2)
        cutter = cutter.translate((h_dist, 0, plate_z))
        plate = plate.cut(cutter)
        
    # Combine extrusion and plate
    arm = ext.union(plate)
    
    # Rotate the entire arm assembly around Z axis
    arm = arm.rotate((0,0,1), (0,0,0), angle)
    
    return arm

# --- Main Construction ---

# 1. Central Hub (Triangular Prism)
# Calculate apothem to size it correctly relative to extrusions
# Prism needs to be big enough to hold the extrusions
# Create a triangular prism
hub = (cq.Workplane("XY")
       .polygon(3, prism_side * 1.5) # Triangle
       .extrude(prism_height)
       .translate((0, 0, -prism_height/2 + extrusion_size/2 + 5)) # Shift up/down to align visually
      )

# The image shows a triangular top cap and a central vertical element.
# Let's make a central vertical triangular core.
core_triangle = (cq.Workplane("XY")
                 .polygon(3, prism_side)
                 .extrude(prism_height)
                 .translate((0,0, -prism_height/2))
                )

# 2. Create the 3 Arms
arm1 = create_arm_assembly(30)   # 0 degrees usually points X+, triangle symmetry is 120 deg
arm2 = create_arm_assembly(150)  # 30 + 120
arm3 = create_arm_assembly(270)  # 150 + 120

# 3. Combine everything
result = core_triangle.union(arm1).union(arm2).union(arm3)

# 4. Refine the central connection
# The image shows the extrusions meeting at a triangular block. 
# The initial simple core union works, but let's add the top triangular cap specifically visible in the image.
top_cap = (cq.Workplane("XY")
           .polygon(3, prism_side * 1.2)
           .extrude(3) # Thin cap
           .translate((0, 0, extrusion_size/2)) # Placed on top of the extrusions
          )

# Add the central vertical triangular column that connects everything
center_post = (cq.Workplane("XY")
               .polygon(3, prism_side * 0.8)
               .extrude(extrusion_size) # Height of the horizontal extrusions
               .translate((0,0, -extrusion_size/2))
              )


result = result.union(top_cap)

# Add small mounting holes on the top cap? (Optional, hard to see but common)
# Let's clean up the union to make it a single solid
result = result.combine()
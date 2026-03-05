import cadquery as cq

# Parametric dimensions
body_width = 40.0   # Width of the square base
body_height = 60.0  # Height of the main box

boss_diameter = 25.0  # Diameter of the raised circular boss
boss_height = 3.0     # Height of the raised boss

hole_spacing = 28.0   # Distance between mounting holes (center-to-center)
hole_diameter = 3.0   # Diameter of the corner mounting holes
hole_depth = 10.0     # Depth of the mounting holes

center_bore_diameter = 10.0  # Diameter of the inner recess
center_bore_depth = 5.0      # Depth of the inner recess

center_pin_diameter = 5.0    # Diameter of the central pin
center_pin_height = 3.0      # Height of the pin relative to the bottom of the bore
                             # (effectively making it flush with top of boss if heights align)

# Create the main body
result = (
    cq.Workplane("XY")
    .box(body_width, body_width, body_height)
    
    # Select the top face
    .faces(">Z")
    .workplane()
    
    # Create the circular boss
    .circle(boss_diameter / 2)
    .extrude(boss_height)
    
    # Create the central bore (recess) inside the boss
    .faces(">Z")
    .workplane()
    .circle(center_bore_diameter / 2)
    .cutBlind(-center_bore_depth)
    
    # Create the central pin rising from the bottom of the bore
    # We select the face at the bottom of the cut we just made
    .faces("<Z[1]") # Select the second highest Z face (which is the bottom of the bore)
    .workplane()
    .circle(center_pin_diameter / 2)
    .extrude(center_pin_height)
    
    # Create the 4 corner mounting holes on the top of the main body
    # We need to go back to the top surface of the main box
    .faces(">Z[2]") # Select the "shoulder" face of the box
    .workplane()
    .rect(hole_spacing, hole_spacing, forConstruction=True)
    .vertices()
    .hole(hole_diameter, hole_depth)
)
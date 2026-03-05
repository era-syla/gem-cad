import cadquery as cq

# --- Parametric Dimensions ---
# Handle (Grip)
handle_length = 80.0
handle_width = 20.0
handle_thickness = 15.0
handle_fillet = 3.0

# Shaft
shaft_length = 120.0
shaft_diameter = 10.0

# Head (Ratchet mechanism housing)
head_outer_diameter = 32.0
head_thickness = 18.0
head_neck_width = 16.0  # Where shaft meets head
head_neck_fillet = 10.0 # Transition fillet
head_cavity_diameter = 22.0
head_cavity_depth = 12.0

# --- Geometry Construction ---

# 1. Handle (Grip)
# Creating a rectangular prism with rounded edges/corners
handle = (
    cq.Workplane("XY")
    .rect(handle_width, handle_thickness)
    .extrude(handle_length)
    .edges("|Z")
    .fillet(handle_fillet)
    # Chamfer the back end for a nicer look like in the image
    .faces("<Z")
    .edges()
    .chamfer(1.5)
)

# 2. Shaft
# Cylinder connecting handle to head
# We start from the front face of the handle
shaft = (
    cq.Workplane("XY")
    .workplane(offset=handle_length)
    .circle(shaft_diameter / 2)
    .extrude(shaft_length)
)

# 3. Head
# The head is a bit complex. It looks like a rounded shape with a cavity.
# Center of head relative to end of shaft
head_center_z = handle_length + shaft_length + (head_outer_diameter / 2) - 5 # Slight overlap

# Base shape of the head (a rounded rectangle/lofted shape)
# Let's create a profile and extrude it
head_sketch = (
    cq.Workplane("XY")
    .workplane(offset=handle_length + shaft_length)
    # Move the workplane to be centered on the head body
    .center(0, 0)
    # Create the profile: a circle combined with a rectangle for the neck
    .rect(head_outer_diameter, head_thickness) # Base rect
    .extrude(head_outer_diameter + 5) # Extrude longer than needed, then cut
)

# Create a more accurate head shape using a cylinder and blending
head_cylinder = (
    cq.Workplane("YZ")
    .workplane(offset=0) # Centered on X
    .center(0, handle_length + shaft_length + head_outer_diameter/2)
    .circle(head_outer_diameter / 2)
    .extrude(head_thickness, both=True)
)

# Create the transition/neck area
neck_transition = (
    cq.Workplane("XY")
    .workplane(offset=handle_length + shaft_length - 5) # Start inside shaft
    .rect(shaft_diameter, shaft_diameter) # Start circular-ish
    .workplane(offset=15) # Distance to head bulk
    .rect(head_neck_width, head_thickness)
    .loft(combine=False)
)

# Refined Head Construction strategy:
# 1. Main cylindrical body of the ratchet head
head_main = (
    cq.Workplane("XY")
    .workplane(offset=handle_length + shaft_length + head_outer_diameter/2)
    .cylinder(head_thickness, head_outer_diameter/2, centered=(True, True, True))
    .rotate((0,0,0), (0,1,0), 90) # Rotate so flat faces are on sides
    .translate((0, 0, 0)) # Ensure position
)

# 2. Add the transition block from shaft to head
neck_block = (
    cq.Workplane("XY")
    .workplane(offset=handle_length + shaft_length)
    .rect(head_outer_diameter, head_thickness)
    .extrude(head_outer_diameter/2)
    .intersect(head_main) # Keep only the overlapping part to round the back
)

# Combine parts so far
part = handle.union(shaft).union(head_main)

# Add fillets to smooth the transition from shaft to head
# This is tricky with boolean unions, so we select edges near the junction
try:
    part = part.faces(">Z[1]").edges().fillet(2.0)
except:
    pass # Fallback if specific selection fails

# Cut the cavity for the ratchet mechanism
cavity = (
    cq.Workplane("XY")
    .workplane(offset=handle_length + shaft_length + head_outer_diameter/2)
    .circle(head_cavity_diameter / 2)
    .extrude(head_cavity_depth/2) # Cut into top
    .translate((0, head_thickness/2, 0)) # Move to top surface
    .rotate((1,0,0), (0,0,0), 90)
)

# Create a through hole or deeper recess
inner_hole = (
    cq.Workplane("XY")
    .workplane(offset=handle_length + shaft_length + head_outer_diameter/2)
    .circle(head_cavity_diameter / 3)
    .extrude(head_thickness * 2) # Through all
    .translate((0, 0, 0)) 
    .rotate((1,0,0), (0,0,0), 90)
)

# Apply cuts
result = part.cut(cavity).cut(inner_hole)

# Apply fillets to the head for the cast/forged look
result = result.edges(cq.selectors.BoxSelector(
    (-head_outer_diameter, -head_thickness, handle_length + shaft_length),
    (head_outer_diameter, head_thickness, handle_length + shaft_length + head_outer_diameter + 10)
)).fillet(1.0)

# Apply fillet to the handle-shaft transition
result = result.edges(cq.selectors.NearestToPointSelector((0, 0, handle_length))).fillet(2.0)

# Rotate for better viewing angle similar to image
result = result.rotate((0,0,0), (1,0,0), -45).rotate((0,0,0), (0,0,1), 45)
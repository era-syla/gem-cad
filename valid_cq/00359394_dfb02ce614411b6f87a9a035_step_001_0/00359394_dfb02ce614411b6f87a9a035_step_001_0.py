import cadquery as cq

# --- Parameter Definitions ---
length = 150.0        # Total width (X-axis)
width_left = 110.0    # Depth of the left side (Y-axis)
width_right = 80.0    # Depth of the right side (Y-axis)
thickness = 20.0      # Total thickness of the plate
thin_thickness = 12.0 # Thickness of the stepped down section
step_x_pos = 20.0     # X-axis position where the step occurs
concavity = 25.0      # Sagitta (depth) of the front concave curve
fillet_rad = 5.0      # Radius of the fillet at the step root

# Hole parameters
hole_dia = 6.5
cbore_dia = 12.0
cbore_depth = 6.0
csk_dia = 13.0
csk_angle = 90.0

# --- 1. Create Base Shape ---
# Define the 4 corners and the curved front edge centered roughly on X
x_min = -length / 2
x_max = length / 2

p_bl = (x_min, 0)              # Bottom Left
p_tl = (x_min, width_left)     # Top Left
p_tr = (x_max, width_right)    # Top Right
p_br = (x_max, 0)              # Bottom Right
p_curve_mid = (0, concavity)   # Midpoint for the concave arc (Y > 0 goes "in")

# Create the solid block with the concave front
base = (
    cq.Workplane("XY")
    .moveTo(*p_bl)
    .lineTo(*p_tl)
    .lineTo(*p_tr)
    .lineTo(*p_br)
    .threePointArc(p_curve_mid, p_bl) # Arc back to start point
    .close()
    .extrude(thickness)
)

# --- 2. Create the Step Cut ---
# Cut the right side to create the thinner section
# The cut removes material from the top face down
cut_depth = thickness - thin_thickness

# Draw a rectangle on the top face that covers the right side
# starting from step_x_pos
result = (
    base.faces(">Z").workplane()
    .moveTo(step_x_pos, -10) # Start with some margin Y
    .lineTo(step_x_pos, width_left + 10)
    .lineTo(x_max + 10, width_left + 10)
    .lineTo(x_max + 10, -10)
    .close()
    .cutBlind(-cut_depth)
)

# --- 3. Add Step Fillet ---
# Fillet the internal edge formed where the step wall meets the thin floor
# We select the edge near the step position and the thin height
edge_selector = cq.NearestToPointSelector((step_x_pos, width_left/2, thin_thickness))
result = result.edges(edge_selector).fillet(fillet_rad)

# --- 4. Add Holes ---

# Set 1: Counterbored holes on the thick (left) section
h_left_1 = (-45, 45)
h_left_2 = (-35, 90)

result = (
    result.faces(">Z") # Select the highest face
    .workplane()
    .pushPoints([h_left_1, h_left_2])
    .cboreHole(hole_dia, cbore_dia, cbore_depth)
)

# Set 2: Countersunk holes on the thin (right) section
h_right_1 = (50, 40)
h_right_2 = (60, 65)

# Select the face at the height of the thin section
face_selector = cq.NearestToPointSelector((x_max - 20, width_right/2, thin_thickness))

result = (
    result.faces(face_selector)
    .workplane()
    .pushPoints([h_right_1, h_right_2])
    .cskHole(hole_dia, csk_dia, csk_angle)
)
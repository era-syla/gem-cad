import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions roughly estimated from the visual proportions
# (Assuming units in mm)
total_length = 300.0
max_width = 90.0
plate_thickness = 4.0

# Define the geometry relative to the "waist" (widest point)
# Front section (shorter, blunter)
front_length = 80.0
front_tip_width = 50.0

# Rear section (longer, more tapered)
rear_length = 220.0
rear_tip_width = 25.0

# Hole Configurations
# Front tip mounting holes (Countersunk)
front_hole_dia = 5.0
front_csk_dia = 10.0
front_csk_angle = 90.0
front_hole_spacing = 25.0
front_hole_setback = 15.0 # Distance from front edge

# Central chassis mounting holes (Standard)
body_hole_dia = 4.0

# Define body hole pattern coordinates (x, y) relative to waist center (0,0)
# Pattern mimics the cluster visible in the image:
# - A wide pair near the waist
# - A central rectangular group
# - A wide pair further back
body_hole_locations = [
    # Pair 1: Wide spacing near waist (x ~ -20)
    (-20, 30), (-20, -30),
    
    # Pair 2: Narrow spacing (start of center rect)
    (10, 15), (10, -15),
    
    # Pair 3: Narrow spacing (end of center rect)
    (40, 15), (40, -15),
    
    # Pair 4: Wide spacing (rear)
    (60, 25), (60, -25)
]

# --- Modeling ---

# 1. Define the Profile Points (Counter-Clockwise)
# Axis alignment: X is longitudinal, Y is lateral. Origin at max width.
p1 = (-front_length, front_tip_width / 2.0)
p2 = (0.0, max_width / 2.0)
p3 = (rear_length, rear_tip_width / 2.0)
p4 = (rear_length, -rear_tip_width / 2.0)
p5 = (0.0, -max_width / 2.0)
p6 = (-front_length, -front_tip_width / 2.0)

profile_pts = [p1, p2, p3, p4, p5, p6]

# 2. Create Base Plate
result = (
    cq.Workplane("XY")
    .polyline(profile_pts)
    .close()
    .extrude(plate_thickness)
)

# 3. Create Front Countersunk Holes
# Calculate position relative to global origin
front_hole_x = -front_length + front_hole_setback
front_hole_pts = [
    (front_hole_x, front_hole_spacing / 2.0),
    (front_hole_x, -front_hole_spacing / 2.0)
]

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(front_hole_pts)
    .cskHole(diameter=front_hole_dia, 
             cskDiameter=front_csk_dia, 
             cskAngle=front_csk_angle)
)

# 4. Create Body Pattern Holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(body_hole_locations)
    .hole(body_hole_dia)
)
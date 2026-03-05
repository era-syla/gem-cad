import cadquery as cq

# Parametric dimensions for the Bishop
base_diameter = 30.0
base_height = 4.0
collar_height = 2.0
body_lower_diameter = 26.0
neck_diameter = 12.0
neck_height = 35.0
head_collar_diameter = 16.0
head_collar_height = 2.0
head_diameter = 16.0
head_height = 18.0
top_ball_diameter = 4.0
slot_width = 2.0
slot_depth = 8.0
slot_angle = 45.0

# 1. Create the Profile for Revolution
# We will define points for a spline or polyline representing the half-profile of the bishop.
# The profile starts at (0,0) and goes up along the Y-axis.

# Base section
pts = [
    (0, 0),
    (base_diameter / 2, 0),
    (base_diameter / 2, base_height * 0.5),
    (base_diameter / 2 - 2, base_height), # Slight taper in on the first step
]

current_height = base_height

# Main Body (The swooping curve)
# We need a nice curve from the base collar to the neck collar
p_start_body = (base_diameter / 2 - 2, current_height)
p_end_body = (neck_diameter / 2, current_height + neck_height)
p_control_body_1 = (base_diameter / 2 - 2, current_height + neck_height * 0.4) # Control point to keep it wide initially
p_control_body_2 = (neck_diameter / 2 * 1.5, current_height + neck_height * 0.8) # Control point to curve into neck

# Head Collar section
current_height += neck_height
p_start_collar = (neck_diameter / 2, current_height)
p_mid_collar = (head_collar_diameter / 2, current_height)
p_end_collar = (head_collar_diameter / 2, current_height + head_collar_height)

current_height += head_collar_height

# Head (The mitre)
p_start_head = (head_collar_diameter / 2, current_height)
# The head is roughly egg-shaped
p_mid_head = (head_diameter / 2, current_height + head_height * 0.4)
p_end_head = (0, current_height + head_height) # Top tip of the mitre

# Top Ball
current_height += head_height
# We'll add the ball separately as a sphere for cleaner geometry or revolve a small arc here.
# Let's revolve a small arc for the finial ball.
p_ball_center = (0, current_height + top_ball_diameter/2)

# Build the main body using a revolution of the profile
# We construct the wires carefully.
base_wire = cq.Workplane("XY").polyline(pts).close()

# Let's use Splines for the organic shapes
bishop_profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(base_diameter / 2, 0)
    .lineTo(base_diameter / 2, base_height * 0.4)
    # The bottom decorative ridges
    .spline([(body_lower_diameter/2, base_height), (neck_diameter/2, base_height + neck_height)], includeCurrent=True)
    .lineTo(head_collar_diameter/2, base_height + neck_height)
    .lineTo(head_collar_diameter/2, base_height + neck_height + head_collar_height)
    # The head (mitre)
    .spline([(0, base_height + neck_height + head_collar_height + head_height)], 
            tangents=[(0, 1), (0, 1)], includeCurrent=True)
    .lineTo(0, 0)
    .close()
)

# Refined profile approach for better shape control based on the image
# Constructing piecewise to get the sharp transitions (collars) correct
x_axis = cq.Vector(1, 0, 0)
y_axis = cq.Vector(0, 1, 0)
z_axis = cq.Vector(0, 0, 1)

# Base tiers
base_w = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(base_diameter / 2, 0)
    .lineTo(base_diameter / 2, base_height * 0.3)
    .spline([(base_diameter / 2 - 1.5, base_height)], includeCurrent=True)
    .lineTo(0, base_height)
    .close()
    .revolve()
)

# Main Body (Neck)
neck_bottom_y = base_height
neck_top_y = base_height + neck_height
neck_w = (
    cq.Workplane("XZ")
    .moveTo(0, neck_bottom_y)
    .lineTo(base_diameter / 2 - 1.5, neck_bottom_y)
    .spline([(neck_diameter / 2, neck_top_y)], tangents=[(0, 1), (0, 1)], includeCurrent=True)
    .lineTo(0, neck_top_y)
    .close()
    .revolve()
)

# Collar
collar_bottom_y = neck_top_y
collar_top_y = collar_bottom_y + head_collar_height
collar_w = (
    cq.Workplane("XZ")
    .moveTo(0, collar_bottom_y)
    .lineTo(head_collar_diameter / 2, collar_bottom_y)
    .lineTo(head_collar_diameter / 2, collar_top_y)
    .lineTo(0, collar_top_y)
    .close()
    .revolve()
)

# Head (Mitre)
head_bottom_y = collar_top_y
head_top_y = head_bottom_y + head_height
head_w = (
    cq.Workplane("XZ")
    .moveTo(0, head_bottom_y)
    .lineTo(head_collar_diameter / 2 * 0.85, head_bottom_y) # Start slightly inside the collar
    .spline([(0, head_top_y)], tangents=[(0.2, 1), (0, 1)], includeCurrent=True)
    .close()
    .revolve()
)

# Top Ball
ball_center_y = head_top_y + top_ball_diameter/2 * 0.6 # slightly sunk in
ball_w = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, 0, ball_center_y))
    .sphere(top_ball_diameter / 2)
)


# Combine all revolved parts
bishop_solid = base_w.union(neck_w).union(collar_w).union(head_w).union(ball_w)

# Create the Cut (Slot) in the mitre
# The slot is angled. We create a box and subtract it.
cut_center_z = head_bottom_y + (head_height / 2) + 2
cut_box = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, 0, cut_center_z))
    .transformed(rotate=cq.Vector(0, slot_angle, 0))
    .box(head_diameter, slot_width, slot_depth * 2) # Make box large enough to cut through
)

# Apply Fillets to smooth transitions like in the image
# Fillet base
try:
    bishop_solid = bishop_solid.edges(cq.selectors.NearestToPointSelector((base_diameter/2, 0, 0))).fillet(0.5)
except:
    pass # In case selection fails due to geometry specifics

# Fillet neck transition
try:
    bishop_solid = bishop_solid.edges(cq.selectors.NearestToPointSelector((neck_diameter/2, neck_top_y, 0))).fillet(1.0)
except:
    pass

final_bishop = bishop_solid.cut(cut_box)

# Create the second bishop for the scene (just a translation)
bishop2 = final_bishop.translate((base_diameter * 1.5, base_diameter, 0))

# Combine for final result
result = final_bishop.union(bishop2)
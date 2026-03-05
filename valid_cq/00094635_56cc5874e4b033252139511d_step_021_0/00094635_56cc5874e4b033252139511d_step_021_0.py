import cadquery as cq

# Parametric dimensions for the weight/plumb bob
main_diameter = 40.0
main_height = 50.0
bottom_cone_height = 5.0

shoulder_height = 6.0
shoulder_top_diameter = 24.0

collar_height = 4.0
neck_diameter = 16.0
neck_height = 5.0

head_diameter = 30.0
head_height = 6.0

# Derived radii
r_main = main_diameter / 2.0
r_shoulder = shoulder_top_diameter / 2.0
r_neck = neck_diameter / 2.0
r_head = head_diameter / 2.0

# Initialize height tracker
current_z = 0.0
points = []

# Start at the bottom tip (0,0)
points.append((0, current_z))

# 1. Bottom Cone: Move up to the start of the main cylinder
current_z += bottom_cone_height
points.append((r_main, current_z))

# 2. Main Cylinder Body: Vertical line up
current_z += main_height
points.append((r_main, current_z))

# 3. Tapered Shoulder: Angled line inwards
current_z += shoulder_height
points.append((r_shoulder, current_z))

# 4. Collar: Vertical section above the shoulder
current_z += collar_height
points.append((r_shoulder, current_z))

# 5. Neck Groove: Horizontal in, then Vertical up
points.append((r_neck, current_z))  # Move In
current_z += neck_height
points.append((r_neck, current_z))  # Move Up

# 6. Head/Knob: Horizontal out, then Vertical up
points.append((r_head, current_z))  # Move Out
current_z += head_height
points.append((r_head, current_z))  # Move Up

# 7. Top Closure: Return to the Z-axis
points.append((0, current_z))

# Create the revolution solid
result = (
    cq.Workplane("XZ")
    .polyline(points)
    .close()
    .revolve()
)
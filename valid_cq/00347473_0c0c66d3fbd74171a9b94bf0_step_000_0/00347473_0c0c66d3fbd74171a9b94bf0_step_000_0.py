import cadquery as cq

# Parameters for the 3D model dimensions
sphere_radius = 8.0
top_pin_height = 12.0
top_pin_radius = 0.8
long_rod_length = 160.0
long_rod_radius = 0.6
wing_width = 12.0      # Dimension along the rod axis (X)
wing_span = 36.0       # Dimension perpendicular to rod axis (Y)
wing_thickness = 1.5
frame_width = 70.0     # External width of the loop
frame_depth = 45.0     # External depth of the loop
frame_thickness = 1.0  # Thickness of the wireframe

# 1. Central Sphere
# Create the main spherical body centered at the origin
sphere = cq.Workplane("XY").sphere(sphere_radius)

# 2. Top Antenna
# A small cylinder protruding vertically from the top of the sphere
top_antenna = (
    cq.Workplane("XY")
    .workplane(offset=sphere_radius * 0.85)  # Start slightly inside the sphere
    .circle(top_pin_radius)
    .extrude(top_pin_height)
)

# 3. Long Horizontal Rods
# Two long thin rods extending along the X-axis (modeled as one cylinder)
long_rods = (
    cq.Workplane("YZ")
    .circle(long_rod_radius)
    .extrude(long_rod_length)
    .translate((-long_rod_length / 2, 0, 0))
)

# 4. Wings / Cross Structure
# Flat plates extending along the Y-axis, simulating solar panels or fins
wings = (
    cq.Workplane("XY")
    .box(wing_width, wing_span, wing_thickness)
)

# 5. Central Base Plate
# A small rectangular reinforcement plate under the sphere
base_plate = (
    cq.Workplane("XY")
    .box(16, 16, wing_thickness * 1.2)
)

# 6. Rectangular Frame
# A thin rectangular loop surrounding the central assembly on the XY plane
frame = (
    cq.Workplane("XY")
    .rect(frame_width, frame_depth)
    .rect(frame_width - 2 * frame_thickness, frame_depth - 2 * frame_thickness)
    .extrude(frame_thickness)
    .translate((0, 0, -frame_thickness / 2))  # Center vertically at Z=0
)

# Combine all components into the final geometry
result = (
    sphere
    .union(top_antenna)
    .union(long_rods)
    .union(wings)
    .union(base_plate)
    .union(frame)
)
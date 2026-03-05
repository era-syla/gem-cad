import cadquery as cq

# Parametric dimensions to approximate the organic shape
# Coordinates are defined in the XZ plane (X=radius, Z=height)
inner_radius_base = 22.0
inner_radius_top = 22.0
inner_mid_x = 16.0       # Creates the concave inner curvature (arch)
total_height = 42.0
peak_height = 47.0       # Height of the top dome

outer_radius_top = 40.0
outer_bulge_x = 48.0     # Creates the convex outer curvature
step_height = 10.0       # Height of the bottom flange/step feature
step_outer_x = 45.0      # Radius at the top of the step
step_inner_x = 41.0      # Radius at the bottom of the step (recess depth)

revolve_angle = 80.0     # Angle of the partial revolution

# Define key points for the profile
p0_start = (inner_radius_base, 0)
p1_inner_mid = (inner_mid_x, total_height / 2.0)
p2_inner_top = (inner_radius_top, total_height)
p3_peak = ((inner_radius_top + outer_radius_top) / 2.0, peak_height)
p4_outer_top = (outer_radius_top, total_height)
p5_outer_mid = (outer_bulge_x, (total_height + step_height) / 2.0)
p6_step_top = (step_outer_x, step_height)
p7_step_in = (step_inner_x, step_height)
p8_step_bottom = (step_inner_x, 0)

# Create the geometry
result = (
    cq.Workplane("XZ")
    .moveTo(*p0_start)
    # Inner wall: Concave arc creating the arched void
    .threePointArc(p1_inner_mid, p2_inner_top)
    # Top wall: Dome shape connecting inner and outer walls
    .threePointArc(p3_peak, p4_outer_top)
    # Outer wall: Convex arc bulging outwards
    .threePointArc(p5_outer_mid, p6_step_top)
    # Bottom flange feature: Stepped profile
    .lineTo(*p7_step_in)
    .lineTo(*p8_step_bottom)
    .close() # Closes the loop back to p0_start (0 height)
    .revolve(revolve_angle)
)
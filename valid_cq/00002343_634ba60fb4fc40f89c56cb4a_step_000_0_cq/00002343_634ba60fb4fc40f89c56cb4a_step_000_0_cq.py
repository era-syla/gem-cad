import cadquery as cq

# Parametric dimensions
width_overall = 100.0  # Total width (distance between outer cylindrical feet centers)
depth_overall = 80.0   # Total depth (length of the side rods)
foot_diameter = 10.0   # Diameter of the 4 cylindrical feet
foot_height = 8.0      # Height of the 4 cylindrical feet
rod_diameter = 3.0     # Diameter of the connecting rods
crossbar_diameter = 5.0 # Diameter of the central thicker crossbar
crossbar_position = 0.5 # Position of the crossbar along the depth (0.5 = middle)

# Derived dimensions
side_rod_length = depth_overall
crossbar_length = width_overall

# 1. Create the four feet
# Locations for the four corners
feet_locations = [
    (-width_overall / 2, -depth_overall / 2),
    (width_overall / 2, -depth_overall / 2),
    (width_overall / 2, depth_overall / 2),
    (-width_overall / 2, depth_overall / 2)
]

feet = (
    cq.Workplane("XY")
    .pushPoints(feet_locations)
    .circle(foot_diameter / 2)
    .extrude(foot_height)
)

# 2. Create the two side rods
# Left rod connecting front-left and back-left feet
left_rod = (
    cq.Workplane("XY")
    .center(-width_overall / 2, 0) # Center on left side
    .workplane(offset=foot_height/2) # Lift to mid-height of feet
    .transformed(rotate=(90, 0, 0)) # Rotate to extrude along Y
    .circle(rod_diameter / 2)
    .extrude(depth_overall, both=True) # Extrude both ways to cover full depth
)

# Right rod connecting front-right and back-right feet
right_rod = (
    cq.Workplane("XY")
    .center(width_overall / 2, 0) # Center on right side
    .workplane(offset=foot_height/2)
    .transformed(rotate=(90, 0, 0))
    .circle(rod_diameter / 2)
    .extrude(depth_overall, both=True)
)

# 3. Create the central crossbar
# Spanning between the two side rods
crossbar = (
    cq.Workplane("XY")
    .workplane(offset=foot_height/2) # Mid-height of feet
    .transformed(rotate=(0, 90, 0)) # Rotate to extrude along X
    .circle(crossbar_diameter / 2)
    .extrude(width_overall, both=True) # Extrude both ways to span width
)

# Combine everything
result = feet.union(left_rod).union(right_rod).union(crossbar)
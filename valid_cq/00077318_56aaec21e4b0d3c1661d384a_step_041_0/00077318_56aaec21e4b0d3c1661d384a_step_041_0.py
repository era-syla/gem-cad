import cadquery as cq

# -- Parameters --
handle_height = 50.0       # Total height of the handle
handle_width_outer = 100.0 # Distance between outer edges of the legs
thickness = 10.0           # Thickness of the material (cross-section)
depth = 15.0               # Depth of the handle (Y-axis width)
foot_length = 15.0         # Length of the mounting feet extending outwards
hole_diameter = 6.0        # Diameter of the mounting holes

# -- Geometry Coordinates --
# Calculate coordinates for the 2D profile on the XZ plane.
# Origin is at the bottom center of the gap between the legs.
x_leg_outer = handle_width_outer / 2.0
x_leg_inner = x_leg_outer - thickness
x_foot_tip = x_leg_outer + foot_length

y_ground = 0.0
y_foot_top = thickness
y_handle_top = handle_height
y_handle_inner = handle_height - thickness

# Define the points of the profile tracing the material boundary
profile_points = [
    # Start at bottom-left tip of the foot
    (-x_foot_tip, y_ground),
    (-x_foot_tip, y_foot_top),
    (-x_leg_outer, y_foot_top),      # Transition to vertical leg
    (-x_leg_outer, y_handle_top),    # Top-left outer corner
    
    (x_leg_outer, y_handle_top),     # Top-right outer corner
    (x_leg_outer, y_foot_top),       # Transition to foot
    (x_foot_tip, y_foot_top),
    (x_foot_tip, y_ground),          # Bottom-right tip
    
    # Return path along the inner surface
    (x_leg_inner, y_ground),         # Inner bottom of right leg
    (x_leg_inner, y_handle_inner),   # Inner top corner right
    (-x_leg_inner, y_handle_inner),  # Inner top corner left
    (-x_leg_inner, y_ground)         # Inner bottom of left leg
    # The shape automatically closes back to the start point
]

# -- Solid Generation --

# 1. Extrude the main profile
# We extrude from the XZ plane along the Y axis
main_body = (
    cq.Workplane("XZ")
    .polyline(profile_points)
    .close()
    .extrude(depth)
)

# 2. Cut mounting holes
# Calculate hole centers
hole_x_offset = x_leg_outer + (foot_length / 2.0)
hole_y_center = depth / 2.0

# Create a cutting tool (cylinders) on the XY plane
# Since the feet sit on the ground (Z=0) and are 'thickness' high,
# we extrude the cutter from Z=0 to Z=thickness.
cutters = (
    cq.Workplane("XY")
    .pushPoints([
        (-hole_x_offset, hole_y_center),  # Left hole position
        (hole_x_offset, hole_y_center)    # Right hole position
    ])
    .circle(hole_diameter / 2.0)
    .extrude(thickness)
)

# Subtract the cutters from the main body
result = main_body.cut(cutters)
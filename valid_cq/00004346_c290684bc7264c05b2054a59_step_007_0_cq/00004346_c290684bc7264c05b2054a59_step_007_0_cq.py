import cadquery as cq

# --- Parameter Definitions ---
thickness = 10.0      # Thickness of the plate
top_radius = 20.0     # Radius of the semi-circular top
top_width = top_radius * 2
straight_height = 15.0 # Height of the straight vertical section below the semi-circle
flare_angle = 15.0    # Angle of the side flares
bottom_radius = 80.0  # Radius of the large bottom arc
total_height = 90.0   # Approximate total height

# Hole parameters
hole_diameter = 4.0
# Coordinates for the four holes based on visual estimation relative to the top center
# Top row holes
top_hole_dx = 10.0
top_hole_dy = 0.0     # Relative to the center of the top arc
# Bottom row holes
bottom_hole_dx = 12.0
bottom_hole_dy = -20.0 # Distance down from the top holes

# --- Geometry Construction ---

# We will construct the 2D profile first
# The origin (0,0) will be the center of the top semi-circle

# Create the main outline
# 1. Start at the left tangent point of the top arc
# 2. Go up and around the arc to the right tangent point
# 3. Go down the straight section
# 4. Flare outwards to the bottom
# 5. Connect the bottom with a large arc

# Calculate key points
p_top_center = (0, 0)
p_top_right_tangent = (top_radius, 0)
p_top_left_tangent = (-top_radius, 0)

# End of straight section
p_straight_right = (top_radius, -straight_height)
p_straight_left = (-top_radius, -straight_height)

# Bottom corners (calculated simply for the sketch, the arc will define the bottom)
# We need to determine where the side lines end. Let's assume a total length
# and simple flaring lines.
# Let's define the side lines by vectors or endpoints.
# The sides flare out.
bottom_width_half = 35.0 # Estimate
p_bottom_right = (bottom_width_half, -total_height + top_radius) 
p_bottom_left = (-bottom_width_half, -total_height + top_radius)

# Constructing the sketch
result = (
    cq.Workplane("XY")
    # Start at the top left of the straight section
    .moveTo(*p_straight_left)
    # Line up to start of arc
    .lineTo(*p_top_left_tangent)
    # Top semi-circle
    .threePointArc((0, top_radius), p_top_right_tangent)
    # Line down straight section
    .lineTo(*p_straight_right)
    # Flared side line
    .lineTo(*p_bottom_right)
    # Bottom curved edge (large radius arc)
    .radiusArc(p_bottom_left, -bottom_radius)
    # Close the shape back to start
    .lineTo(*p_straight_left)
    .close()
    .extrude(thickness)
)

# --- Adding Holes ---
# We have a pattern of 4 holes.
# It looks like a rectangular pattern or slightly trapezoidal. 
# Let's assume a rectangular pattern centered horizontally.

holes = [
    (-top_hole_dx, top_hole_dy),
    (top_hole_dx, top_hole_dy),
    (-bottom_hole_dx, bottom_hole_dy),
    (bottom_hole_dx, bottom_hole_dy)
]

for x, y in holes:
    result = result.faces(">Z").workplane().center(x, y).hole(hole_diameter)

# Result is stored in the 'result' variable
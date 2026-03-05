import cadquery as cq

# --- Parametric Dimensions ---
# House body dimensions
house_length = 40.0
house_width = 30.0
wall_height = 25.0
roof_peak_height = 15.0  # Height from top of wall to roof peak

# Chimney dimensions
chimney_width = 6.0
chimney_depth = 6.0
chimney_height = 10.0 # Height extending above the roof surface approx
chimney_x_offset = 5.0 # Offset from the center along the length
chimney_y_offset = 5.0 # Offset from the center along the width (on the slope)

# --- Modeling ---

# 1. Create the main house body (box + roof prism)
# Strategy: Create a sketch on the front face (XZ plane) and extrude it.
# We will draw the pentagon shape of the house profile.

points = [
    (0, 0),
    (house_width, 0),
    (house_width, wall_height),
    (house_width / 2, wall_height + roof_peak_height),
    (0, wall_height)
]

# Create the main extrusion
house = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(house_length)
)

# Rotate to match the typical Z-up orientation if needed, 
# but currently it's extruded along Z based on XY plane sketch, 
# so 'house_length' is the Z height. 
# Let's re-orient to make Z "up" for the roof peak.
# The sketch was X (width) and Y (height). Extrusion was Z (length).
# Let's rebuild more intuitively: Sketch on Front Plane (XZ), extrude along Y (length).

# Revised Strategy:
# X axis: width
# Z axis: height
# Y axis: length

pts = [
    (-house_width / 2, 0),
    (house_width / 2, 0),
    (house_width / 2, wall_height),
    (0, wall_height + roof_peak_height),
    (-house_width / 2, wall_height)
]

main_body = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .extrude(house_length)
)

# 2. Create the Chimney
# The chimney needs to sit on the roof. 
# It looks like a simple box that intersects the roof.
# We can just create a box and union it.

chimney = (
    cq.Workplane("XY")
    .workplane(offset=wall_height + roof_peak_height / 2) # Start somewhat high up
    .center(-chimney_x_offset, chimney_y_offset) # Position relative to center
    .box(chimney_width, chimney_depth, chimney_height * 2) # Make it tall enough to sink into roof
)

# 3. Combine parts
result = main_body.union(chimney)

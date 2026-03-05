import cadquery as cq

# Model parameters
v_height = 80.0       # Height of the vertical section
v_thickness = 25.0    # Width (X) of the vertical section
depth = 20.0          # Depth (Y) of the entire part
h_length = 100.0      # Total length (X)
h_height = 25.0       # Height of the horizontal section

pocket_len = 40.0     # Length of the rectangular pocket
pocket_width = 12.0   # Width of the rectangular pocket
pocket_depth = 5.0    # Depth of the cut

# Define the points for the L-shape profile in the XZ plane
# Starting from bottom-left (0,0)
pts = [
    (0, 0),
    (h_length, 0),
    (h_length, h_height),
    (v_thickness, h_height),
    (v_thickness, v_height),
    (0, v_height)
]

# Create the base solid
result = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .extrude(depth)
)

# Calculate a point on the target face (top of horizontal leg) to aid selection
# Center of the horizontal arm area
target_x = v_thickness + (h_length - v_thickness) / 2
target_y = depth / 2
target_z = h_height

# Create the pocket
result = (
    result
    .faces("+Z")  # Select faces with normal pointing up
    .faces(cq.NearestToPointSelector((target_x, target_y, target_z))) # Filter for the lower horizontal face
    .workplane()
    .rect(pocket_len, pocket_width)
    .cutBlind(-pocket_depth)
)
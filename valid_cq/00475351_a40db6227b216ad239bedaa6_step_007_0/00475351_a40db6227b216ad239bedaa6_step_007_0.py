import cadquery as cq

# Parametric dimensions
shank_diameter = 10.0
shank_length = 40.0
head_diameter = 20.0
head_height = 6.0
chamfer_size = 1.0

# Calculated radii
r_shank = shank_diameter / 2.0
r_head = head_diameter / 2.0

# Define the profile points for revolution on the XZ plane
# Coordinates are (x=radius, y=height along Z axis)
profile_points = [
    (0, 0),                                  # Center bottom
    (r_shank, 0),                            # Shank outer edge bottom
    (r_shank, shank_length),                 # Shank meets Head
    (r_head, shank_length + head_height),    # Head outer rim
    (0, shank_length + head_height)          # Center top
]

# Create the rivet geometry
result = (
    cq.Workplane("XZ")
    .polyline(profile_points)
    .close()
    .revolve()  # Revolves 360 degrees around the Z-axis (local Y of XZ plane)
)

# Apply chamfer to the tail end of the shank
# We select the edge closest to the outer radius at Z=0
result = result.edges(cq.NearestToPointSelector((r_shank, 0, 0))).chamfer(chamfer_size)
import cadquery as cq

# Define parametric dimensions
length = 100.0  # Total length of the building
width = 50.0    # Width of the base
wall_height = 40.0  # Height of the vertical walls
roof_height = 15.0  # Height of the roof peak relative to the top of the walls

# Create the profile of the "house" shape on the front face (XZ plane)
# We start at the bottom-left corner and trace the outline
profile_pts = [
    (0, 0),                      # Bottom-left
    (width, 0),                  # Bottom-right
    (width, wall_height),        # Top of right wall
    (width / 2.0, wall_height + roof_height), # Roof peak
    (0, wall_height),            # Top of left wall
    (0, 0)                       # Close the loop
]

# Create the solid by extruding the profile
# We draw on the YZ plane (or XZ plane) and extrude along the length
result = (
    cq.Workplane("XY")
    .polyline(profile_pts)
    .close()
    .extrude(length)
)

# Optional: If you prefer the length to be along X, width along Y, height along Z:
# result = (
#     cq.Workplane("front") # XZ plane
#     .polyline(profile_pts)
#     .close()
#     .extrude(length)
# )
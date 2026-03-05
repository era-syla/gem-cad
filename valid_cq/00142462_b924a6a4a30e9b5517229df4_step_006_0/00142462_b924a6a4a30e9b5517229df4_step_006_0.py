import cadquery as cq

# Parametric dimensions for the profile
length = 150.0          # Total length of the part
total_height = 60.0     # Total height
base_width = 15.0       # Width of the bottom-most section
base_height = 12.0      # Height of the bottom-most section
mid_width = 10.0        # Width of the middle section
mid_height_top = 45.0   # Z-height where the middle section ends
top_width = 6.0         # Width of the top section
chamfer_size = 2.0      # Size of the 45-degree chamfer at the top-front edge

# Define points for the cross-sectional profile on the YZ plane.
# Coordinates are (y, z) where y is thickness/width and z is height.
# The profile assumes the back face is flat against y=0.
profile_points = [
    (0, 0),                                       # Bottom-Back corner
    (base_width, 0),                              # Bottom-Front corner
    (base_width, base_height),                    # Top of base section
    (mid_width, base_height),                     # Step in to middle section
    (mid_width, mid_height_top),                  # Top of middle section
    (top_width, mid_height_top),                  # Step in to top section
    (top_width, total_height - chamfer_size),     # Start of chamfer on vertical face
    (top_width - chamfer_size, total_height),     # End of chamfer on top face
    (0, total_height)                             # Top-Back corner
]

# Generate the 3D model
# 1. Select the YZ plane to draw the profile (X axis will be the extrusion direction)
# 2. Draw the polyline defined by the points
# 3. Close the profile
# 4. Extrude along the X axis
result = (
    cq.Workplane("YZ")
    .polyline(profile_points)
    .close()
    .extrude(length)
)
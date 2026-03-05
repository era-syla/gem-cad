import cadquery as cq

# Parametric dimensions
length = 120.0          # Total length of the part
width = 50.0            # Total width of the base
base_thickness = 10.0   # Thickness of the main plate
ridge_height = 5.0      # Additional height of the ridge above the base
ridge_top_width = 4.0   # Width of the flat top of the ridge
chamfer_width = 5.0     # Horizontal width of the sloped section

# Derived dimension
total_height = base_thickness + ridge_height

# Define the cross-section profile
# We sketch on the YZ plane (Right plane) and extrude along the X axis
# Local coordinates for the sketch are (Y, Z)
profile_points = [
    (0, 0),                                            # Bottom-left (Rear-bottom)
    (width, 0),                                        # Bottom-right (Front-bottom)
    (width, base_thickness),                           # Top-right (Front-top of base)
    (ridge_top_width + chamfer_width, base_thickness), # Start of slope on base surface
    (ridge_top_width, total_height),                   # Top of slope / Start of ridge top
    (0, total_height),                                 # Top-left (Rear-top of ridge)
    (0, 0)                                             # Close loop
]

# Generate the 3D model
result = (
    cq.Workplane("YZ")
    .polyline(profile_points)
    .close()
    .extrude(length)
)
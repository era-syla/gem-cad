import cadquery as cq

# Parametric dimensions based on the visual proportions of the image
inner_diameter = 80.0
base_outer_diameter = 92.0
top_outer_diameter = 86.0
base_height = 3.0
top_height = 4.0

# Derived dimensions
r_inner = inner_diameter / 2.0
r_base = base_outer_diameter / 2.0
r_top = top_outer_diameter / 2.0
total_height = base_height + top_height

# Define the cross-section profile points (radius, height)
# Starting from the bottom-inner corner and moving counter-clockwise
profile_points = [
    (r_inner, 0),                   # Bottom Inner
    (r_base, 0),                    # Bottom Outer
    (r_base, base_height),          # Flange Step Outer
    (r_top, base_height),           # Flange Step Inner
    (r_top, total_height),          # Top Outer
    (r_inner, total_height),        # Top Inner
    (r_inner, 0)                    # Close Loop
]

# Create the model by revolving the profile around the Z-axis
result = (
    cq.Workplane("XZ")
    .polyline(profile_points)
    .close()
    .revolve(360.0)
)
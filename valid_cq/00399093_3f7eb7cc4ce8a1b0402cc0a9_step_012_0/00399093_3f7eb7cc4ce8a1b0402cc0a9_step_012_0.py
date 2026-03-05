import cadquery as cq

# Parametric dimensions
total_length = 80.0       # Total length of the nozzle
cylinder_length = 20.0    # Length of the straight cylindrical section
large_diameter = 35.0     # Outer diameter at the base
small_diameter = 12.0     # Outer diameter at the tip
wall_thickness = 4.0      # Thickness of the wall

# Derived radii
r_large_outer = large_diameter / 2.0
r_small_outer = small_diameter / 2.0
r_large_inner = r_large_outer - wall_thickness
r_small_inner = r_small_outer - wall_thickness

# Define points for the revolution profile on the XZ plane
# X corresponds to radial distance, Y (local) corresponds to axial height (Global Z)
profile_points = [
    (r_large_inner, 0),                    # Inner bottom
    (r_large_outer, 0),                    # Outer bottom
    (r_large_outer, cylinder_length),      # Outer transition cylinder->cone
    (r_small_outer, total_length),         # Outer top
    (r_small_inner, total_length),         # Inner top
    (r_large_inner, cylinder_length),      # Inner transition (maintains cylindrical bore in base)
    (r_large_inner, 0)                     # Close the loop
]

# Create the solid by revolving the profile 360 degrees around the Z-axis
result = (
    cq.Workplane("XZ")
    .polyline(profile_points)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)
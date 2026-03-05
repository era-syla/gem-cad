import cadquery as cq

# Parametric dimensions for the roller shaft
main_diameter = 12.0
main_length = 150.0
stub_diameter = 8.0
stub_length = 6.0

# Calculate radii
r_main = main_diameter / 2.0
r_stub = stub_diameter / 2.0

# Define the points for the revolution profile on the XZ plane.
# The profile represents half of the cross-section to be revolved around the Z-axis.
points = [
    (0, 0),                                           # Start at bottom center
    (r_stub, 0),                                      # Bottom stub outer edge
    (r_stub, stub_length),                            # Bottom stub shoulder corner
    (r_main, stub_length),                            # Main shaft bottom corner
    (r_main, stub_length + main_length),              # Main shaft top corner
    (r_stub, stub_length + main_length),              # Top stub shoulder corner
    (r_stub, stub_length + main_length + stub_length),# Top stub top edge
    (0, stub_length + main_length + stub_length)      # End at top center
]

# Create the 3D model by revolving the profile 360 degrees
result = (
    cq.Workplane("XZ")
    .polyline(points)
    .close()
    .revolve()
)
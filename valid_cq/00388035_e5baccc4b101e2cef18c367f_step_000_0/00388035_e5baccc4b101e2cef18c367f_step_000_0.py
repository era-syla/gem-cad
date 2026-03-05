import cadquery as cq

# Parametric dimensions for the tapered ring/cone model
base_outer_radius = 30.0
top_outer_radius = 22.0
height = 10.0
thickness = 2.0

# Calculate inner coordinates assuming a horizontal wall thickness
# (This creates flat top and bottom faces)
base_inner_radius = base_outer_radius - thickness
top_inner_radius = top_outer_radius - thickness

# Define the points for the trapezoidal cross-section
# Defined on the XZ plane: (Radial Distance, Height)
points = [
    (base_outer_radius, 0),
    (top_outer_radius, height),
    (top_inner_radius, height),
    (base_inner_radius, 0)
]

# Generate the 3D solid by revolving the profile
result = (
    cq.Workplane("XZ")
    .polyline(points)
    .close()
    .revolve()  # Default axis for XZ plane is the Z-axis
)
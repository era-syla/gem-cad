import cadquery as cq

# Geometric parameters based on the visual estimation of the model
outer_radius = 50.0       # Radius of the outer edge of the cone
inner_hole_radius = 6.0   # Radius of the central hole
boss_radius = 12.0        # Radius where the flat center transitions to the cone
cone_height = 20.0        # Vertical distance from center plane to outer rim
thickness = 2.5           # Material thickness

# Define the points for the cross-sectional profile on the XZ plane
# The profile represents half of the shape to be revolved around the Z-axis
# Z=0 represents the bottom face of the flat central area
points = [
    (inner_hole_radius, 0),                 # Start at inner hole bottom
    (boss_radius, 0),                       # End of flat boss area
    (outer_radius, -cone_height),           # Outer rim bottom (sloping down)
    (outer_radius, -cone_height + thickness), # Outer rim top
    (boss_radius, thickness),               # Start of flat boss area top
    (inner_hole_radius, thickness)          # End at inner hole top
]

# Generate the 3D model by creating the profile and revolving it
result = (
    cq.Workplane("XZ")
    .polyline(points)
    .close()
    .revolve()  # Revolve 360 degrees around the Z-axis
)
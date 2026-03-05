import cadquery as cq

# Parametric dimensions for the cone
base_radius = 15.0  # Radius of the circular base
cone_height = 40.0  # Total height from base to apex

# Generate the 3D model
# We sketch a right-angled triangle on the XZ plane (Front plane)
# and revolve it around the vertical axis (Local Y of XZ plane corresponds to Global Z)
result = (
    cq.Workplane("XZ")
    .polyline([(0, 0), (base_radius, 0), (0, cone_height)])
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)
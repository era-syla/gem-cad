import cadquery as cq

# Parametric dimensions based on visual estimation
rod_length = 60.0      # Length of the rods
rod_diameter = 12.0    # Diameter of the rods
rod_spacing = 35.0     # Center-to-center distance between the rods

# Create the CAD model
# We sketch on the XZ plane (Front) and extrude along the Y axis (Depth)
# to create two parallel cylindrical rods.
result = (
    cq.Workplane("XZ")
    .pushPoints([(-rod_spacing / 2, 0), (rod_spacing / 2, 0)])
    .circle(rod_diameter / 2)
    .extrude(rod_length)
)
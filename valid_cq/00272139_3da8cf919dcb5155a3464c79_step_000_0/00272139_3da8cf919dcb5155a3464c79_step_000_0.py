import cadquery as cq

# Parametric dimensions for the reducer/nozzle geometry
base_diameter = 40.0
base_height = 25.0
cone_height = 45.0
top_diameter = 18.0
top_height = 15.0
wall_thickness = 1.5

# derived parameters
r_base = base_diameter / 2.0
r_top = top_diameter / 2.0
total_height = base_height + cone_height + top_height

# Define the points for the revolution profile (half-section) on the XZ plane.
# The profile starts at the center axis, outlines the outer shape, and returns to the axis.
points = [
    (0, 0),                                      # Center bottom
    (r_base, 0),                                 # Base outer radius
    (r_base, base_height),                       # Top of base cylinder
    (r_top, base_height + cone_height),          # Top of tapered section
    (r_top, total_height),                       # Top of upper cylinder
    (0, total_height)                            # Center top
]

# Generate the base solid
# 1. Create a workplane on XZ
# 2. Draw the polyline profile
# 3. Revolve 360 degrees around the Z-axis (vertical axis of the plane)
result = (
    cq.Workplane("XZ")
    .polyline(points)
    .close()
    .revolve()
)

# Hollow out the object
# 1. Select the top (>Z) and bottom (<Z) faces
# 2. Apply shell with negative thickness to remove selected faces and hollow inwards
result = result.faces("<Z or >Z").shell(-wall_thickness)
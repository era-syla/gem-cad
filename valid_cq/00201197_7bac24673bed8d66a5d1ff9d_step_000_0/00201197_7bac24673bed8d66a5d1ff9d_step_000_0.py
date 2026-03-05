import cadquery as cq

# --- Parameters ---
length = 100.0        # Distance between the centers of the two holes
end_radius = 12.0     # Outer radius of the cylindrical ends
hole_radius = 6.0     # Radius of the inner holes
bar_width = 14.0      # Width of the rectangular connecting section
thickness = 10.0      # Thickness (height) of the extrusion

# --- Modeling ---

# 1. Create the left cylindrical end
# Centered at -length/2 on the X axis
left_cylinder = (
    cq.Workplane("XY")
    .center(-length / 2.0, 0)
    .circle(end_radius)
    .extrude(thickness)
)

# 2. Create the right cylindrical end
# Centered at length/2 on the X axis
right_cylinder = (
    cq.Workplane("XY")
    .center(length / 2.0, 0)
    .circle(end_radius)
    .extrude(thickness)
)

# 3. Create the central connecting bar
# A rectangle centered at (0,0) spanning the distance between the cylinders
# The length of the rectangle equals the center-to-center distance to ensure connection
bar = (
    cq.Workplane("XY")
    .rect(length, bar_width)
    .extrude(thickness)
)

# 4. Combine the base geometries
# Union the cylinders and the bar into a single solid
base_solid = left_cylinder.union(right_cylinder).union(bar)

# 5. Cut the holes
# Select the top face, push points to the cylinder centers, and cut
result = (
    base_solid
    .faces(">Z")
    .workplane()
    .pushPoints([(-length / 2.0, 0), (length / 2.0, 0)])
    .circle(hole_radius)
    .cutThruAll()
)
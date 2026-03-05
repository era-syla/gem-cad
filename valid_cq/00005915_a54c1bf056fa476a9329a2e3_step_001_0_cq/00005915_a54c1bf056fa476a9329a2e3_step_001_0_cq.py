import cadquery as cq

# Parameters for the linkage arm
# Top solid cylinder dimensions
top_cyl_diameter = 10.0
top_cyl_length = 20.0

# Bottom hollow cylinder dimensions
bottom_cyl_outer_diameter = 12.0
bottom_cyl_inner_diameter = 8.0
bottom_cyl_length = 10.0

# Connecting shaft (rod) dimensions
shaft_width = 4.0
shaft_thickness = 4.0
center_distance = 60.0  # Distance between centers of top and bottom cylinders

# Create the top cylinder
# We'll orient the cylinders along the Y axis for this example
top_cylinder = (
    cq.Workplane("XZ")
    .circle(top_cyl_diameter / 2.0)
    .extrude(top_cyl_length)
    .translate((0, -top_cyl_length / 2.0, center_distance / 2.0))
)

# Create the bottom cylinder
bottom_cylinder = (
    cq.Workplane("XZ")
    .circle(bottom_cyl_outer_diameter / 2.0)
    .extrude(bottom_cyl_length)
    .translate((0, -bottom_cyl_length / 2.0, -center_distance / 2.0))
)

# Cut the hole in the bottom cylinder
bottom_cylinder = bottom_cylinder.faces(">Y").workplane().circle(bottom_cyl_inner_diameter / 2.0).cutThruAll()

# Create the connecting shaft
# This connects the outer surfaces of the cylinders
shaft = (
    cq.Workplane("XY")
    .rect(shaft_width, shaft_thickness)
    .extrude(center_distance)
    .translate((0, 0, -center_distance / 2.0))
)

# Combine all parts
result = top_cylinder.union(bottom_cylinder).union(shaft)
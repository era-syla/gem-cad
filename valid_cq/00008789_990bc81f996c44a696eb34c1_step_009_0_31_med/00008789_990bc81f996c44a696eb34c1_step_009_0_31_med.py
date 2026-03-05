import cadquery as cq

# Parameters for the geometric model
length = 100.0
width = 80.0
thickness = 5.0
chamfer_size = 35.0
hole_dist_x = 55.0
hole_dist_y = 40.0
hole_dia = 6.0

# Create the base rectangular plate
result = cq.Workplane("XY").box(length, width, thickness)

# Chamfer one of the corners to match the asymmetrical shape
# The selector "|Z and >X and <Y" grabs the specific vertical edge at the +X, -Y corner
result = result.edges("|Z and >X and <Y").chamfer(chamfer_size)

# Add the four through-holes using a construction rectangle
result = (
    result.faces(">Z").workplane()
    .rect(hole_dist_x, hole_dist_y, forConstruction=True)
    .vertices()
    .hole(hole_dia)
)
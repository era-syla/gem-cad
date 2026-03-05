import cadquery as cq

# Define plate parameters
thickness = 5
top_width = 90
top_flat_height = 15
total_height = 110
bottom_radius = 12

# Create the main outer plate
plate = (
    cq.Workplane("XY")
    .moveTo(-45, 60)
    .lineTo(45, 60)
    .lineTo(45, 45)
    .lineTo(12, -40)
    .threePointArc((0, -52), (-12, -40))
    .lineTo(-45, 45)
    .close()
    .extrude(thickness)
)

# Apply a small fillet to the outer vertical edges
plate = plate.edges("|Z").fillet(2)

# Add the central hole
plate = plate.faces(">Z").workplane().center(0, 10).hole(22)

# Add the top row of holes
plate = (
    plate.faces(">Z").workplane()
    .pushPoints([(-35, 52), (-15, 52), (15, 52), (35, 52)])
    .hole(6)
)

# Add the bottom holes
plate = (
    plate.faces(">Z").workplane()
    .pushPoints([(0, -25), (0, -40)])
    .hole(6)
)

# Create the internal cutouts using a separate tool body to easily apply fillets
cutout_tool = (
    cq.Workplane("XY").workplane(offset=-2)
    # Bottom cutout
    .moveTo(-6, -14)
    .lineTo(6, -14)
    .lineTo(15, 0)
    .lineTo(0, -4)
    .lineTo(-15, 0)
    .close()
    # Top left cutout
    .moveTo(-38, 42)
    .lineTo(-11, 42)
    .lineTo(-15, 24)
    .lineTo(-30, 24)
    .close()
    # Top right cutout
    .moveTo(38, 42)
    .lineTo(11, 42)
    .lineTo(15, 24)
    .lineTo(30, 24)
    .close()
    .extrude(thickness + 4)
)

# Fillet the corners of the cutouts
cutout_tool = cutout_tool.edges("|Z").fillet(3)

# Subtract the cutouts from the main plate
result = plate.cut(cutout_tool)
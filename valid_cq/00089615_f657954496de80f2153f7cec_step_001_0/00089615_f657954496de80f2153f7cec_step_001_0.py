import cadquery as cq

# Parametric dimensions
length = 80.0
width = 50.0
plate_thickness = 10.0
rib_width = 25.0
rib_height = 15.0
fillet_radius = 6.0
cutout_radius = 16.0

# 1. Create the Top Plate
# We start with a rectangle on the XY plane and extrude upwards
plate = (
    cq.Workplane("XY")
    .rect(length, width)
    .extrude(plate_thickness)
    .edges("|Z")  # Select vertical edges for filleting
    .fillet(fillet_radius)
)

# 2. Create the Bottom Rib
# We start on the XY plane and extrude downwards
rib = (
    cq.Workplane("XY")
    .rect(length, rib_width)
    .extrude(-rib_height)
)

# 3. Combine Plate and Rib into a single solid
base_geo = plate.union(rib)

# 4. Create the Semi-Circular Cutout
# We select the top face, move to the edge midpoint, and cut through the entire assembly
result = (
    base_geo
    .faces(">Z")
    .workplane()
    .moveTo(0, -width / 2.0)  # Move to the center of the front edge
    .circle(cutout_radius)
    .cutThruAll()
)
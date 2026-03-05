import cadquery as cq

# Parameter definitions
height_tall = 40.0
width_tall = 15.0
height_low = 15.0
length_total = 60.0
depth = 15.0
fillet_radius = 5.0
hole_diameter = 4.0
cutout_radius = 7.0
text_size = 10.0
text_extrusion = 2.0

# 1. Base L-Shape Geometry
# Create the profile on the XZ plane and extrude along Y
result = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(length_total, 0)
    .lineTo(length_total, height_low)
    .lineTo(width_tall, height_low)
    .lineTo(width_tall, height_tall)
    .lineTo(0, height_tall)
    .close()
    .extrude(depth)
)

# 2. Fillet the top-front edge
# Selecting the edge at the top (Z max) and front (Y min)
result = result.edges(">Z and <Y").fillet(fillet_radius)

# 3. Hole on the Left Face (Top section)
# Face <X (X=0 plane), projected origin allows using global Y, Z coordinates locally
result = (
    result.faces("<X")
    .workplane(centerOption="ProjectedOrigin")
    .moveTo(depth / 2, height_tall - 8.0)
    .hole(hole_diameter)
)

# 4. Hole on the Front Face (Bottom section)
# Face <Y (Y=0 plane), projected origin allows using global X, Z coordinates locally
result = (
    result.faces("<Y")
    .workplane(centerOption="ProjectedOrigin")
    .moveTo(width_tall / 2, height_low / 2)
    .hole(hole_diameter)
)

# 5. Hole on the Right Face
# Face >X, using center of bounding box to place hole in the middle of the face
result = (
    result.faces(">X")
    .workplane(centerOption="CenterOfBoundBox")
    .hole(hole_diameter)
)

# 6. U-Cutout on the Lower Shelf
# Select the top face of the lower section using a point selector
cutout_center_x = width_tall + (length_total - width_tall) / 2
result = (
    result.faces(cq.NearestToPointSelector((cutout_center_x, depth/2, height_low)))
    .workplane(centerOption="CenterOfBoundBox")
    # Move to the back edge (local Y max) to create a U-shaped cutout
    .moveTo(0, depth / 2)
    .hole(cutout_radius * 2)
)

# 7. Embossed "R" Text
# Place text on the front face, offset from the inner corner
text_x_pos = width_tall + 6.0
text_z_pos = height_low / 2
result = (
    result.faces("<Y")
    .workplane(centerOption="ProjectedOrigin")
    .moveTo(text_x_pos, text_z_pos)
    .text("R", text_size, text_extrusion)
)
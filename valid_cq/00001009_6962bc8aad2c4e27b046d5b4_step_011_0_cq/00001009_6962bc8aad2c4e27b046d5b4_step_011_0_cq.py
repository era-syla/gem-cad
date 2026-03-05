import cadquery as cq

# -- Parameters --
# Dimensions derived from visual estimation of standard mechanical proportions
# Cylinder (Barrel)
cyl_outer_diam = 20.0
cyl_length = 30.0

# Flange
flange_thickness = 8.0
flange_width = 40.0  # Total width
flange_height = 28.0 # Total height
flange_corner_radius = 14.0 # Rounded ends (semi-circle if radius = height/2)

# Holes
center_hole_diam = 10.0
mounting_hole_diam = 4.0
mounting_hole_spacing = 26.0 # Distance between centers of small holes

# -- Modeling --

# 1. Create the cylindrical barrel
# Oriented along Z-axis initially
barrel = cq.Workplane("XY").circle(cyl_outer_diam / 2.0).extrude(cyl_length)

# 2. Create the Flange
# We'll sketch this on the top face of the barrel (or rather, the XY plane at z=0)
# The image shows the flange perpendicular to the cylinder axis.
# Let's build the flange profile. It looks like a rectangle with rounded sides (slot shape) 
# or a rectangle with large fillets.
flange_sk = (
    cq.Sketch()
    .rect(flange_width, flange_height)
    .vertices()
    .fillet(flange_corner_radius) # Heavily rounded corners to match the look
)

# Extrude the flange. 
# We extrude it in the opposite direction of the barrel so the barrel sticks out of it, 
# or we can position it at the end. In the image, the barrel extends back from the flange.
flange = (
    cq.Workplane("XY")
    .placeSketch(flange_sk)
    .extrude(-flange_thickness)
)

# 3. Combine initial bodies
part = barrel.union(flange)

# 4. Create the Through Hole (Center)
part = part.faces(">Z").workplane().hole(center_hole_diam)

# 5. Create Mounting Holes
# These are on the flange face.
part = (
    part.faces("<Z") # Select the back face of the flange (flat side)
    .workplane()
    .pushPoints([(-mounting_hole_spacing / 2.0, 0), (mounting_hole_spacing / 2.0, 0)])
    .hole(mounting_hole_diam)
)

# 6. Final cleanup / Orientation
# To match the isometric view in the image better:
# The cylinder points roughly -Y or -X depending on convention. 
# Let's rotate it to align nicely.
result = part

# If needed to match the specific camera angle of the prompt image visually:
# (Optional, but 'result' variable is required)
result = result.rotate((0, 0, 0), (1, 0, 0), -90) # Rotate so cylinder points along Y
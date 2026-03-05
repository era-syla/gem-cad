import cadquery as cq

# Parameters for the geometry
width = 160.0
depth = 80.0
thickness = 6.0
fillet_radius = 4.0

pad_inset = 4.0
pad_height = 1.2

base_inset_x = 20.0
base_inset_y = 10.0
base_height = 6.0

lip_extension = 25.0
lip_thickness = 5.0
lip_tip_height = 2.0  # Height of the tip relative to the bottom of the main plate

# 1. Create the Main Plate
# A rectangular box with rounded corners
main_plate = (
    cq.Workplane("XY")
    .box(width, depth, thickness)
    .edges("|Z")
    .fillet(fillet_radius)
)

# 2. Create the Top Pad
# Raised surface on top of the plate
top_pad = (
    main_plate.faces(">Z")
    .workplane()
    .rect(width - 2 * pad_inset, depth - 2 * pad_inset)
    .extrude(pad_height)
    .edges("|Z")
    .fillet(fillet_radius)
)

# 3. Create the Bottom Base/Stand
# A block underneath the main plate, inset from the edges
bottom_base = (
    main_plate.faces("<Z")
    .workplane()
    .rect(width - 2 * base_inset_x, depth - 2 * base_inset_y)
    .extrude(base_height)  # Extrudes in the normal direction (downwards)
)

# 4. Create the Front Lip
# Define the profile on the side (YZ plane) and extrude across the width
# Coordinates are relative to the center of the main_plate box
# Front face y = -depth/2, Top z = thickness/2, Bottom z = -thickness/2

p_bottom_conn = (-depth / 2, -thickness / 2)
p_top_conn = (-depth / 2, thickness / 2)
p_tip_bottom = (-depth / 2 - lip_extension, -thickness / 2 + lip_tip_height)
p_tip_top = (-depth / 2 - lip_extension + 2, -thickness / 2 + lip_tip_height + lip_thickness)

lip_profile = (
    cq.Workplane("YZ")
    .workplane(offset=width / 2)  # Move sketch plane to the positive X face
    .moveTo(*p_bottom_conn)
    .lineTo(*p_tip_bottom)
    .lineTo(*p_tip_top)
    .lineTo(*p_top_conn)
    .close()
    .extrude(-width)  # Extrude to the negative X face
)

# Union the parts so far
result = bottom_base.union(lip_profile)

# 5. Style the Lip (Tapered Ends)
# Cut the corners of the lip to create the tapered look
taper_width = 20.0
cutter_l = (
    cq.Workplane("XY")
    .workplane(offset=-20)
    .moveTo(-width / 2, -depth / 2)
    .lineTo(-width / 2, -depth / 2 - lip_extension - 5)
    .lineTo(-width / 2 + taper_width, -depth / 2 - lip_extension - 5)
    .close()
    .extrude(50)  # Cut vertically through
)

cutter_r = cutter_l.mirror("YZ")  # Mirror for the right side

result = result.cut(cutter_l).cut(cutter_r)

# 6. Center Detail on Lip
# Create a recess/notch in the center of the lip
notch_width = 40.0
notch = (
    cq.Workplane("XY")
    .workplane(offset=0) # Z=0 is center of main plate
    .moveTo(0, -depth / 2 - lip_extension + 2)
    .rect(notch_width, 10)
    .extrude(20) # Cut upwards through the lip tip
)

result = result.cut(notch)

# Final smooth fillet on the lip's main long edge for aesthetics
# result = result.edges(cq.selectors.BoxSelector((-width/2+10, -depth/2-lip_extension, 0), (width/2-10, -depth/2, 10))).fillet(1)
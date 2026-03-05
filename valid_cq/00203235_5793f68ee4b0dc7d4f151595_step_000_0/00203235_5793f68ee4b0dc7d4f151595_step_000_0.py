import cadquery as cq

# Parameters for dimensions
base_width = 60.0
base_length = 60.0
base_thickness = 4.0
base_fillet = 5.0
base_chamfer = 1.0

plate_length = 46.0
plate_height = 30.0  # Height above the base
plate_thickness = 3.5
plate_gap = 4.0
plate_chamfer = 10.0  # Top corner chamfer size
groove_radius = 1.2

rib_width = 12.0
rib_height = 20.0
rib_thickness = 3.0

# 1. Create the Base
# A square plate with rounded corners and a chamfered top edge
base = (
    cq.Workplane("XY")
    .rect(base_width, base_length)
    .extrude(base_thickness)
    .edges("|Z")
    .fillet(base_fillet)
    .faces(">Z")
    .edges()
    .chamfer(base_chamfer)
)

# 2. Create the Vertical Plates
# We calculate the Y position of the plates based on the gap
y_pos = (plate_gap / 2.0) + (plate_thickness / 2.0)
groove_y_pos = plate_gap / 2.0

# Create the basic block for plates
plates_solid = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    # Right Plate
    .moveTo(0, y_pos)
    .rect(plate_length, plate_thickness)
    # Left Plate
    .moveTo(0, -y_pos)
    .rect(plate_length, plate_thickness)
    .extrude(plate_height)
)

# Create the vertical groove cutters
# These are cylinders centered on the inner face of the plates
groove_cutters = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .moveTo(0, groove_y_pos)
    .circle(groove_radius)
    .moveTo(0, -groove_y_pos)
    .circle(groove_radius)
    .extrude(plate_height)
)

# Cut the grooves from the plates
plates_grooved = plates_solid.cut(groove_cutters)

# Apply chamfers to the top corners of the plates
# We select the top face, then the edges parallel to Y (the short ends)
final_plates = (
    plates_grooved
    .faces(">Z")
    .edges("|Y")
    .chamfer(plate_chamfer)
)

# 3. Create the Gussets (Support Ribs)
# Defined on the YZ plane (side view), extruded symmetrically in X
# Right Gusset
gusset_right = (
    cq.Workplane("YZ")
    .workplane(origin=(0, 0, base_thickness))
    .moveTo(y_pos + plate_thickness/2.0, 0)
    .lineTo(y_pos + plate_thickness/2.0 + rib_width, 0)
    .lineTo(y_pos + plate_thickness/2.0, rib_height)
    .close()
    .extrude(rib_thickness / 2.0, both=True)
)

# Left Gusset (Mirror of right, or drawn explicitly)
gusset_left = (
    cq.Workplane("YZ")
    .workplane(origin=(0, 0, base_thickness))
    .moveTo(-(y_pos + plate_thickness/2.0), 0)
    .lineTo(-(y_pos + plate_thickness/2.0 + rib_width), 0)
    .lineTo(-(y_pos + plate_thickness/2.0), rib_height)
    .close()
    .extrude(rib_thickness / 2.0, both=True)
)

# 4. Combine all parts
result = base.union(final_plates).union(gusset_right).union(gusset_left)
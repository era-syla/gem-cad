import cadquery as cq

# --- Parametric Dimensions ---
# Main Cradle Dimensions
cradle_radius = 18.0
cradle_wall_thickness = 6.0
cradle_width = 44.0
cradle_outer_radius = cradle_radius + cradle_wall_thickness

# Left Flange Dimensions
flange_length = 38.0
flange_width = 44.0
flange_thickness = 5.0
hole_spacing_x = 26.0
hole_spacing_y = 32.0
mount_hole_dia = 4.5

# Right Mount Dimensions
right_ext_length = 35.0
side_plate_thickness = 6.0
side_plate_height_drop = 20.0  # How far down the nose goes

# Feature Dimensions
rib_width = 14.0
rib_height = 3.5
channel_width = 5.0
channel_depth = 2.0

# --- Geometry Construction ---

# 1. Central Cradle (Semi-cylindrical shell)
# Oriented along Y-axis, centered at X=0, Top cut at Z=0
cradle_profile = (
    cq.Workplane("XZ")
    .circle(cradle_outer_radius)
    .extrude(cradle_width / 2, both=True)
)

cradle_cutout = (
    cq.Workplane("XZ")
    .circle(cradle_radius)
    .extrude(cradle_width, both=True)
)

cradle_top_trim = (
    cq.Workplane("XY")
    .rect(cradle_outer_radius * 3, cradle_width * 2)
    .extrude(cradle_outer_radius * 2)
    .translate((0, 0, cradle_outer_radius))
)

cradle = cradle_profile.cut(cradle_cutout).cut(cradle_top_trim)

# 2. Left Flange Assembly
# Positioned on the -X side
flange_base = (
    cq.Workplane("XY")
    .workplane(offset=-flange_thickness)
    .moveTo(-cradle_outer_radius, 0)
    .rect(flange_length, flange_width, centered=(False, True))
    .translate((-flange_length, 0, 0))
    .extrude(flange_thickness)
)

# Flange Ears (Rounded corners for holes)
ears_pts = [
    (-cradle_outer_radius - flange_length + 6, -flange_width/2),
    (-cradle_outer_radius - flange_length + 6, flange_width/2),
    (-cradle_outer_radius - 6, -flange_width/2),
    (-cradle_outer_radius - 6, flange_width/2)
]

flange_ears = (
    cq.Workplane("XY")
    .workplane(offset=-flange_thickness)
    .pushPoints(ears_pts)
    .circle(6.0)
    .extrude(flange_thickness)
)

# Central Rib with Channel
rib_body = (
    cq.Workplane("XY")
    .moveTo(-cradle_outer_radius - flange_length, 0)
    .rect(flange_length, rib_width, centered=(False, True))
    .extrude(rib_height)
)

rib_channel = (
    cq.Workplane("XY")
    .workplane(offset=rib_height - channel_depth)
    .moveTo(-cradle_outer_radius - flange_length, 0)
    .rect(flange_length, channel_width, centered=(False, True))
    .extrude(channel_depth)
)

flange_assembly = flange_base.union(flange_ears).union(rib_body.cut(rib_channel))

# Cut Mounting Holes
flange_assembly = (
    flange_assembly.faces(">Z").workplane()
    .pushPoints(ears_pts)
    .hole(mount_hole_dia)
)

# 3. Right Side Structure
# Consists of a base extension and a vertical side plate

# Base Extension (Floor)
right_base = (
    cq.Workplane("XY")
    .workplane(offset=-cradle_outer_radius) # Bottom of cradle
    .moveTo(cradle_outer_radius - 2, 0)
    .rect(right_ext_length, cradle_width, centered=(False, True))
    .extrude(flange_thickness)
)

# Vertical Side Plate (Front/-Y side)
vp_start_x = cradle_outer_radius - 5
vp_length = 40.0
vp_poly = [
    (vp_start_x, 0), # Top Left
    (vp_start_x + 25, -5), # Top Slope Start
    (vp_start_x + 35, -side_plate_height_drop), # Nose
    (vp_start_x + 35, -cradle_outer_radius), # Bottom Right
    (vp_start_x, -cradle_outer_radius) # Bottom Left
]

side_plate = (
    cq.Workplane("XZ")
    .workplane(offset=-cradle_width/2)
    .polyline(vp_poly).close()
    .extrude(side_plate_thickness)
)

# Side Plate Features (Hole and Boss)
side_plate = (
    side_plate.faces("<Y").workplane()
    .pushPoints([(vp_start_x + 25, -12)])
    .hole(5.0)
)

side_boss = (
    cq.Workplane("XZ")
    .workplane(offset=-cradle_width/2)
    .center(vp_start_x + 25, -12)
    .circle(7.0)
    .extrude(2.0)
)

# Internal Support Gusset
gusset = (
    cq.Workplane("XZ")
    .workplane(offset=-cradle_width/2 + side_plate_thickness) # Inside face
    .moveTo(vp_start_x + 5, -8)
    .lineTo(vp_start_x + 20, -cradle_outer_radius + flange_thickness)
    .lineTo(vp_start_x + 5, -cradle_outer_radius + flange_thickness)
    .close()
    .extrude(8.0)
)

# Internal block/latch detail
latch_block = (
    cq.Workplane("XY")
    .workplane(offset=-cradle_outer_radius + flange_thickness) # On floor
    .moveTo(vp_start_x + 10, -cradle_width/2 + side_plate_thickness)
    .rect(10, 10, centered=(False, False))
    .extrude(12)
    .edges("|Z").fillet(1.0)
)

# Rear Boss (on +Y side of cradle axis)
rear_boss = (
    cq.Workplane("XZ")
    .workplane(offset=cradle_width/2)
    .center(0, -cradle_radius/2)
    .circle(8.0)
    .extrude(2.0)
)

# --- Assembly ---

result = (
    cradle
    .union(flange_assembly)
    .union(right_base)
    .union(side_plate)
    .union(side_boss)
    .union(gusset)
    .union(latch_block)
    .union(rear_boss)
)

# Final Fillets for smooth cast look
# Selecting vertical edges on the flange connection
try:
    result = result.edges(cq.selectors.BoxSelector(
        (-cradle_outer_radius - 1, -20, -10), 
        (-cradle_outer_radius + 1, 20, 10)
    )).fillet(2.0)
except:
    pass # Skip if selection fails

# Fillet the cradle internal edge for smoothness
try:
    result = result.edges(cq.selectors.RadiusNthSelector(0)).fillet(1.0)
except:
    pass

# Export or display
# show_object(result) 
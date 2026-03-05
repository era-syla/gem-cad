import cadquery as cq
import math

# --- Parameters ---

# Crankcase (Central Body)
crank_od = 30.0
crank_id = 24.0
crank_length = 35.0
wall_thickness = 3.0

# Cylinder Head (Vertical Part)
cyl_height = 45.0
cyl_od = 32.0
cyl_id = 22.0
fin_count = 6
fin_thickness = 1.0
fin_gap = 2.0
fin_diameter = 36.0
bolt_circle_dia = 27.0
bolt_hole_dia = 2.5
num_bolts = 5

# Exhaust Port (Rectangular protrusion)
exhaust_width = 28.0
exhaust_height = 14.0
exhaust_depth = 15.0
exhaust_fillet = 3.0
exhaust_wall = 2.0
exhaust_z_offset = 15.0 # From center of crank

# Carburetor Intake (Front Nozzle)
intake_od = 18.0
intake_id = 12.0
intake_len = 20.0
intake_flange_od = 22.0
intake_flange_thick = 5.0

# Mounting Lugs
mount_width = 45.0 # Total width across lugs
mount_length = 30.0
mount_thickness = 4.0
mount_hole_dia = 3.5
mount_hole_spacing_x = 36.0
mount_hole_spacing_y = 18.0
mount_z_offset = -5.0 # Relative to center

# Rear Cover Interface
rear_od = 32.0
rear_depth = 5.0

# Auxiliary Port (The small angled port on the side of the intake)
aux_port_od = 10.0
aux_port_id = 6.0
aux_port_len = 8.0

# --- Construction ---

# 1. Main horizontal crankcase cylinder
crankcase = (
    cq.Workplane("YZ")
    .circle(crank_od / 2.0)
    .extrude(crank_length / 2.0, both=True) # Centered on Origin
)

# 2. Vertical Cylinder Block
cylinder_block = (
    cq.Workplane("XY")
    .circle(cyl_od / 2.0)
    .extrude(cyl_height)
)

# Add Cooling Fins
fins = cq.Workplane("XY")
for i in range(fin_count):
    z_pos = cyl_height - (i * (fin_thickness + fin_gap)) - 2.0
    fin = (
        cq.Workplane("XY")
        .workplane(offset=z_pos)
        .circle(fin_diameter / 2.0)
        .extrude(fin_thickness)
    )
    if i == 0:
        fins = fin
    else:
        fins = fins.union(fin)

cylinder_block = cylinder_block.union(fins)

# Combine Crankcase and Cylinder
main_body = crankcase.union(cylinder_block)

# 3. Hollow out the main chamber (vertical and horizontal)
# Horizontal bore
h_bore = (
    cq.Workplane("YZ")
    .circle(crank_id / 2.0)
    .extrude(crank_length / 2.0, both=True)
)

# Vertical bore
v_bore = (
    cq.Workplane("XY")
    .circle(cyl_id / 2.0)
    .extrude(cyl_height)
)

main_body = main_body.cut(h_bore).cut(v_bore)

# 4. Exhaust Port
exhaust_profile = (
    cq.Workplane("YZ")
    .rect(exhaust_height, exhaust_width) # Swapped because of YZ plane orientation
    .extrude(exhaust_depth)
)

# Fillet the exhaust outer edges
exhaust_profile = exhaust_profile.edges("|X").fillet(exhaust_fillet)

# Move exhaust to position
exhaust_solid = exhaust_profile.translate((-exhaust_depth/2 - cyl_od/2 + 2, 0, exhaust_z_offset))

# Create exhaust hollow
exhaust_cut = (
    cq.Workplane("YZ")
    .rect(exhaust_height - 2*exhaust_wall, exhaust_width - 2*exhaust_wall)
    .extrude(exhaust_depth + 10) # Oversize for cut
    .edges("|X").fillet(exhaust_fillet - exhaust_wall)
    .translate((-exhaust_depth/2 - cyl_od/2 + 2, 0, exhaust_z_offset))
)

main_body = main_body.union(exhaust_solid).cut(exhaust_cut)


# 5. Front Intake Section (Carburetor mount)
# This extends from the main crankcase forward (+X direction relative to crank axis, but here +Y is crank axis)
# Let's assume the crank axis is Y. The intake is actually sticking out in X direction.

intake_neck = (
    cq.Workplane("YZ")
    .workplane(offset=crank_length/2.0)
    .circle(intake_od / 2.0)
    .extrude(intake_len)
)

# Intake Flange (at the tip)
intake_flange = (
    cq.Workplane("YZ")
    .workplane(offset=crank_length/2.0 + intake_len - intake_flange_thick)
    .circle(intake_flange_od / 2.0)
    .extrude(intake_flange_thick)
)

intake_total = intake_neck.union(intake_flange)

# Intake bore
intake_bore = (
    cq.Workplane("YZ")
    .workplane(offset=crank_length/2.0 - 5) # Start inside
    .circle(intake_id / 2.0)
    .extrude(intake_len + 10)
)

main_body = main_body.union(intake_total).cut(intake_bore)


# 6. Mounting Lugs (Wings on the side)
# Defined on XY plane, extruded down
# The lugs are usually attached to the sides of the crankcase.

lug_shape = (
    cq.Workplane("XY")
    .rect(mount_length, mount_width)
    .extrude(mount_thickness)
    .translate((0, 0, -crank_od/2 + mount_z_offset))
)

# Cut the middle to fit the round crankcase
lug_cutout = (
    cq.Workplane("YZ")
    .circle(crank_od/2.0)
    .extrude(mount_length + 10, both=True)
)

lugs = lug_shape.cut(lug_cutout)

# Add mounting holes
for x_sign in [-1, 1]:
    for y_sign in [-1, 1]:
        hole = (
            cq.Workplane("XY")
            .workplane(offset=-crank_od/2 + mount_z_offset + mount_thickness + 1)
            .moveTo(x_sign * mount_hole_spacing_y/2.0, y_sign * mount_hole_spacing_x/2.0) # Swapped axes for orientation
            .circle(mount_hole_dia / 2.0)
            .extrude(-mount_thickness - 5)
        )
        lugs = lugs.cut(hole)
        
# Fillet the connection between lugs and body
# This is tricky with boolean operations, often better to construct reinforcement ribs
# Simple integration for now:
main_body = main_body.union(lugs)

# 7. Bolt holes on Cylinder Head
head_bolts = cq.Workplane("XY").workplane(offset=cyl_height)
for i in range(num_bolts):
    angle = (360.0 / num_bolts) * i
    rad = math.radians(angle)
    x = (bolt_circle_dia / 2.0) * math.cos(rad)
    y = (bolt_circle_dia / 2.0) * math.sin(rad)
    
    bolt_hole = (
        cq.Workplane("XY")
        .workplane(offset=cyl_height + 1)
        .moveTo(x, y)
        .circle(bolt_hole_dia / 2.0)
        .extrude(-10) # Depth of screw hole
    )
    main_body = main_body.cut(bolt_hole)

# 8. Reinforcement / Webbing (simplified)
# Triangular webbing between intake neck and cylinder
web = (
    cq.Workplane("XY")
    .moveTo(intake_od/2, 0)
    .lineTo(intake_od/2 + 10, 0)
    .lineTo(intake_od/2, 15)
    .close()
    .extrude(2)
    .translate((0, crank_length/2 + 2, 10))
    .rotate((0,0,0), (0,0,1), 90) # Orient correctly
)
# Often there are multiple webs, omitting complex lofting for brevity while keeping shape.


# 9. Small Angled Boss on Intake
boss_plane = (
    cq.Workplane("XY")
    .translate((0, crank_length/2 + 5, 0))
    .rotate((0,1,0), (0,0,0), 45) # Angle it
)

boss = (
    boss_plane
    .circle(aux_port_od / 2.0)
    .extrude(aux_port_len)
)

boss_hole = (
    boss_plane
    .workplane(offset=aux_port_len)
    .circle(aux_port_id / 2.0)
    .extrude(-aux_port_len - 5)
)

main_body = main_body.union(boss).cut(boss_hole)


# 10. Smoothing and Clean up (Fillets)
# Applying fillets to complex unions can be fragile in CAD kernels. 
# We apply selective fillets where geometry allows.

try:
    # Fillet the vertical cylinder to crankcase transition
    main_body = main_body.edges("(>Z[-30] and <Z[-10]) and (not %CIRCLE)").fillet(2.0)
except:
    pass # Fallback if edge selection is ambiguous

try:
    # Fillet the top rim of cylinder
    main_body = main_body.edges(">Z").fillet(0.5)
except:
    pass

result = main_body
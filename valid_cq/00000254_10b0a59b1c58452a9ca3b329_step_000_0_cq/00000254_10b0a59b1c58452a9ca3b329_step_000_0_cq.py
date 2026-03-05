import cadquery as cq
import math

# --- Parameters ---

# Main Truss/Frame dimensions
truss_length = 200.0
truss_width = 40.0
truss_height_rear = 50.0
truss_height_front = 20.0
wall_thickness = 4.0

# Pivot Bracket (Front) dimensions
pivot_plate_width = 80.0
pivot_plate_height = 90.0
pivot_plate_thickness = 10.0
pivot_hole_dia = 12.0
ball_joint_dia = 25.0
ball_joint_stem_len = 15.0

# Cylinder dimensions
cyl_body_dia = 30.0
cyl_body_len = 80.0
cyl_rod_dia = 8.0
cyl_rod_extension = 60.0  # Visible length
cyl_end_cap_dia = 34.0
cyl_end_cap_thk = 8.0

# Cylinder Mounts
rear_mount_height = 25.0
front_clevis_width = 15.0

# --- Helper Functions ---

def create_truss_profile(length, h_rear, h_front, thickness):
    """Creates the tapering truss body with cutouts."""
    
    # Define the side profile points
    pts = [
        (0, 0),
        (length, 0),
        (length, h_front),
        (0, h_rear)
    ]
    
    # Extrude the solid block first
    solid = (
        cq.Workplane("XY")
        .polyline(pts)
        .close()
        .extrude(truss_width)
    )
    
    # Shelling operation to make it a frame
    # We select faces to remove (front, back, and the internal volume)
    # A robust way is to hollow it out manually with cuts to get the truss structure
    
    # Let's try a different approach: Build walls and ribs
    # Base structure
    shell = solid.faces("<Y").shell(-thickness)
    
    # Create side cutouts (truss pattern)
    # Define cutout shapes on the side face
    
    cutout_plane = solid.faces(">Z").workplane().center(0, -truss_width/2)
    
    # Calculate cutout geometry based on length
    num_cutouts = 4
    cutout_spacing = 5.0
    avail_len = length - (num_cutouts + 1) * cutout_spacing
    cutout_len = avail_len / num_cutouts
    
    # We need to project cutouts onto the angled face or just cut through Y
    # Cutting through Y (side to side) is easier
    
    cutter = cq.Workplane("XZ").workplane(offset=-truss_width/2 - 1)
    
    for i in range(num_cutouts):
        x_pos = cutout_spacing + i * (cutout_len + cutout_spacing)
        
        # Calculate local heights for the trapezoidal cutout
        h1 = h_rear - (x_pos / length) * (h_rear - h_front) - wall_thickness*1.5
        h2 = h_rear - ((x_pos + cutout_len) / length) * (h_rear - h_front) - wall_thickness*1.5
        
        pts_cutout = [
            (x_pos, wall_thickness),
            (x_pos + cutout_len, wall_thickness),
            (x_pos + cutout_len, h2),
            (x_pos, h1)
        ]
        
        cutter = cutter.polyline(pts_cutout).close().extrude(truss_width + 2)
        
    shell = shell.cut(cutter)
    
    # Add top/bottom cutouts
    top_cutter = (
        cq.Workplane("XY")
        .workplane(offset=h_rear) # Start high
        .transformed(rotate=(0, math.degrees(math.atan2(h_front-h_rear, length)), 0)) # Rotate to match slope
        .center(length/2, truss_width/2)
        .rect(length - 20, truss_width - 2*wall_thickness)
        .extrude(-50, combine=False) # Cut down
    )
    
    # Simplification: just cut the top face with rectangular holes
    shell = shell.faces(">Z").workplane().rect(length*0.8, truss_width-2*wall_thickness).cutBlind(-wall_thickness)

    return shell

def create_pneumatic_cylinder():
    """Creates the cylinder assembly."""
    body = cq.Workplane("YZ").circle(cyl_body_dia/2).extrude(cyl_body_len)
    
    # End caps
    cap_rear = cq.Workplane("YZ").circle(cyl_end_cap_dia/2).extrude(cyl_end_cap_thk)
    cap_front = cq.Workplane("YZ").workplane(offset=cyl_body_len).circle(cyl_end_cap_dia/2).extrude(cyl_end_cap_thk)
    
    # Rod
    rod = cq.Workplane("YZ").workplane(offset=cyl_body_len + cyl_end_cap_thk).circle(cyl_rod_dia/2).extrude(cyl_rod_extension)
    
    # Rear Clevis Mount on Cylinder
    clevis_box = (
        cq.Workplane("YZ")
        .workplane(offset=-10)
        .rect(cyl_end_cap_dia, cyl_end_cap_dia)
        .extrude(15)
    )
    
    # Combine cylinder parts
    cyl = body.union(cap_rear).union(cap_front).union(rod).union(clevis_box)
    
    return cyl

# --- Build Process ---

# 1. Create the main truss arm
truss = create_truss_profile(truss_length, truss_height_rear, truss_height_front, wall_thickness)

# 2. Create the Front Pivot Plate Assembly
# This is the "face" plate at the larger end of the truss
pivot_plate = (
    cq.Workplane("YZ")
    .workplane(offset=-pivot_plate_thickness)
    .rect(pivot_plate_width, pivot_plate_height)
    .extrude(pivot_plate_thickness)
)

# Chamfer corners of plate
pivot_plate = pivot_plate.edges("|X").chamfer(10)

# Add holes to plate
pivot_plate = (
    pivot_plate.faces(">X")
    .workplane()
    .pushPoints([(0, 20), (0, -20)])
    .circle(pivot_hole_dia/2)
    .cutThruAll()
)

# Add ball joints
ball_l = (
    cq.Workplane("YZ")
    .workplane(offset=-pivot_plate_thickness)
    .center(-pivot_plate_width/2 + 10, -20)
    .circle(8).extrude(-ball_joint_stem_len)
    .faces("<X").workplane()
    .sphere(ball_joint_dia/2)
)

ball_r = (
    cq.Workplane("YZ")
    .workplane(offset=-pivot_plate_thickness)
    .center(pivot_plate_width/2 - 10, -20)
    .circle(8).extrude(-ball_joint_stem_len)
    .faces("<X").workplane()
    .sphere(ball_joint_dia/2)
)

pivot_assembly = pivot_plate.union(ball_l).union(ball_r)

# Align pivot assembly to the front of the truss (at X=0)
# The truss starts at 0,0,0 and goes +X.
# The pivot plate needs to be at X=0, centered on the truss width (Y)
pivot_assembly = pivot_assembly.translate((0, truss_width/2, truss_height_rear/2))


# 3. Create Pivot Brackets on the truss (for the cylinder rod)
# Located near the front (X=0)
rod_bracket_base = (
    cq.Workplane("XY")
    .workplane(offset=truss_height_rear)
    .center(20, truss_width/2)
    .rect(30, 20)
    .extrude(20)
)

# Clevis shape for rod bracket
rod_bracket = (
    rod_bracket_base
    .faces(">Z").workplane()
    .rect(30, 8) # Slot
    .cutBlind(-15)
    .faces(">Y").workplane(centerOption="CenterOfMass")
    .center(0, -5)
    .circle(4)
    .cutThruAll()
)


# 4. Create Rear Cylinder Mount
# Located at the rear of the truss
rear_mount = (
    cq.Workplane("XY")
    .workplane(offset=truss_height_front) # Approximation of height at rear
    .center(truss_length - 30, truss_width/2)
    .rect(30, truss_width)
    .extrude(rear_mount_height)
)

# Cut slot for cylinder rear clevis
rear_mount = (
    rear_mount.faces(">Z").workplane()
    .rect(30, 15)
    .cutBlind(-rear_mount_height)
    .faces(">Y").workplane(centerOption="CenterOfMass")
    .center(0, -rear_mount_height/2 + 5)
    .circle(5)
    .cutThruAll()
)

# 5. Position and create Cylinder
cylinder = create_pneumatic_cylinder()

# Rotate cylinder to match angle between brackets
# Rear mount pos: (truss_length - 30, truss_width/2, truss_height_front + rear_mount_height/2)
# Front bracket pos: (20, truss_width/2, truss_height_rear + 15)
p1 = cq.Vector(truss_length - 30, truss_width/2, truss_height_front + 15)
p2 = cq.Vector(20, truss_width/2, truss_height_rear + 10)
cyl_vec = p2 - p1
cyl_angle = math.degrees(math.atan2(cyl_vec.z, -cyl_vec.x)) # Simple 2D angle in XZ plane roughly

cylinder = (
    cylinder
    .rotate((0,0,0), (0,1,0), 180 + cyl_angle) # Orient towards front
    .translate((p1.x, p1.y, p1.z))
)

# Add Rod End Clevis
rod_clevis = (
    cq.Workplane("XY")
    .box(20, 15, 20)
    .rotate((0,0,0), (0,1,0), cyl_angle)
    .translate((p2.x, p2.y, p2.z))
)

# 6. Combine all parts
result = (
    truss
    .union(pivot_assembly)
    .union(rod_bracket)
    .union(rear_mount)
    .union(cylinder)
    .union(rod_clevis)
)

# Filleting for aesthetics (optional but good for look)
try:
    result = result.edges("|Z").fillet(1.0)
except:
    pass

import cadquery as cq
import math

# --- Parameters ---
plate_thickness = 8.0
center_hole_diam = 20.0
# The overall shape is roughly triangular with cut corners
# Let's define the radius of the circumscribed circle for the main vertices
outer_radius = 50.0  
# The radius for the recessed areas between the main arms
inner_radius = 25.0

# Joint Parameters
ball_joint_offset = 55.0  # Distance from center to the ball joint axis
ball_joint_spacing = 40.0 # Distance between pair of joints on one side
ball_radius = 8.0         # Radius of the spherical cutouts
rod_diam = 4.0            # Diameter of the rods sticking out (visualization)
rod_length = 15.0         # Length of the rods sticking out
slot_width = 4.0          # Width of the slot cut into the ball joint

# Mounting Holes
mounting_hole_diam = 3.0
mounting_hole_spacing = 15.0 # Spacing for holes near the center

# --- Helper Functions ---

def create_ball_joint_socket(loc):
    """
    Creates the complex geometry for the ball joint socket:
    - A spherical cutout
    - A rod sticking out
    - Slots for the rod movement
    """
    # Create the sphere
    sphere = cq.Workplane().sphere(ball_radius)
    
    # Create the rod (cylinder)
    rod = cq.Workplane("YZ").circle(rod_diam/2).extrude(rod_length)
    rod = rod.translate((0, 0, 0)) # Centered
    
    # Create the slot cutout (a box or extruded shape to allow rod movement)
    # The slot needs to cut through the sphere to allow the rod to pivot
    slot_cutout = (
        cq.Workplane("XY")
        .rect(ball_radius * 2.5, slot_width)
        .extrude(ball_radius * 2.5)
        .translate((0, 0, -ball_radius))
    )
    
    # Another slot perpendicular for cross movement flexibility
    slot_cutout2 = (
        cq.Workplane("YZ")
        .rect(ball_radius * 2.5, slot_width)
        .extrude(ball_radius * 2.5)
        .translate((-ball_radius, 0, 0))
    )
    
    # Combine to make the negative volume for the socket
    # In this specific visual, it looks like a positive housing with a ball inside?
    # Actually, looking closely, it looks like a printed part holding a metal ball.
    # The printed part has fingers.
    # Let's approximation: A sphere subtracted from the main body, plus slots cut out of the housing.
    
    return sphere, rod, slot_cutout.union(slot_cutout2)

# --- Main Geometry Construction ---

# 1. Base Plate Shape
# We'll create a sketch based on a polygon with fillets/arcs
def create_base_shape():
    # Points for a 3-lobed shape
    # We will use polar coordinates to define the vertices
    pts = []
    num_lobes = 3
    for i in range(num_lobes):
        angle = 2 * math.pi * i / num_lobes - math.pi / 2 # Start pointing down/up
        
        # We need a pair of points for each "arm" to hold the joints
        # The joints are spaced by ball_joint_spacing
        
        # Vector perpendicular to radial vector
        dx = (ball_joint_spacing / 2.0) * math.cos(angle + math.pi/2)
        dy = (ball_joint_spacing / 2.0) * math.sin(angle + math.pi/2)
        
        # Radial vector
        rx = ball_joint_offset * math.cos(angle)
        ry = ball_joint_offset * math.sin(angle)
        
        # Point 1 (Left of arm)
        pts.append((rx + dx, ry + dy))
        # Point 2 (Right of arm)
        pts.append((rx - dx, ry - dy))
        
        # Mid-point for the inner curve
        next_angle = 2 * math.pi * (i + 1) / num_lobes - math.pi / 2
        mid_angle = (angle + next_angle) / 2
        mx = inner_radius * math.cos(mid_angle)
        my = inner_radius * math.sin(mid_angle)
        
        # We insert the midpoint to help guide a spline or polyline, 
        # but a simple polyline with fillets is often more robust.
        # Let's stick to the main vertices and fillet heavily.
    
    # Reorder points to ensure correct winding if necessary, but the loop above generates (Right, Left) pairs relative to center
    # Actually, let's just make a simple hull of cylinders at the joint locations
    return pts

# Alternative approach: Constructive Solid Geometry (CSG)
# Start with the central hub and add arms.

# Central Hub
base = cq.Workplane("XY").circle(outer_radius/1.5).extrude(plate_thickness)

# Cut the center hole
base = base.faces(">Z").circle(center_hole_diam/2).cutThruAll()

# Create the Arms and Joint Housings
arms = cq.Workplane("XY")

for i in range(3):
    angle_deg = 90 + (i * 120) # 90, 210, 330
    
    # Create a local workplane for this arm
    arm_plane = (
        cq.Workplane("XY")
        .center(0, 0)
        .transformed(rotate=(0, 0, angle_deg))
    )
    
    # Create the rectangular block for the arm
    # Width covers the joint spacing
    arm_width = ball_joint_spacing + ball_radius * 2.5
    arm_len = ball_joint_offset
    
    # Draw the arm shape
    arm_geo = (
        arm_plane
        .moveTo(0, 0)
        .lineTo(arm_width/2, 0)
        .lineTo(arm_width/2, arm_len)
        .lineTo(-arm_width/2, arm_len)
        .lineTo(-arm_width/2, 0)
        .close()
        .extrude(plate_thickness)
    )
    
    # Add housing cylinders at the end for the joints
    # Left Joint Housing
    left_cyl = (
        arm_plane
        .center(-ball_joint_spacing/2, ball_joint_offset)
        .circle(ball_radius + 2)
        .extrude(plate_thickness)
    )
    
    # Right Joint Housing
    right_cyl = (
        arm_plane
        .center(ball_joint_spacing/2, ball_joint_offset)
        .circle(ball_radius + 2)
        .extrude(plate_thickness)
    )
    
    # Fuse them
    base = base.union(arm_geo).union(left_cyl).union(right_cyl)

# Refine the shape: Fillet the connections between arms
# This is computationally expensive, so we approximate with a cylinder subtraction
for i in range(3):
    angle_deg = 30 + (i * 120) # Between arms
    cutout = (
        cq.Workplane("XY")
        .polarArray(inner_radius + 10, i * 120 + 30, 360, 1) # radius, start angle
        .circle(15) # Radius of the "neck" cutout
        .extrude(plate_thickness)
    )
    # This polar array logic is a bit tricky with single items, let's do explicit placement
    rad = inner_radius + 5
    x = rad * math.cos(math.radians(angle_deg))
    y = rad * math.sin(math.radians(angle_deg))
    
    cutter = cq.Workplane("XY").center(x, y).circle(15).extrude(plate_thickness)
    base = base.cut(cutter)

# --- Detail Features ---

# 1. Magnet/Ball Joint Cutouts
# We need to cut spherical pockets and slots into the 6 joint locations
for i in range(3):
    angle_deg = 90 + (i * 120)
    
    # Calculate global positions for the two joints on this arm
    # Rotation matrix logic simplified
    rad_ang = math.radians(angle_deg)
    cos_a = math.cos(rad_ang)
    sin_a = math.sin(rad_ang)
    
    # Local coordinates of joints: (+- spacing/2, offset)
    for x_local in [-ball_joint_spacing/2, ball_joint_spacing/2]:
        # Transform to global
        gx = x_local * cos_a - ball_joint_offset * sin_a
        gy = x_local * sin_a + ball_joint_offset * cos_a
        
        # Cut the sphere
        sphere_cutter = (
            cq.Workplane("XY")
            .center(gx, gy)
            .workplane(offset=plate_thickness/2) # Center sphere in plate thickness usually
            .sphere(ball_radius)
        )
        base = base.cut(sphere_cutter)
        
        # Cut the slots (The "fingers" look)
        # Vertical slot (aligned with rod direction roughly)
        # The rods point outwards radially.
        
        # Vector from center to joint
        joint_angle = math.degrees(math.atan2(gy, gx))
        
        slot_cutter = (
            cq.Workplane("XY")
            .center(gx, gy)
            .transformed(rotate=(0, 0, joint_angle))
            .rect(ball_radius*3, slot_width) # Long slot along radius
            .extrude(plate_thickness*2)
            .translate((0,0, -plate_thickness))
        )
        
        cross_slot_cutter = (
             cq.Workplane("XY")
            .center(gx, gy)
            .transformed(rotate=(0, 0, joint_angle))
            .rect(slot_width, ball_radius*3) # Cross slot
            .extrude(plate_thickness*2)
            .translate((0,0, -plate_thickness))
        )
        
        base = base.cut(slot_cutter).cut(cross_slot_cutter)
        
        # Add the "rod" visualization (simulating the ball stud)
        # This is a separate solid usually, but requested as one model "result"
        # We will union it for the visual
        rod = (
            cq.Workplane("XY")
            .center(gx, gy)
            .transformed(rotate=(0, 90, joint_angle)) # Rotate to point radially outward
            .circle(rod_diam/2)
            .extrude(rod_length + 10) # Length of rod
            .translate((0, 0, -5)) # Shift so it starts inside the socket
        )
        
        # Add the ball back (simulating the joint ball)
        ball = (
             cq.Workplane("XY")
            .center(gx, gy)
            .workplane(offset=plate_thickness/2)
            .sphere(ball_radius - 0.5) # Slightly smaller to look like it fits
        )
        
        # Combine rod and ball
        assembly = rod.union(ball)
        
        # Union with base (even though in reality they are separate parts, 
        # the prompt asks for the model in the image which shows everything)
        base = base.union(assembly)


# 2. Rectangular Slots (Belt pass-throughs?)
# Located radially between center and arms
for i in range(3):
    angle_deg = 90 + (i * 120)
    slot_dist = 28.0
    
    rect_slot = (
        cq.Workplane("XY")
        .center(0, 0)
        .transformed(rotate=(0, 0, angle_deg))
        .center(0, slot_dist)
        .rect(12, 5) # Width, Height (relative to rotation)
        .extrude(plate_thickness)
    )
    base = base.cut(rect_slot)

# 3. Small Mounting Holes
# Pairs of holes on the arms
for i in range(3):
    angle_deg = 90 + (i * 120)
    
    # Create hole cutter pair
    holes = (
        cq.Workplane("XY")
        .center(0, 0)
        .transformed(rotate=(0, 0, angle_deg))
        .center(0, 40) # Distance along arm
        .pushPoints([(-6, 0), (6, 0)]) # Side by side
        .circle(mounting_hole_diam/2)
        .extrude(plate_thickness)
    )
    base = base.cut(holes)
    
# 4. Side mounting holes (on the vertical faces between arms)
# Looking at the image, there's a hole on the flat face between the arms
for i in range(3):
    angle_deg = 30 + (i * 120) # 30, 150, 270 (The flat cutouts)
    rad = inner_radius - 2 # Approx location
    
    # We need to drill perpendicular to the Z axis, radially inward
    side_hole = (
        cq.Workplane("XY")
        .transformed(rotate=(0, 0, angle_deg))
        .transformed(rotate=(0, 90, 0)) # Rotate so Z points radially outward
        .center(plate_thickness/2, 0) # Center vertically on plate
        .circle(2.0)
        .extrude(50) # Drill inwards
        .translate((0, 0, 15)) # Start from outside
    )
    
    # To subtract this properly, we need to locate it correctly in global space
    # It's easier to define the cylinder globally
    
    vx = math.cos(math.radians(angle_deg))
    vy = math.sin(math.radians(angle_deg))
    
    # Define a cylinder starting outside and pointing in
    c_start = (vx * 40, vy * 40, plate_thickness/2)
    c_end = (0, 0, plate_thickness/2)
    
    # Create the cylinder
    # Workplane approach
    side_cutter = (
        cq.Workplane("XY")
        .workplane(offset=plate_thickness/2)
        .transformed(rotate=(0, 0, angle_deg))
        .center(25, 0) # Start radius
        .circle(1.5)
        .extrude(20) # Extrude outwards? No, we want a solid to subtract
    )
    # Let's try creating a cylinder oriented specifically
    side_cutter = (
        cq.Workplane("YZ") # Perpendicular plane
        .circle(1.5)
        .extrude(20)
        .translate((-10, 0, 0)) # Center it
        .rotate((0,0,0), (0,1,0), 90) # Point along X
        .translate((30, 0, plate_thickness/2)) # Move to radius
        .rotate((0,0,0), (0,0,1), angle_deg) # Rotate around Z
    )
    
    base = base.cut(side_cutter)

# Apply final fillets to vertical edges to smooth the look
# This can be fragile with complex topology, so we select carefully
try:
    base = base.edges("|Z").fillet(2.0)
except:
    # Fallback if fillet fails on complex geometry
    pass

result = base
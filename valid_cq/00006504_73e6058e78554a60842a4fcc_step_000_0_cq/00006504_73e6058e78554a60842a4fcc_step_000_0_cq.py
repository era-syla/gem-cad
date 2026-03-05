import cadquery as cq
from math import sin, cos, radians, sqrt

# --- Parameters ---
# Overall dimensions
height = 60.0
pillar_height = 40.0
arm_length = 35.0  # Distance from center to outer joints

# Top Platform
top_radius = 20.0
top_thickness = 5.0
center_hole_dia = 12.0
mount_hole_dia = 3.5
mount_hole_offset = 12.0 # Distance from center for the 3 mounting holes

# Pillars
pillar_width = 8.0
pillar_thickness = 5.0
pillar_offset_radius = 16.0 # Where the pillars attach relative to center

# Base Ring / Frame
base_arm_length = 40.0
base_thickness = 8.0
base_width = 8.0
joint_cylinder_dia = 10.0
joint_cylinder_length = 20.0 # Length of the horizontal cylinders at the tips
joint_hole_dia = 3.0
joint_cone_len = 5.0

# --- Helper Functions ---

def create_top_platform():
    # Hexagonal-ish shape with a central hole and mounting holes
    # Start with a cylinder base
    
    # Main body - hexagon shape
    pts = []
    for i in range(6):
        angle = radians(i * 60 + 30) # Rotate to align flat side
        r = top_radius
        pts.append((r * cos(angle), r * sin(angle)))
    
    # Extrude the basic hex shape
    top = cq.Workplane("XY").polyline(pts).close().extrude(top_thickness)
    
    # Add chamfers on top edges
    # top = top.faces(">Z").edges().chamfer(1.0) # Can be tricky with complex shapes, simplify
    
    # Central hole
    top = top.faces(">Z").workplane().circle(center_hole_dia/2).cutThruAll()
    
    # Mounting holes pattern (3 holes)
    top = top.faces(">Z").workplane() \
             .polarArray(mount_hole_offset, 0, 360, 3) \
             .circle(mount_hole_dia/2).cutThruAll()
             
    # Create the raised features for the screw heads (counterbore-ish)
    # We add cylinders around the holes
    raised_pads = cq.Workplane("XY").workplane(offset=top_thickness) \
                     .polarArray(mount_hole_offset, 0, 360, 3) \
                     .circle(mount_hole_dia/2 + 2.0).extrude(2.0)
                     
    top = top.union(raised_pads)
    
    # Re-cut holes to clear the new pads
    top = top.faces(">Z").workplane() \
             .polarArray(mount_hole_offset, 0, 360, 3) \
             .circle(mount_hole_dia/2).cutThruAll()

    # Move top to correct height
    return top.translate((0, 0, pillar_height))

def create_pillar():
    # A simple rectangular pillar
    p = cq.Workplane("XY").rect(pillar_width, pillar_thickness).extrude(pillar_height)
    return p

def create_base_structure():
    # The base consists of three arms forming a triangular structure
    # Let's model one 120-degree sector and rotate it
    
    # Center to outer joint
    # The structure looks like a ring made of 3 segments.
    # Let's create the connecting bars first.
    
    # Calculate triangle geometry
    # Distance from center to the midpoint of the chord
    chord_dist = 25.0
    
    # Create one segment of the "ring"
    # It connects two joint locations. 
    # Actually, looking closely, it's a central hub with 3 arms or a triangular ring. 
    # It looks like a triangular ring with vertices at the rod end locations.
    
    # Let's build it as a sketch of the whole ring to ensure connectivity
    # Outer radius for the triangular frame
    r_outer = 45.0
    r_inner = 30.0
    
    # Draw a triangle with rounded corners effectively
    # Using a hull of circles at the corners is a robust way
    
    # The corners are where the rod ends attach.
    # Let's define the 3 corner points
    corners = []
    for i in range(3):
        angle = radians(i * 120 + 90) # Pointing up, left-down, right-down
        x = r_outer * cos(angle)
        y = r_outer * sin(angle)
        corners.append((x,y))
        
    # Create the horizontal cylinders (rod end housings) at these corners
    # The axis of these cylinders is tangent to the circle
    housings = cq.Workplane("XY")
    
    for i in range(3):
        angle_deg = i * 120 + 90
        # Position of the housing center
        x = r_outer * cos(radians(angle_deg))
        y = r_outer * sin(radians(angle_deg))
        
        # Create a cylinder oriented tangent to the radius (perpendicular to radial vector)
        # We create it at origin, rotate, then translate
        
        # The main body of the joint
        cyl = cq.Workplane("YZ").circle(joint_cylinder_dia/2).extrude(joint_cylinder_length)
        cyl = cyl.translate((-joint_cylinder_length/2, 0, 0)) # Center it
        
        # Add the conical ends
        cone_l = cq.Workplane("YZ").workplane(offset=-joint_cylinder_length/2) \
                   .circle(joint_cylinder_dia/2).workplane(offset=-joint_cone_len) \
                   .circle(joint_hole_dia/2).loft(combine=True)
                   
        cone_r = cq.Workplane("YZ").workplane(offset=joint_cylinder_length/2) \
                   .circle(joint_cylinder_dia/2).workplane(offset=joint_cone_len) \
                   .circle(joint_hole_dia/2).loft(combine=True)
        
        full_joint = cyl.union(cone_l).union(cone_r)
        
        # Rotate to align tangent
        # Tangent direction at angle A is A + 90 degrees
        full_joint = full_joint.rotate((0,0,0), (0,0,1), angle_deg + 90)
        
        # Translate to position
        full_joint = full_joint.translate((x, y, 0))
        
        housings = housings.union(full_joint)

    # Now create the connecting beams between these housings
    # We can loft between rectangular profiles on the housings, or extrude a sketch
    
    # Let's extrude a shape that connects them.
    # We'll draw a sketch on XY plane.
    # Outer boundary
    pts_outer = []
    pts_inner = []
    
    beam_width = 8.0
    
    sketch = cq.Workplane("XY")
    
    # We will union 3 straight bars connecting the locations
    bars = cq.Workplane("XY")
    for i in range(3):
        p1 = corners[i]
        p2 = corners[(i+1)%3]
        
        # Distance and angle
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        dist = sqrt(dx**2 + dy**2)
        angle = -90 + (i * 120 + 90 + 60) # Rough heuristic for bar rotation
        
        # Midpoint
        mx = (p1[0] + p2[0])/2
        my = (p1[1] + p2[1])/2
        
        # Create bar
        # We need to cut it short so it doesn't overlap the joint cylinders weirdly
        bar_len = dist - joint_cylinder_length
        
        b = cq.Workplane("XY").rect(bar_len, base_width).extrude(base_thickness)
        
        # Rotate and move
        # Angle of the edge connecting corners i and i+1 is (i*120 + 90) + 120 + something?
        # Let's calculate angle from coordinates
        import math
        ang = math.degrees(math.atan2(dy, dx))
        
        b = b.rotate((0,0,0), (0,0,1), ang)
        b = b.translate((mx, my, -base_thickness/2)) # Centered on Z=0
        
        bars = bars.union(b)
    
    # Combine housings and bars
    base = housings.union(bars)
    
    # Add hex nut traps or holes on the joints?
    # The image shows hex indentations on the side of the joints.
    # Let's add a hexagonal cut to one side of each joint housing.
    for i in range(3):
        angle_deg = i * 120 + 90
        x = r_outer * cos(radians(angle_deg))
        y = r_outer * sin(radians(angle_deg))
        
        # Vector pointing to the joint center
        # We want to cut into the "faces" of the cylinder ends
        
        # Transform a hex polygon to the location
        # Orientation matches the joint cylinder axis
        joint_axis_angle = angle_deg + 90
        
        # Left side cut (relative to joint axis)
        hex_cut = cq.Workplane("YZ").polygon(6, 6.0).extrude(3.0) # 6mm hex nut, 3mm deep
        hex_cut = hex_cut.rotate((0,0,0), (0,0,1), joint_axis_angle)
        
        # Shift to one end of the cylinder
        # Offset along the tangent vector
        tan_x = cos(radians(joint_axis_angle))
        tan_y = sin(radians(joint_axis_angle))
        
        offset_dist = joint_cylinder_length/2
        
        cut_pos_x = x + tan_x * offset_dist
        cut_pos_y = y + tan_y * offset_dist
        
        # We need to position the cut correctly. 
        # The extrude goes along X axis of workplane (which was YZ, so global X).
        # It's tricky to align perfectly with rotate/translate chain.
        
        # Easier: Define workplane on the face of the cylinder
        # Find the point on the end of the cylinder
        p_end = (x + tan_x * (joint_cylinder_length/2), y + tan_y * (joint_cylinder_length/2), 0)
        
        # Normal vector is (tan_x, tan_y, 0)
        # Create a plane there looking at the point
        # This is complex in basic CQ without specific plane math.
        
        # Alternative: Just cut the base object with positioned solids
        cutter = cq.Workplane("YZ").polygon(6, 6.0).extrude(10.0) # Cut deep
        cutter = cutter.translate((-10.0 + 3.0, 0, 0)) # Position depth
        cutter = cutter.rotate((0,0,0), (0,0,1), joint_axis_angle)
        
        # Move to end of cylinder
        # The cutter was at origin. We move it along the joint axis vector
        cutter = cutter.translate((x + tan_x * joint_cylinder_length/2, y + tan_y * joint_cylinder_length/2, 0))
        
        base = base.cut(cutter)

    # Add center hole features or mounting points on the connecting bars if visible?
    # Image shows holes in the middle of the connecting bars (base frame).
    # Let's add holes in the middle of the bars.
    for i in range(3):
        p1 = corners[i]
        p2 = corners[(i+1)%3]
        mx = (p1[0] + p2[0])/2
        my = (p1[1] + p2[1])/2
        
        # Create a hole cutter
        hole = cq.Workplane("XY").circle(2.0).extrude(20).translate((mx, my, -10))
        base = base.cut(hole)

    return base

# --- Assembly Construction ---

# 1. Create Base
base_assembly = create_base_structure()

# 2. Create Top Platform
top_assembly = create_top_platform()

# 3. Create Pillars connecting Base and Top
# We need 3 pillars. They usually sit near the corners of the triangle/hexagon
pillars = cq.Workplane("XY")

for i in range(3):
    angle = radians(i * 120 + 30) # Offset to align with flat sides or corners
    # Looking at image, pillars are at the corners of the top hex (flat side alignment?)
    # The top is a hex. The pillars seem to come down from the mounting holes area?
    # No, they are separate. They seem to be at 120 deg intervals.
    # Let's put them at radius `pillar_offset_radius`
    
    px = pillar_offset_radius * cos(angle)
    py = pillar_offset_radius * sin(angle)
    
    p = create_pillar()
    # Rotate pillar to align with radial direction?
    p = p.rotate((0,0,0), (0,0,1), i * 120 + 30)
    p = p.translate((px, py, 0))
    
    pillars = pillars.union(p)

# In the image, the pillars attach to the top platform. The base ring attaches to the bottom of the pillars.
# Let's adjust Z positions.
# Let Base be at Z=0 (center).
# Let Pillars go from Z=0 up to Z=height.
# Let Top be at Z=height.

# Adjust Base: The image shows the base ring is 'held' by the pillars or integrated.
# The pillars seem to go down past the ring? No, they merge into the ring.
# The base ring connects the bottom of the pillars.

# Let's refine the pillar position to match the base ring shape.
# The base is a triangle. The pillars should likely be at the midpoints of the triangle sides?
# Or corners? 
# Image: The top is a Hexagon. The pillars come from 3 alternating sides of the hexagon.
# The base is a Triangle. The pillars connect to the midpoints of the triangle bars.

# Let's re-orient the base to match the pillars.
# Pillars are at angles 30, 150, 270.
# Base triangle corners are at 90, 210, 330.
# The midpoints of the base bars are at 150, 270, 30.
# Perfect match.

# So pillars are at the midpoints of the base bars.
# Let's just unite everything.

final_assembly = base_assembly.union(pillars).union(top_assembly)

# Add fillets to smooth transitions (optional, can be heavy)
# final_assembly = final_assembly.edges("|Z").fillet(1.0) 

# Image details: 
# The top platform has chamfered edges.
# The pillars have chamfers or recesses.
# The base ends are conical.

# Refining the top platform shape to look more like the image (Hexagon with chamfers)
# We already used a polyline for hex. Let's add the chamfer at the bottom/top of the hex platform.
# It's easier to recreate the top platform as a loft or chamfered extrude.

result = final_assembly
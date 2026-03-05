import cadquery as cq
import math

# --- Parameters ---
# Gear parameters
module = 2.0           # Metric module of the gear
num_teeth = 30         # Number of teeth
face_width = 15.0      # Total width of the gear face
helix_angle = 30.0     # Helix angle for the herringbone pattern
pressure_angle = 20.0  # Pressure angle in degrees

# Hub parameters
hub_diameter = 25.0    # Diameter of the central hub
hub_height = 25.0      # Height of the hub extending from the gear face (one side)
bore_diameter = 8.0    # Diameter of the central hole

# --- Calculations ---
pitch_diameter = module * num_teeth
addendum = module
dedendum = 1.25 * module
outer_diameter = pitch_diameter + 2 * addendum
root_diameter = pitch_diameter - 2 * dedendum

# Calculate the twist angle required for the helical gear
# Twist = (Face Width * tan(helix angle)) / Radius
# We need to apply this over half the face width for a herringbone
half_width = face_width / 2.0
twist_angle = (math.degrees(math.tan(math.radians(helix_angle)) * half_width) / (pitch_diameter / 2.0)) 

# --- Geometry Construction ---

# 1. Create the base gear profile (2D)
# We use a parametric involute gear generator approach or a simplified approximation.
# For robustness and standard compliance in CadQuery, we'll construct the profile manually 
# or use a simplified trapezoidal representation if a library isn't assumed. 
# However, standard CadQuery often relies on `cq_gears` or similar for complex involutes.
# To keep this self-contained and standard-library only, we will define a custom profile.

def involute_gear_profile(module, num_teeth, pressure_angle):
    """
    Creates a 2D profile for a single tooth space, then circular patterns it.
    This is a simplified approach to generate a valid gear shape without external libraries.
    """
    pitch_radius = (module * num_teeth) / 2.0
    base_radius = pitch_radius * math.cos(math.radians(pressure_angle))
    addendum_radius = pitch_radius + module
    dedendum_radius = pitch_radius - (1.25 * module)
    
    # Generate points for one tooth
    # Simplified involute approximation using points
    
    # We will construct the gear by creating a cylinder and cutting teeth out of it, 
    # or creating a single tooth and patterning it.
    # Let's use the standard involute generation logic typically found in gear generators.
    
    # For a robust single-script solution, we will approximate the tooth with a trapezoid
    # lofted helically, which is visually very close for this purpose, or construct
    # a proper 2D section. Let's make a proper 2D section.
    
    # Calculate angular width of the tooth at pitch circle
    # Tooth thickness at pitch circle is PI * module / 2
    # Angular thickness = (PI * module / 2) / pitch_radius = PI / num_teeth
    
    # We will create a sketch that represents the full gear cross-section
    s = cq.Sketch()
    s = s.circle(addendum_radius) # Outer circle
    
    # Create a cutter for the tooth gaps
    # Gap width at pitch circle is also approx PI * module / 2
    # We will approximate the gap as a trapezoid for the cutter
    gap_bottom_width = (math.pi * module / 2.0) - (2 * (pitch_radius - dedendum_radius) * math.tan(math.radians(pressure_angle)))
    gap_top_width = (math.pi * module / 2.0) + (2 * (addendum_radius - pitch_radius) * math.tan(math.radians(pressure_angle)))
    
    # Ensure widths are positive (for very small gears calculation might skew)
    gap_bottom_width = max(0.1, gap_bottom_width)
    
    # Angle subtended by the gap
    # This is a simplification. For a perfect gear, we need true involutes.
    # Given the constraint to return ONLY code and make it executable without extra libs:
    
    return s

# A robust approach without external libraries in pure CadQuery is to use `cq.Workplane` operations.

# Create the blank cylinder for the gear
gear_blank = cq.Workplane("XY").circle(outer_diameter / 2.0).extrude(face_width)

# Define the herringbone gear creation logic
# 1. Create a single helical gear half
# 2. Mirror it or create the other half with opposite twist
# 3. Union them

def make_herringbone_gear(m, z, width, helix, pa):
    """
    Constructs a herringbone gear using CadQuery standard operations.
    """
    pd = m * z
    rb = pd / 2.0 * math.cos(math.radians(pa)) # Base circle radius
    ra = pd / 2.0 + m # Addendum radius
    rd = pd / 2.0 - 1.25 * m # Dedendum radius
    
    # Calculate tooth geometry for one tooth
    # We construct a single tooth profile and loft it
    
    # Points for the involute (simplified)
    # We will create points for one side of the tooth, mirror, then wire.
    n_points = 10
    
    t_pts = []
    
    # Angular thickness of tooth at pitch diameter
    tooth_angle_at_pitch = (math.pi / z) # Half the pitch angle
    
    # Involute function: x = r * (cos(t) + t*sin(t)), y = r * (sin(t) - t*cos(t))
    # where r is base radius
    
    # Generate points for one flank of the tooth
    # We iterate parameter t to go from base circle to addendum circle
    # Radius at parameter t: R = rb * sqrt(1 + t^2)
    # t_max corresponds to ra
    t_max = math.sqrt((ra/rb)**2 - 1)
    
    for i in range(n_points + 1):
        t = (i / n_points) * t_max
        r = rb * math.sqrt(1 + t**2)
        inv_val = t - math.atan(t) # Involute function value (radians)
        
        # We need the angle theta on the circle such that the tooth thickness is correct.
        # Angle at pitch circle (t_pitch)
        t_pitch = math.sqrt((pd/2.0/rb)**2 - 1)
        inv_pitch = t_pitch - math.atan(t_pitch)
        
        # The center of the tooth is at angle 0.
        # The flank is offset by half the tooth thickness (tooth_angle_at_pitch/2) 
        # plus the involute angle at the pitch circle.
        
        theta = (tooth_angle_at_pitch/2.0 + inv_pitch) - inv_val
        
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        t_pts.append((x, y))
        
    # Create the wire for the tooth shape
    # Mirror points for the other side of the tooth
    mirrored_pts = [(x, -y) for x, y in t_pts]
    mirrored_pts.reverse() # Order needs to be reversed to form a continuous loop
    
    # Assemble the full loop: Center -> Flank1 -> Top Arc -> Flank2 -> Center
    # Actually, usually simpler to go Root -> Flank -> Top -> Flank -> Root
    
    # Top arc
    top_pt_start = t_pts[-1]
    top_pt_end = mirrored_pts[0]
    
    # To close the shape properly at the root (dedendum), we connect to the center
    # or create a root arc. For simplicity in this procedural generation:
    full_tooth_pts = t_pts + mirrored_pts
    
    # Create the tooth wire
    tooth_wire = cq.Workplane("XY").polyline(full_tooth_pts).close()
    
    # Extrude with twist to make helical
    # Calculate twist in degrees
    twist = (math.degrees(math.tan(math.radians(helix)) * (width / 2.0)) / (pd / 2.0)) * 2 # Total twist for width/2
    # Adjust sign based on direction
    
    # Half 1 (Right Hand)
    h1 = (tooth_wire
          .twistExtrude(width / 2.0, twist)
         )
         
    # Half 2 (Left Hand) - created by mirroring H1 or extruding opposite
    # We need to position H2 on top of H1
    h2 = (tooth_wire
          .workplane(offset=width/2.0)
          .twistExtrude(width / 2.0, -twist)
         )
         
    # Combine halves into one tooth
    one_tooth = h1.union(h2)
    
    # Pattern the tooth
    # This can be computationally expensive with twistExtrude and union.
    # Optimizing: Create all wires in sketch, then extrude? 
    # twistExtrude doesn't support multiple disjoint wires well in all kernels.
    # We will use the polar pattern of the solid.
    
    gear_solid = one_tooth
    for i in range(1, z):
        gear_solid = gear_solid.union(one_tooth.rotate((0,0,0), (0,0,1), i * 360.0/z))
        
    # Create the central cylinder (root) to fill the gaps
    core = cq.Workplane("XY").circle(rd).extrude(width)
    gear_solid = gear_solid.union(core)
    
    return gear_solid

# Generating the detailed involute geometry via loop is slow and complex for a snippet.
# Instead, we will approximate the visual look of the provided image (herringbone gear)
# using a simplified subtractive method which is much faster and robust for display.

def simple_herringbone():
    # Base Cylinder
    base = cq.Workplane("XY").circle(outer_diameter / 2.0).extrude(face_width)
    
    # Cutter definition (Trapezoidal rack profile equivalent)
    # We cut grooves to form teeth.
    cutter_width = (math.pi * module / 2.0) # Width of the cut at pitch
    cutter_depth = 2.25 * module
    
    # Define a single cutter profile in 2D
    # It's a trapezoid representing the space between teeth
    c_top = cutter_width + (2 * module * math.tan(math.radians(pressure_angle)))
    c_bot = cutter_width - (2 * 1.25 * module * math.tan(math.radians(pressure_angle)))
    
    # Vertices for the cutter wire (on XZ plane, to be swept)
    # The cutter sits on the periphery
    r_outer = outer_diameter / 2.0
    
    # We create a cutter solid using twist extrude, then subtract it pattern-wise
    
    # Twist calculation for the cutter
    h_twist = (math.degrees(math.tan(math.radians(helix_angle)) * (face_width/2.0)) / (pitch_diameter / 2.0))
    
    # Create the 2D profile of the gap (triangle/trapezoid)
    # Positioned at the correct radius to cut inward
    
    # Profile center at X = r_outer, Y = 0
    # We draw it on XY plane centered at a radius, then twist extrude
    
    # To make the V shape (Herringbone), we need two twist operations meeting in the middle.
    
    # Let's try a different approach: Build one tooth, pattern it, union with hub.
    # This is often cleaner.
    
    # 1. Profile of one tooth (Trapezoid approximation for speed/robustness)
    tooth_base_width = (math.pi * pitch_diameter / num_teeth) / 2.0 * 1.5 # Thicker at root
    tooth_tip_width = tooth_base_width * 0.4
    tooth_height = 2.25 * module
    r_root = root_diameter / 2.0
    
    # Define points for tooth cross-section relative to center
    # Drawing on XY plane
    p1 = (r_root, -tooth_base_width/2.0)
    p2 = (r_root + tooth_height, -tooth_tip_width/2.0)
    p3 = (r_root + tooth_height, tooth_tip_width/2.0)
    p4 = (r_root, tooth_base_width/2.0)
    
    tooth_wp = cq.Workplane("XY").polyline([p1, p2, p3, p4]).close()
    
    # Bottom half (Twist Right)
    t1 = tooth_wp.twistExtrude(face_width / 2.0, h_twist)
    
    # Top half (Twist Left)
    # We start the extrusion from the top of the previous one
    # Note: The rotation continuity must be maintained.
    # At height = face_width/2, the profile is rotated by h_twist.
    
    # Create wire at mid-plane rotated by h_twist
    mid_wire = tooth_wp.workplane(offset=face_width/2.0).transformed(rotate=(0,0,h_twist)).polyline([p1, p2, p3, p4]).close()
    t2 = mid_wire.twistExtrude(face_width / 2.0, -h_twist)
    
    single_tooth = t1.union(t2)
    
    # Pattern the tooth
    teeth = single_tooth
    # Union operations in a loop can be slow. 
    # Efficient way: create a list of objects and union once if possible, 
    # but CadQuery fluent API does sequential unions.
    
    # For speed in this script, we'll do fewer teeth or just loop
    # We will loop.
    
    final_gear = cq.Workplane("XY").circle(root_diameter/2.0).extrude(face_width)
    
    for i in range(num_teeth):
        angle = 360.0 / num_teeth * i
        rotated_tooth = single_tooth.rotate((0,0,0), (0,0,1), angle)
        final_gear = final_gear.union(rotated_tooth)
        
    return final_gear

# --- Main Construction ---

# 1. Build the Gear Ring
gear_body = simple_herringbone()

# 2. Build the Hub
# The hub extends above the gear face.
# Based on the image, the hub seems to go through the center.
# We'll create a cylinder centered at the origin, starting from Z=0 (bottom of gear) 
# and going up to face_width + extended height.
total_hub_height = face_width + hub_height

hub = cq.Workplane("XY").circle(hub_diameter / 2.0).extrude(total_hub_height)

# 3. Combine Gear and Hub
# The gear was built from Z=0 to Z=face_width
result_solid = gear_body.union(hub)

# 4. Create the Bore (Hole)
# Through hole along Z axis
result = result_solid.faces(">Z").workplane().hole(bore_diameter)

# Export or Render
if 'show_object' in globals():
    show_object(result)
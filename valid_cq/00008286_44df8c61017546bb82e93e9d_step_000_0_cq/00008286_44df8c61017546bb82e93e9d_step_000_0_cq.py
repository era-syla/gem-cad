import cadquery as cq
import math

# --- Parametric Dimensions ---
# Wheel dimensions
wheel_diameter = 700.0  # Overall diameter (approx 700c road bike)
rim_width = 25.0        # Width of the rim profile
rim_height = 15.0       # Radial height of the rim
rim_thickness = 2.0     # Wall thickness of the rim

# Hub dimensions
hub_diameter = 40.0     # Outer diameter of the hub shell
hub_length = 50.0       # Width of the hub (OLD - Over Locknut Dimension)
hub_bore = 12.0         # Axle hole diameter
flange_diameter = 50.0  # Diameter of the spoke flanges
flange_width = 3.0      # Thickness of the flanges
flange_offset = 18.0    # Distance from center to flange

# Spoke dimensions
spoke_diameter = 2.0
num_spokes = 32         # Common spoke count
spoke_cross = 2         # Basic radial pattern or slight cross simulation

# --- Geometry Construction ---

# 1. Create the Rim
# We'll sweep a profile or subtract cylinders. Subtracting cylinders is often cleaner for simple rings.
rim_outer_r = wheel_diameter / 2.0
rim_inner_r = rim_outer_r - rim_height

rim = (cq.Workplane("XY")
       .circle(rim_outer_r)
       .circle(rim_inner_r)
       .extrude(rim_width)
       .translate((0, 0, -rim_width / 2.0)))

# 2. Create the Hub
# Main cylinder body
hub_body = (cq.Workplane("XY")
            .circle(hub_diameter / 2.0)
            .extrude(hub_length)
            .translate((0, 0, -hub_length / 2.0)))

# Flanges (Left and Right)
flange_l = (cq.Workplane("XY")
            .circle(flange_diameter / 2.0)
            .extrude(flange_width)
            .translate((0, 0, -flange_offset - flange_width / 2.0)))

flange_r = (cq.Workplane("XY")
            .circle(flange_diameter / 2.0)
            .extrude(flange_width)
            .translate((0, 0, flange_offset - flange_width / 2.0)))

# Axle bore (cut)
hub_assembly = hub_body.union(flange_l).union(flange_r)
hub_assembly = hub_assembly.faces("<Z").workplane().circle(hub_bore / 2.0).cutThruAll()

# 3. Create Spokes
# We need to generate spokes connecting the flanges to the rim.
# A realistic bicycle wheel has spokes angling from left/right flanges to the center of the rim.

spokes = cq.Assembly()

angle_step = 360.0 / num_spokes

# Helper function to create a single spoke
def create_spoke(angle, side_offset):
    # Calculate rim attachment point (center of rim width)
    # The rim is at radius rim_inner_r
    rim_x = rim_inner_r * math.cos(math.radians(angle))
    rim_y = rim_inner_r * math.sin(math.radians(angle))
    rim_z = 0  # Rim centerline

    # Calculate hub attachment point (on the flange)
    # We rotate the hub attachment slightly if we wanted a cross pattern, 
    # but for visual simplicity in this prompt, a direct radial-ish connection works well.
    # To mimic the image better, spokes often alternate sides.
    
    hub_radius = flange_diameter / 2.0 - 2.0 # Slightly inside the flange edge
    hub_x = hub_radius * math.cos(math.radians(angle))
    hub_y = hub_radius * math.sin(math.radians(angle))
    hub_z = side_offset

    # Create the vector for the spoke path
    p1 = (hub_x, hub_y, hub_z)
    p2 = (rim_x, rim_y, rim_z)
    
    # Create the spoke cylinder
    # We use a helper workplane oriented along the vector
    spoke_len = math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2 + (p2[2]-p1[2])**2)
    
    # CadQuery construction: define line, then sweep circle? 
    # Simpler: Make a cylinder at origin and rotate/translate it.
    
    # Using Workplane logic to orient 'Z' along the spoke direction
    spoke = (cq.Workplane("XY")
             .circle(spoke_diameter / 2.0)
             .extrude(spoke_len))
    
    # Calculate orientation vectors
    # Current vector is (0,0,1)
    # Target vector is P2 - P1
    v_target = cq.Vector(p2) - cq.Vector(p1)
    v_start = cq.Vector(0, 0, 1)
    
    # Rotate spoke to align with vector
    # Find axis of rotation (cross product) and angle
    
    # A simpler approach in pure CQ without manual vector math for rotation matrices:
    # Use solids creation directly between points if available, but standard API uses extrusion.
    # Let's use the transform approach:
    
    # Create a dummy object to act as the path
    path = cq.Workplane("XY").polyline([p1, p2])
    
    # Actually, constructing a cylinder directly is usually easiest if we just find the center and rotation.
    # But for robustness in a script, simply sweeping a circle along a path is very reliable.
    
    path_wire = cq.Workplane("XY").polyline([p1, p2]).wire()
    
    spoke_solid = (cq.Workplane("XY")
                   .workplane(offset=0) # Dummy plane
                   .newObject([path_wire.val()]) # Add the wire
                   .plane.toWorldCoords((0,0,0)) # Reset context if needed (less critical here)
                   )
    
    # Alternative: construct cylinder from point to point
    # Since specific "cylinder from p1 to p2" isn't a single primitive command in basic CQ API:
    center_point = ((p1[0]+p2[0])/2, (p1[1]+p2[1])/2, (p1[2]+p2[2])/2)
    
    # Let's try the solid makeCylinder approach from the kernel, wrapped in Workplane
    # Or, simple geometry:
    # Create cylinder along Z, rotate, translate.
    
    dx, dy, dz = v_target.x, v_target.y, v_target.z
    xy_dist = math.sqrt(dx*dx + dy*dy)
    phi = math.degrees(math.atan2(dy, dx)) # Rotation around Z
    theta = math.degrees(math.atan2(xy_dist, dz)) # Rotation from Z axis
    
    spoke = (cq.Workplane("XY")
             .circle(spoke_diameter/2.0)
             .extrude(spoke_len)
             .rotate((0,0,0), (0,1,0), theta) # Tilt away from Z
             .rotate((0,0,0), (0,0,1), phi)   # Spin around Z
             .translate(p1))
             
    return spoke

all_spokes = []

# Generate spokes alternating between left and right flanges
for i in range(num_spokes):
    angle = i * angle_step
    # Alternate flanges: Left (-offset) then Right (+offset)
    side = -flange_offset if i % 2 == 0 else flange_offset
    
    # Create the spoke
    spoke_geo = create_spoke(angle, side)
    all_spokes.append(spoke_geo)

# Combine everything
final_wheel = rim.union(hub_assembly)
for s in all_spokes:
    final_wheel = final_wheel.union(s)

result = final_wheel
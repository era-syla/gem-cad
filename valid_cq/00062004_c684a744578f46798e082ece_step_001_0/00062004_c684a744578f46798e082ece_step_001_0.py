import cadquery as cq
import math

# --- Parametric Dimensions ---
# Basic dimensions for the chain links
cyl_radius = 2.4
cyl_height = 12.0
link_pitch = 6.0      # Distance between cylinder centers
web_thickness = 1.0   # Thickness of the connecting bridge
web_height = 12.0     # Height of the bridge (same as cylinders)

# Gear dimensions
num_teeth = 16
gear_outer_radius = 16.0
gear_inner_radius = 11.0
gear_height = 12.0
gear_hole_radius = 1.0

# --- Helper Functions ---

def create_chain_strip(points):
    """
    Generates a solid chain strip from a list of (x,y) coordinates 
    representing the centers of the cylinders.
    """
    solids = []
    
    # 1. Create Cylinders
    for x, y in points:
        c = cq.Workplane("XY").center(x, y).circle(cyl_radius).extrude(cyl_height)
        solids.append(c)
        
    # 2. Create Connecting Webs
    for i in range(len(points) - 1):
        p1 = points[i]
        p2 = points[i+1]
        
        # Calculate geometry for the bridge
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        dist = math.sqrt(dx**2 + dy**2)
        angle_deg = math.degrees(math.atan2(dy, dx))
        
        mid_x = (p1[0] + p2[0]) / 2.0
        mid_y = (p1[1] + p2[1]) / 2.0
        
        # Create web at origin, rotate, then translate
        w = cq.Workplane("XY").rect(dist, web_thickness).extrude(web_height)
        w = w.rotate((0,0,0), (0,0,1), angle_deg).translate((mid_x, mid_y, 0))
        solids.append(w)
        
    # 3. Union all components
    compound = solids[0]
    for s in solids[1:]:
        compound = compound.union(s)
        
    return compound

def create_ratchet_gear():
    """
    Generates the sawtooth gear shape.
    """
    pts = []
    for i in range(num_teeth):
        # Calculate angles in radians
        angle_start = (2 * math.pi * i) / num_teeth
        angle_tip = (2 * math.pi * (i + 0.65)) / num_teeth # Tip is offset to create slope
        
        # Polar to Cartesian
        # Root point
        xr = gear_inner_radius * math.cos(angle_start)
        yr = gear_inner_radius * math.sin(angle_start)
        
        # Tip point
        xt = gear_outer_radius * math.cos(angle_tip)
        yt = gear_outer_radius * math.sin(angle_tip)
        
        pts.append((xr, yr))
        pts.append((xt, yt))
        
    pts.append(pts[0]) # Close the loop
    
    # Extrude gear profile
    gear = cq.Workplane("XY").polyline(pts).close().extrude(gear_height)
    
    # Cut center hole
    gear = gear.faces(">Z").workplane().circle(gear_hole_radius).cutThruAll()
    
    return gear

# --- Build the Assembly ---

# 1. Left Assembly: Two parallel, offset chains
# Row 1 (Back)
pts_row1 = [(i * link_pitch, 0) for i in range(6)]
chain_row1 = create_chain_strip(pts_row1)

# Row 2 (Front) - Offset for hexagonal packing look
# Vertical offset calculated for 60 degree triangle packing
row_spacing = link_pitch * math.sin(math.radians(60)) 
offset_x = link_pitch * 0.5
pts_row2 = [(i * link_pitch + offset_x, -row_spacing) for i in range(5)]
chain_row2 = create_chain_strip(pts_row2)

# Combine left parts and position them
left_assembly = chain_row1.union(chain_row2)
left_assembly = left_assembly.translate((-45, 0, 0))


# 2. Right Assembly: Gear and feeding chain
# Create Gear
gear = create_ratchet_gear()
# Position Gear
gear_center = (35, 5, 0)
gear = gear.translate(gear_center)

# Create Chain segment feeding into the gear
# We manually define points to simulate the chain wrapping around the gear
# Starting straight then curving up
start_x = 0
start_y = -8
pts_right = [
    (start_x, start_y),
    (start_x + link_pitch, start_y),
    (start_x + 2*link_pitch, start_y),
    (start_x + 3*link_pitch - 0.5, start_y + 1.5), # Begin slight curve
    (start_x + 4*link_pitch - 1.5, start_y + 4.5)  # Curving into gear
]

chain_right = create_chain_strip(pts_right)

# Combine everything into final result
result = left_assembly.union(chain_right).union(gear)

# If running in CQ-Editor, this will render the result
# show_object(result)
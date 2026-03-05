import cadquery as cq

# --- Parametric Dimensions ---
# Main Cylinder Body
total_length = 160.0
tube_radius = 22.0
cap_radius = 32.0
cap_width = 20.0

# Mounting Lugs (Ends)
lug_protrusion = 25.0   # Length extending from the cap face
lug_thickness = 18.0    # Width in Y
lug_height = 36.0       # Height in Z
lug_hole_diam = 12.0

# Fluid Ports (Bosses)
port_base_size = 18.0
port_height_above_cap = 8.0
port_hole_diam = 8.0
port_fillet = 3.0

# --- Geometry Construction ---

# 1. Main Tube (Centered between caps)
# The tube spans the distance between the two end caps
tube_length = total_length - (2 * cap_width)
tube = cq.Workplane("YZ").workplane(offset=cap_width).circle(tube_radius).extrude(tube_length)

# 2. End Caps
# Left Cap at X=0
cap_left = cq.Workplane("YZ").circle(cap_radius).extrude(cap_width)
# Right Cap at X=total_length - cap_width
cap_right = cq.Workplane("YZ").workplane(offset=total_length - cap_width).circle(cap_radius).extrude(cap_width)

# Combine Tube and Caps
body = tube.union(cap_left).union(cap_right)

# Add fillets at the transition between tube and caps
# Select edges near the junction points
junction_l = (cap_width, tube_radius, 0)
junction_r = (total_length - cap_width, tube_radius, 0)

try:
    body = body.edges(cq.selectors.NearestToPointSelector(junction_l)).fillet(3.0)
    body = body.edges(cq.selectors.NearestToPointSelector(junction_r)).fillet(3.0)
except Exception:
    # Fallback if selection fails, though coordinates should be precise
    pass

# 3. Fluid Ports
# Function to create a port boss
def create_port(x_center):
    # Create box
    p = (cq.Workplane("XY")
         .workplane(offset=cap_radius - 1.0) # Start slightly inside cap for overlap
         .rect(port_base_size, port_base_size)
         .extrude(port_height_above_cap + 1.0)
         )
    # Fillet vertical edges
    p = p.edges("|Z").fillet(port_fillet)
    # Drill hole
    p = p.faces(">Z").workplane().hole(port_hole_diam)
    # Move to correct X position
    p = p.translate((x_center, 0, 0))
    return p

port_l = create_port(cap_width / 2.0)
port_r = create_port(total_length - (cap_width / 2.0))

body = body.union(port_l).union(port_r)

# 4. End Mounting Lugs
# Function to create a lug using a profile sketch on XZ plane
def create_lug(is_left_side):
    sk = cq.Workplane("XZ")
    
    # Dimensions for the profile
    h = lug_height
    r = h / 2.0
    l_ext = lug_protrusion
    
    if is_left_side:
        # Drawing on Left (Negative X)
        x_face = 0
        x_center = -l_ext + r # Center of the rounded end
        
        # Profile: Start at face top, go to arc start, arc, back to face bottom, close
        sk = (sk.moveTo(x_face, r)
              .lineTo(x_center, r)
              .threePointArc((x_center - r, 0), (x_center, -r))
              .lineTo(x_face, -r)
              .close())
        hole_x = x_center
    else:
        # Drawing on Right (Positive X)
        x_face = total_length
        x_center = total_length + l_ext - r
        
        sk = (sk.moveTo(x_face, r)
              .lineTo(x_center, r)
              .threePointArc((x_center + r, 0), (x_center, -r))
              .lineTo(x_face, -r)
              .close())
        hole_x = x_center
        
    # Extrude symmetrically in Y
    lug = sk.extrude(lug_thickness / 2.0, both=True)
    
    # Cut the mounting hole
    # We select the side face (perpendicular to Y) to drill through
    lug = lug.faces("<Y").workplane().moveTo(hole_x, 0).hole(lug_hole_diam)
    
    return lug

lug_left = create_lug(True)
lug_right = create_lug(False)

# Final Union
result = body.union(lug_left).union(lug_right)
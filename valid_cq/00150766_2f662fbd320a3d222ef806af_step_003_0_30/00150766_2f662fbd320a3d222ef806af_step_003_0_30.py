import cadquery as cq
import math

# --- Parameters ---
# Duct / Prop Guard dimensions
duct_id = 42.0          # Inner diameter of the duct
duct_wall = 1.5         # Thickness of the duct wall
duct_height = 12.0      # Height of the duct
lip_radius = 1.2        # Radius of the flared lip at the top
duct_od = duct_id + (2 * duct_wall)

# Motor Hub dimensions
hub_od = 8.0            # Outer diameter of motor hub
hub_id = 4.0            # Hole for motor
hub_height = 6.0        # Height of the hub
strut_thickness = 1.8   # Thickness of struts connecting hub to duct
strut_height = 4.0      # Vertical height of struts

# Frame dimensions
wheelbase_x = 70.0      # Distance between motors (width)
wheelbase_y = 60.0      # Distance between motors (length)
plate_thickness = 3.0   # Thickness of the central plate
plate_width = 35.0      # Width of the central platform
plate_length = 50.0     # Length of the central platform

# Hex Pattern dimensions
hex_radius = 2.5        # Size of honeycomb holes
hex_spacing = 1.2       # Wall thickness between hexes

# --- Component Builders ---

def make_motor_pod():
    """Creates a single duct with motor hub and struts."""
    
    # 1. Main Duct Tube
    duct = (cq.Workplane("XY")
            .circle(duct_od / 2.0)
            .circle(duct_id / 2.0)
            .extrude(duct_height)
            )
    
    # 3. Motor Hub
    hub = (cq.Workplane("XY")
           .circle(hub_od / 2.0)
           .circle(hub_id / 2.0)
           .extrude(hub_height)
           )
    
    # 4. Struts (3 spokes)
    struts = cq.Workplane("XY")
    strut_len = (duct_id - hub_od) / 2.0
    
    for i in range(3):
        angle = 90 + (i * 120)  # Offset to look symmetrical
        s = (cq.Workplane("XY")
             .transformed(rotate=(0, 0, angle))
             .center(0, (hub_od/2.0) + (strut_len/2.0))
             .box(strut_thickness, strut_len + 1.0, strut_height) # +1 overlap for union
             .translate((0, 0, strut_height / 2.0))
             )
        struts = struts.union(s)
        
    # Combine all parts of the pod
    pod = duct.union(hub).union(struts)
    return pod

def make_honeycomb_grid(width, length, r, spacing):
    """Creates a honeycomb grid pattern to cut from the plate."""
    # Calculate geometric properties of hexagons
    # pointy topped hex
    # w = sqrt(3) * r
    # h = 2 * r
    hex_w = math.sqrt(3) * r
    hex_h = 2 * r
    
    col_step = hex_w + spacing
    row_step = (hex_h * 0.75) + spacing
    
    cols = int(width / col_step)
    rows = int(length / row_step)
    
    start_x = -((cols-1) * col_step) / 2
    start_y = -((rows-1) * row_step) / 2
    
    pts = []
    for row in range(rows):
        for col in range(cols):
            x_pos = start_x + col * col_step
            y_pos = start_y + row * row_step
            
            # Offset every other row
            if row % 2 == 1:
                x_pos += col_step / 2
            
            # Keep within the bounding box with some margin
            if (abs(x_pos) + hex_w/2 < width/2) and (abs(y_pos) + hex_h/2 < length/2):
                pts.append((x_pos, y_pos))
                
    hexes = (cq.Workplane("XY")
             .pushPoints(pts)
             .polygon(6, r * 2 * 0.9) # Diameter approx
             .extrude(plate_thickness * 2) # Ensure cut goes through
             )
    return hexes

# --- Assembly Construction ---

# 1. Create one pod instance
pod_geo = make_motor_pod()

# 2. Position 4 pods
pods = cq.Workplane("XY")
positions = [
    (wheelbase_x/2, wheelbase_y/2),
    (wheelbase_x/2, -wheelbase_y/2),
    (-wheelbase_x/2, wheelbase_y/2),
    (-wheelbase_x/2, -wheelbase_y/2)
]

for x, y in positions:
    p = pod_geo.translate((x, y, 0))
    pods = pods.union(p)

# 3. Create Central Frame Body
# We need a body that connects the pods.
# Strategy: Create a central box, and arms extending to the pods, then fillet.

# Center Plate Z-position: Align with the bottom-mid of the ducts
z_pos = (duct_height - plate_thickness) / 2.0

frame_body = (cq.Workplane("XY")
              .box(plate_width, plate_length + 20, plate_thickness) # +20 to reach towards pods
              .translate((0, 0, z_pos + plate_thickness/2.0))
              )

# Arms connecting the center to the pods
# We create a shape that bridges the center to the motor hubs/ducts
arms = (cq.Workplane("XY")
        .rect(wheelbase_x, wheelbase_y/2.0) # Horizontal bar top
        .rect(wheelbase_x, wheelbase_y/2.0) # Horizontal bar bottom
        .extrude(plate_thickness)
        .translate((0, 0, z_pos))
        )
# Shift arms to proper Y locations
arm_top = (cq.Workplane("XY")
           .center(0, wheelbase_y/2.0)
           .box(wheelbase_x + duct_id/2, 10, plate_thickness)
           .translate((0, 0, z_pos + plate_thickness/2))
           )
arm_bot = (cq.Workplane("XY")
           .center(0, -wheelbase_y/2.0)
           .box(wheelbase_x + duct_id/2, 10, plate_thickness)
           .translate((0, 0, z_pos + plate_thickness/2))
           )

# Union the structural parts
structure = pods.union(frame_body).union(arm_top).union(arm_bot)

# 4. Refine intersections (Fillets)
# This blends the arms into the ducts and the body for the "molded" look
# Note: Complex fillets can sometimes fail in CAD kernels, we use a conservative radius
try:
    structure = structure.edges("|Z").fillet(5.0)
except:
    # Fallback if fillet fails (usually due to geometry complexity)
    pass

# 5. Create Honeycomb Cutout
grid_cutter = make_honeycomb_grid(plate_width - 4, plate_length + 10, hex_radius, hex_spacing)
grid_cutter = grid_cutter.translate((0, 0, z_pos - 1)) # Position for cutting

# 6. Final boolean operations
result = structure.cut(grid_cutter)

# Optional: Add small fillets to the hex cuts for realism (computationally expensive, skipping for speed)
# result = result.edges("|Z").fillet(0.2)
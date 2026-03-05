import cadquery as cq

# ==========================================
# Parameters
# ==========================================

# Overall Tray Dimensions
tray_width = 240.0
tray_depth = 160.0
tray_height = 15.0

# Construction Parameters
wall_thickness = 2.0
floor_thickness = 2.0

# Internal Layout Configuration
# Column weights (Left, Middle, Right)
# Ratios estimated from image: 1 part, 2 parts, 2 parts
col_ratios = [1, 2, 2] 
# Row weights (Bottom to Top divisions)
row_ratios = [1, 1, 1, 1] 

# Texture (Grid of bumps) Parameters
bump_radius = 1.2
bump_spacing = 4.0  # Center-to-center distance
bump_margin = 1.5   # Minimum distance from walls

# ==========================================
# Helper Functions
# ==========================================

def calculate_grid_points(x_min, y_min, width, height, spacing, margin):
    """
    Generates a list of global (x, y) coordinates for the texture grid 
    centered within a specified rectangular area.
    """
    points = []
    
    # Effective area dimensions for bumps
    eff_w = width - 2 * margin
    eff_h = height - 2 * margin
    
    # Check if area is large enough for at least one bump
    if eff_w <= 0 or eff_h <= 0:
        return points
        
    # Calculate number of bumps in X and Y
    nx = int(eff_w / spacing)
    ny = int(eff_h / spacing)
    
    if nx <= 0 or ny <= 0:
        return points

    # Calculate starting offset to center the grid in the pocket
    span_x = (nx - 1) * spacing
    span_y = (ny - 1) * spacing
    
    # Starting coordinates (bottom-left of the grid)
    start_x = x_min + margin + (eff_w - span_x) / 2
    start_y = y_min + margin + (eff_h - span_y) / 2
    
    for i in range(nx):
        for j in range(ny):
            px = start_x + i * spacing
            py = start_y + j * spacing
            points.append((px, py))
            
    return points

# ==========================================
# Geometry Generation
# ==========================================

# 1. Create Base Block
# The tray is centered at the origin (0,0,0)
result = cq.Workplane("XY").box(tray_width, tray_depth, tray_height)

# 2. Calculate Compartment Layout Geometry
# Calculate unit dimensions based on available internal space
num_v_walls = len(col_ratios) + 1 # 2 outer + internal dividers
num_h_walls = len(row_ratios) + 1 

internal_width = tray_width - (num_v_walls * wall_thickness)
internal_depth = tray_depth - (num_h_walls * wall_thickness)

unit_width = internal_width / sum(col_ratios)
unit_depth = internal_depth / sum(row_ratios)

# Define Compartment List: tuples of (x_bottom_left, y_bottom_left, width, height)
compartments = []

# Start coordinates (bottom-left of the internal area, relative to global origin)
start_x = -tray_width/2 + wall_thickness
start_y = -tray_depth/2 + wall_thickness

current_x = start_x

# --- Column 1 (Left): 4 Vertically stacked compartments ---
c1_w = unit_width * col_ratios[0]
c1_y = start_y
for r in range(4):
    h = unit_depth * row_ratios[r]
    compartments.append((current_x, c1_y, c1_w, h))
    c1_y += h + wall_thickness

current_x += c1_w + wall_thickness

# --- Column 2 (Middle): 2 Compartments ---
c2_w = unit_width * col_ratios[1]
c2_y = start_y

# Bottom Middle (combines bottom 2 rows)
h_bot = (unit_depth * row_ratios[0]) + wall_thickness + (unit_depth * row_ratios[1])
compartments.append((current_x, c2_y, c2_w, h_bot))

# Top Middle (combines top 2 rows)
c2_y_top = c2_y + h_bot + wall_thickness
h_top = (unit_depth * row_ratios[2]) + wall_thickness + (unit_depth * row_ratios[3])
compartments.append((current_x, c2_y_top, c2_w, h_top))

current_x += c2_w + wall_thickness

# --- Column 3 (Right): 1 Large Compartment ---
c3_w = unit_width * col_ratios[2]
c3_y = start_y
# Spans full depth
h_full = tray_depth - 2 * wall_thickness
compartments.append((current_x, c3_y, c3_w, h_full))


# 3. Cut Pockets and Generate Texture Points
bump_points = []
cut_depth = tray_height - floor_thickness

for (x, y, w, h) in compartments:
    # Calculate center of the pocket for the rect() operation
    cx = x + w/2
    cy = y + h/2
    
    # Cut the pocket from the top face
    result = result.faces(">Z").workplane().moveTo(cx, cy).rect(w, h).cutBlind(-cut_depth)
    
    # Generate texture points for this specific pocket
    pts = calculate_grid_points(x, y, w, h, bump_spacing, bump_margin)
    bump_points.extend(pts)

# 4. Create and Union Texture Bumps
# Bumps are placed on the floor surface
floor_z_level = -tray_height/2 + floor_thickness

if bump_points:
    # Create a compound of spheres
    # We position the workplane at the floor level
    # pushPoints places the centers of the spheres at the points
    # Sphere radius creates a bump sticking up and embedded down
    bumps = (
        cq.Workplane("XY")
        .workplane(offset=floor_z_level)
        .pushPoints(bump_points)
        .sphere(bump_radius)
    )
    
    # Union the bumps to the main body
    result = result.union(bumps)

# Final result is stored in 'result'
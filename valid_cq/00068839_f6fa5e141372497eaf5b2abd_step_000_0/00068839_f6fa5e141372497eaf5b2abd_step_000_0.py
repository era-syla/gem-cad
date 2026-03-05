import cadquery as cq
import math

# --- Parameters ---
inner_radius = 30.0        # Radius of the central hole
ring_width = 8.0           # Width of the solid inner ring
spiral_width = 8.0         # Width of the spiral arms
gap = 2.0                  # Gap between arms
height = 6.0               # Thickness of the part
num_arms = 2               # Number of spiral arms
turns = 1.25               # Number of turns for each arm
pocket_size = 3.0          # Size of the square pockets
pocket_depth = 1.5         # Depth of the pockets
res = 128                  # Resolution for spiral discretization

# --- Derived Geometry Calculations ---
r_start = inner_radius + ring_width
# Archimedean spiral growth rate k
# Radial growth per 360/N degrees must be (width + gap)
# k * (2*pi / N) = width + gap  =>  k = N*(width + gap) / (2*pi)
k = (num_arms * (spiral_width + gap)) / (2 * math.pi)
total_angle = turns * 2 * math.pi

# --- Helper Functions ---

def generate_spiral_arm(angle_offset_deg):
    """Generates a spiral arm solid rotated by a specific angle."""
    pts_in = []
    pts_out = []
    
    # Generate points for inner and outer walls of the spiral arm
    for i in range(res + 1):
        theta = (i / res) * total_angle
        
        # Archimedean spiral equation
        r_in = r_start + k * theta
        r_out = r_in + spiral_width
        
        # Convert to Cartesian coordinates
        x_in = r_in * math.cos(theta)
        y_in = r_in * math.sin(theta)
        x_out = r_out * math.cos(theta)
        y_out = r_out * math.sin(theta)
        
        pts_in.append((x_in, y_in))
        pts_out.append((x_out, y_out))
        
    # Construct the closed wire (inner path -> close end -> outer path reversed -> close start)
    # Note: pts_out is reversed to traverse back to start
    pts = pts_in + pts_out[::-1]
    
    # Create the solid
    arm = (cq.Workplane("XY")
           .polyline(pts)
           .close()
           .extrude(height)
           .rotate((0,0,0), (0,0,1), angle_offset_deg))
    return arm

def cut_pockets_on_arm(solid, arm_start_angle_deg):
    """Cuts decorative/functional pockets into an existing solid along the spiral path."""
    # Locations of pockets in terms of local spiral theta (radians)
    # One near the tip, one ~180 degrees back
    locations = [total_angle - 0.2, total_angle - math.pi - 0.2]
    
    result_solid = solid
    
    for theta_local in locations:
        # Calculate center position of the pocket
        r_mid = r_start + k * theta_local + (spiral_width / 2.0)
        
        # Global angle includes the arm's rotation
        theta_global = theta_local + math.radians(arm_start_angle_deg)
        
        pos_x = r_mid * math.cos(theta_global)
        pos_y = r_mid * math.sin(theta_global)
        
        # Calculate tangent angle to align the square pocket with the arm
        # Derivative of position with respect to theta
        # x = r*cos(t), y = r*sin(t) -> x' = r'*cos(t) - r*sin(t), y' = r'*sin(t) + r*cos(t)
        dr = k
        dx = dr * math.cos(theta_global) - r_mid * math.sin(theta_global)
        dy = dr * math.sin(theta_global) + r_mid * math.cos(theta_global)
        tangent_angle_deg = math.degrees(math.atan2(dy, dx))
        
        # Create a tool object for the cut
        pocket_tool = (cq.Workplane("XY")
                       .rect(pocket_size, pocket_size)
                       .extrude(pocket_depth)
                       .rotate((0,0,0), (0,0,1), tangent_angle_deg)
                       .translate((pos_x, pos_y, height - pocket_depth)))
        
        result_solid = result_solid.cut(pocket_tool)
        
    return result_solid

# --- Main Geometry Construction ---

# 1. Inner Center Ring
center_ring = (cq.Workplane("XY")
               .circle(r_start)
               .circle(inner_radius)
               .extrude(height))

# 2. Generate Arms
arm1 = generate_spiral_arm(0)
arm2 = generate_spiral_arm(180)

# 3. Fuse Base Geometry
base_geo = center_ring.union(arm1).union(arm2)

# 4. Add Features (Pockets)
# We apply cuts to the fused geometry for each arm's logic
result = cut_pockets_on_arm(base_geo, 0)
result = cut_pockets_on_arm(result, 180)
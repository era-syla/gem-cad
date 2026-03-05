import cadquery as cq
import math

# --- Parametric Variables ---
# Table Top Dimensions
table_length = 1600.0
table_width = 800.0
table_thickness = 30.0

# Leg Dimensions
leg_height = 720.0  # Vertical height from floor to underside of table
leg_top_radius = 25.0
leg_mid_radius = 20.0
leg_bottom_radius = 15.0

# Leg Styling Details
groove_section_length = 120.0 # Length of the bottom section with grooves
groove_count = 3
groove_width = 5.0
groove_depth = 2.0
foot_height = 10.0
foot_radius = 22.0

# Leg Positioning
leg_inset_x = 150.0  # Distance from short edge
leg_inset_y = 100.0  # Distance from long edge
leg_splay_angle = 10.0 # Degrees legs are tilted outwards

# --- Helper Functions ---

def create_leg():
    """
    Creates a single detailed table leg with a taper and grooves.
    The leg is created vertically centered at the origin, pointing -Z.
    """
    
    # 1. Main Shaft (Tapered)
    # Total length of the wooden part excluding the foot
    shaft_length = leg_height - foot_height
    
    # Create the main tapered cylinder
    shaft = cq.Workplane("XY").circle(leg_top_radius).workplane(offset=-shaft_length).circle(leg_bottom_radius).loft()
    
    # 2. Add Grooves near the bottom
    # We'll cut rings out of the shaft
    
    # Calculate spacing for grooves within the groove_section_length
    # Let's place them evenly near the bottom of the shaft
    start_z = -shaft_length + foot_height + 15.0 # Start a bit up from the foot
    spacing = 20.0 
    
    for i in range(groove_count):
        z_pos = start_z + (i * spacing)
        # Calculate local radius at this Z height (linear interpolation)
        t = abs(z_pos) / shaft_length
        local_r = leg_top_radius - (leg_top_radius - leg_bottom_radius) * t
        
        # Create a cutter
        cutter = (cq.Workplane("XY")
                  .workplane(offset=z_pos)
                  .circle(local_r + 5) # Outer boundary (large enough)
                  .circle(local_r - groove_depth) # Inner groove bottom
                  .extrude(groove_width)
                  )
        # Perform cut. Note: ring creation logic is: OuterCircle - InnerCircle = Ring, then cut
        # Actually easier to just revolve a profile or cut a torus, but extrude cut works fine
        
        # Correct approach for boolean cut of a ring:
        # We need the solid ring to subtract
        ring = (cq.Workplane("XY")
                .workplane(offset=z_pos)
                .circle(local_r + 10) # Outer
                .circle(local_r - groove_depth) # Inner
                .extrude(groove_width))
        
        shaft = shaft.cut(ring)

    # 3. Add the Foot
    foot = (cq.Workplane("XY")
            .workplane(offset=-shaft_length)
            .circle(foot_radius)
            .extrude(-foot_height))
            
    leg_assembly = shaft.union(foot)
    return leg_assembly

# --- Main Assembly Construction ---

# 1. Create Table Top
table_top = cq.Workplane("XY").box(table_length, table_width, table_thickness)

# 2. Create the Base Leg Geometry
base_leg = create_leg()

# 3. Position and Rotate Legs
legs = cq.Assembly()

# Corner positions (relative to center of table)
corners = [
    (1, 1),   # Top Right
    (1, -1),  # Bottom Right
    (-1, -1), # Bottom Left
    (-1, 1)   # Top Left
]

# Create a composite solid for the legs
all_legs = None

for x_sign, y_sign in corners:
    # Position where the leg meets the table
    pos_x = x_sign * (table_length / 2.0 - leg_inset_x)
    pos_y = y_sign * (table_width / 2.0 - leg_inset_y)
    pos_z = -table_thickness / 2.0
    
    # Determine rotation axis and angle for the splay
    # If x is pos and y is pos, we want to rotate around vector (-1, 1, 0)? No.
    # We simply rotate around X and Y axes independently or construct a vector.
    # Simple method: Rotate around local X and Y.
    
    rot_x = -y_sign * leg_splay_angle # Rotate around X tilts it in Y direction
    rot_y = x_sign * leg_splay_angle  # Rotate around Y tilts it in X direction
    
    # Transform the leg
    transformed_leg = (base_leg
                       .rotate((0,0,0), (1,0,0), rot_x)
                       .rotate((0,0,0), (0,1,0), rot_y)
                       .translate((pos_x, pos_y, pos_z)))
                       
    if all_legs is None:
        all_legs = transformed_leg
    else:
        all_legs = all_legs.union(transformed_leg)

# Combine everything
result = table_top.union(all_legs)

# Export for visualization (optional in some viewers, standard pattern here)
if 'show_object' in globals():
    show_object(result)
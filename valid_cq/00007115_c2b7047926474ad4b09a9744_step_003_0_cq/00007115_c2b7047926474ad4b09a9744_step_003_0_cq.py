import cadquery as cq
from math import pi, cos, sin, radians

def create_involute_gear(module=1, teeth=30, pressure_angle=20, width=10, 
                         clearance=0.1, backlash=0.0):
    """
    Creates a standard involute spur gear.
    
    Args:
        module: The module of the gear (pitch diameter / number of teeth).
        teeth: Number of teeth.
        pressure_angle: Pressure angle in degrees (usually 20).
        width: The thickness of the gear.
        clearance: Bottom clearance factor.
        backlash: Gap between teeth (not strictly necessary for visual model but good practice).
    
    Returns:
        A CadQuery Workplane object representing the gear.
    """
    
    # Calculate gear parameters
    pitch_radius = (module * teeth) / 2.0
    base_radius = pitch_radius * cos(radians(pressure_angle))
    addendum = module
    dedendum = 1.25 * module  # Standard dedendum
    outer_radius = pitch_radius + addendum
    root_radius = pitch_radius - dedendum

    # Generate the involute profile for one tooth
    # We need points for the involute curve
    # The involute starts at the base circle and goes outwards
    
    # Calculate tooth thickness angle at pitch circle
    # tooth_thickness_at_pitch = (pi * module) / 2 - backlash
    # angle_tooth_thickness = tooth_thickness_at_pitch / pitch_radius # in radians
    
    # More simply, the angular width of a tooth + gap is 360/teeth
    # A tooth takes up half of that minus backlash adjustments.
    
    # We will construct the profile by defining points
    points = []
    
    # Resolution for the involute curve
    num_points = 10
    
    # Angle where the involute meets the outer circle
    # arccos(base_radius / outer_radius) gives the pressure angle at the tip
    # inv(alpha) = tan(alpha) - alpha
    
    import math
    
    # Calculate the angle offset for the involute intersection at pitch radius
    # Involute function: inv(alpha) = tan(alpha) - alpha
    alpha_pitch = radians(pressure_angle)
    inv_alpha_pitch = math.tan(alpha_pitch) - alpha_pitch
    
    # Angle step per tooth (360 / teeth)
    pitch_angle = 2 * pi / teeth
    
    # Half tooth angle at base circle (this is the tricky part in involute generation)
    # The angle subtended by the half-tooth thickness at the base circle is:
    # angle_offset = (pi / (2*teeth)) + inv_alpha_pitch
    
    angle_offset = (pi / (2 * teeth)) + inv_alpha_pitch
    
    # Generate points for the right side of the tooth
    # Parametric variable t ranges from 0 upwards
    # r = base_radius / cos(t)
    # theta = tan(t) - t
    
    # Find max t for outer radius
    # outer_radius = base_radius / cos(t_max)
    t_max = math.acos(base_radius / outer_radius)
    
    tooth_profile = []
    
    # Root fillet/bottom land
    tooth_profile.append((root_radius * cos(-pitch_angle/2), root_radius * sin(-pitch_angle/2)))
    
    # Involute curve (Right Side)
    # We iterate t to create the curve
    # We need to rotate this curve so it sits correctly relative to the centerline
    
    right_involute = []
    for i in range(num_points + 1):
        t = (i / num_points) * t_max
        r = base_radius / math.cos(t)
        theta_inv = math.tan(t) - t
        
        # The involute generates starting from theta=0 at the base circle.
        # We need to rotate it so the tooth is centered on the X axis.
        # The involute at pitch radius (pressure angle) should act at angle = - (pi/2*teeth)
        
        theta = -angle_offset + theta_inv
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        
        # Only add if r >= root_radius (undercut check simplified)
        if r >= root_radius:
            right_involute.append((x, y))
            
    # If the base radius is larger than root radius, connect root to start of involute
    if base_radius > root_radius:
        # Start of involute
        start_inv_x, start_inv_y = right_involute[0]
        # Calculate intersection with root circle at the angle of start of involute
        # This is a simplification; real gears have trochoidal fillets
        tooth_profile.append((root_radius * cos(-angle_offset), root_radius * sin(-angle_offset)))
        
    tooth_profile.extend(right_involute)
    
    # Left Side (Mirror of Right Side)
    left_involute = []
    for x, y in reversed(right_involute):
        left_involute.append((x, -y))
        
    tooth_profile.extend(left_involute)
    
    # Close the loop to the next tooth start (simplified)
    # tooth_profile.append((root_radius * cos(pitch_angle/2), root_radius * sin(pitch_angle/2)))

    # Create the single tooth wire
    tooth_wire = cq.Workplane("XY").polyline(tooth_profile).close()
    
    # Extrude the single tooth
    tooth_solid = tooth_wire.extrude(width)
    
    # Create the central cylinder (root cylinder)
    # Note: To ensure solidity, we make the cylinder slightly larger than root radius just to be safe, 
    # but theoretically root_radius is correct.
    core = cq.Workplane("XY").circle(root_radius).extrude(width)
    
    # Pattern the tooth
    # We unite the core and one tooth, then polar pattern the result? 
    # Or create all teeth and unite.
    
    # Efficient way in CQ: Pattern the tooth solid
    teeth_solids = tooth_solid.rotateAboutCenter((0,0,1), 0) # Just to initialize patterning context if needed
    
    # Create the full gear by unioning patterned teeth
    final_gear = core
    for i in range(teeth):
        angle = (360.0 / teeth) * i
        rotated_tooth = tooth_solid.rotate((0,0,0), (0,0,1), angle)
        final_gear = final_gear.union(rotated_tooth)
        
    return final_gear

# --- Model Parameters ---
module_val = 2.0
num_teeth = 36
gear_width_total = 30.0
pressure_angle_val = 20.0

# Calculate geometries derived from parameters
pd = module_val * num_teeth # Pitch diameter
rd = pd - (2 * 1.25 * module_val) # Approximate root diameter for the groove

# The image shows a gear that looks like it has a groove in the middle, 
# essentially splitting the gear face into two sections.
section_width = gear_width_total / 2.0 # Wait, the groove is in the middle.
# Let's say top gear section is 12mm, bottom is 12mm, middle groove is 6mm.
# Actually, looking closely, it looks like a single gear with a groove cut into it.

# Strategy:
# 1. Create a full width gear.
# 2. Cut a groove (revolve cut or cylinder cut) in the middle.

# Generate the base gear
gear = create_involute_gear(
    module=module_val,
    teeth=num_teeth,
    pressure_angle=pressure_angle_val,
    width=gear_width_total
)

# Define groove parameters
groove_width = 4.0
groove_depth_from_tip = 3.5 # How deep the cut goes
# The cut seems to go down to roughly the root diameter or slightly above it.
# Let's define the diameter of the groove.
# Root Diameter calculation: Pitch Dia - 2 * 1.25 * Module
root_diameter = (module_val * num_teeth) - (2.5 * module_val)
groove_diameter = root_diameter + 1.0 # Slightly above root for visual similarity

# Create the cutting tool for the groove
# We need a cylinder or ring to subtract from the middle
# Z position of the cut: It's centered vertically.
z_center = gear_width_total / 2.0

# Create a large cylinder to cut the outer teeth away, but leaving the inner core
# We can do this by creating a tube (outer radius very large, inner radius = groove radius)
outer_cut_radius = (module_val * num_teeth / 2.0) + module_val + 5.0 # Well clear of the gear tips
inner_cut_radius = groove_diameter / 2.0

cutter = (
    cq.Workplane("XY")
    .workplane(offset=z_center - (groove_width / 2.0)) # Move to start of cut
    .circle(outer_cut_radius)
    .circle(inner_cut_radius)
    .extrude(groove_width)
)

# Apply the cut
result = gear.cut(cutter)

# Optional: Add a central bore (shaft hole) as is typical for gears, 
# though not explicitly visible in the isometric view (top surface is solid).
# The image shows a solid top surface, so no bore hole.

# Move result to center the Z axis usually, but default extrude starts at Z=0, which is fine.
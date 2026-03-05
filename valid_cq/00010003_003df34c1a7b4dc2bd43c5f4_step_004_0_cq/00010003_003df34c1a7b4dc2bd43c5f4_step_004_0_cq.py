import cadquery as cq
import math

# Parameters for the large gear
large_gear_teeth = 30
large_gear_module = 2.0  # Module controls the size of teeth
large_gear_thickness = 15.0
large_gear_pressure_angle = 20.0

# Parameters for the small gear
small_gear_teeth = 12
small_gear_module = 2.0
small_gear_thickness = 15.0
small_gear_pressure_angle = 20.0

# Central bore
bore_diameter = 5.0

# Helper function to generate an involute gear profile
# CadQuery creates gears somewhat manually or via specialized logic. 
# For a standard visual representation, trapezoidal teeth are often sufficient 
# if the involute calculation is too verbose for a concise script, 
# but CadQuery has a parametric geometry capability we can build.
# However, a simpler approach for visual accuracy without needing an external
# 'involute_gear' library is to construct the shape using a polar array of teeth.

def create_gear(num_teeth, module, thickness, pressure_angle=20.0, bore_diam=0):
    # Calculate dimensions
    pitch_diameter = module * num_teeth
    addendum = module
    dedendum = 1.25 * module
    outer_radius = (pitch_diameter / 2) + addendum
    root_radius = (pitch_diameter / 2) - dedendum
    
    # Calculate angular widths
    # Pitch point angle
    pitch_angle = 360.0 / num_teeth
    
    # Simplified tooth geometry (trapezoidal approximation of involute)
    # At the root, the tooth is wider. At the tip, it is narrower.
    # Base tooth width at pitch circle is approx pi * module / 2
    tooth_width_pitch = (math.pi * module) / 2
    
    # Angle covered by tooth at pitch circle
    half_tooth_angle = (tooth_width_pitch / (pitch_diameter / 2)) * (180 / math.pi) / 2
    
    # Create the profile of one tooth valley and one tooth
    # We will define a profile and extrude it
    
    # Base circle
    base = cq.Workplane("XY").circle(root_radius).extrude(thickness)
    
    # Define a single tooth shape
    # Points for a simplified trapezoidal tooth
    # We work in coordinates relative to the center, rotated
    
    # Tip width (narrower than pitch width)
    tip_width_angle = half_tooth_angle * 0.6 # approximation
    
    # Root width (wider than pitch width)
    root_width_angle = half_tooth_angle * 1.4 # approximation
    
    def get_point(radius, angle_deg):
        rad = math.radians(angle_deg)
        return (radius * math.cos(rad), radius * math.sin(rad))

    # Points for one tooth centered on X axis
    p1 = get_point(root_radius - 0.1, -root_width_angle) # slightly inside root
    p2 = get_point(outer_radius, -tip_width_angle)
    p3 = get_point(outer_radius, tip_width_angle)
    p4 = get_point(root_radius - 0.1, root_width_angle) # slightly inside root
    
    tooth_profile = (
        cq.Workplane("XY")
        .polyline([p1, p2, p3, p4])
        .close()
        .extrude(thickness)
    )
    
    # Create all teeth by rotating and unioning
    teeth = tooth_profile
    for i in range(1, num_teeth):
        rotated_tooth = tooth_profile.rotate((0, 0, 0), (0, 0, 1), i * pitch_angle)
        teeth = teeth.union(rotated_tooth)
        
    # Combine base cylinder and teeth
    gear = base.union(teeth)
    
    # Cut the bore
    if bore_diam > 0:
        gear = gear.faces("<Z").workplane().circle(bore_diam / 2).cutThruAll()
        
    return gear

# Create the large gear (bottom)
large_gear = create_gear(
    num_teeth=large_gear_teeth,
    module=large_gear_module,
    thickness=large_gear_thickness,
    pressure_angle=large_gear_pressure_angle,
    bore_diam=0 # We will cut the bore at the end through both
)

# Create the small gear (top)
small_gear = create_gear(
    num_teeth=small_gear_teeth,
    module=small_gear_module,
    thickness=small_gear_thickness,
    pressure_angle=small_gear_pressure_angle,
    bore_diam=0
)

# Move the small gear to the top of the large gear
small_gear_translated = small_gear.translate((0, 0, large_gear_thickness))

# Combine the two gears
compound_gear = large_gear.union(small_gear_translated)

# Cut the central shaft hole through the entire assembly
result = (
    compound_gear
    .faces("<Z")
    .workplane()
    .circle(bore_diameter / 2)
    .cutThruAll()
)
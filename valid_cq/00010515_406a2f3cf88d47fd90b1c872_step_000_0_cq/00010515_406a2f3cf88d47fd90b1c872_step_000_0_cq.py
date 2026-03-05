import cadquery as cq
import math

# ------------------------------------------------------------------
# Parametric Constants
# ------------------------------------------------------------------

# Gear Parameters
MODULE = 1.0              # Size of teeth
NUM_TEETH = 80            # Number of teeth
PRESSURE_ANGLE = 20.0     # Standard pressure angle
GEAR_THICKNESS = 5.0      # Thickness of the gear face

# Hub Parameters
HUB_DIAMETER = 20.0       # Diameter of the central hub
HUB_HEIGHT = 10.0         # Height of the hub extending from gear face
BORE_DIAMETER = 8.0       # Center hole diameter

# Set Screw Parameters
SETSCREW_DIAMETER = 3.0   # Diameter of the set screw hole
SETSCREW_DISTANCE = 5.0   # Distance from hub edge (or appropriate placement)
SETSCREW_OFFSET = HUB_HEIGHT / 2.0 # Vertical placement on the hub

# Calculated dimensions
PITCH_RADIUS = (MODULE * NUM_TEETH) / 2.0
OUTER_RADIUS = PITCH_RADIUS + MODULE
ROOT_RADIUS = PITCH_RADIUS - (1.25 * MODULE)
TOTAL_HEIGHT = GEAR_THICKNESS + HUB_HEIGHT

# ------------------------------------------------------------------
# Helper Function: Involute Gear Profile
# ------------------------------------------------------------------

def create_spur_gear(module, num_teeth, thickness, pressure_angle=20.0):
    """
    Creates a simple spur gear approximation using CadQuery.
    """
    pitch_diameter = module * num_teeth
    base_diameter = pitch_diameter * math.cos(math.radians(pressure_angle))
    addendum = module
    dedendum = 1.25 * module
    outside_diameter = pitch_diameter + 2 * addendum
    root_diameter = pitch_diameter - 2 * dedendum
    
    # We will use the standard involute_gear generator provided by 
    # some CadQuery extensions, or build a simplified one. 
    # However, CadQuery Core doesn't have a built-in "gear" primitive 
    # easily accessible without extra libraries in a single script.
    # We will model the gear by creating a cylinder and cutting teeth 
    # to ensure the script runs standalone with standard CQ.
    
    # Base disk
    gear_blank = cq.Workplane("XY").circle(outside_diameter / 2).extrude(thickness)
    
    # Tooth Cutter Shape (Trapezoidal approximation for visual fidelity)
    # A real involute is complex to script from scratch without the add-on.
    # This creates a "rack" profile shape to cut out the gaps.
    
    # Calculate angular pitch
    angle_pitch = 360.0 / num_teeth
    
    # Tooth gap geometry parameters
    # Width at pitch circle ~ pi * m / 2
    tooth_width_pitch = (math.pi * module) / 2
    
    # Create a cutting tool for the gap between teeth
    # Gap shape is roughly trapezoidal, wider at top
    gap_bottom_width = tooth_width_pitch * 0.8 # approx
    gap_top_width = tooth_width_pitch * 1.4 # approx
    gap_depth = addendum + dedendum
    
    # Coordinates for a single tooth gap cutter (centered on Y axis)
    # We cut from the outside moving in.
    cutter_pts = [
        (-gap_top_width/2, outside_diameter/2 + 1),
        (gap_top_width/2, outside_diameter/2 + 1),
        (gap_bottom_width/2, root_diameter/2),
        (-gap_bottom_width/2, root_diameter/2)
    ]
    
    cutter = (
        cq.Workplane("XY")
        .polyline(cutter_pts)
        .close()
        .extrude(thickness)
    )
    
    # Subtract the cutter geometric pattern from the blank
    for i in range(num_teeth):
        angle = i * angle_pitch
        rotated_cutter = cutter.rotate((0,0,0), (0,0,1), angle)
        gear_blank = gear_blank.cut(rotated_cutter)
        
    return gear_blank

# ------------------------------------------------------------------
# Main Modeling Logic
# ------------------------------------------------------------------

# 1. Create the Gear (Face)
# Using the function above to generate the toothed profile
gear_body = create_spur_gear(MODULE, NUM_TEETH, GEAR_THICKNESS, PRESSURE_ANGLE)

# 2. Create the Hub
# The hub is a cylinder attached to the gear face.
hub = (
    cq.Workplane("XY")
    .workplane(offset=GEAR_THICKNESS)
    .circle(HUB_DIAMETER / 2.0)
    .extrude(HUB_HEIGHT)
)

# Combine gear and hub
main_body = gear_body.union(hub)

# 3. Create the Bore (Central Hole)
# Cut through the entire assembly
main_body_with_bore = (
    main_body
    .faces("<Z")
    .workplane()
    .circle(BORE_DIAMETER / 2.0)
    .cutThruAll()
)

# 4. Create Set Screw Holes
# The image shows two set screw holes on the hub, likely 90 degrees apart.
# We need to target the side of the hub.

# Position for set screws (middle of the hub height)
screw_z_pos = GEAR_THICKNESS + (HUB_HEIGHT / 2.0)

# Create the first set screw hole
result = (
    main_body_with_bore
    .faces(">Z") # Select the top face of the hub
    .workplane()
    .transformed(offset=(0, 0, -HUB_HEIGHT/2.0)) # Move plane to middle of hub
    .transformed(rotate=(90, 0, 0)) # Rotate to face the side
    .circle(SETSCREW_DIAMETER / 2.0)
    .cutThruAll() # Simple cut through the hub wall
)

# Create the second set screw hole (rotated 90 degrees)
# We achieve this by rotating a cutter or rotating the workplane logic.
# Here we'll create a second cut explicitly.
cutter_hole_2 = (
    cq.Workplane("XZ") # Start from side plane
    .workplane(offset=0)
    .center(0, screw_z_pos) # Center at correct height
    .circle(SETSCREW_DIAMETER / 2.0)
    .extrude(HUB_DIAMETER) # Make a long cylinder to cut with
)

# Align the cutter correctly if needed, but easier method:
# Just reuse the workplane logic rotated 90 degrees around Z
result = (
    result
    .faces(">Z")
    .workplane()
    .transformed(offset=(0, 0, -HUB_HEIGHT/2.0))
    .transformed(rotate=(90, 0, 90)) # Rotate 90 deg around Z, then face side
    .circle(SETSCREW_DIAMETER / 2.0)
    .cutThruAll()
)

# Add a chamfer to the bore entrance for realism
result = result.faces("<Z[0]").edges(cq.selectors.RadiusNthSelector(0)).chamfer(0.5)

# Optional: Add small fillet between hub and gear face
# Selecting the edge at the intersection of Z=GEAR_THICKNESS and radius=HUB_DIAMETER/2
try:
    result = result.edges(
        cq.selectors.NearestToPointSelector((HUB_DIAMETER/2, 0, GEAR_THICKNESS))
    ).fillet(1.0)
except:
    # Fallback if selection is tricky due to mesh complexity
    pass 

# Final assignment
result = result
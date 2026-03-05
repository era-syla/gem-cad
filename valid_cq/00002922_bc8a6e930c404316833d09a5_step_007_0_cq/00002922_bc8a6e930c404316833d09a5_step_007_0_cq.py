import cadquery as cq
import math

# --- Parametric Dimensions ---
# Pulley body dimensions
pulley_teeth_count = 20
pulley_pitch = 2.0  # e.g., GT2 pitch
pulley_od = (pulley_teeth_count * pulley_pitch) / math.pi  # Outer Diameter
pulley_width = 7.0  # Width of the toothed section
flange_od = pulley_od + 4.0  # Flanges need to be larger than the teeth
flange_thickness = 1.0
hub_od = 12.0
hub_length = 6.0
bore_diameter = 5.0
chamfer_size = 0.5

# Tooth profile dimensions (simplified GT2-like profile)
tooth_depth = 0.75
tooth_width = 1.2  # Approximate width of the groove

# --- Helper Function for Tooth Profile ---
def create_tooth_cutter(od, depth, width, length):
    """Creates a cutting solid for a single tooth groove."""
    # Create a profile that will be extruded to cut the tooth
    # The profile is a rounded groove
    
    # Calculate radius for the groove bottom
    r = width / 2.0
    
    # Points for the groove profile (2D) centered on Y axis, cutting into -Y
    # We will position this relative to the pulley later
    
    # Create a sketch for the groove cross-section
    # Using a simple U-shape or semi-circle for the groove
    s = (
        cq.Workplane("XY")
        .moveTo(width/2, 0)
        .lineTo(width/2, depth)
        .lineTo(-width/2, depth)
        .lineTo(-width/2, 0)
        .threePointArc((0, -depth*0.5), (width/2, 0))
        .close()
    )
    
    # Extrude the cutter
    cutter = s.extrude(length)
    
    # Rotate and position the cutter to bite into the cylinder
    # Orient so the 'depth' goes towards the center of the pulley
    cutter = cutter.rotate((0,0,0), (1,0,0), 90) # Orient length along Z
    cutter = cutter.translate((0, od/2, length/2)) # Move to OD
    
    return cutter

# --- Main Construction ---

# 1. Create the main toothed cylinder body
# Start with a solid cylinder representing the OD
main_body = cq.Workplane("XY").circle(pulley_od / 2).extrude(pulley_width)

# 2. Create the teeth
# We create one cutter and pattern it
cutter_profile = (
    cq.Workplane("XZ")
    .moveTo(-tooth_width/2, pulley_od/2)
    .lineTo(-tooth_width/2, pulley_od/2 - tooth_depth)
    # Create the bottom arc of the tooth groove
    .threePointArc((0, pulley_od/2 - tooth_depth - 0.2), (tooth_width/2, pulley_od/2 - tooth_depth))
    .lineTo(tooth_width/2, pulley_od/2)
    .close()
)

# Extrude the cutter profile through the width of the pulley
tooth_cutter = cutter_profile.extrude(pulley_width)

# Create a list of rotation angles
angles = range(0, 360, int(360/pulley_teeth_count))

# Cut the teeth
for angle in angles:
    main_body = main_body.cut(tooth_cutter.rotate((0,0,0), (0,0,1), angle))

# 3. Create the flanges
# Top Flange
flange_top = (
    cq.Workplane("XY")
    .workplane(offset=pulley_width)
    .circle(flange_od / 2)
    .extrude(flange_thickness)
)

# Bottom Flange (offset downwards to clamp the belt area)
flange_bottom = (
    cq.Workplane("XY")
    .workplane(offset=-flange_thickness)
    .circle(flange_od / 2)
    .extrude(flange_thickness)
)

# 4. Create the Hub
hub = (
    cq.Workplane("XY")
    .workplane(offset=-flange_thickness - hub_length) # Stick out the back
    .circle(hub_od / 2)
    .extrude(hub_length)
)

# 5. Small boss/raised ring on the top flange (visible in image)
top_boss_od = hub_od * 0.8
top_boss_height = 0.5
top_boss = (
    cq.Workplane("XY")
    .workplane(offset=pulley_width + flange_thickness)
    .circle(top_boss_od / 2)
    .extrude(top_boss_height)
)

# Combine all positive volumes
pulley = main_body.union(flange_top).union(flange_bottom).union(hub).union(top_boss)

# 6. Create the central Bore
pulley = pulley.faces(">Z").workplane().circle(bore_diameter / 2).cutThruAll()

# 7. Add Chamfers
# Chamfer the bore entrance slightly
pulley = (
    pulley.faces(">Z")
    .edges(cq.selectors.RadiusNthSelector(0)) # Select the smallest radius edge (the hole)
    .chamfer(chamfer_size/2)
)

# Chamfer the hub edge
pulley = (
    pulley.faces("<Z")
    .edges(cq.selectors.RadiusNthSelector(1)) # Select the hub outer edge
    .chamfer(chamfer_size)
)

result = pulley
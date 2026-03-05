import cadquery as cq

# --- Parameter Definitions ---
# Overall dimensions
wheel_radius = 50.0       # Radius from center to the center of the rim cross-section
rim_thickness = 8.0       # Diameter of the rim's circular cross-section

# Hub dimensions
hub_outer_diameter = 18.0
hub_inner_diameter = 8.0
hub_height = 25.0         # Total height of the central hub

# Spoke dimensions
num_spokes = 3
spoke_width = 12.0        # Width of the spoke (as seen from top)
spoke_thickness = 6.0     # Thickness of the spoke (Z-height)
spoke_offset_z = 5.0      # Offset of spokes from the bottom of the hub (approximate visual placement)

# Handle boss dimensions (the small cylinder on one spoke)
handle_boss_diameter = 8.0
handle_boss_hole_diameter = 4.0
handle_boss_height = 8.0
handle_boss_offset = 38.0 # Distance from center to handle boss center

# --- Geometry Construction ---

# 1. Create the Rim
# We sweep a circle along a circular path
rim = (
    cq.Workplane("XZ")
    .moveTo(wheel_radius, 0)
    .circle(rim_thickness / 2)
    .revolve(360, (0, 0, 0), (0, 1, 0))
)

# 2. Create the Central Hub
hub = (
    cq.Workplane("XY")
    .circle(hub_outer_diameter / 2)
    .extrude(hub_height)
    # Add the through hole
    .faces(">Z")
    .hole(hub_inner_diameter)
)

# 3. Create the Spokes
# We create one spoke and then rotate it pattern-wise
single_spoke = (
    cq.Workplane("XY")
    .workplane(offset=spoke_offset_z + spoke_thickness / 2) # Center the spoke vertically relative to Z position
    .rect(wheel_radius * 2, spoke_width) # Create a long rectangle spanning the diameter
    .extrude(spoke_thickness / 2, both=True) # Extrude symmetrically
    # Cut the spoke to fit between hub and rim properly (optional but cleaner)
    # Here we just rely on boolean union, but limiting length prevents sticking out
    .intersect(
        cq.Workplane("XY")
        .circle(wheel_radius)
        .extrude(100)
    )
    # Cut out the center so it doesn't overlap weirdly inside the hub hole (though union fixes this)
    .cut(
        cq.Workplane("XY")
        .circle(hub_outer_diameter / 2)
        .extrude(100)
    )
)

# The strategy above made a full bar across. Let's make a single radial spoke instead for easier rotation.
single_radial_spoke = (
    cq.Workplane("XY")
    .workplane(offset=spoke_offset_z)
    .moveTo(hub_outer_diameter/2 - 1, 0) # Start slightly inside hub for overlap
    .lineTo(wheel_radius, 0) # Go to rim center
    .lineTo(wheel_radius, spoke_width/2)
    .lineTo(hub_outer_diameter/2 - 1, spoke_width/2)
    .close()
    .mirrorX() # Mirror to make full width
    .extrude(spoke_thickness)
)

# Create the pattern of spokes
spokes = single_radial_spoke
for i in range(1, num_spokes):
    spokes = spokes.union(single_radial_spoke.rotate((0,0,0), (0,0,1), i * (360/num_spokes)))

# 4. Create the Handle Boss (small cylinder on one spoke)
# We place this on the X-axis spoke
handle_boss = (
    cq.Workplane("XY")
    .workplane(offset=spoke_offset_z + spoke_thickness) # Start on top of the spoke
    .moveTo(handle_boss_offset, 0)
    .circle(handle_boss_diameter / 2)
    .extrude(handle_boss_height)
    .faces(">Z")
    .hole(handle_boss_hole_diameter)
)

# --- Combine All Parts ---

# Note: Adjusting vertical position of Rim to align with spokes if desired. 
# In the image, the rim's center plane seems aligned with the spokes.
# The rim was revolved around (0,0,0). The spokes are at Z = spoke_offset_z.
# Let's move the rim up.
rim = rim.translate((0, 0, spoke_offset_z + spoke_thickness/2))

result = hub.union(rim).union(spokes).union(handle_boss)

# Optional: Add fillets to smooth transitions (as seen in image)
try:
    result = result.edges("|Z").fillet(1.0)
except:
    pass # Skip fillets if geometry is too complex for simple selection
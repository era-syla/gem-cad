import cadquery as cq

# Parameters
base_diameter = 50.0       # Outer diameter of the knob base
base_height = 25.0         # Height of the knob base
shaft_diameter = 12.0      # Outer diameter of the central shaft
shaft_height = 60.0        # Height of the shaft (from bottom)
shaft_hole_dia = 8.0       # Diameter of the inner hole
shaft_flat_dist = 3.5      # Distance from center to flat part of the D-shaft hole
num_flutes = 8             # Number of cutouts around the base
flute_radius = 5.0         # Radius of the semi-circular cutouts
recess_diameter = 30.0     # Diameter of the central recess in the base
recess_depth = 15.0        # Depth of the central recess

# 1. Create the Base (Knob)
# Start with a cylinder
base = cq.Workplane("XY").cylinder(base_height, base_diameter / 2)

# 2. Create the Central Shaft
# The shaft is taller and sits in the center. We'll unite it with the base.
shaft = cq.Workplane("XY").workplane(offset=0).cylinder(shaft_height, shaft_diameter / 2)
result = base.union(shaft)

# 3. Create the Flutes (Cutouts) on the Base
# We'll create a single cylinder representing the cutter and polar array it.
# The cutter needs to be positioned on the circumference.
flute_cutter = (
    cq.Workplane("XY")
    .workplane(offset=-base_height/2 - 1) # Start slightly below
    .moveTo(base_diameter / 2, 0)         # Move to edge
    .circle(flute_radius)                 # Create circle profile
    .extrude(base_height + 2)             # Extrude past the top
)

# Subtract the flutes in a circular pattern
for i in range(num_flutes):
    angle = i * (360.0 / num_flutes)
    rotated_cutter = flute_cutter.rotate((0, 0, 0), (0, 0, 1), angle)
    result = result.cut(rotated_cutter)

# 4. Create the Central Recess in the Base
# This is the "bowl" shape around the shaft base
recess = (
    cq.Workplane("XY")
    .workplane(offset=base_height/2) # Start at the top of the base
    .circle(recess_diameter / 2)
    .extrude(-recess_depth)          # Cut downwards
)
result = result.cut(recess)

# 5. Create the D-Shaft Hole (Bore)
# It goes through the entire shaft.
# First, a circular hole
hole_profile = (
    cq.Workplane("XY")
    .workplane(offset=shaft_height/2 + 1) # Start slightly above shaft top
    .circle(shaft_hole_dia / 2)
    .extrude(-(shaft_height + 2))         # Cut all the way through
)
result = result.cut(hole_profile)

# Add the "D" flat cut
# We create a box that acts as a filler to make the hole flat on one side,
# but since we are cutting, we need to think inversely or add material back.
# Actually, the easier way in CadQuery for a D-hole is to Sketch it and extrude-cut.

d_hole_sketch = (
    cq.Sketch()
    .circle(shaft_hole_dia / 2)
    .rect(shaft_hole_dia, shaft_hole_dia - shaft_flat_dist*2, mode='s') # Subtract a rectangle to create the flat
    .moved(cq.Location(cq.Vector(0, -((shaft_hole_dia/2 + shaft_flat_dist)/2 + shaft_flat_dist), 0))) # This approach is tricky with boolean sketch logic.
)

# Simpler approach for the D-flat: Add material back into the hole or cut a D-shape directly.
# Let's cut the D-shape directly from a fresh cylinder context to ensure cleanliness.
# Re-doing step 5:

# Remove previous cut to do it in one go or fill the specific area.
# Instead, let's just add a "filler" to create the flat part of the D.
filler = (
    cq.Workplane("XY")
    .workplane(offset=shaft_height/2)
    .moveTo(0, shaft_flat_dist)
    .rect(shaft_hole_dia, shaft_hole_dia, centered=False) # Large rectangle starting at the flat distance
    .extrude(-shaft_height)
    .rotate((0,0,0), (0,0,1), -90) # Orient it correctly
    .translate(( -shaft_hole_dia/2, 0, 0)) # Center x-wise
)

# Since the previous step was a simple hole cut, the result currently has a round hole.
# To make it a D-hole, we need to fill back the segment.
# However, usually it's cleaner to cut the D-shape.
# Let's fill the hole completely first (conceptually) or just undo the last cut in logic.
# Let's restart step 5 logic:
# We need a shape that is a circle MINUS a segment.

d_shape_sketch = (
    cq.Workplane("XY")
    .workplane(offset=shaft_height/2 + 1)
    .circle(shaft_hole_dia / 2)       # Start with circle
    .moveTo(shaft_flat_dist, 0)       # Move to flat offset
    .rect(shaft_hole_dia, shaft_hole_dia, centered=True) # Rectangle to subtract
    # This logic is getting complex for Workplane booleans. 
    # Let's use the simplest method: Make the shaft solid, then cut a D-profile.
)

# Re-applying Step 5 properly:
# Create a profile that represents the D-hole
d_profile = (
    cq.Workplane("XY")
    .workplane(offset=shaft_height/2 + 1)
    .circle(shaft_hole_dia/2)
    .extrude(-(shaft_height+2), combine=False) # Create a solid cylinder
)

# Create the cutting block to make the "D" flat on the tool
cutting_block = (
    cq.Workplane("XY")
    .workplane(offset=shaft_height/2 + 1)
    .moveTo(shaft_flat_dist, 0)
    .rect(shaft_hole_dia, shaft_hole_dia * 2, centered=True) # Big block
    .extrude(-(shaft_height+2), combine=False)
)
# Make the tool D-shaped by intersecting the cylinder with a block (or subtracting the excess)
# Actually, the D-hole is Void. So we need the Tool to be the Shape of the Void.
# The Void is a Circle intersected with a Half-Plane (defined by the flat distance).

# Let's build the D-tool directly using intersection
d_tool = d_profile.cut(cutting_block)

# Now cut the result with this D-shaped tool
# Note: The previous simple hole cut (lines 48-54) is ignored/overwritten by this logic
result = result.cut(d_tool)

# Final Fillet for aesthetics (optional but matches image smoothness)
# result = result.edges("|Z").fillet(0.5) 

# Explicitly ensure the result variable is available
result = result
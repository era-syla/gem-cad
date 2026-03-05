import cadquery as cq

# --- Parameters ---
# Vertical Barbed Stem
stem_height = 40.0
stem_outer_diameter = 12.0
stem_inner_diameter = 7.0

# Barbs
barb_count = 8
barb_spacing = 3.0
barb_height = 2.0  # Length of the conical section
barb_overhang = 0.8  # How much wider the barb is than the stem
barb_start_offset = 5.0  # Distance from top before barbs start

# Flange (Stop ring)
flange_diameter = 16.0
flange_thickness = 2.0
flange_offset_from_bottom = 10.0 # Height of the smooth part above the saddle

# Saddle (Base)
saddle_length = 30.0
saddle_outer_radius = 10.0
saddle_inner_radius = 8.0 # Wall thickness = outer - inner
saddle_rotation = 90.0 # Orient the saddle perpendicular to the view

# --- Construction ---

# 1. Create the Saddle Base
# We'll create a tube and then cut it in half to make a saddle
saddle = (
    cq.Workplane("XY")
    .circle(saddle_outer_radius)
    .circle(saddle_inner_radius)
    .extrude(saddle_length)
    .translate((0, 0, -saddle_length / 2)) # Center it along Z
    .rotate((0, 1, 0), (0, 0, 0), 90) # Rotate to lie horizontally
    .rotate((0, 0, 1), (0, 0, 0), saddle_rotation)
)

# Cut the bottom half off to make it a saddle (clip) shape
cutting_box = (
    cq.Workplane("XY")
    .box(saddle_length * 2, saddle_outer_radius * 2, saddle_outer_radius * 2)
    .translate((0, 0, -saddle_outer_radius))
)
saddle = saddle.cut(cutting_box)

# 2. Create the Vertical Stem (Main cylinder)
# Calculate where the stem sits relative to the saddle surface
stem_base_z = saddle_outer_radius 
stem_total_height = stem_height + saddle_outer_radius

stem = (
    cq.Workplane("XY")
    .workplane(offset=0) # Start from origin
    .circle(stem_outer_diameter / 2)
    .extrude(stem_total_height)
)

# 3. Create the Flange
flange_z_pos = saddle_outer_radius + flange_offset_from_bottom
flange = (
    cq.Workplane("XY")
    .workplane(offset=flange_z_pos)
    .circle(flange_diameter / 2)
    .extrude(flange_thickness)
)

# 4. Create the Barbs
# We will create one barb profile and revolve it or stack cones
barbs = cq.Workplane("XY")

# The top of the stem is at z = stem_total_height
# We want barbs starting from the top down
current_z = stem_total_height - barb_start_offset

for i in range(barb_count):
    # A barb is essentially a cone frustum getting wider as it goes down (or up, depending on perspective)
    # Looking at image: sharp edge is at the top, ramps out downwards? 
    # Actually, standard hose barbs ramp out upwards (wider at top) to grip the hose when pulling off.
    # Looking closely at the image: The ridges are horizontal. 
    # Usually, it's a cone: Base (wider) at top, Tip (narrower) at bottom. Or vice versa.
    # Let's assume standard barb: Cone where bottom radius > top radius is incorrect for insertion.
    # Standard: Cone where Bottom Radius = Stem Radius, Top Radius = Stem Radius + Overhang.
    
    # Let's model it as a union of tapered rings.
    
    # Top of this specific barb segment
    top_z = current_z 
    bottom_z = current_z - barb_height
    
    b = (
        cq.Workplane("XY")
        .workplane(offset=bottom_z)
        .circle(stem_outer_diameter / 2) # Bottom of barb connects to stem
        .workplane(offset=barb_height)
        .circle(stem_outer_diameter / 2 + barb_overhang) # Top of barb flares out
        .loft(combine=False)
    )
    
    # We also need the "step" back down to the stem diameter instantly at the top
    # The loft creates the slope. The next iteration handles the gap or we leave it as valid geo.
    # The image shows discrete ridges.
    
    if i == 0:
        barbs = b
    else:
        barbs = barbs.union(b)
        
    current_z -= barb_spacing

# 5. Combine External Shapes
# We union the saddle, stem, flange, and barbs
# Note: The stem penetrates the saddle, which is good for the boolean.
main_body = saddle.union(stem).union(flange).union(barbs)

# 6. Create the Through-Hole
# A bore going all the way through the stem into the saddle area
hole = (
    cq.Workplane("XY")
    .circle(stem_inner_diameter / 2)
    .extrude(stem_total_height * 1.5) # Make it long enough to cut everything
    .translate((0, 0, -10)) # Shift down to ensure clean cut through bottom
)

# 7. Final Operation
result = main_body.cut(hole)

# Fillet the junction between stem and saddle for strength and aesthetics
# Select edges where Z is near the intersection
try:
    result = result.edges(
        cq.selectors.BoxSelector(
            (-saddle_length/2, -saddle_outer_radius, saddle_outer_radius),
            (saddle_length/2, saddle_outer_radius, saddle_outer_radius + 2)
        )
    ).fillet(1.0)
except:
    # Fallback if selection is tricky, though parametric box usually works
    pass
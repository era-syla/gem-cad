import cadquery as cq

# --- Parametric Dimensions ---

# Base Plate Dimensions
base_length = 100.0
base_width = 60.0
base_height = 8.0
base_fillet = 4.0

# Base Mounting Holes
base_hole_spacing_x = 80.0
base_hole_spacing_y = 40.0
base_hole_diameter = 5.0
base_hole_counterbore_dia = 8.0
base_hole_counterbore_depth = 3.0

# Upright Block Dimensions
block_length = 80.0
block_width = 20.0
block_height = 40.0
block_fillet = 6.0

# Central Feature (Arc Cutout)
arc_radius_outer = 18.0  # The main cutout radius
arc_radius_inner = 14.0  # The groove/step inside
groove_depth = 2.0       # How deep the step is

# Top Holes on Upright
top_hole_spacing = 50.0
top_hole_dia = 6.0

# Side Rectangular Slots
slot_width = 10.0
slot_height = 5.0
slot_spacing = 50.0 # Distance between centers
slot_z_pos = 25.0   # Height from base bottom

# Lower Circular Holes on Upright
side_hole_dia = 5.0
side_hole_spacing = 20.0
side_hole_z_pos = 15.0 # Height from base bottom

# --- Construction ---

# 1. Create the Base Plate
# Start with a simple rectangle centered on XY
base = (
    cq.Workplane("XY")
    .box(base_length, base_width, base_height)
    .edges("|Z")
    .fillet(base_fillet)
)

# 2. Add Counterbored Holes to Base
# Position holes relative to center
base = (
    base.faces(">Z")
    .workplane()
    .rect(base_hole_spacing_x, base_hole_spacing_y, forConstruction=True)
    .vertices()
    .cboreHole(base_hole_diameter, base_hole_counterbore_dia, base_hole_counterbore_depth)
)

# 3. Create the Upright Block
# We will create this as a separate solid first or union it.
# Let's extrude from the top of the base.
# It sits at the back edge of the base? No, it looks centered in Y direction or slightly offset.
# Looking at the image, it seems centered along the X-axis, and roughly centered or slightly back on Y.
# Let's assume centered on X and centered on Y for simplicity, sitting on top of the base.

upright = (
    cq.Workplane("XY")
    .workplane(offset=base_height/2) # Start from top of base (base is centered on Z=0, so top is h/2)
    .box(block_length, block_width, block_height, centered=(True, True, False))
)

# Apply fillets to the vertical edges of the upright block
upright = upright.edges("|Z").fillet(block_fillet)

# 4. Create the Central Arc Cutout
# This cuts from the top face downwards.
# It seems to have a stepped profile (a wider arc and a narrower arc).

# Cut the main large arc
upright = (
    upright.faces(">Z")
    .workplane()
    .center(0, 0)
    # Draw a shape to cut: a rectangle going down + a circle
    # But a cut slot is easier with a simple cut.
    # Let's cut a cylinder horizontally? No, it's a vertical cradle.
    # Let's use a circle sketch and cut down.
    .circle(arc_radius_outer)
    .cutBlind(-arc_radius_outer) # Cut deep enough
)

# The image shows a "lip" or groove. It looks like the main cut is radius_outer, 
# and there is a smaller radius cut deeper, or perhaps the outer radius is a shallow shoulder.
# Let's look closer. It looks like a through-cut of radius_inner, and a counter-bore of radius_outer.
# Actually, looking at the shadow, it's a saddle.
# Let's cut the main saddle shape across the Y axis.

# Re-approach for the saddle:
# Cut a cylinder transverse to the block (along Y axis).
saddle_cut_z = base_height/2 + block_height # Top of block
saddle_radius = 18.0

# We need to cut a "U" shape.
# Let's cut a cylinder through the block along Y axis, shifted up.
upright = (
    upright.faces(">Y").workplane(centerOption="CenterOfBoundBox")
    .moveTo(0, block_height) # Move to top center relative to face
    .circle(arc_radius_outer)
    .cutThruAll()
)

# Now add the inner groove/step. This looks like a slightly larger radius cut 
# on the faces, or a smaller radius passing through?
# Looking at the lip, there is a central rib that is lower.
# It looks like the main cut goes through, and then the outer edges are higher?
# Or rather, there is a central groove cut into the saddle.
# Let's assume a main cut of radius 14, and a wider cut of radius 18 that doesn't go all the way?
# Actually, looking at the ridge, it looks like a simple stepped cut.
# Let's cut the larger radius slightly less deep from the top? No, that's not right for a saddle.
# Let's assume a groove cut into the saddle surface.
# We will cut a larger cylinder (radius_outer) all the way through, 
# then create a "ring" or simply not cut the inner part?
# Let's try this: The block has a cutout. There is a step.
# It looks like a bore for a bearing.
# Let's cut the smaller radius all the way through (Y-axis).
# Then cut the larger radius from the front and back faces inward to a depth.

# Reset upright to just the filleted block to do this cleanly
upright_base = (
    cq.Workplane("XY")
    .workplane(offset=base_height/2)
    .box(block_length, block_width, block_height, centered=(True, True, False))
    .edges("|Z").fillet(block_fillet)
)

# Cut the main through-hole (smaller radius)
upright_with_hole = (
    upright_base.faces(">Y").workplane()
    .transformed(offset=(0, block_height, 0)) # Shift origin to top edge
    .circle(arc_radius_inner)
    .cutThruAll()
)

# Cut the counterbores (larger radius) for the saddle steps
# Front side
upright_with_hole = (
    upright_with_hole.faces(">Y").workplane()
    .transformed(offset=(0, block_height, 0))
    .circle(arc_radius_outer)
    .cutBlind(-groove_depth)
)
# Back side
upright_with_hole = (
    upright_with_hole.faces("<Y").workplane()
    .transformed(offset=(0, block_height, 0))
    .circle(arc_radius_outer)
    .cutBlind(-groove_depth)
)


# 5. Top Vertical Holes
# These are on the top flat faces remaining after the saddle cut.
upright_with_hole = (
    upright_with_hole.faces(">Z").workplane()
    .pushPoints([(-top_hole_spacing/2, 0), (top_hole_spacing/2, 0)])
    .hole(top_hole_dia)
)

# 6. Side Rectangular Slots
# On the front face (>Y in global if we assume Y is width) or a side face.
# The image shows them on the long face. Let's assume the long face is Y-normal or X-normal?
# In step 3 we made length along X. So long face is >Y or <Y.
# We'll put them on the "front" face (>Y? No, standard view usually puts -Y as front).
# Let's put them on the face that is visible.
upright_with_features = (
    upright_with_hole.faces("<Y").workplane(centerOption="CenterOfBoundBox")
    # Coordinate system is now on the face. X is usually along the block length.
    # Y on the workplane is usually Z global.
    .pushPoints([(-slot_spacing/2, slot_z_pos - (base_height/2 + block_height/2)), 
                 (slot_spacing/2, slot_z_pos - (base_height/2 + block_height/2))])
    .rect(slot_width, slot_height)
    .cutBlind(-5.0) # Depth of slot
)

# 7. Lower Circular Holes on Upright
# Also on the front face, below the slots/center.
upright_with_features = (
    upright_with_features.faces("<Y").workplane(centerOption="CenterOfBoundBox")
    .pushPoints([(-side_hole_spacing/2, side_hole_z_pos - (base_height/2 + block_height/2)), 
                 (side_hole_spacing/2, side_hole_z_pos - (base_height/2 + block_height/2))])
    .hole(side_hole_dia, depth=10.0)
)

# 8. Combine Base and Upright
result = base.union(upright_with_features)

# Apply a small fillet at the junction of base and upright for realism
result = result.faces(cq.NearestToPointSelector((0, 0, base_height/2))).edges().fillet(1.0)
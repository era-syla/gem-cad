import cadquery as cq

# --- Parameter Definitions ---
# Main enclosure dimensions
box_width = 80.0
box_height = 100.0
box_depth = 50.0

# Flange dimensions
flange_thickness = 5.0
flange_width = 15.0  # How much it protrudes from the side
flange_height = 60.0 # Length of the flange strip

# Mounting hole parameters
hole_dia = 4.0
hole_spacing = 40.0 # Distance between hole centers
c_sink_dia = 7.0    # Countersink diameter
c_sink_angle = 90.0 # Countersink angle

# --- Model Construction ---

# 1. Create the main enclosure box
# Using centered=False makes it easier to position relative to origin (0,0,0) usually,
# but centered=True is often cleaner for symmetry. Let's align the back face to the XY plane.
main_box = (
    cq.Workplane("XY")
    .box(box_width, box_height, box_depth)
)

# 2. Create the side flange
# We need to position it on the side of the box. 
# Let's attach it to the right face (+X).
flange = (
    cq.Workplane("YZ")
    .workplane(offset=box_width/2) # Move to the right face
    .center(0, -box_height/2 + flange_height/2 + 10) # Position vertically (arbitrary offset from bottom)
    # Actually, looking at the image, the flange is centered vertically on the side or offset slightly.
    # Let's align it relative to the side face.
)

# Alternative approach: Union two simple shapes.
# Let's stick with the main_box and add the flange geometry.

# Create the flange solid separately then union
flange_geo = (
    cq.Workplane("YZ")
    .workplane(offset=box_width/2)  # Plane on the right face of the box
    .center(box_depth/2, 0)         # Center relative to the side face (YZ plane local coordinates)
    # The flange looks like it's flush with the BACK of the box? 
    # In the image, the flange is attached to the side face (YZ), protruding outwards (+X? No, attached to side).
    # Wait, looking closely: It's a flat plate attached to the right side face.
    # Let's refine dimensions based on visual proportions.
    
    .box(box_depth, flange_height, flange_thickness, centered=(True, True, False)) 
    # Dimensions: Depth (along Y of global), Height (along Z of global), Thickness (along X of global)
    # But working on YZ plane: x_local=box_depth, y_local=flange_height, z_local (extrusion)=thickness
)

# Let's rebuild more intuitively.
# Main Box
result = cq.Workplane("XY").box(box_width, box_depth, box_height) 
# Note: Interpreting dimensions: Width(X), Depth(Y), Height(Z)

# Flange attached to the +X face
# The flange is a rectangular plate.
# Width = flange_thickness
# Depth (along Y) seems to be protruding or flush?
# In the image, the flange is attached to the Face. It looks like an extension.
# Let's assume it's a mounting tab screwed onto or welded to the side.

flange_solid = (
    cq.Workplane("YZ")
    .workplane(offset=box_width/2) # Move to right face
    .center(0, -box_height/4)      # Shift down a bit based on image
    .box(box_depth, flange_height, flange_thickness, centered=(True, True, False))
)

# Actually, the image shows the flange is THINNER than the box depth? No, it looks like a strip.
# Let's look at the image again.
# The flange is a strip attached to the right side face. 
# It runs vertically.
# It seems to be flush with the BACK edge (hidden) or just centered. Let's center it on the depth.

result = cq.Workplane("XY").box(box_width, box_depth, box_height)

# Create the flange on the right side (+X)
flange = (
    result.faces(">X").workplane()
    .center(0, -box_height/4) # Shift down on the face
    .box(flange_thickness, flange_height, 5.0, centered=(False, True, True)) # Extruding OUT
    # Wait, box() on a workplane creates a solid.
    # Let's try drawing the rectangle and extruding.
)

# Re-evaluating the shape:
# It is a large block. On the right side, there is a thinner plate attached.
# The plate has holes.
# Let's create the block.
block = cq.Workplane("XY").box(80, 50, 80)

# Create the flange
# It is attached to the +X face.
# It has a thickness (extruding in X), a width (along Y), and a height (along Z).
# In the image, the flange thickness is small (maybe 5mm).
# The flange is attached to the SIDE, protruding OUTWARDS? 
# No, usually flanges are flush with the back to mount to a wall.
# Let's assume the large face we see is the FRONT. The flange is on the RIGHT.
# The flange allows mounting to a backplane. So the back of the flange is flush with the back of the box.

# Revised Parameters
w = 60.0  # Box Width
h = 80.0  # Box Height
d = 40.0  # Box Depth
f_th = 4.0 # Flange Thickness
f_w = 12.0 # Flange Width (sticking out from side? Or is it a strip ON the side?)
# Image interpretation: The flange is a strip attached to the side face.
# It does NOT stick out past the back. It seems centered or aligned.
# Let's assume it's a strip of material welded to the side.

f_h = 50.0 # Flange vertical length

result = (
    cq.Workplane("XY")
    .box(w, d, h) # Main body
    .faces(">X")  # Select right face
    .workplane()
    .center(0, -10) # Shift down slightly relative to center of side face
    .rect(d, f_h)   # Rectangle covering the depth of the side, but shorter height?
                    # No, looking at image, the flange is narrower than the depth of the box.
    .rect(10, f_h)  # A strip 10mm wide, 50mm high
    .extrude(f_th)  # Extrude outwards
)

# Let's look closer at the image.
# The flange is attached to the Right Face.
# It is a rectangular prism.
# It contains two countersunk holes.
# The holes go through the thickness of the flange (X axis).

# Final strategy:
# 1. Base Box.
# 2. Flange geometry added to the side.
# 3. Cut holes in flange.

res_box = cq.Workplane("XY").box(60, 40, 70) # Width, Depth, Height

# Flange
# Position: Right side (+X), centered in Y (Depth), offset downwards in Z.
flange_thickness = 4.0
flange_height = 50.0
flange_width = 10.0 # Dimension along Y

# To reproduce the specific visual:
# The flange seems to be a thin strip running vertically.
# It looks flush with the back, maybe?
# Let's assume centered in Y for simplicity, it looks reasonably centered.

res_flange = (
    cq.Workplane("XY")
    .workplane(offset=30) # Move to X=30 (Right face of box)
    .center(0, -5)        # Center Y, shift Z down by 5
    .box(flange_thickness, flange_width, flange_height, centered=(False, True, True))
    # box arguments: length (x), width (y), height (z)
    # centered: x=False (extrude away from plane), others True
)

# Combine
result = res_box.union(res_flange)

# Add Holes
# Holes go through the flange in the X direction (perpendicular to the broad face of the flange shown?)
# No, usually holes go through the THINNEST part to screw into a wall.
# In the image, we see the heads of the screws would go into the holes on the face visible to us (the side face).
# The holes go INTO the box? No, that makes no sense for a flange.
# The flange is likely sticking OUT from the back, but here it's on the side.
# If it's on the side, the holes go through the Y axis (thickness of the strip)?
# OR the X axis (into the box)?
# Let's look at the chamfers/countersinks. They are on the outer face of the flange.
# So the vector is -X (into the box) or +/- Y?
# The flange is on the +X face. The large flat surface of the flange is in the YZ plane.
# Wait, looking at the image: The flange is a separate plate attached to the side face.
# The holes are on the face parallel to the side of the box.
# So the holes go along the X axis? That would drill into the box.
# Unless the flange overhangs the back? The image doesn't show an overhang.
# 
# Correction: The image shows a block. On the right side, there is a strip.
# The holes are in that strip.
# Visually, the holes are countersunk.
# It implies the fastener goes *through* the strip.
# If the strip is welded to the box, the fastener would hit the box wall immediately.
# This implies either:
# A) It's a blind hole for aesthetics in this render.
# B) The flange sticks out past the back of the box (we can't see the back).
# C) The holes are threaded holes for something to mount TO the box.
#
# Let's code it exactly as it looks geometrically.
# Holes on the +X face of the flange.

result = (
    result
    .faces(">X")          # Select the outermost face (the face of the flange)
    .workplane()
    .center(0, -5)        # Re-center to match where we put the flange (center of flange is -5Z)
    .pushPoints([(0, 15), (0, -15)]) # Two holes, vertically spaced relative to flange center
    .cskHole(3.0, 6.0, 90.0, depth=None) # Countersunk hole
)

# Re-adjusting the flange position logic for robustness
# Let's define the flange explicitly on the face.

result = (
    cq.Workplane("XY")
    .box(60, 40, 70)      # Main Body
    .faces(">X")          # Select Right Face
    .workplane()
    .center(0, -10)       # Shift coordinate system down by 10mm relative to box center
    .rect(12, 55)         # Draw the footprint of the flange (Width 12mm, Height 55mm)
    .extrude(5)           # Extrude 5mm outwards to create the flange volume
    .faces(">X")          # Select the new outer face of the flange
    .workplane()
    .pushPoints([(0, 18), (0, -18)]) # Place points relative to center of the flange face
    .cskHole(diameter=3.5, cskDiameter=7.0, cskAngle=90.0, depth=5.0) # Cut holes
)
# The image shows the flange width (along Y) is smaller than box depth.
# The flange height (along Z) is smaller than box height.
# The holes are vertically aligned.

# Refined parameters for visual match
box_w, box_d, box_h = 60, 40, 70
flange_w, flange_h, flange_th = 8, 50, 4
hole_dist = 30

result = (
    cq.Workplane("XY")
    .box(box_w, box_d, box_h)
    .faces(">X").workplane()  # Work on the right face
    .center(0, -10)           # Shift down Z
    .rect(flange_w, flange_h) # Rectangle for flange (Width along Y, Height along Z on this plane)
    .extrude(flange_th)       # Extrude along X
    .faces(">X").workplane()  # Work on face of flange
    .pushPoints([(0, hole_dist/2), (0, -hole_dist/2)])
    .cskHole(3, 6, 90)
)
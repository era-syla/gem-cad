import cadquery as cq

# Parametric dimensions
shaft_diameter = 6.0
shaft_length = 20.0
head_diameter = 10.0
head_thickness = 1.5
bottom_nub_diameter = 7.0
bottom_nub_height = 0.5
chamfer_size = 0.5
fillet_radius = 0.2

# Create the main shaft
shaft = cq.Workplane("XY").circle(shaft_diameter / 2).extrude(shaft_length)

# Create the top chamfer
shaft = shaft.faces(">Z").chamfer(chamfer_size)

# Create the head (flange) at the bottom
# We move the workplane to the bottom of the shaft
head = (
    cq.Workplane("XY")
    .workplane(offset=0) # Start at Z=0 (bottom of shaft if shaft goes up)
    .circle(head_diameter / 2)
    .extrude(-head_thickness) # Extrude downwards
)

# Create the small bottom nub/feature below the head
bottom_nub = (
    head.faces("<Z")
    .workplane()
    .circle(bottom_nub_diameter / 2)
    .extrude(-bottom_nub_height)
)

# Combine all parts
# Note: Since 'head' was built off XY and extruded down, and 'shaft' was built off XY and extruded up,
# they implicitly touch at Z=0. However, depending on the kernel operations, a explicit union is safest.
# In the sequence above:
# 1. 'shaft' is a standalone object.
# 2. 'head' is a standalone object (created from new workplane).
# 3. 'bottom_nub' is part of the 'head' object's history.

# Let's reconstruct cleanly to ensure a single solid 'result'.

# Method: Revolution profile for cleaner single-body construction
# Profile is on XZ plane
# Profile shape:
# 1. Shaft vertical line
# 2. Top chamfer
# 3. Top horizontal
# 4. Centerline
# 5. Bottom nub
# 6. Head thickness
# 7. Head radius

# Let's stick to the stacking method as it is more readable for this simple shape, 
# ensuring we union them properly.

# Re-doing construction for a guaranteed single solid result:
result = (
    cq.Workplane("XY")
    # 1. The Head (Flange)
    .circle(head_diameter / 2)
    .extrude(head_thickness)
    # 2. The Shaft on top of the head
    .faces(">Z").workplane()
    .circle(shaft_diameter / 2)
    .extrude(shaft_length)
    # 3. Chamfer the top of the shaft
    .faces(">Z").chamfer(chamfer_size)
    # 4. The bottom nub below the head
    .faces("<Z").workplane() # Go to absolute bottom
    .circle(bottom_nub_diameter / 2)
    .extrude(bottom_nub_height)
    # 5. Add a small chamfer/fillet to the very bottom for the "button" look
    .faces(">Z").chamfer(bottom_nub_height * 0.8) # Chamfer the nub we just made (which is now >Z relative to the workplane extrusion direction, or simply pick the face by position)
)

# Refinement on step 4/5: The extrusion direction and face selection can be tricky. 
# Let's use a standard "Stacking upwards" approach for absolute clarity.

# 1. Bottom Nub
p1 = cq.Workplane("XY").circle(bottom_nub_diameter/2).extrude(bottom_nub_height)
# Chamfer the bottom edge of the nub (which is at Z=0)
p1 = p1.faces("<Z").chamfer(bottom_nub_height * 0.5)

# 2. Head
p2 = p1.faces(">Z").workplane().circle(head_diameter/2).extrude(head_thickness)

# 3. Shaft
p3 = p2.faces(">Z").workplane().circle(shaft_diameter/2).extrude(shaft_length)

# 4. Top Chamfer
result = p3.faces(">Z").chamfer(chamfer_size)

# Optional: Fillet under the head for realism
# result = result.faces(cq.NearestToPointSelector((0, shaft_diameter/2 + 0.1, bottom_nub_height + head_thickness))).fillet(fillet_radius)
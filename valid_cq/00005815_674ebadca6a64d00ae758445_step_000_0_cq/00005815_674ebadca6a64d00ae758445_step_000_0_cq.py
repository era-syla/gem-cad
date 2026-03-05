import cadquery as cq

# --- Parametric Dimensions ---
# Main body (curved block) dimensions
body_width = 80.0
body_height = 80.0
body_thickness = 15.0
body_curvature_radius = 120.0  # Controls the bulge of the main body

# Front rectangular plate dimensions
plate_width = 60.0
plate_height = 70.0
plate_thickness = 2.0

# Mounting holes
hole_distance = 40.0  # Vertical distance between hole centers
hole_diameter = 4.0
hole_depth = 10.0     # Depth into the body

# --- Geometry Construction ---

# 1. Create the main curved body
# We start with a block and will intersect it with a cylinder or loft to get the curve.
# A simpler approach for the specific "pillow" shape is intersecting a box with a large cylinder 
# or creating a sketch with an arc. Let's use an extruded sketch with an arc for the profile.

# Create the profile sketch (top-down view of the curve)
# We draw an arc on the top and bottom, straight lines on sides
def create_curved_profile(w, h, r):
    # Calculate the sagitta (height of the arc) or just use 3-point arc
    # Let's try a simple intersection method which is often more robust for this "bulged" look.
    # We will make a base block and intersect it with a large cylinder.
    
    # Actually, looking at the image, it's a "squircle" or rounded rectangle that is puffed out.
    # Let's try creating a base block that is rounded, then intersect with a large cylinder/sphere for the face curvature.
    # Or simply: Extrude a rectangle, then cut the sides with a large radius?
    
    # Let's go with: Extrude a base shape, then apply the front curvature.
    # The base shape looks like a rectangle with rounded corners (filleted).
    base = cq.Workplane("XY").box(w, h, body_thickness)
    
    # Apply heavy fillets to the corners to match the image's rounded silhouette
    base = base.edges("|Z").fillet(15.0)
    
    # Now create the "bulge" or curvature on the front face. 
    # The image shows a curve along the vertical axis (top to bottom) primarily, 
    # but the sides look flat. 
    # Actually, looking closely, the top and bottom surfaces are curved. 
    # Let's re-evaluate. It looks like a loft or an intersection.
    
    # Strategy B: Intersection of a box and a large cylinder.
    # The cylinder axis would be horizontal (Y-axis) to curve the top/bottom? 
    # No, the curve is on the large face.
    # Let's try constructing the profile from the side (YZ plane) and extruding? No.
    
    # Strategy C (Refined): 
    # 1. Create the back base shape (a rounded rectangle).
    # 2. Create a cutting object to curve the front face.
    # 3. Add the rectangular plate.
    
    return base

# Step 1: Base Block
main_body = cq.Workplane("XY").box(body_width, body_height, body_thickness)
main_body = main_body.edges("|Z").fillet(15.0) # Round corners

# Step 2: Apply curvature to the front face
# We will cut away material using a large sphere or cylinder to create the convex shape.
# Alternatively, valid parametric way: Intersect with a large cylinder.
# The curve seems to be along the top and bottom edges primarily.
# Let's use a large cylinder to cut the "front" face to give it that convex look.
# Actually, the image shows the face is convex. To make a box convex, we intersect.
# To create the specific "shield" like curvature:
curved_surface_radius = 200.0
# Center the cutting tool way behind the object
center_offset = curved_surface_radius - body_thickness/2.0
# We want the intersection of a block and a cylinder/sphere.
# Let's use a Sphere for a compound curve or Cylinder for a simple curve.
# Image looks like a simple curve along one axis (cylindrical).
# Axis of cylinder is vertical (Y)? No, horizontal (X).
# If axis is X, the curve goes up/down. 
# Looking at the top edge, it's curved. Looking at side edge, it's straight.
# This implies the cutting cylinder is oriented along the Y axis? No.
# Let's assume it's a "crowned" top.

# Let's try a different approach: An intersection of two extrusions.
# Profile 1 (XY): Rounded Square.
# Profile 2 (XZ): The curve.

# Re-doing Main Body Construction
# 1. Base outline: Rounded Rectangle
base_outline = (
    cq.Workplane("XY")
    .rect(body_width, body_height)
    .extrude(body_thickness)
    .edges("|Z").fillet(20.0)
)

# 2. Curvature Cut
# The image shows the face tapering towards the edges.
# We will create a large cylinder to subtract from the "front" to curve it back? 
# No, the center is thickest.
# Let's intersect with a large cylinder whose axis is Y-aligned.
cyl_radius = (body_width**2 + body_thickness**2) / (2*body_thickness) * 1.5 # Flatter curve
# Actually, let's just make a simple intersection with a cylinder.
cutter = (
    cq.Workplane("YZ")
    .workplane(offset=0) # centered
    .circle(100) # Big radius
    .extrude(200) # Wide enough
    .translate((100 - body_thickness/2 - 2, 0, 0)) # Shift so just the edge touches
)
# This is getting complicated to guess.

# Simplest interpretation of the image:
# 1. A base block with rounded corners.
# 2. The top and bottom faces are curved (arched).
# 3. A rectangular plate on front.

final_body_thickness = 12.0
base_block = (
    cq.Workplane("XY")
    .box(body_width, body_height, final_body_thickness)
    .edges("|Z").fillet(18.0)
)

# Create the curve on top/bottom faces.
# We cut with a large cylinder from the side.
# Axis along X.
cut_radius = 160.0
cut_center_z = -cut_radius + final_body_thickness/2.0 + 3.0 # Tuning offset
# We need to cut the "top" (Z+) face? No, looking at the image, 
# the Z-axis is likely coming out of the screen.
# The curve is on the Y-max and Y-min edges.
# So we need a cylinder with axis along X, positioned behind the part (negative Z)
# to intersect? No, the image shows the thickness varies.
# The center is thick, edges are thin.
# This is an intersection with a cylinder aligned with X axis.

convex_maker = (
    cq.Workplane("YZ")
    .center(0, -500 + final_body_thickness/2 + 2) # Offset large circle
    .circle(500)
    .extrude(body_width + 20, both=True) # Extrude along X
)
# Re-orient to cut along Y direction logic
convex_maker = (
    cq.Workplane("XZ")
    .center(0, -180) # Center the circle far down in Z (if looking from top) 
                     # Wait, we are extruding along Y.
    .circle(180 + final_body_thickness/2) # Radius
    .extrude(body_height + 20, both=True)
)
# Rotate to match orientation
convex_maker = convex_maker.rotate((0,0,0), (1,0,0), 90) # Rotate to align axis with X?
# Actually, simpler: Workplane("YZ") is side view. Circle there, extruded X.
convex_maker = (
    cq.Workplane("YZ")
    .center(0, -140) # Move center down (negative Z in local plane, which maps to global Y or Z depending)
    .circle(140 + final_body_thickness/2) # Large radius
    .extrude(body_width + 10, both=True)
)

# Let's construct the main body by intersecting the rounded block with this cylinder
# This creates the curved front/back surface while keeping the rounded outline.
# However, the image shows the back is flat (presumably) and front is curved?
# Let's assume symmetrical or flat back. The image shows it mounted on something potentially.
# Let's assume flat back, curved front.
main_shape = base_block.intersect(convex_maker)

# Since intersect might center things weirdly, let's ensure flat back is on Z=0
# But `intersect` keeps the common volume.
# Let's try a different simpler approach that guarantees the result.
# 1. Sketch profile on XZ plane (arc)
# 2. Extrude along Y
# 3. Intersect with Rounded Rectangle outline on XY.

# 1. The Arc Profile (thickness profile)
arc_radius = 200.0
sagitta = final_body_thickness
chord = body_height # The arc spans the height

# We create a solid that represents the thickness variation
thickness_solid = (
    cq.Workplane("YZ")
    .moveTo(0, body_height/2)
    .lineTo(0, -body_height/2)
    .lineTo(final_body_thickness, -body_height/2)
    # 3-point arc for the curved face
    .threePointArc((final_body_thickness + 3.0, 0), (final_body_thickness, body_height/2))
    .close()
    .extrude(body_width + 10, both=True) # Extrude wide enough to cover width
)
# Rotate so thickness is Z, Height is Y, Width is X
thickness_solid = thickness_solid.rotate((0,0,0), (0,1,0), -90).rotate((0,0,0), (0,0,1), 90)

# 2. The Outline (Round Rect)
outline_solid = (
    cq.Workplane("XY")
    .rect(body_width, body_height)
    .extrude(final_body_thickness * 2) # Plenty thick
    .edges("|Z").fillet(15.0)
)

# 3. Intersect
body = outline_solid.intersect(thickness_solid)

# Ensure it sits on Z=0
# Determine bounding box to center it?
# The construction above puts the flat face at roughly X=0 in the YZ plane logic,
# which rotated becomes Z=0.

# Step 3: The Front Rectangular Plate
# This plate sits on the "top" of the curved surface.
# It appears to be a flat plate floating or attached.
# Given the shadow, it looks like a separate extrude sitting on the apex of the curve.
front_plate = (
    cq.Workplane("XY")
    .workplane(offset=body.val().BoundingBox().zmax) # Start at the highest point of body
    .rect(plate_width, plate_height)
    .extrude(plate_thickness)
)

# Step 4: Combine Body and Plate
result_obj = body.union(front_plate)

# Step 5: Mounting Holes
# Two holes, vertically aligned
result = (
    result_obj.faces(">Z") # Select top face
    .workplane()
    .pushPoints([(0, hole_distance/2), (0, -hole_distance/2)])
    .hole(hole_diameter, hole_depth)
)

# Final result variable
result = result

# Optional: Export for verification (commented out)
# cq.exporters.export(result, "model.step")
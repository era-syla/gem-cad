import cadquery as cq

# Parametric dimensions
base_diameter = 100.0
top_diameter = 80.0
base_height = 10.0
domed_fillet_radius = 10.0
top_plate_thickness = 5.0
handle_width = 10.0
handle_length = 50.0
handle_height = 15.0
handle_thickness = 8.0 # Thickness of the horizontal part of the handle

# 1. Create the main body
# We'll start with the wider base and loft or extrude/fillet to the top
# The shape looks like a frustum or a large fillet. Let's try a revolved profile for the best control of the curved side.

# Define points for the cross-section of the lid
p0 = (0, 0)
p1 = (base_diameter / 2.0, 0)
p2 = (base_diameter / 2.0, 2.0) # Small vertical lip at bottom
p3 = (top_diameter / 2.0, base_height)
p4 = (0, base_height)

# Create the base revolution
base = (
    cq.Workplane("XZ")
    .moveTo(*p0)
    .lineTo(*p1)
    .lineTo(*p2)
    # Create the curved transition. We use a 3-point arc or spline. 
    # A tangent arc or spline is best here. Let's approximate the curve seen in the image.
    .spline([p3], tangents=[(0, 1), (-1, 0)], includeCurrent=True) 
    .lineTo(*p4)
    .close()
    .revolve()
)

# 2. Add the flat top plate (if distinct from the curve, though the revolve handles most of it)
# The image shows a very distinct flat top circle with a sharp edge meeting the curve.
# Let's refine: The previous revolve creates the 'skirt'. Let's add the top cylindrical cap.
# Actually, looking at the image, there is a distinct cylinder on top of a curved base.

# Alternative approach:
# 1. Bottom curved section (revolve)
# 2. Top flat cylinder
# 3. Handle

# Let's adjust dimensions for this logic
bottom_curve_height = 15.0
top_cyl_height = 2.0
total_height = bottom_curve_height + top_cyl_height

# Re-doing the base to match the "curved skirt" look better
# Bottom radius R50, Top Radius R40.
base_skirt = (
    cq.Workplane("XY")
    .circle(base_diameter / 2.0)
    .extrude(bottom_curve_height)
    # Apply a large fillet to the bottom edge to give it that "bell" shape
    # or apply a draft. The image looks like a convex curve (fillet on top) or a concave curve (fillet on bottom)?
    # It looks like a convex curve going from wide to narrow.
    # Let's construct it as a loft for better control.
)

# Loft approach for the skirt
skirt = (
    cq.Workplane("XY")
    .circle(base_diameter / 2.0)
    .workplane(offset=bottom_curve_height)
    .circle(top_diameter / 2.0)
    .loft(combine=True)
)

# Add the top flat cap
cap = (
    cq.Workplane("XY")
    .workplane(offset=bottom_curve_height)
    .circle(top_diameter / 2.0)
    .extrude(top_cyl_height)
)

# Combine skirt and cap
body = skirt.union(cap)

# Apply a fillet to the transition between skirt and cap if needed, 
# but the image shows a sharpish line there. 
# However, the skirt itself is curved. A loft is straight-sided.
# Let's use the fillet method on a simple cylinder to get the "bell" shape.

# Strategy 3 (Most robust for this shape): 
# Create a cylinder and fillet the bottom edge heavily, but invert the logic.
# Cylinder of top_diameter, extrude down, then flare out?
# Let's stick to the Revolve profile, it's the most accurate for the "Bell" shape.

final_base_radius = 50.0
top_flat_radius = 38.0
skirt_height = 15.0
lip_height = 2.0

# Profile points in XZ plane
pts = [
    (0, 0),
    (final_base_radius, 0),
    (final_base_radius, 1), # Small vertical edge at bottom
    # Curve up to the top flat section
    (top_flat_radius, skirt_height), 
    (top_flat_radius, skirt_height + lip_height),
    (0, skirt_height + lip_height)
]

lid_body = (
    cq.Workplane("XZ")
    .moveTo(0,0)
    .lineTo(final_base_radius, 0)
    .lineTo(final_base_radius, 1)
    # Tangent arc for the bell curve
    .tangentArcPoint((top_flat_radius, skirt_height), relative=False)
    .lineTo(top_flat_radius, skirt_height + lip_height)
    .lineTo(0, skirt_height + lip_height)
    .close()
    .revolve()
)

# 3. Create the Handle
# The handle is a bridge shape (inverted U).
handle_height_rel = 12.0
handle_total_length = 40.0
handle_thickness_xz = 6.0 # Width of the bar
handle_thickness_y = 6.0  # Depth of the bar

# Locate the top surface
top_face_z = skirt_height + lip_height

handle = (
    cq.Workplane("XY")
    .workplane(offset=top_face_z)
    # Draw the footprint of the two legs
    .rect(handle_total_length, handle_thickness_y)
    .extrude(handle_height_rel)
)

# Cut out the middle of the block to make it a handle
cutout_length = handle_total_length - (2 * handle_thickness_xz)
cutout_height = handle_height_rel - handle_thickness_xz

cutout = (
    cq.Workplane("XY")
    .workplane(offset=top_face_z)
    .rect(cutout_length, handle_thickness_y)
    .extrude(cutout_height)
)

handle_final = handle.cut(cutout)

# Combine everything
result = lid_body.union(handle_final)

# Optional: Add fillets to handle edges to match the smooth look
result = result.edges("|Z").fillet(0.5) # Vertical edges of handle
result = result.edges("|Y").filter(lambda e: e.Center().z > top_face_z + handle_height_rel - 1).fillet(0.5) # Top edges
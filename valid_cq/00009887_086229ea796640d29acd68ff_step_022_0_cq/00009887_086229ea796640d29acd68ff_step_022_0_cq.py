import cadquery as cq

# -- Parametric Dimensions --
# Main Body
body_diameter = 40.0
body_height = 60.0

# Bottom Cone
cone_height = 10.0  # Height of the pointed tip

# Neck / Top Section
shoulder_height = 5.0     # The tapered part connecting body to neck
shoulder_top_dia = 20.0   # Diameter at top of shoulder/base of neck assembly

neck_lower_dia = 20.0     # The wider ring at the base of the neck
neck_lower_height = 4.0

neck_narrow_dia = 14.0    # The narrowest part of the neck
neck_narrow_height = 6.0

cap_dia = 22.0            # The top-most disc
cap_height = 6.0

# -- Construction --

# 1. Main cylindrical body
body = cq.Workplane("XY").circle(body_diameter / 2.0).extrude(body_height)

# 2. Bottom pointed cone
# We create a cone and unite it to the bottom face of the body.
# Note: In CadQuery, a cone is often made by lofting or extruding with taper, 
# or revolving. Here, a simple revolve of a triangle is robust.
p1 = (0, 0)
p2 = (body_diameter / 2.0, 0)
p3 = (0, -cone_height)
cone = (
    cq.Workplane("XZ")
    .polyline([p1, p2, p3, p1])
    .close()
    .revolve()
)

# 3. Top Section Assembly
# We will build up from the top face of the main body.

# The shoulder (tapered transition)
# We can create a cone transition or a simple chamfer. The image shows a conical taper.
shoulder = (
    cq.Workplane("XY")
    .workplane(offset=body_height)
    .circle(body_diameter / 2.0)
    .workplane(offset=shoulder_height)
    .circle(shoulder_top_dia / 2.0)
    .loft(combine=False)
)

# The lower ring of the neck
neck_base = (
    cq.Workplane("XY")
    .workplane(offset=body_height + shoulder_height)
    .circle(neck_lower_dia / 2.0)
    .extrude(neck_lower_height, combine=False)
)

# The narrow part of the neck
neck_narrow = (
    cq.Workplane("XY")
    .workplane(offset=body_height + shoulder_height + neck_lower_height)
    .circle(neck_narrow_dia / 2.0)
    .extrude(neck_narrow_height, combine=False)
)

# The top cap
cap = (
    cq.Workplane("XY")
    .workplane(offset=body_height + shoulder_height + neck_lower_height + neck_narrow_height)
    .circle(cap_dia / 2.0)
    .extrude(cap_height, combine=False)
)

# Combine all parts
result = body.union(cone).union(shoulder).union(neck_base).union(neck_narrow).union(cap)

# Optional: Fillets to smooth transitions if desired, but the image looks fairly sharp 
# except perhaps the shoulder transition. We'll leave it sharp as per standard primitives.

# Export or visualization would happen here in a typical workflow
# show_object(result)
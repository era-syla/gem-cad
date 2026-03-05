import cadquery as cq

# Parametric dimensions
total_height = 50.0
outer_diameter_bottom = 40.0
outer_diameter_top = 50.0
top_section_height = 15.0
wall_thickness = 5.0

# Calculate derived dimensions
radius_bottom = outer_diameter_bottom / 2.0
radius_top = outer_diameter_top / 2.0
inner_radius_bottom = radius_bottom - wall_thickness
inner_radius_top = radius_top - wall_thickness

# Create the main body
# We can model this as a revolution of a profile or by stacking cylinders and cutting.
# A revolution approach is robust for the internal curvature, but stacking cylinders is simpler for the outer shape.
# Let's use a revolution to capture the smooth internal transition which looks like a fillet or loft.

# However, looking closely, the outside is just two cylinders.
# The inside looks like a funnel. Let's model the outside first.

# 1. Base Cylinder (Bottom part)
base = cq.Workplane("XY").circle(radius_bottom).extrude(total_height)

# 2. Top Collar (Top part)
# We extrude a larger circle from the top face downwards or create a new cylinder at the correct height.
# It's easier to just union a larger cylinder at the top.
collar = (
    cq.Workplane("XY")
    .workplane(offset=total_height - top_section_height)
    .circle(radius_top)
    .extrude(top_section_height)
)

# Combine outer shapes
outer_body = base.union(collar)

# 3. Create the inner hollow shape
# The image shows a smooth transition on the inside, like a funnel.
# Let's create a loft for the cut.
# Bottom inner circle
bottom_cut_circle = cq.Workplane("XY").circle(inner_radius_bottom)

# Top inner circle
top_cut_circle = cq.Workplane("XY").workplane(offset=total_height).circle(inner_radius_top)

# To get that nice curved look inside, we might use a loft with a mid-section or just a straight loft.
# The image suggests a straight taper or a fillet. A loft is a safe parametric bet for a "funnel".
# Alternatively, we can just drill a hole and fillet the bottom edge of the top hole, but a loft is more precise.

# Let's assume it's a simple straight chamfer/loft between the two inner diameters.
# If it needs to be curved like a bowl, we would need a revolution profile.
# Looking at the shadow inside, it looks slightly curved (bowl-like) near the top.
# Let's stick to a straight loft cut for simplicity and robustness, or a revolution profile if we want to be fancy.
# Given the "funnel" description, a loft between circles is the standard way to make a conical hole.

# Let's refine the inner cut.
# It seems the hole goes all the way through.
# The top inner diameter is larger than the bottom inner diameter.
# Let's create a solid representing the negative space (the air inside) and cut it.

inner_solid = (
    cq.Workplane("XY")
    .circle(inner_radius_bottom)
    .workplane(offset=total_height)
    .circle(inner_radius_top)
    .loft(combine=False)
)

# If the bottom section is supposed to be straight cylinder inside and only flare at top:
# The image shows the shadow gradient going deep, suggesting the taper might go all the way or most of the way.
# However, standard pipe fittings often have a straight bore and a chamfer.
# Let's try a hybrid approach which looks most like the image:
# A straight bore at the bottom, and a loft/chamfer at the top section.
# But visually, the inner wall looks like one continuous taper or a bowl.
# Let's assume a continuous taper (loft) from top to bottom for the "funnel" look.

result = outer_body.cut(inner_solid)

# Optional: Adding a fillet to the inner edge if it looks rounded. 
# The image shows a sharp-ish rim at the top, but a smooth gradient inside.
# A loft provides a straight conical face. 
# If a "bowl" shape is desired, we could use the revolution of a specific spline.
# Based on the request for a generic CAD model matching the image, the loft is the most standard interpretation.

# Refinement: Looking really closely at the top rim, it's flat. The transition from the inner wall to the top face is a hard edge.
# The transition from outer cylinder to collar is a hard edge (90 deg).
# The inner surface looks like a cone.

result = result
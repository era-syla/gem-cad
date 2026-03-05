import cadquery as cq

# Parametric dimensions
hull_length = 100.0
hull_diameter = 12.0
bow_length = 15.0  # Length of the rounded front
stern_length = 25.0  # Length of the tapering rear section

# Sail (Tower) dimensions
sail_length = 12.0
sail_width = 4.0
sail_height = 8.0
sail_position_x = 10.0  # Offset from center towards bow

# Control surfaces (Rudders/Planes)
stern_plane_span = 14.0
stern_plane_chord = 6.0
stern_plane_thickness = 1.0

# Construction

# 1. Main Hull Body
# Create the central cylindrical section
mid_section_length = hull_length - bow_length - stern_length
mid_section = cq.Workplane("XY").circle(hull_diameter / 2).extrude(mid_section_length)

# Create the Bow (front) - Ellipsoidal shape
bow = (
    cq.Workplane("XY")
    .workplane(offset=mid_section_length)
    .circle(hull_diameter / 2)
    .workplane(offset=bow_length)
    .circle(0.1) # Tiny circle at the tip to loft to
    .loft(combine=True)
)

# Refine Bow Shape (Make it more rounded/elliptical than a cone)
# We can approximate an elliptical nose by creating a revolution instead for better control, 
# but a loft with a few sections or a simple fillet on a cylinder works. 
# Let's stick to the loft approach but maybe add a midpoint for curvature or just use a revolution for the whole hull.
# Actually, let's rebuild the hull as a revolution for smoother transitions.

def make_hull_profile():
    # Points for the revolution profile (Y is radius, X is length)
    pts = []
    
    # Stern tip
    pts.append((0, 0))
    
    # Stern taper start
    pts.append((stern_length, hull_diameter / 2))
    
    # Parallel mid-body end
    pts.append((stern_length + mid_section_length, hull_diameter / 2))
    
    # Bow tip (we use a spline for the bow curve)
    # This is simplified; usually, we'd define a spline. 
    # Let's just return the polyline for the main body and handle the bow separately to make it round.
    return pts

# Re-approach: Stick components together. It's more robust for CadQuery beginners reading the code.

# A. Central Cylinder
main_body = (
    cq.Workplane("YZ")
    .circle(hull_diameter / 2)
    .extrude(mid_section_length)
    .translate((mid_section_length / 2, 0, 0)) # Center it roughly
)

# B. Bow (Front Dome) - use a revolution of an arc
bow_profile = (
    cq.Workplane("XY")
    .moveTo(mid_section_length, hull_diameter / 2)
    .threePointArc((mid_section_length + bow_length * 0.6, hull_diameter * 0.4), (mid_section_length + bow_length, 0))
    .lineTo(mid_section_length, 0)
    .close()
    .revolve(axisStart=(0,0,0), axisEnd=(1,0,0))
)

# C. Stern (Rear Taper)
stern_profile = (
    cq.Workplane("XY")
    .moveTo(0, hull_diameter / 2)
    .lineTo(-stern_length, 0.5) # Blunt end for propeller mounting
    .lineTo(0, 0)
    .close()
    .revolve(axisStart=(0,0,0), axisEnd=(1,0,0))
)

# Combine Hull parts
hull = main_body.union(bow_profile).union(stern_profile)

# 2. Sail (Conning Tower)
# Create a streamlined airfoil shape for the sail
sail_profile = (
    cq.Workplane("XY")
    .moveTo(sail_length/2, 0)
    .spline([(0, sail_width/2), (-sail_length/2, 0)], includeCurrent=True)
    .mirrorX()
    .extrude(sail_height)
)

# Fillet the top of the sail
sail_profile = sail_profile.edges("|Z").fillet(0.5)

# Position the sail on the hull
sail = sail_profile.translate((sail_position_x, 0, hull_diameter/2 - 1.0)) # Sink slightly into hull

# 3. Stern Planes (X-tail or Cruciform configuration)
def create_fin(rotation_angle):
    fin = (
        cq.Workplane("XY")
        .moveTo(0, 0)
        .lineTo(-stern_plane_chord, 0)
        .lineTo(-stern_plane_chord + 2, stern_plane_span/2) # Tapered back edge
        .lineTo(-2, stern_plane_span/2) # Tapered front edge
        .close()
        .extrude(stern_plane_thickness)
        .translate((-stern_length * 0.6, 0, 0)) # Position near rear
        .rotate((0,0,0), (1,0,0), rotation_angle)
    )
    return fin

# Create 4 fins in a cross configuration
fin_top = create_fin(90)
fin_bottom = create_fin(-90)
fin_left = create_fin(0)
fin_right = create_fin(180)

fins = fin_top.union(fin_bottom).union(fin_left).union(fin_right)

# 4. Details (Top Deck Casing)
# A raised platform running along the top spine
deck_casing_width = hull_diameter * 0.6
deck_casing_length = mid_section_length * 0.8
deck_casing = (
    cq.Workplane("YZ")
    .rect(deck_casing_width, hull_diameter/2) # Simple rect slice
    .extrude(deck_casing_length)
    .translate((deck_casing_length/2 - 5, 0, hull_diameter/4))
    .intersect(
        cq.Workplane("YZ").circle(hull_diameter/2).extrude(1000).translate((500,0,0))
    )
)
# That intersection method is messy. Let's make a simple flat extrusion that sits on top.
deck_casing_clean = (
    cq.Workplane("XY")
    .rect(deck_casing_length, deck_casing_width)
    .extrude(hull_diameter/2 + 0.5)
    .translate((5, 0, 0))
    .edges("|Z").fillet(deck_casing_width/2.1) # Round ends
)
# Intersect with a slightly larger hull to conform it
mask = (
    cq.Workplane("YZ")
    .circle(hull_diameter/2 + 0.5)
    .extrude(hull_length * 2)
    .translate((hull_length/2, 0, 0))
)
deck_feature = deck_casing_clean.intersect(mask).cut(hull) # Ensure it sits on surface not inside

# Assemble final submarine
result = hull.union(sail).union(fins)

# Apply fillet to the junction where the sail meets the hull
# This can be computationally expensive or fail on complex intersections, 
# so we select edges carefully.
try:
    result = result.edges(cq.selectors.NearestToPointSelector((sail_position_x, 0, hull_diameter/2))).fillet(1.0)
except:
    pass # Skip if geometry is too complex for automatic filleting kernel

# Optional: Add diving planes to the sail
sail_plane = (
    cq.Workplane("XY")
    .rect(4, 8)
    .extrude(0.5)
    .translate((sail_position_x, 0, hull_diameter/2 + sail_height * 0.6))
)
result = result.union(sail_plane)

# Center the model
result = result.translate((-mid_section_length/2, 0, 0))
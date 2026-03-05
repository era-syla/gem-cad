import cadquery as cq

# Parametric dimensions
height = 50.0         # Total height of the object
max_diameter = 40.0   # Maximum outer diameter at the broadest points
min_diameter = 30.0   # Diameter at top/bottom flat faces
waist_diameter = 32.0 # Diameter at the central groove/waist
hole_diameter = 15.0  # Diameter of the through-hole

# Geometric calculations
# The shape is essentially a surface of revolution.
# It looks like two convex curves meeting at a concave waist.
# We can model this by drawing the profile on the XZ plane and revolving it around the Z axis.

def create_profile(h, d_max, d_min, d_waist, d_hole):
    r_max = d_max / 2.0
    r_min = d_min / 2.0
    r_waist = d_waist / 2.0
    r_hole = d_hole / 2.0
    
    # Points for the profile (working on positive X side, revolving around Z)
    p_bot_inner = (r_hole, 0)
    p_bot_outer = (r_min, 0)
    
    # We estimate the control points for the curves based on the visual.
    # The profile goes from bottom outer radius -> bulge out -> waist in -> bulge out -> top outer radius.
    
    # Let's define the height levels
    h_waist = h / 2.0
    h_bulge_bot = h * 0.25
    h_bulge_top = h * 0.75
    
    p_bulge_bot = (r_max, h_bulge_bot)
    p_waist_outer = (r_waist, h_waist)
    p_bulge_top = (r_max, h_bulge_top)
    
    p_top_outer = (r_min, h)
    p_top_inner = (r_hole, h)
    
    # Construct the profile wire
    # Using spline to get smooth organic curves similar to the image
    
    # Bottom section curve: from bottom flat to waist
    # We need a 3-point interpolation or spline
    
    return (
        cq.Workplane("XZ")
        .moveTo(*p_bot_inner)
        .lineTo(*p_bot_outer)
        # Curve 1: Bottom flat edge to waist, passing through max bulge
        .spline([p_bulge_bot, p_waist_outer], includeCurrent=True)
        # Curve 2: Waist to top flat edge, passing through max bulge
        .spline([p_bulge_top, p_top_outer], includeCurrent=True)
        .lineTo(*p_top_inner)
        .close()
    )

# Create the profile wire
profile_wire = create_profile(height, max_diameter, min_diameter, waist_diameter, hole_diameter)

# Revolve the profile to create the solid
result = profile_wire.revolve(360)

# If we want to be more explicit about the central groove being sharper (as it appears in the image
# to have a distinct transition rather than a perfectly smooth sine wave), we might construct it differently.
# Let's refine the profile logic to match the image better. The image shows a distinct "waist" line.
# It looks like two separate convex arcs meeting.

# Revised Approach: Two Arcs
r_max = max_diameter / 2.0
r_min = min_diameter / 2.0
r_waist = waist_diameter / 2.0
r_hole = hole_diameter / 2.0

# Calculate radius for a 3-point arc (Start, Mid, End)
# Bottom Bulb: Starts at (r_min, 0), Mid at (r_max, h*0.25), Ends at (r_waist, h*0.5)
# Top Bulb: Starts at (r_waist, h*0.5), Mid at (r_max, h*0.75), Ends at (r_min, h)

result = (
    cq.Workplane("XZ")
    # Start at bottom inner hole
    .moveTo(r_hole, 0)
    # Line to bottom outer edge
    .lineTo(r_min, 0)
    # Arc for the bottom section
    .threePointArc((r_max, height * 0.25), (r_waist, height * 0.5))
    # Arc for the top section
    .threePointArc((r_max, height * 0.75), (r_min, height))
    # Line to top inner hole
    .lineTo(r_hole, height)
    # Close the shape back to start
    .close()
    # Revolve around Z axis
    .revolve()
)
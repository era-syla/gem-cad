import cadquery as cq
import math

# --- Parametric Dimensions ---

# Base dimensions
base_diameter = 60.0
base_height = 10.0

# Stem dimensions
stem_diameter = 10.0
stem_height = 40.0

# Funnel/Top dimensions
top_rim_diameter = 40.0
max_diameter = 160.0
funnel_height = 70.0
funnel_thickness = 2.0

# Fillet/Curve parameters
# This controls how aggressively the shape flares out.
# A spline approach is best for this organic "trumpet" shape.
p1 = (top_rim_diameter / 2.0, 0)
p2 = (top_rim_diameter / 2.0, -funnel_height * 0.3)  # Go straight down a bit
p3 = (max_diameter / 2.0, -funnel_height * 0.7)      # Flare out
p4 = (max_diameter / 2.0, -funnel_height)            # End point

# --- Geometry Construction ---

# 1. Create the Base
base = cq.Workplane("XY").circle(base_diameter / 2.0).extrude(base_height)

# 2. Create the Stem
# The stem sits on top of the base.
stem = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    .circle(stem_diameter / 2.0)
    .extrude(stem_height)
)

# 3. Create the Funnel/Trumpet Shape using a Surface of Revolution
# We define a profile in the XZ plane and revolve it around the Z axis.
# The top of the funnel starts at base_height + stem_height + funnel_height.
# However, to make reasoning easier, let's build the profile relative to the top rim
# and then move it into position.

def make_funnel_profile(thickness):
    # Outer profile points (relative to top center at 0,0)
    # Using a Spline for smooth curvature
    outer_pts = [
        (top_rim_diameter / 2.0, 0),
        (top_rim_diameter / 2.0 + 2, -15), # Initial straight-ish section
        (top_rim_diameter / 2.0 + 10, -35), # Start curving
        (max_diameter / 2.0, -funnel_height)
    ]
    
    # Inner profile points (offset by thickness)
    inner_pts = [
        (max_diameter / 2.0, -funnel_height),
        (max_diameter / 2.0 - thickness, -funnel_height), # Bottom thickness
        (top_rim_diameter / 2.0 + 10 - thickness*0.2, -35), # Approx offset
        (top_rim_diameter / 2.0 + 2 - thickness, -15),
        (top_rim_diameter / 2.0 - thickness, 0)
    ]
    
    return outer_pts, inner_pts

# Creating the revolution profile
# We will use a spline for the outer curve for that smooth organic look
funnel_top_z = base_height + stem_height + funnel_height

# We construct the solid by revolving a face.
# Let's define the points for the cross-section on the XZ plane.
s_pts = [
    (top_rim_diameter / 2.0, funnel_top_z),
    (top_rim_diameter / 2.0, funnel_top_z - 15),
    (max_diameter / 2.0, base_height + stem_height)
]

# Create the solid funnel
funnel_solid = (
    cq.Workplane("XZ")
    .moveTo(top_rim_diameter / 2.0, funnel_top_z)
    .spline(
        [(top_rim_diameter / 2.0 + 5, funnel_top_z - 25), 
         (max_diameter / 2.0, base_height + stem_height)],
        includeCurrent=True,
        tangents=[(0, -1), (1, 0)] # Tangent down at start, horizontal at end
    )
    .hLine(-funnel_thickness) # Thickness at the bottom rim
    # Create the inner surface spline going back up
    .spline(
        [(top_rim_diameter / 2.0 + 5 - funnel_thickness, funnel_top_z - 25),
         (top_rim_diameter / 2.0 - funnel_thickness, funnel_top_z)],
        includeCurrent=True,
        tangents=[(-1, 0), (0, 1)] # Horizontal start, vertical end
    )
    .close()
    .revolve()
)

# 4. Combine all parts
result = base.union(stem).union(funnel_solid)

# Optional: Add fillets to junctions for realism
result = result.edges(cq.selectors.NearestToPointSelector((0, 0, base_height))).fillet(2.0)
result = result.edges(cq.selectors.NearestToPointSelector((0, 0, base_height + stem_height))).fillet(2.0)
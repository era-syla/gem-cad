import cadquery as cq

# Parametric dimensions
height = 100.0   # Total vertical height
width = 30.0     # Maximum width at the center
thickness = 5.0  # Thickness of the plate
hole_diam = 6.0  # Diameter of the center hole
arc_radius = 150.0 # Radius of the side arcs (controls curvature)

# Create the sketch profile
# We will create one half and mirror it or draw the full shape using arcs
# Strategy: Draw a 3-point arc for one side, mirror for the other, connect top/bottom

# Calculate half-width for points
half_w = width / 2.0
half_h = height / 2.0

# Define points for the profile
# Top-Right, Bottom-Right, Bottom-Left, Top-Left
# However, the sides are curved. The shape looks like two large radius arcs intersection
# or a rectangle with bulging sides. Let's assume bulging sides (convex).

# Using the intersection of two circles approach or 3-point arcs is best.
# Let's use a sketch with 3-point arcs.

result = (
    cq.Workplane("XY")
    .moveTo(0, half_h) # Top center
    .lineTo(half_w/2, half_h) # Small flat top section? The image looks slightly flat or just very curved. 
                              # Actually, looking closely, it has distinct flat top and bottom edges.
    
    # Let's refine the shape logic based on the image:
    # It looks like a rectangle where the long vertical sides are replaced by outward curving arcs.
    # Top and bottom edges are straight horizontal lines.
    
    .moveTo(half_w, half_h) # Start Top Right (actually we need to move to the corner of the flat top)
    # Let's define the top width. It tapers. 
    # Let's assume a top_width parameter.
)

# Revised Parameters
total_height = 80.0
center_width = 30.0
tip_width = 10.0   # Width at the very top and bottom
thickness = 4.0
hole_diameter = 6.0

# Construction
result = (
    cq.Workplane("XY")
    .moveTo(tip_width / 2.0, total_height / 2.0)  # Top Right Corner
    .threePointArc((center_width / 2.0, 0), (tip_width / 2.0, -total_height / 2.0)) # Arc to Bottom Right
    .lineTo(-tip_width / 2.0, -total_height / 2.0) # Bottom Edge
    .threePointArc((-center_width / 2.0, 0), (-tip_width / 2.0, total_height / 2.0)) # Arc to Top Left
    .close()
    .extrude(thickness)
    .faces(">Z").workplane()
    .circle(hole_diameter / 2.0)
    .cutThruAll()
)
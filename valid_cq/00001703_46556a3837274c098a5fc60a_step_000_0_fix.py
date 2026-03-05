import cadquery as cq
import math

# This appears to be a curved rail/trim piece that curves up at the right end
# It has a cross-section with multiple ridges/channels and sweeps along a curved path

# Define the cross-section profile (small rectangular profile with ridges)
def make_profile():
    """Create the cross-section profile of the rail"""
    # Profile is roughly rectangular with some grooves
    w = 8  # width of profile
    h = 4  # height of profile
    
    pts = [
        (0, 0),
        (w, 0),
        (w, h),
        (0, h),
        (0, 0),
    ]
    return pts

# Create the sweep path - straight section then curves up at right end
# The piece is mostly horizontal with a curve at the right end going upward

# Path: start at left, go right (mostly straight), then curve upward at the right
# Looking at the image: long horizontal section, then curves up at right end

path_length = 180  # horizontal length
curve_radius = 60  # radius of the upward curve at right end
curve_angle = 70   # degrees of the upward curve

# Build the sweep path as a wire
# Start from left, go right, then curve upward
path = (
    cq.Workplane("XZ")
    .moveTo(-path_length/2, 0)
    .lineTo(path_length/2 - curve_radius, 0)
    .radiusArc((path_length/2 - curve_radius + curve_radius * math.sin(math.radians(curve_angle)),
                curve_radius - curve_radius * math.cos(math.radians(curve_angle))),
               curve_radius)
)

path_wire = path.wire()

# Define the cross-section on a perpendicular plane
# Cross section has 3 parallel ridges
def make_cross_section(wp):
    """Multi-ridge cross section"""
    total_w = 10
    h_base = 3
    ridge_h = 1.5
    ridge_w = 1.5
    gap = 2.5
    
    # Make a base rectangle with grooves cut in top
    result = (wp
        .rect(total_w, h_base)
    )
    return result

# Use a simpler approach: sweep a profile along a path
# Profile cross-section: flat bar with ridges on top

# Create cross section profile points
def profile_wire():
    w = 10
    h = 3.5
    groove_depth = 1.5
    groove_w = 1.0
    
    # Base shape
    pts = []
    pts.append((-w/2, -h/2))
    pts.append((w/2, -h/2))
    pts.append((w/2, h/2))
    # Add groove features on top
    pts.append((w/2 - 2, h/2))
    pts.append((w/2 - 2, h/2 + groove_depth))
    pts.append((w/2 - 2 - groove_w, h/2 + groove_depth))
    pts.append((w/2 - 2 - groove_w, h/2))
    pts.append((0 + groove_w/2, h/2))
    pts.append((0 + groove_w/2, h/2 + groove_depth))
    pts.append((0 - groove_w/2, h/2 + groove_depth))
    pts.append((0 - groove_w/2, h/2))
    pts.append((-w/2 + 2 + groove_w, h/2))
    pts.append((-w/2 + 2 + groove_w, h/2 + groove_depth))
    pts.append((-w/2 + 2, h/2 + groove_depth))
    pts.append((-w/2 + 2, h/2))
    pts.append((-w/2, h/2))
    pts.append((-w/2, -h/2))
    
    return pts

# Build the path
path_wp = (
    cq.Workplane("XY")
    .moveTo(-90, 0)
    .lineTo(30, 0)
    .radiusArc((30 + 60 * math.sin(math.radians(65)), 60 - 60 * math.cos(math.radians(65))), 60)
)

path_wire_obj = path_wp.wire().vals()[0]

# Build cross section
cross_section = (
    cq.Workplane("YZ")
    .moveTo(0, 0)
    .polyline([(5, 0), (5, 3.5), (3, 3.5), (3, 5), (2, 5), (2, 3.5),
               (0.5, 3.5), (0.5, 5), (-0.5, 5), (-0.5, 3.5),
               (-2, 3.5), (-2, 5), (-3, 5), (-3, 3.5), (-5, 3.5), (-5, 0)])
    .close()
)

cross_wire = cross_section.wire().vals()[0]

result = (
    cq.Workplane("YZ")
    .add(cross_wire)
    .toPending()
    .sweep(path_wire_obj)
)

# Add fillets to soften edges
try:
    result = result.edges("|Z").fillet(0.8)
except:
    pass
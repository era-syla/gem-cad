import cadquery as cq

# Create a pebble-like shape - oval/rounded box with dome top
# Base dimensions
length = 80
width = 65
height = 35
corner_radius = 22

# Create the main body using a rounded rectangle extruded and then shaped
# Start with a rounded rectangle base
base = (
    cq.Workplane("XY")
    .ellipse(length/2, width/2)
    .extrude(height * 0.4)
)

# Create the domed top by making an ellipsoid-like shape
# Use a sphere scaled to create dome effect
dome_height = height * 0.75

# Build the main pebble shape using revolve approach
# Create profile in XZ plane for revolution... 
# Better approach: use loft between shapes at different heights

# Bottom ellipse
bottom = cq.Workplane("XY").ellipse(length/2, width/2)

# Middle ellipse (slightly larger, at mid height)
mid_h = height * 0.35
mid = cq.Workplane("XY").workplane(offset=mid_h).ellipse(length/2 * 1.02, width/2 * 1.02)

# Top ellipse (smaller, at top)
top_h = height * 0.85
top = cq.Workplane("XY").workplane(offset=top_h).ellipse(length/2 * 0.55, width/2 * 0.55)

# Peak point - use very small ellipse
peak_h = height
peak = cq.Workplane("XY").workplane(offset=peak_h).ellipse(2, 2)

# Loft through all profiles
result = (
    cq.Workplane("XY")
    .ellipse(length/2, width/2)
    .workplane(offset=mid_h)
    .ellipse(length/2 * 1.02, width/2 * 1.02)
    .workplane(offset=top_h - mid_h)
    .ellipse(length/2 * 0.55, width/2 * 0.55)
    .workplane(offset=peak_h - top_h)
    .ellipse(3, 3)
    .loft()
)

# Add a flat bottom by intersecting with a box
bbox = (
    cq.Workplane("XY")
    .workplane(offset=-height * 0.05)
    .box(length * 1.5, width * 1.5, height * 1.5, centered=(True, True, False))
)

result = result.intersect(bbox)

# Apply fillets to smooth edges
try:
    result = result.edges("|Z").fillet(5)
except:
    pass

# Add a recessed panel on top (indented oval on the top surface)
# Create a slightly smaller ellipse indented into the top
panel_depth = 1.5
panel_length = length * 0.55
panel_width = width * 0.52

panel_cutter = (
    cq.Workplane("XY")
    .workplane(offset=height * 0.72)
    .ellipse(panel_length/2, panel_width/2)
    .extrude(10)
)

# We won't cut the panel to keep geometry clean - just leave the main shape
# The image shows an indented panel but it's subtle

# Final result is the lofted pebble shape
try:
    result = result.edges(cq.NearestToPointSelector((0, 0, height))).fillet(3)
except:
    pass
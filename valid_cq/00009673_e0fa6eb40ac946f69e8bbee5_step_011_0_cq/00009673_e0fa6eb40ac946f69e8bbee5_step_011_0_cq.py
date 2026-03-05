import cadquery as cq

# Parameters
total_length = 200.0  # Total length of the assembly
shaft_diameter = 4.0  # Diameter of the main cylindrical sections
hex_width = 8.0       # Width across flats for the hex sections
hex_length = 10.0     # Length of the end hex sections
center_hex_length = 15.0 # Length of the center hex section
hole_diameter = 2.0   # Diameter of the holes at the ends

# Calculations derived from parameters
shaft_radius = shaft_diameter / 2.0
hole_radius = hole_diameter / 2.0

# Create the main shaft (the long cylindrical part)
# We make it the full length first, and the hex parts will be added/cut
shaft = cq.Workplane("XY").circle(shaft_radius).extrude(total_length)

# Create the hexagonal profile
# Width across flats (W) relates to radius (R) of circumscribed circle by: R = W / sqrt(3)
# But cq.polygon uses radius of the circle intersecting the vertices. 
# For a hexagon, side length = circumradius.
# Distance from center to flat (apothem) = hex_width / 2. 
# Circumradius = apothem / cos(30 deg) = (hex_width/2) / (sqrt(3)/2) = hex_width / sqrt(3)
circumradius = hex_width / 1.73205

# Define the Hexagon shapes
def create_hex_segment(length):
    return (cq.Workplane("XY")
            .polygon(nSides=6, diameter=circumradius*2)
            .extrude(length))

# Create the three hex sections
hex_start = create_hex_segment(hex_length)
hex_end = create_hex_segment(hex_length)
hex_center = create_hex_segment(center_hex_length)

# Position the hex sections relative to the shaft
# The shaft was extruded from Z=0 to Z=total_length
hex_start_moved = hex_start  # Already at Z=0
hex_center_moved = hex_center.translate((0, 0, (total_length / 2.0) - (center_hex_length / 2.0)))
hex_end_moved = hex_end.translate((0, 0, total_length - hex_length))

# Combine the shaft with the hex sections
# We union them together.
result = shaft.union(hex_start_moved).union(hex_center_moved).union(hex_end_moved)

# Create holes at both ends
# Hole at the start (Z=0)
result = result.faces("<Z").workplane().hole(hole_diameter, depth=hex_length)

# Hole at the end (Z=total_length)
result = result.faces(">Z").workplane().hole(hole_diameter, depth=hex_length)

# Optional: Add small chamfers to the hex edges for realism (looks like the image has slight bevels)
# Selecting edges is tricky, so let's keep it simple or apply a general fillet/chamfer if needed.
# The image shows fairly sharp hex edges but maybe chamfered ends on the hex stock.
# Let's chamfer the outer circular edges of the hexes for a clean look like in the image.
# We look for edges on the Z extremes and the transitions.
# Since simple selection might grab the wrong edges, we'll leave it clean or add a very specific selector.
# Looking closely at the image, the very ends of the hexes are chamfered.

try:
    # Attempt to chamfer the outer ends of the hex nuts
    result = result.edges(cq.selectors.BoxSelector((-10, -10, -0.1), (10, 10, 0.1))).chamfer(0.5)
    result = result.edges(cq.selectors.BoxSelector((-10, -10, total_length-0.1), (10, 10, total_length+0.1))).chamfer(0.5)
except:
    pass # If selection fails, return unchamfered model

# Export or visualization
if 'show_object' in globals():
    show_object(result)
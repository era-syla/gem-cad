import cadquery as cq
import math

# --- Parameters ---
thickness = 2.0  # Thickness of the plate

# Central hub
hub_radius = 8.0
center_hole_radius = 1.0  # Small center hole
hex_hole_width = 3.0 # Size of hexagonal cutout

# Long petal parameters
long_petal_length = 35.0  # Distance from center to tip
long_petal_width_base = 3.0  # Width near the hub
long_petal_width_tip = 7.0   # Width at the widest part near tip
long_petal_count = 6

# Short spike parameters
short_spike_length = 22.0  # Distance from center to tip
short_spike_width_base = 2.0
short_spike_width_mid = 4.0
short_spike_count = 6

# --- Helper Functions ---

def create_long_petal():
    """
    Creates a single long petal shape oriented along the Y-axis.
    The shape widens towards the tip and ends in a full semicircle/round.
    """
    # Define key points
    # Start at the hub boundary
    y_start = hub_radius * 0.9 # Slight overlap for boolean union
    y_end = long_petal_length
    
    # Calculate radius for the rounded tip
    tip_radius = long_petal_width_tip / 2.0
    y_straight_end = y_end - tip_radius
    
    # Create the profile
    # We will draw half the profile and mirror it
    pts = [
        (0, y_start),
        (long_petal_width_base / 2.0, y_start),
        (long_petal_width_tip / 2.0, y_straight_end),
        (0, y_end) # Top center point for arc
    ]
    
    # Construct the sketch
    # Using spline for the side to give it a nice organic curve
    sk = (
        cq.Workplane("XY")
        .moveTo(0, y_start)
        .lineTo(long_petal_width_base / 2.0, y_start)
        .spline([(long_petal_width_tip / 2.0, y_straight_end)], includeCurrent=True)
        # Create the rounded tip
        .threePointArc((0, y_end), (-long_petal_width_tip / 2.0, y_straight_end))
        # Complete the other side with a spline back to base
        .spline([(-long_petal_width_base / 2.0, y_start)], includeCurrent=True)
        .lineTo(0, y_start)
        .close()
    )
    
    return sk

def create_short_spike():
    """
    Creates a single short spike shape oriented along the Y-axis.
    The shape is angular/diamond-like.
    """
    y_start = hub_radius * 0.9 # Slight overlap
    y_mid = (y_start + short_spike_length) * 0.7 # Where it is widest
    y_end = short_spike_length
    
    pts = [
        (0, y_start),
        (short_spike_width_base / 2.0, y_start),
        (short_spike_width_mid / 2.0, y_mid),
        (0, y_end),
        (-short_spike_width_mid / 2.0, y_mid),
        (-short_spike_width_base / 2.0, y_start),
    ]
    
    sk = (
        cq.Workplane("XY")
        .polyline(pts)
        .close()
    )
    return sk

# --- Construction ---

# 1. Create the central hub
hub = cq.Workplane("XY").circle(hub_radius).extrude(thickness)

# 2. Create the long petals pattern
long_petals = cq.Workplane("XY")
petal_shape = create_long_petal().extrude(thickness)

for i in range(long_petal_count):
    angle = i * (360.0 / long_petal_count)
    rotated_petal = petal_shape.rotate((0,0,0), (0,0,1), angle)
    long_petals = long_petals.union(rotated_petal)

# 3. Create the short spikes pattern
# These are offset by half the angle between long petals
short_spikes = cq.Workplane("XY")
spike_shape = create_short_spike().extrude(thickness)
angle_offset = (360.0 / long_petal_count) / 2.0

for i in range(short_spike_count):
    angle = i * (360.0 / short_spike_count) + angle_offset
    rotated_spike = spike_shape.rotate((0,0,0), (0,0,1), angle)
    short_spikes = short_spikes.union(rotated_spike)

# 4. Combine everything
result = hub.union(long_petals).union(short_spikes)

# 5. Add the center details (Hexagon hole inside a small circular recess)
# Looking closely at the image, there is a hexagonal hole in the center.
# There might be a slight recess, but it's hard to be certain. Let's stick to the hex hole.
# Actually, looking very closely, it looks like a hexagonal recess with a circular hole, 
# or a hexagonal hole. Let's do a hexagonal hole as it's a common mechanical feature.

result = result.faces(">Z").polygon(6, hex_hole_width).cutThruAll()

# Refine edges? The image shows fairly sharp edges, standard for laser cut or 3D printed parts.
# No fillets required based on visual inspection.

# Ensure 'result' is the final variable
result = result
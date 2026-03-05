import cadquery as cq

# Parametric Dimensions
head_diameter = 20.0       # Outer diameter of the countersunk head
shaft_diameter = 10.0      # Main shaft diameter
total_length = 40.0        # Total length of the rivet/fastener
head_angle = 80.0          # Included angle of the countersink
head_height_ref = 5.0      # Approximate height of the head section
chamfer_size = 1.0         # Chamfer at the end of the shaft
fillet_radius = 0.5        # Slight fillet at the transition if needed (optional)

# Calculate derived dimensions based on geometry
# The head is conical. Let's construct it by revolving a profile or lofting.
# A simpler approach for this standard shape is stacking cylinders and cones.

# 1. Create the main shaft
# We'll build it along the Z axis.
shaft_length = total_length - head_height_ref 

# Create the shaft
shaft = cq.Workplane("XY").circle(shaft_diameter / 2.0).extrude(shaft_length)

# 2. Create the countersunk head
# We need a cone that starts at the shaft diameter and flares out to the head diameter.
# We align it at the top of the shaft.
# Height of the cone can be calculated or specified. Let's use the reference height.
head = (
    cq.Workplane("XY")
    .workplane(offset=shaft_length)
    .circle(shaft_diameter / 2.0)
    .workplane(offset=head_height_ref)
    .circle(head_diameter / 2.0)
    .loft(combine=True)
)

# Combine the shaft and the head
# Note: CadQuery's loft usually combines automatically if created on the stack, 
# but we need to ensure the base shaft is part of the operation.
# Alternatively, create the whole profile and revolve it, which is often cleaner for turned parts.

# --- Alternative Revolve Method (Cleaner for this geometry) ---

# Define the profile points for a revolution
# Origin is at the bottom center of the shaft
pts = [
    (0, 0),                                     # Center bottom
    (shaft_diameter / 2.0 - chamfer_size, 0),   # Chamfer start
    (shaft_diameter / 2.0, chamfer_size),       # Chamfer end / Shaft start
    (shaft_diameter / 2.0, shaft_length),       # Shaft end / Head start
    (head_diameter / 2.0, total_length),        # Head rim
    (0, total_length),                          # Center top
    (0, 0)                                      # Close loop
]

# Create the solid by revolving the profile
result = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .revolve()
)

# In the image, there is a very subtle cylindrical section just before the cone (a shoulder)
# Let's refine the profile to match the image more closely.
# The image shows: 
# 1. Chamfered end
# 2. Long cylindrical shaft
# 3. A transition fillet or small groove? No, it looks like a clean transition.
# Actually, looking closely at the 'neck', there is a line indicating a transition. 
# It looks like a standard solid rivet with a countersunk head. 
# The render mesh lines suggest a simple cylinder-to-cone transition.

# Let's stick to the revolve profile but ensuring the chamfer is explicit.

result = result.edges(">Z").fillet(0.2) # Optional soft edge on the flat top

# Final check of the logic:
# 1. (0,0) -> Bottom center
# 2. Chamfer out
# 3. Up the shaft
# 4. Flare out for the head (countersink)
# 5. Back to center
# 6. Close

# Refined parameters for the specific look in the image (slightly steeper head)
head_h = 6.0
shaft_len = 30.0
shaft_rad = 4.0
head_rad = 10.0
chamfer = 1.0

pts_refined = [
    (0, 0),
    (shaft_rad - chamfer, 0),
    (shaft_rad, chamfer),
    (shaft_rad, shaft_len),
    (head_rad, shaft_len + head_h),
    (0, shaft_len + head_h)
]

result = (
    cq.Workplane("XZ")
    .polyline(pts_refined)
    .close()
    .revolve()
)
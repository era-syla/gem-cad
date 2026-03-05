import cadquery as cq

# Parameters for the gear rack
length = 150.0       # Total length of the rack
width = 10.0         # Width of the rack
base_height = 5.0    # Height of the solid base below the teeth
tooth_height = 4.0   # Height of each tooth
pitch = 5.0          # Distance between corresponding points on adjacent teeth
tooth_base_w = 3.0   # Width of the tooth at the bottom
tooth_top_w = 1.0    # Width of the tooth at the top (trapezoidal profile)

# Calculate the number of teeth that fit in the length
# We leave a small margin at the ends usually, or just fill it.
# Let's create a pattern that fits within the length.
num_teeth = int(length / pitch)

# 1. Create the base rectangular bar
# We center it on X and Y for convenience, but the teeth will be built on top (Z+)
base = cq.Workplane("XY").box(length, width, base_height)

# 2. Define the profile of a single tooth
# We'll draw the trapezoidal shape on the side (XZ plane) or extrude across Y.
# Let's draw it on the YZ plane (side view) and extrude along X? No, the rack is long in X.
# It's better to sketch the tooth profile on the XZ plane and extrude it in Y (width).
# But wait, CadQuery works best by adding to a face.

# Strategy: Create the base, then select the top face, sketch the tooth profile, and extrude.
# Or better: Create a single tooth solid, and pattern it.

def create_tooth_profile(loc):
    """
    Creates a trapezoidal tooth profile centered at the given location.
    """
    return (
        cq.Workplane("XY")
        .workplane(offset=base_height / 2) # Move to top of base
        .center(loc, 0) # Move to specific X location along the rack
        .polyline([
            (-tooth_base_w / 2, 0),
            (-tooth_top_w / 2, tooth_height),
            (tooth_top_w / 2, tooth_height),
            (tooth_base_w / 2, 0),
        ])
        .close()
        .extrude(width/2, both=True) # Extrude to match width
    )

# Since CadQuery handles patterns efficiently, let's create the base and then unite teeth.
# However, iterating and uniting boolean operations can be slow.
# A more efficient approach in CadQuery is to sketch the entire side profile (sawtooth) and extrude.

# Efficient Approach: Sketch the side profile (XZ plane)
def rack_profile():
    # Start at bottom left corner
    pts = [(-length / 2, -base_height / 2), (length / 2, -base_height / 2), (length / 2, base_height / 2)]
    
    # Generate teeth points from right to left
    # We need to calculate the starting X position for the first tooth on the right
    # To keep it centered, we calculate offsets.
    
    start_x = -length / 2
    
    # We need to construct the top profile
    current_x = length / 2
    
    # Moving right to left along the top
    top_points = []
    
    # Calculate centering offset
    total_teeth_width = num_teeth * pitch
    margin = (length - total_teeth_width) / 2
    
    # Add right margin
    if margin > 0:
        top_points.append((length/2, base_height/2))
        top_points.append((length/2 - margin, base_height/2))
    
    # Generate teeth
    # Coordinate system: X is length, Z is height (relative to center or bottom)
    # Let's adjust Z relative to base_height/2
    z_base = base_height / 2
    z_top = base_height / 2 + tooth_height
    
    for i in range(num_teeth):
        # We are moving Right to Left. 
        # Tooth structure (Right to Left): Gap -> Tooth -> ...
        # Or Tooth center based.
        
        # Let's work Left to Right for the list to be simpler, then reverse? 
        # No, let's just build the points list directly.
        pass

# Let's try the simplest robust method: 
# 1. Create Base Box.
# 2. Create one tooth as a solid.
# 3. Create a list of locations for the teeth.
# 4. Use `union` to add them all at once (or in a loop).

# Create one reference tooth
# Centered at (0,0,0) locally
tooth_sketch = (
    cq.Workplane("XZ")
    .polyline([
        (-tooth_base_w / 2, 0),
        (-tooth_top_w / 2, tooth_height),
        (tooth_top_w / 2, tooth_height),
        (tooth_base_w / 2, 0)
    ])
    .close()
    .extrude(width/2, both=True) # Extrude along Y
)

# Create the list of points for the pattern
# The rack is length 'length', centered at 0. Range is -length/2 to length/2.
# We want to center the pattern of teeth.
pattern_width = (num_teeth - 1) * pitch
start_x = -pattern_width / 2

pts = [(start_x + i * pitch, 0, base_height/2) for i in range(num_teeth)]

# Create the base
result = cq.Workplane("XY").box(length, width, base_height)

# Add the teeth using the points
# We iterate to place the single tooth geometry at every point
for pt in pts:
    # Translate the reference tooth to the point location
    located_tooth = tooth_sketch.translate(pt)
    result = result.union(located_tooth)

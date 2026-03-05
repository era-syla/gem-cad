import cadquery as cq

# Parameters for the segmented biological shape
num_segments = 9
head_radius = 14.0
tail_radius = 3.5
spacing_factor = 0.82  # Controls overlap: smaller = more overlap, larger = more separated

# Initialize the result container
result = None
current_x = 0.0

# Generate the body by unioning a series of decreasing spheres
for i in range(num_segments):
    # Calculate interpolation factor t (0.0 at head, 1.0 at tail)
    t = i / (num_segments - 1)
    
    # Calculate radius for the current segment
    # Using a power curve (t^0.9) to maintain bulk near the head slightly longer
    radius = head_radius - (head_radius - tail_radius) * (t ** 0.9)
    
    # Create the sphere for this segment
    segment = cq.Workplane("XY").sphere(radius).translate((current_x, 0, 0))
    
    # Combine with the main body
    if result is None:
        result = segment
    else:
        result = result.union(segment)
    
    # Calculate position for the next segment
    # The spacing is proportional to the current radius to maintain consistent 'waist' depth
    current_x += radius * spacing_factor

# Create the detail feature on the head (leftmost segment)
# This creates the flat circular indentation visible on the front
head_feature_cut = (
    cq.Workplane("YZ")
    .workplane(offset=-head_radius + 1.5)  # Position plane slightly inside the front surface
    .circle(head_radius * 0.35)            # Radius of the flat spot
    .extrude(-10)                          # Extrude outwards (negative X) to cut
)

# Apply the cut to the body
result = result.cut(head_feature_cut)
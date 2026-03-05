import cadquery as cq

# Parametric dimensions based on visual estimation
profile_width = 4.0
profile_height = 4.0
# Lengths of the 5 segments from longest (bottom-left) to shortest (top-right)
segment_lengths = [160.0, 50.0, 35.0, 20.0, 10.0]
gap_size = 10.0

# List to store the generated solids
solids = []
current_x_pos = 0.0

# Loop through each length to create the segmented bars
for length in segment_lengths:
    # Calculate the center position for the current segment
    # Box is created centered, so we move it by current_pos + length/2
    center_offset = current_x_pos + (length / 2.0)
    
    # Create the rectangular bar segment
    segment = (
        cq.Workplane("XY")
        .box(length, profile_width, profile_height)
        .translate((center_offset, 0, 0))
    )
    
    # Add the solid geometry to our list
    solids.append(segment.val())
    
    # Update the X position for the next segment (length of current + gap)
    current_x_pos += length + gap_size

# Combine all disjoint solids into a single Workplane object
result = cq.Workplane("XY").newObject(solids)
import cadquery as cq

# Parameters for the step block
strip_width = 20.0
strip_height = 10.0
lengths = [60, 80, 90, 100, 120]  # Lengths of the strips from front to back
labels = ["60", "80", "90", "100", "120"]
text_extrusion = 1.0

# Initialize a list to hold all solid components
solids = []

for i, (length, label) in enumerate(zip(lengths, labels)):
    # Calculate Y position. 
    # We place strips side-by-side along the Y axis.
    y_pos = i * strip_width
    
    # 1. Create the rectangular strip
    # The strips are centered on the X-axis (symmetric stepping)
    strip = (
        cq.Workplane("XY")
        .box(length, strip_width, strip_height)
        .translate((0, y_pos, strip_height / 2))
    )
    solids.append(strip)
    
    # 2. Create the embossed text
    # Determine text properties based on strip index
    if i == 0:
        # Main label ("60") is larger and centered
        font_size = 14
        x_pos = 0 
    else:
        # Step labels are smaller and aligned to the right edge
        font_size = 7
        # Estimate text width to align properly (font aspect ratio approx 0.6)
        text_width_est = len(label) * (font_size * 0.6)
        margin = 3.0
        # Position center of text such that it is 'margin' distance from the edge
        x_pos = (length / 2) - (text_width_est / 2) - margin
        
    text = (
        cq.Workplane("XY")
        .text(label, font_size, text_extrusion)
        .translate((x_pos, y_pos, strip_height))
    )
    solids.append(text)

# Union all components into the final single solid
result = solids[0]
for solid in solids[1:]:
    result = result.union(solid)
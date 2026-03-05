import cadquery as cq

# --- Parameter Definitions ---
# Main spine parameters
spine_length = 200.0
spine_diameter = 8.0
spine_radius = spine_diameter / 2.0

# Tine parameters
num_tines = 12
tine_length = 150.0
tine_diameter = 6.0
tine_radius = tine_diameter / 2.0
tine_spacing = 15.0  # Center-to-center spacing

# Tine tip parameters (tapered section)
tip_length = 15.0
tip_end_diameter = 2.0
tip_end_radius = tip_end_diameter / 2.0

# --- Geometry Construction ---

# 1. Create the main spine
# Oriented along the X-axis
spine = (cq.Workplane("YZ")
         .circle(spine_radius)
         .extrude(spine_length)
         .translate((0, 0, 0)) # Position start at origin
        )

# 2. Create a single tine
# Oriented along the Y-axis (perpendicular to spine)
# The tine has a main cylindrical body and a tapered tip
tine_body = (cq.Workplane("XZ")
             .circle(tine_radius)
             .extrude(tine_length)
            )

# Create the tapered tip
# We create a cone at the end of the tine body
tine_tip = (cq.Workplane("XZ")
            .workplane(offset=tine_length)
            .circle(tine_radius)
            .workplane(offset=tip_length)
            .circle(tip_end_radius)
            .loft(combine=True)
           )

# Combine body and tip into one tine object
single_tine = tine_body.union(tine_tip)

# Rotate the tine to be perpendicular to the spine
# The spine is along X. Let's orient tines along Y.
# Currently tine is extruded along normal of XZ plane, which is Y. So it is already correct.
# We need to rotate it 90 degrees around X to lie flat if "up" is Z, or just keep it as is.
# Looking at the image, if spine is X, tines are Y.
# Let's adjust the position relative to the spine.
# The tines seem to emerge from the center of the spine.

# 3. Create the array of tines
# Calculate starting position to center the array or align it nicely along the spine
# Let's say the spine length fits the tines exactly with some margin.
# Total width of tines array = (num_tines - 1) * spacing
total_tine_span = (num_tines - 1) * tine_spacing
start_offset = (spine_length - total_tine_span) / 2.0

tines = cq.Workplane("XY") # Dummy object to start accumulation

# Loop to create and position each tine
for i in range(num_tines):
    # Calculate position
    x_pos = start_offset + (i * tine_spacing)
    
    # Copy the single tine and move it
    # The spine is effectively from x=0 to x=spine_length.
    # The spine axis is (0,0,0) to (spine_length, 0, 0).
    # The tine is built on XZ plane, extruding in Y.
    # We translate it to the correct X position along the spine.
    current_tine = single_tine.translate((x_pos, 0, 0))
    
    if i == 0:
        tines = current_tine
    else:
        tines = tines.union(current_tine)

# 4. Combine spine and tines
result = spine.union(tines)

# Optional: Rotate for better viewing orientation similar to image
# The image shows tines pointing somewhat towards the viewer-left
result = result.rotate((0,0,0), (0,0,1), 0) 

# Export/Show
if 'show_object' in globals():
    show_object(result)
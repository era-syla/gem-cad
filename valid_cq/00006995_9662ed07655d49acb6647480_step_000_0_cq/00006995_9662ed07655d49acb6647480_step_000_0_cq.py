import cadquery as cq

# Parametric dimensions
length = 100.0        # Total length of the extrusion
base_width = 30.0     # Width at the bottom
top_width = 10.0      # Width at the top
height = 60.0         # Height of the block
rib_width = 5.0       # Width of the small ribs on the angled face
rib_depth = 3.0       # How far the ribs stick out
rib_thickness = 3.0   # Thickness of the ribs in the vertical direction
num_ribs = 3          # Number of ribs
rib_spacing = 15.0    # Vertical spacing between ribs

# Create the main wedge shape profile
# We'll sketch on the YZ plane and extrude along X
# The shape is a trapezoid: vertical back, flat top/bottom, angled front
pts = [
    (0, 0),                 # Bottom-right (if looking from side)
    (base_width, 0),        # Bottom-left
    (top_width, height),    # Top-left
    (0, height)             # Top-right
]

# Create the main body
main_body = (
    cq.Workplane("YZ")
    .polyline(pts)
    .close()
    .extrude(length)
)

# Create the ribs on the angled face
# We need to determine the angle to place the ribs correctly or just subtract/add blocks.
# A simpler approach is to create a reference plane or simply cut slots.
# Looking closely at the image, there are small U-shaped or rectangular protrusions on the angled face.
# They look like small brackets or clips.
# Let's model them as simple rectangular protrusions for simplicity based on the low-res image.

# Calculate the slope to position ribs
# The angled face connects (base_width, 0) and (top_width, height)
# Equation of line: y - y1 = m(x - x1)
# m = (height - 0) / (top_width - base_width) = height / (top_width - base_width)

ribs = cq.Workplane("YZ")

for i in range(num_ribs):
    # Calculate vertical position for each rib
    # Distribute them on the lower half/middle of the angled face
    y_pos = (i + 1) * rib_spacing
    
    # Calculate x position on the slope for this y
    # x = (y - y1)/m + x1
    # x = y / (height / (top_width - base_width)) + base_width
    slope = height / (top_width - base_width)
    x_pos = y_pos / slope + base_width
    
    # Create a small sketch for the rib
    # We will orient this rib relative to the global YZ plane
    # The image shows U-channels or just small blocks. Let's make small U-channels.
    
    # Define the U-channel profile
    u_w = rib_width
    u_h = rib_depth
    u_t = 1.0 # wall thickness of the U-channel
    
    # Draw U-shape
    rib_sketch = (
        cq.Workplane("YZ")
        .workplane(offset=0) # Reset to origin relative
        .moveTo(x_pos, y_pos)
        .rect(u_h * 2, rib_thickness) # Base rectangle sticking out
        .extrude(length/5) # Short extrusion, but we want it across the whole length?
                           # The image shows ribs spanning the whole length.
    )
    # Actually, the image shows the ribs running ALONG the length (X-axis).
    # Re-evaluating: The ribs are continuous rails along the length of the part.
    pass 

# Correction: The ribs are continuous rails along the length.
# We should add the rib profiles to the initial sketch or add them afterwards.
# Let's create a single profile that includes the ribs to ensure they are perfectly attached.

# Re-defining the sketch logic
# Main trapezoid
points = [
    (0, 0),
    (base_width, 0)
]

# Add rib details on the angled face
# We walk up the angled face adding bumps
slope = (top_width - base_width) / height # change in x per unit y
current_y = 0
current_x = base_width

# Define rib parameters
rib_y_start_offset = 10.0
rib_height_local = 4.0
rib_protrusion = 2.0
rib_gap = 12.0
number_of_rails = 3

# Generate points up the slope
for i in range(number_of_rails):
    # Move up the slope to the start of the rib
    segment_height = rib_gap if i > 0 else rib_y_start_offset
    current_y += segment_height
    current_x += segment_height * slope
    points.append((current_x, current_y))
    
    # Create the protrusion (rail)
    # Outward
    points.append((current_x + rib_protrusion, current_y))
    # Up
    current_y += rib_height_local
    current_x += rib_height_local * slope
    points.append((current_x + rib_protrusion, current_y))
    # Inward (back to slope)
    points.append((current_x, current_y))

# Finish the path to the top
points.append((top_width, height))
points.append((0, height))
points.append((0, 0)) # Close loop

# Execute geometry generation
result = (
    cq.Workplane("YZ")
    .polyline(points)
    .close()
    .extrude(length)
)
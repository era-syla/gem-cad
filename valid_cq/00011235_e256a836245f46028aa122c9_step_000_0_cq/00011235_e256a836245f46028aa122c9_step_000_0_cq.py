import cadquery as cq

# Parameters for the geometry
bar_length = 100.0  # Length of the rectangular bars
bar_width = 20.0    # Width of each rectangular bar
bar_height = 10.0   # Height (thickness) of the bars
bar_spacing = 5.0   # Gap between bars
pin_diameter = 6.0  # Diameter of the cylindrical pins
pin_height = 8.0    # Height of the cylindrical pins

num_bars = 4        # Number of bars in the assembly

# Calculate total width to center the model if needed, though simpler to build iteratively
# Pitch is the distance from the start of one bar to the start of the next
pitch = bar_width + bar_spacing

# Create a list to hold the solid parts
parts = []

for i in range(num_bars):
    # Determine the Y position for the current bar
    # We'll position them so the first bar is at y=0, second at y=pitch, etc.
    # Alternatively, center the whole array. Let's center the array around Y=0.
    total_array_width = num_bars * bar_width + (num_bars - 1) * bar_spacing
    y_pos = (i * pitch) - (total_array_width / 2) + (bar_width / 2)
    
    # Create the rectangular bar
    bar = cq.Workplane("XY").center(0, y_pos).box(bar_length, bar_width, bar_height)
    
    # Calculate pin position
    # The pins are staggered diagonally.
    # Let's say the pins move from left to right as we go from front to back bars.
    # Or simply: pin x-coordinate depends on the bar index 'i'.
    # Looking at the image, let's assume a linear offset.
    # Let's define a range for the pins along the X axis.
    pin_x_range = 40.0 # Total x-distance covered by pins from first to last
    
    if num_bars > 1:
        # Interpolate x position from -range/2 to +range/2
        x_pos = -pin_x_range/2 + (i * pin_x_range / (num_bars - 1))
    else:
        x_pos = 0
        
    # Create the pin on top of the bar
    # Select the top face of the bar
    pin = bar.faces(">Z").workplane().center(x_pos, 0).circle(pin_diameter / 2).extrude(pin_height)
    
    parts.append(pin)

# Combine all parts into a single compound object
result = parts[0]
for part in parts[1:]:
    result = result.union(part)

# If you want to export or visualize:
# show_object(result)
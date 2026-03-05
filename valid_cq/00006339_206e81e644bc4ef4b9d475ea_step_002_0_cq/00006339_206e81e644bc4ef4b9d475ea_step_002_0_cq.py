import cadquery as cq

# Parametric dimensions
bar_height = 100.0  # Height of each bar
bar_width = 10.0    # Width of each bar
bar_thickness = 5.0 # Total thickness of the bar
chamfer_size = 2.0  # Size of the chamfer on the front face
spacing = 30.0      # Distance between centers of the bars
num_bars = 3        # Number of bars to create

def create_chamfered_bar(height, width, thickness, chamfer):
    """
    Creates a single rectangular bar with a chamfered front face.
    The chamfer is created by making a loft between a base rectangle 
    and a smaller top rectangle.
    """
    
    # Calculate dimensions for the top face of the chamfer
    # The top face is smaller by 2 * chamfer_size in both dimensions
    top_width = width - (2 * chamfer)
    top_height = height - (2 * chamfer)
    
    # Base height (thickness before the chamfer slope starts)
    base_thickness = thickness - chamfer
    
    # Method 1: Extrude base and then loft the top
    # Create the base rectangle
    base = (cq.Workplane("XY")
            .box(width, height, base_thickness, centered=(True, True, False)))
    
    # Create the top face for the loft
    # We create a new workplane offset by the base thickness
    # Then draw the smaller rectangle
    # Finally, loft from the base's top face to this new rectangle
    
    # Let's try a cleaner approach: Simple extrusion with chamfer operation
    # Create the full block first
    bar = cq.Workplane("XY").box(width, height, thickness)
    
    # Select the front face (positive Z direction)
    # Then select all edges on that face and chamfer them
    bar = (bar.faces(">Z")
           .edges()
           .chamfer(chamfer))
           
    return bar

# Generate the bars
result = cq.Workplane("XY")

for i in range(num_bars):
    # Create a single bar
    bar = create_chamfered_bar(bar_height, bar_width, bar_thickness, chamfer_size)
    
    # Calculate offset for positioning
    # Centering the group of 3 around the origin usually looks best, 
    # but simple linear spacing is fine too.
    # Let's space them out along the X axis.
    x_offset = (i * spacing) - ((num_bars - 1) * spacing / 2)
    
    # Translate the bar to its position and add to result
    # Note: CadQuery operations are immutable, so we unite them
    translated_bar = bar.translate((x_offset, 0, 0))
    result = result.union(translated_bar)

# If the result is still empty (initial Workplane), we need to ensure we have content.
# The loop logic above adds to an empty plane. A better pattern for multiple independent objects:

bars = []
for i in range(num_bars):
    bar = create_chamfered_bar(bar_height, bar_width, bar_thickness, chamfer_size)
    x_offset = (i * spacing) - ((num_bars - 1) * spacing / 2)
    bars.append(bar.translate((x_offset, 0, 0)))

# Combine all bars into a single compound object
result = bars[0]
for b in bars[1:]:
    result = result.union(b)

# Export or display is handled by the environment, 'result' is the key variable.
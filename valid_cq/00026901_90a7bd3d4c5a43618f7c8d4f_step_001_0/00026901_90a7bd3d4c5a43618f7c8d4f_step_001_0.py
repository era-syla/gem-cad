import cadquery as cq

# Parametric Dimensions
length = 30.0        # Total length of the paperclip
width = 9.0          # Total width of the paperclip
wire_diam = 1.0      # Diameter of the wire

# Derived calculations for wire spacing
# The width spans 4 wire positions (approx), so 3 gaps
# width = 3 * spacing + wire_diam
spacing = (width - wire_diam) / 3.0

# Y coordinates for the 4 wire "tracks" relative to center
# From top (+Y) to bottom (-Y)
y_track_outer_top = 1.5 * spacing
y_track_inner_top = 0.5 * spacing
y_track_inner_bot = -0.5 * spacing
y_track_outer_bot = -1.5 * spacing

# X coordinates for bends and ends
# Aligning the left turn center at x=0
x_left_turn_center = 0.0
x_right_turn_center = length - (width / 2.0)
# The inner loop is slightly shorter than the outer loop
x_right_inner_turn_center = x_right_turn_center - 2.0

# Wire start and end X positions
x_start = x_left_turn_center + (length * 0.35)
x_end = x_left_turn_center + (length * 0.35)

# Generate the wire path
# Topology: Start Inner-Top -> Right -> Turn Down -> Left -> Turn Up -> Right -> Turn Down -> Left -> End Outer-Bottom
path = (
    cq.Workplane("XY")
    .moveTo(x_start, y_track_inner_top)
    .lineTo(x_right_inner_turn_center, y_track_inner_top)
    
    # Turn 1: Inner Right Loop (Inner Top -> Inner Bot)
    .threePointArc(
        (x_right_inner_turn_center + 0.5 * spacing, 0), 
        (x_right_inner_turn_center, y_track_inner_bot)
    )
    
    .lineTo(x_left_turn_center, y_track_inner_bot)
    
    # Turn 2: Left Bridge Loop (Inner Bot -> Outer Top)
    # Connects the bottom inner track to the top outer track
    .threePointArc(
        (x_left_turn_center - spacing, (y_track_inner_bot + y_track_outer_top) / 2.0),
        (x_left_turn_center, y_track_outer_top)
    )
    
    .lineTo(x_right_turn_center, y_track_outer_top)
    
    # Turn 3: Outer Right Loop (Outer Top -> Outer Bot)
    .threePointArc(
        (x_right_turn_center + 1.5 * spacing, 0),
        (x_right_turn_center, y_track_outer_bot)
    )
    
    .lineTo(x_end, y_track_outer_bot)
)

# Create the solid wire by sweeping a circle along the path
result = (
    cq.Workplane("YZ")
    .workplane(offset=x_start)  # Position profile plane at the start of the path
    .moveTo(y_track_inner_top, 0) # Move local profile center to match path start
    .circle(wire_diam / 2.0)
    .sweep(path)
)
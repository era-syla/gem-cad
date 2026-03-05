import cadquery as cq

# Parametric dimensions
thickness = 3.0
handle_length = 20.0
handle_width = 6.0
guard_length = 6.0
guard_total_width = 18.0
blade_length = 65.0
blade_width = 6.0 # Base width of the blade

# Derived parameters
h_offset = handle_width / 2.0
g_offset = guard_total_width / 2.0
b_offset = blade_width / 2.0

# Define X coordinates relative to the guard/blade junction (x=0)
x_handle_start = -(handle_length + guard_length)
x_guard_start = -guard_length
x_blade_start = 0.0
x_notch_start = blade_length * 0.65
x_notch_bottom_start = blade_length * 0.70
x_notch_end = blade_length * 0.85
x_tip = blade_length
x_bottom_taper_start = blade_length * 0.75

# Define Y coordinates (Symmetric around 0 for handle/blade axis)
y_handle_top = h_offset
y_guard_top = g_offset
y_blade_top = b_offset
y_notch_bottom = b_offset * 0.3
y_tip = b_offset * 1.5 # Tip flares up slightly
y_handle_bot = -h_offset
y_guard_bot = -g_offset
y_blade_bot = -b_offset

# Define profile points in counter-clockwise order
points = [
    # Handle Top
    (x_handle_start, y_handle_top),
    (x_guard_start, y_handle_top),
    
    # Guard Top
    (x_guard_start, y_guard_top),
    (x_blade_start, y_guard_top),
    
    # Blade Top Edge
    (x_blade_start, y_blade_top),
    (x_notch_start, y_blade_top),          # Start of top feature
    (x_notch_bottom_start, y_notch_bottom), # Angle down into notch
    (x_notch_end, y_notch_bottom),          # Flat bottom of notch
    (x_tip, y_tip),                         # Angle up to tip point
    
    # Blade Bottom Edge
    (x_bottom_taper_start, y_blade_bot),    # Bottom straight section end
    (x_blade_start, y_blade_bot),
    
    # Guard Bottom
    (x_blade_start, y_guard_bot),
    (x_guard_start, y_guard_bot),
    
    # Handle Bottom
    (x_guard_start, y_handle_bot),
    (x_handle_start, y_handle_bot)
]

# Generate the geometry
result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(thickness)
)
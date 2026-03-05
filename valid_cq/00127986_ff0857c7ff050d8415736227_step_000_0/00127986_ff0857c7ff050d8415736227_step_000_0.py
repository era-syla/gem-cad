import cadquery as cq

# Parametric dimensions for the bars
bar_width = 10.0
bar_height = 10.0
short_len = 80.0
long_len = 180.0

# Spacing parameters
gap_between_bars = 5.0      # Small gap between parallel bars in a pair
gap_between_groups = 20.0   # Larger gap between the short pair and long pair
long_x_offset = 30.0        # Shift of the long bars along the X-axis

# Function to create a positioned bar
def create_bar(length, x, y):
    # Create a box centered at the origin
    # Translate to align the corner to (x, y, 0)
    return (cq.Workplane("XY")
            .box(length, bar_width, bar_height)
            .translate((x + length / 2, y + bar_width / 2, bar_height / 2)))

# --- Construct the geometry ---

# 1. Pair of short bars
# Bar 1 at Y=0
short_bar_1 = create_bar(short_len, 0, 0)

# Bar 2 shifted by width + gap
y_pos_short_2 = bar_width + gap_between_bars
short_bar_2 = create_bar(short_len, 0, y_pos_short_2)

# 2. Pair of long bars
# Determine starting Y position for the long pair (after short pair + group gap)
y_pos_long_1 = y_pos_short_2 + bar_width + gap_between_groups

# Bar 3 (Long) with X offset
long_bar_1 = create_bar(long_len, long_x_offset, y_pos_long_1)

# Bar 4 (Long) shifted by width + gap from Bar 3
y_pos_long_2 = y_pos_long_1 + bar_width + gap_between_bars
long_bar_2 = create_bar(long_len, long_x_offset, y_pos_long_2)

# Combine all independent solids into one result
result = short_bar_1.union(short_bar_2).union(long_bar_1).union(long_bar_2)
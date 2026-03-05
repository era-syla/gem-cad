import cadquery as cq

# Parametric dimensions
width = 10.0      # Width of each bar
height = 10.0     # Height of each bar
length_short = 100.0  # Length of the shorter bars
length_long = 200.0   # Length of the longer bar
gap = 5.0         # Gap between bars

# Create the first short bar (top)
bar1 = cq.Workplane("XY").box(length_short, width, height)

# Create the second short bar (middle), offset in Y
bar2 = cq.Workplane("XY").center(0, width + gap).box(length_short, width, height)

# Create the third long bar (bottom), offset in Y and shifted in X to align ends
# The image shows the right ends are aligned.
# X-coordinate of the center of short bars: 0
# Right end X coordinate: length_short / 2
# We want the right end of the long bar to be at length_short / 2
# Center of long bar needs to be at: (length_short/2) - (length_long/2)
x_offset_long = (length_short / 2) - (length_long / 2)
y_offset_long = - (width + gap)

bar3 = cq.Workplane("XY").center(x_offset_long, y_offset_long).box(length_long, width, height)

# Combine all bars into a single object
# Based on the image, there are three distinct bars parallel to each other.
# We will union them into one compound object for the 'result'.
result = bar1.union(bar2).union(bar3)
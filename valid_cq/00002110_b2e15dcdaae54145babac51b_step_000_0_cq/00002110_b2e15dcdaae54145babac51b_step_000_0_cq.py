import cadquery as cq

# Parametric dimensions
height = 1000.0       # Total height of the assembly
plate_thickness = 5.0 # Thickness of the top and bottom L-plates
leg_width = 20.0      # Width of the L-shape leg (both sides)
leg_length = 100.0    # Length of the L-plate arms
bar_size = 10.0       # Cross-section size of the vertical bars (square)

# 1. Create the L-shaped Plate (Top and Bottom)
# We draw an L-shape on the XY plane and extrude it.
l_plate = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(leg_length, 0)
    .lineTo(leg_length, leg_width)
    .lineTo(leg_width, leg_width)
    .lineTo(leg_width, leg_length)
    .lineTo(0, leg_length)
    .close()
    .extrude(plate_thickness)
)

# 2. Position the Top and Bottom Plates
# Bottom plate sits on Z=0
bottom_plate = l_plate

# Top plate sits at the top of the height. 
# We need to translate it up.
top_plate = l_plate.translate((0, 0, height - plate_thickness))

# 3. Create the Vertical Bars
# Based on the image, there are three bars connecting the corners of the L-shape.
# - One at the outer corner (0,0)
# - One at the end of the X arm
# - One at the end of the Y arm

bar_height = height - (2 * plate_thickness)

# Define a function to create a bar
def create_bar(x, y):
    return (
        cq.Workplane("XY")
        .rect(bar_size, bar_size)
        .extrude(bar_height)
        .translate((x, y, plate_thickness))
    )

# Calculate positions for the bars so they are centered properly within the L-plate geometry
# The L-plate starts at 0,0 and goes positive.
# Corner bar: Needs to be offset by half bar_size to stay inside, or centered on the corner relative to design intent.
# Looking at the image, the bars seem to be inset slightly or flush with the "inner" edge logic.
# Let's assume the bars are centered within the width of the L-shape arms.

offset = leg_width / 2.0  # Center of the "strip" width

# Bar 1: The corner bar (near 0,0)
bar1 = create_bar(offset, offset)

# Bar 2: The end of the X arm
# X position: leg_length - offset
# Y position: offset
bar2 = create_bar(leg_length - offset, offset)

# Bar 3: The end of the Y arm
# X position: offset
# Y position: leg_length - offset
bar3 = create_bar(offset, leg_length - offset)

# 4. Combine everything
result = bottom_plate.union(top_plate).union(bar1).union(bar2).union(bar3)
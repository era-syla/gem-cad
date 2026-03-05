import cadquery as cq

# Parametric dimensions
length = 140.0       # Total length of the frame
width = 80.0         # Total width of the frame
thickness = 8.0      # Thickness (height) of the frame
bar_width = 8.0      # Width of the structural bars
hole_diam = 4.0      # Diameter of the holes
hole_depth = 20.0    # Depth of the holes

# Calculate internal dimensions
# The frame has two identical rectangular cutouts
cutout_length = length - (2 * bar_width)
# Width available for cutouts is total width minus 3 bars (2 sides + 1 center)
cutout_width = (width - (3 * bar_width)) / 2

# Calculate positions
# Distance from center line to the center of the side bars/holes
side_offset = (width - bar_width) / 2
# Distance from center line to the center of the cutouts
cutout_offset = (bar_width + cutout_width) / 2

# Generate the geometry
result = (
    cq.Workplane("XY")
    # 1. Base Plate
    .box(length, width, thickness)
    
    # 2. Cutouts
    .faces(">Z")
    .workplane()
    .pushPoints([
        (0, cutout_offset),   # Top cutout center
        (0, -cutout_offset)   # Bottom cutout center
    ])
    .rect(cutout_length, cutout_width)
    .cutBlind(-thickness)
    
    # 3. Holes on the end face
    .faces("<X")  # Select the front/end face
    .workplane()
    .pushPoints([
        (0, 0),               # Center hole
        (side_offset, 0),     # Left hole
        (-side_offset, 0)     # Right hole
    ])
    .hole(hole_diam, hole_depth)
)
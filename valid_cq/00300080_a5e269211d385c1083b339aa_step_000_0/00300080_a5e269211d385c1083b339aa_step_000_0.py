import cadquery as cq

# Parameters for the plaque dimensions
length = 120.0
width = 70.0
thickness = 6.0

# Parameters for the text
font_size = 9.0
font_depth = 1.0
line_spacing = 16.0
font_name = "Times New Roman"  # Falls back to default if not available

# Create the base rectangular plate
# The box is centered at the origin (0,0,0)
result = cq.Workplane("XY").box(length, width, thickness)

# Helper function to create text solid at specific Y offset
def create_text_line(content, y_offset):
    # Create text geometry with sufficient height for the boolean operation
    # text() creates a solid extruded along Z
    t = cq.Workplane("XY").text(content, font_size, 5.0, font=font_name)
    return t.translate((0, y_offset, 0))

# Generate the three lines of text
# Line 1: Top
t1 = create_text_line("SAM the SHAM", line_spacing)
# Line 2: Center
t2 = create_text_line("&", 0.0)
# Line 3: Bottom
t3 = create_text_line("ALEX the PHALLIX", -line_spacing)

# Combine all text solids into a single workplane object
text_composite = t1.add(t2).add(t3)

# Apply horizontal mirroring to match the provided image
# Mirroring across the YZ plane flips the X coordinates
text_mirrored = text_composite.mirror("YZ")

# Position the text for engraving (cutting)
# The top face of the plate is at Z = thickness / 2
# We move the text solid up so its bottom starts at the desired cut depth below the surface
z_position = (thickness / 2.0) - font_depth
text_final = text_mirrored.translate((0, 0, z_position))

# Cut the mirrored text from the base plate
result = result.cut(text_final)
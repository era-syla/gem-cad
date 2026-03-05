import cadquery as cq

# Parameters for the geometry
shank_diameter = 10.0
shank_length = 30.0
head_diameter = 16.0
head_height = 9.0

# Parameters for the text
text_string = "0Z-8"
text_size = 5.5
text_thickness = 1.2
text_offset_x = 3.0  # Shift text along X-axis to create the overhang effect on the '8'

# Create the CAD model
result = (
    cq.Workplane("XY")
    # 1. Create the shank (bottom cylinder)
    .circle(shank_diameter / 2.0)
    .extrude(shank_length)
    
    # 2. Create the head (top cylinder) on the top face of the shank
    .faces(">Z")
    .workplane()
    .circle(head_diameter / 2.0)
    .extrude(head_height)
    
    # 3. Add the embossed text on the top face of the head
    # We shift the center of the workplane to position the text
    .faces(">Z")
    .workplane()
    .center(text_offset_x, 0)
    .text(text_string, text_size, text_thickness)
)
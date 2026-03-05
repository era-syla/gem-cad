import cadquery as cq
import math

# Parametric dimensions based on a standard M6 Button Head Cap Screw (ISO 7380)
shaft_diameter = 6.0
shaft_length = 18.0
head_diameter = 10.5
head_height = 3.3
hex_across_flats = 4.0
hex_depth = 2.0
bottom_chamfer = 0.4
head_fillet = 2.5

# Calculate the diameter of the circumscribed circle for the hexagon
hex_circum_diameter = 2.0 * hex_across_flats / math.sqrt(3)

# Build the 3D model
result = (
    cq.Workplane("XY")
    # Shaft
    .circle(shaft_diameter / 2.0)
    .extrude(shaft_length)
    
    # Button Head
    .faces(">Z")
    .workplane()
    .circle(head_diameter / 2.0)
    .extrude(head_height)
    
    # Create the dome of the button head
    .edges(">Z")
    .fillet(head_fillet)
    
    # Hexagonal Socket Cut
    .faces(">Z")
    .workplane()
    .polygon(6, hex_circum_diameter)
    .cutBlind(-hex_depth)
    
    # Add a slight chamfer to the bottom of the screw
    .edges("<Z")
    .chamfer(bottom_chamfer)
)
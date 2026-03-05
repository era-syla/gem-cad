import cadquery as cq

# Parametric dimensions based on visual estimation of the provided image
total_length = 100.0      # Total length of the component
head_length = 6.0         # Height of the top cylindrical head
head_diameter = 5.0       # Outer diameter of the head
shaft_diameter = 2.5      # Diameter of the long shaft
hole_diameter = 1.5       # Diameter of the central hole (tube ID)

# Calculate the length of the shaft section
shaft_length = total_length - head_length

# Create the geometry
result = (
    cq.Workplane("XY")
    # 1. Create the main shaft
    .circle(shaft_diameter / 2.0)
    .extrude(shaft_length)
    
    # 2. Create the head on top of the shaft
    .faces(">Z")
    .workplane()
    .circle(head_diameter / 2.0)
    .extrude(head_length)
    
    # 3. Cut the through-hole from the top through the entire length
    .faces(">Z")
    .workplane()
    .circle(hole_diameter / 2.0)
    .cutBlind(-(total_length + 1.0))  # Cut slightly deeper than total length to ensure clear through-hole
)
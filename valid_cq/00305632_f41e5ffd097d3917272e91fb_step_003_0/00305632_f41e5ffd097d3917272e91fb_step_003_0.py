import cadquery as cq
import math

# --- Parameters ---
shaft_diameter = 5.0
shaft_length = 60.0
head_width_flats = 9.0  # Distance across flats of the hex head
head_height = 3.5

# Calculate the circumscribed diameter for the hexagon input in CadQuery
# For a regular hexagon, Width Across Flats = (sqrt(3)/2) * Circumdiameter
head_circum_diameter = head_width_flats / (math.sqrt(3) / 2)

# --- Modeling ---
result = (
    cq.Workplane("XY")
    # 1. Create the Hexagonal Head
    .polygon(6, head_circum_diameter)
    .extrude(head_height)
    
    # 2. Select the bottom face of the head to start the shaft
    .faces("<Z")
    .workplane()
    
    # 3. Create the Cylindrical Shaft
    .circle(shaft_diameter / 2.0)
    .extrude(shaft_length)
    
    # 4. Create the Rounded Tip (Hemispherical end)
    # Select the bottom edge of the shaft
    .edges("<Z")
    # Apply fillet. Using slightly less than radius to avoid geometric singularities
    .fillet((shaft_diameter / 2.0) - 0.01)
)
import cadquery as cq

# Parametric dimensions based on visual estimation
width = 100.0       # Total width of the plate
height = 70.0       # Total height of the plate
thickness = 2.0     # Thickness of the plate
hole_diameter = 6.0 # Diameter of the mounting hole
hole_margin = 8.0   # Distance from the top edge to the center of the hole

# Create the solid geometry
result = (
    cq.Workplane("XY")
    .box(width, height, thickness)
    .faces(">Z")
    .workplane()
    .moveTo(0, (height / 2.0) - hole_margin)
    .hole(hole_diameter)
)
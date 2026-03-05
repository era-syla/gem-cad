import cadquery as cq

# Parametric dimensions
length = 100.0       # Total length of the base
width = 50.0         # Total width of the base
thickness = 4.0      # Thickness of the material (base, walls, rib)
wall_height = 25.0   # Height of the vertical walls above the base
rib_depth = 12.0     # Depth of the central rib below the base

# Generate the CAD model
result = (
    cq.Workplane("XY")
    # 1. Create the main base plate
    .box(length, width, thickness)
    
    # 2. Create the two vertical walls on the short ends (Top side)
    .faces(">Z").workplane()
    .pushPoints([
        (length/2 - thickness/2, 0), 
        (-length/2 + thickness/2, 0)
    ])
    .rect(thickness, width)
    .extrude(wall_height)
    
    # 3. Create the central stiffening rib along the length (Bottom side)
    .faces("<Z").workplane()
    .rect(length, thickness)
    .extrude(rib_depth)
)
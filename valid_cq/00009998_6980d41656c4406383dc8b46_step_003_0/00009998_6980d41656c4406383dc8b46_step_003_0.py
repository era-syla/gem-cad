import cadquery as cq

# Parametric dimensions for the model
base_length = 100.0
base_width = 30.0
base_thickness = 10.0

pillar_diameter = 20.0
pillar_height = 70.0

# Calculate position for the pillar (near one end of the base)
# We offset from the center (0,0) to the left side
pillar_offset_x = -(base_length / 2.0) + (base_width / 2.0)

# Create the CAD model
result = (
    cq.Workplane("XY")
    # 1. Create the rectangular base plate
    .box(base_length, base_width, base_thickness)
    # 2. Select the top face of the base
    .faces(">Z")
    .workplane()
    # 3. Move local origin to the pillar position
    .center(pillar_offset_x, 0)
    # 4. Draw the circular profile
    .circle(pillar_diameter / 2.0)
    # 5. Extrude the circle upwards to form the pillar
    .extrude(pillar_height)
)
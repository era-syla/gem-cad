import cadquery as cq

# Parameters for the cylindrical tube
outer_diameter = 50.0  # External diameter of the tube
wall_thickness = 3.0   # Thickness of the wall
height = 40.0          # Height of the tube

# Calculate inner diameter based on wall thickness
inner_diameter = outer_diameter - (2 * wall_thickness)

# Create the hollow cylinder
# Method: Create a solid cylinder and cut a smaller cylinder from it
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .extrude(height)
    .faces(">Z")
    .workplane()
    .hole(inner_diameter)
)

# Alternative Method (using tube directly if preferred):
# result = cq.Workplane("XY").circle(outer_diameter/2).circle(inner_diameter/2).extrude(height)
import cadquery as cq

# Parameters for dimensions
length = 60.0       # Length of the plate
width = 40.0        # Width of the plate
thickness = 5.0     # Thickness of the plate
corner_radius = 2.0 # Fillet radius for the corners
hole_diameter = 10.0 # Diameter of the central through hole
countersink_diameter = 18.0 # Outer diameter of the countersink
countersink_angle = 90.0 # Angle of the countersink cone

# Create the main rectangular body
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    # Fillet the four vertical edges
    .edges("|Z")
    .fillet(corner_radius)
    # Select the top face to create the hole
    .faces(">Z")
    .workplane()
    # Create a countersunk hole
    .cskHole(diameter=hole_diameter, cskDiameter=countersink_diameter, cskAngle=countersink_angle)
)

# If the image suggests a slight chamfer or fillet on the top/bottom edges as well
# (it looks very clean, possibly just sharp or very slightly deburred, but standard practice):
# result = result.edges("#Z").fillet(0.5) 

# Export or display is handled by the user's environment, but 'result' is the required variable.
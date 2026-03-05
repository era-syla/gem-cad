import cadquery as cq

# Parameters for the twisted blade-like shape
loft_height = 60.0
base_size = 15.0         # Dimensions of the square base
top_width = 45.0         # Width of the top profile
top_thickness = 8.0      # Thickness of the top profile
twist_angle = 60.0       # Rotation angle between base and top

# Create the geometry using a loft operation
result = (
    cq.Workplane("XY")
    # Base profile: A square
    .rect(base_size, base_size)
    # Create a new workplane offset by the height
    .workplane(offset=loft_height)
    # Rotate the local coordinate system to create the twist
    .transformed(rotate=cq.Vector(0, 0, twist_angle))
    # Top profile: A wider, thinner rectangle
    .rect(top_width, top_thickness)
    # Loft between the base and top profiles to create the solid
    .loft(combine=True)
)
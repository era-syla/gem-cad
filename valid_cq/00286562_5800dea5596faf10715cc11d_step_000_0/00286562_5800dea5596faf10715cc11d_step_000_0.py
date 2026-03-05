import cadquery as cq

# Geometric Parameters
disk_diameter = 60.0    # Outer diameter of the disk
thickness = 2.5         # Thickness of the plate
slot_length = 35.0      # End-to-end length of the slots
slot_width = 8.0        # Width of the slots
inner_radius = 2.5      # Fillet radius at the intersection

# Create the X-shaped profile using a Sketch
# 1. Create two crossing rectangles
# 2. Union them to remove internal overlapping edges
# 3. Fillet outer corners to create rounded slot ends
# 4. Fillet inner corners for the smooth transition shown in the image
x_sketch = (
    cq.Sketch()
    .rect(slot_length, slot_width)
    .rect(slot_width, slot_length)
    .clean()  # Boolean union
    # Select outer vertices (the tips of the X) based on distance from center
    .vertices(lambda v: (v.X**2 + v.Y**2) > slot_width**2)
    .fillet(slot_width / 2.0 - 0.01)  # Full round ends
    # Select inner vertices (the corners of the intersection)
    .vertices(lambda v: (v.X**2 + v.Y**2) < slot_width**2)
    .fillet(inner_radius)
)

# Generate the main body
result = (
    cq.Workplane("XY")
    .circle(disk_diameter / 2.0)
    .extrude(thickness)
    .faces(">Z")
    .workplane()
    # Rotate 45 degrees to orient the "+" shape as an "X"
    .transformed(rotate=cq.Vector(0, 0, 45))
    .placeSketch(x_sketch)
    .cutThruAll()
)
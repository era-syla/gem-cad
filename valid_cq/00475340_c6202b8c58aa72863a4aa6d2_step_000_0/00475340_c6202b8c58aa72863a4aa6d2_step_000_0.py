import cadquery as cq

# Model Parameters
disk_diameter = 50.0
disk_thickness = 4.0
slot_width = 8.0

# Derived Dimension
radius = disk_diameter / 2.0

# 1. Create the base disk
# Start on the XY plane, draw a circle of the given radius, and extrude to thickness
base_disk = cq.Workplane("XY").circle(radius).extrude(disk_thickness)

# 2. Create the slot cutter geometry
# We need a rectangular prism to remove material.
# The slot extends from the center (0,0) to the outer edge along the Y-axis.
# We add a small margin to the length to ensure a clean cut through the perimeter.
cut_length = radius + 2.0
cut_center_y = cut_length / 2.0  # Positioning center so the bottom of the rect is at y=0

slot_cutter = (
    cq.Workplane("XY")
    .moveTo(0, cut_center_y)
    .rect(slot_width, cut_length)
    .extrude(disk_thickness)
)

# 3. Combine geometries using a boolean cut operation
result = base_disk.cut(slot_cutter)
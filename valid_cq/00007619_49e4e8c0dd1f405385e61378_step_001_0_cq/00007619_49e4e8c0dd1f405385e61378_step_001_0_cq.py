import cadquery as cq

# --- Parameter Definitions ---
# The image shows a simple flat disk (a short cylinder).
# We will define parametric variables for its diameter and thickness.
disk_diameter = 100.0  # Diameter of the disk
disk_thickness = 5.0   # Thickness (height) of the disk

# --- Geometry Generation ---
# Create a workplane on the XY plane
# Draw a circle with the specified diameter
# Extrude it to the specified thickness
result = (
    cq.Workplane("XY")
    .circle(disk_diameter / 2.0)
    .extrude(disk_thickness)
)

# The variable 'result' now contains the CadQuery solid object.
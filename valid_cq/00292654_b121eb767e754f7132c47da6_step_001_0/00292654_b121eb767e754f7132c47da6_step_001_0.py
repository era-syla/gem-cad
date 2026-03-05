import cadquery as cq

# Parametric Dimensions
total_height = 300.0         # Total height of the pole
shaft_diameter = 8.0         # Diameter of the main vertical shaft
flange_diameter = 24.0       # Diameter of the circular flanges
flange_thickness = 5.0       # Thickness of the flanges
mid_flange_height = 50.0     # Height from bottom to the start of the middle flange
hole_diameter = 4.0          # Diameter of the hole at the top
hole_top_offset = 10.0       # Distance from the top face to the center of the hole

# 1. Create the main shaft
# Extruded from the bottom (XY plane) to the full height
shaft = cq.Workplane("XY").circle(shaft_diameter / 2.0).extrude(total_height)

# 2. Create the bottom base flange
# Located at Z=0
base_flange = cq.Workplane("XY").circle(flange_diameter / 2.0).extrude(flange_thickness)

# 3. Create the middle flange
# Located at a specific height offset from the bottom
mid_flange = (
    cq.Workplane("XY")
    .workplane(offset=mid_flange_height)
    .circle(flange_diameter / 2.0)
    .extrude(flange_thickness)
)

# Union the shaft and flanges into a single solid body
body = shaft.union(base_flange).union(mid_flange)

# 4. Create the through-hole at the top
# Define a cutter cylinder on the XZ plane (perpendicular to the shaft)
# Center it at the correct height and cut through the body
cutter_height = total_height - hole_top_offset
cutter = (
    cq.Workplane("XZ")
    .center(0, cutter_height)
    .circle(hole_diameter / 2.0)
    .extrude(flange_diameter, both=True) # Extrude extensively to ensure a clean through-cut
)

# Apply the cut to generate the final result
result = body.cut(cutter)
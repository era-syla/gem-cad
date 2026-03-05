import cadquery as cq

# ------------------------------------------------------------------------------
# Dimensions and Parameters
# ------------------------------------------------------------------------------
base_width = 70.0      # Circumscribed diameter of the base hexagon
top_width = 30.0       # Circumscribed diameter of the top hexagon
height = 15.0          # Height of the frustum
wall_thickness = 1.5   # Thickness of the shell
hole_diameter = 14.0   # Diameter of the central hole
notch_diameter = 5.0   # Diameter of the small notch
notch_offset = 7.0     # Distance from center to notch center (approx radius of hole)

# ------------------------------------------------------------------------------
# Modeling Steps
# ------------------------------------------------------------------------------

# 1. Create the base Frustum (Hexagonal Pyramid Section)
# We use a loft operation between a hexagon on the XY plane and a smaller one at height Z.
# polygon(6, d) creates a hexagon with vertices aligned with the X-axis.
frustum = (
    cq.Workplane("XY")
    .polygon(6, base_width)
    .workplane(offset=height)
    .polygon(6, top_width)
    .loft()
)

# 2. Create the Cutting Tool (Keyhole Shape)
# We create a solid that represents the volume of the hole and the notch.
# It needs to be taller than the part to ensure a clean cut.
tool_len = height * 3

# Main central hole cutter
cutter_main = (
    cq.Workplane("XY")
    .workplane(offset=-height) # Start below the part
    .circle(hole_diameter / 2.0)
    .extrude(tool_len)
)

# Notch cutter
# Positioned along the X-axis to align with one of the hexagon vertices
cutter_notch = (
    cq.Workplane("XY")
    .workplane(offset=-height)
    .moveTo(notch_offset, 0)
    .circle(notch_diameter / 2.0)
    .extrude(tool_len)
)

# Combine main hole and notch into a single boolean tool
cutter_tool = cutter_main.union(cutter_notch)

# 3. Cut the hole in the frustum
solid_with_hole = frustum.cut(cutter_tool)

# 4. Shell the object
# We select the bottom face (using the selector "<Z") to be removed.
# A negative thickness creates the walls inwards, preserving the outer dimensions.
result = solid_with_hole.faces("<Z").shell(-wall_thickness)

# Export or Render
if 'show_object' in globals():
    show_object(result)
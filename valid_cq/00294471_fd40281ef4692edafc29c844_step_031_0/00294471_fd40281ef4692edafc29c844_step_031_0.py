import cadquery as cq

# -- Parametric Dimensions --
length = 100.0         # Total length of the part
width = 50.0           # Total width of the top plate
plate_thickness = 8.0  # Thickness of the side edges of the top plate
rib_width = 12.0       # Width of the central vertical rib
rib_extension = 10.0   # How far the rib extends below the plate wings
num_teeth = 3          # Number of serrations/scallops on each wing
tooth_depth = 1.5      # Depth of the serration curve (cut into the material)

# -- Derived Dimensions --
# Total height from bottom of rib to top surface
total_height = plate_thickness + rib_extension
# Width of one wing (side section)
wing_width = (width - rib_width) / 2.0
# Width of a single tooth/scallop
tooth_pitch = wing_width / num_teeth

# -- Profile Construction --
# Drawing on the XZ plane to be extruded along Y
# Coordinate System: Z=0 is the bottom of the rib
result_profile = cq.Workplane("XZ").moveTo(-width / 2.0, total_height)

# 1. Top Edge
result_profile = result_profile.lineTo(width / 2.0, total_height)

# 2. Right Vertical Edge
result_profile = result_profile.lineTo(width / 2.0, rib_extension)

# 3. Right Wing Bottom (Scalloped surface moving inwards)
current_x = width / 2.0
for i in range(num_teeth):
    next_x = current_x - tooth_pitch
    mid_x = (current_x + next_x) / 2.0
    # Arc goes up into the material to form a groove
    result_profile = result_profile.threePointArc(
        (mid_x, rib_extension + tooth_depth), 
        (next_x, rib_extension)
    )
    current_x = next_x

# 4. Central Rib Profile
result_profile = result_profile.lineTo(rib_width / 2.0, 0)      # Rib Right Side
result_profile = result_profile.lineTo(-rib_width / 2.0, 0)     # Rib Bottom
result_profile = result_profile.lineTo(-rib_width / 2.0, rib_extension) # Rib Left Side

# 5. Left Wing Bottom (Scalloped surface moving outwards)
current_x = -rib_width / 2.0
for i in range(num_teeth):
    next_x = current_x - tooth_pitch
    mid_x = (current_x + next_x) / 2.0
    result_profile = result_profile.threePointArc(
        (mid_x, rib_extension + tooth_depth), 
        (next_x, rib_extension)
    )
    current_x = next_x

# 6. Close the loop (connects back to start)
result_profile = result_profile.close()

# -- 3D Generation --
result = result_profile.extrude(length)
import cadquery as cq

# Parametric dimensions based on visual proportions
cabinet_height = 140.0
cabinet_width = 70.0
cabinet_depth = 25.0
top_thickness = 4.0
top_overhang = 2.0
leg_height = 8.0
side_wall_thickness = 4.0  # Determines width of the leg cutout

# 1. Create the main body of the cabinet
# Centered on X and Y, sitting on the XY plane (Z=0)
main_body = cq.Workplane("XY").box(
    cabinet_width, 
    cabinet_depth, 
    cabinet_height, 
    centered=(True, True, False)
)

# 2. Create the cutout for the legs/kickplate area
# This is a rectangular subtraction from the bottom center of the main body
cutout_width = cabinet_width - (2 * side_wall_thickness)
cutout_shape = cq.Workplane("XY").box(
    cutout_width, 
    cabinet_depth, 
    leg_height, 
    centered=(True, True, False)
)

body_with_legs = main_body.cut(cutout_shape)

# 3. Create the top panel
# Positioned at the top of the main body (Z = cabinet_height)
# The panel overhangs the main body on all sides
top_width = cabinet_width + (2 * top_overhang)
top_depth = cabinet_depth + (2 * top_overhang)

top_panel = (
    cq.Workplane("XY")
    .workplane(offset=cabinet_height)
    .box(
        top_width, 
        top_depth, 
        top_thickness, 
        centered=(True, True, False)
    )
)

# 4. Combine the body and the top panel into the final result
result = body_with_legs.union(top_panel)
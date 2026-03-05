import cadquery as cq

# Parametric dimensions
width_overall = 120.0  # Overall width of the handle/bracket
depth_overall = 50.0   # How far it sticks out
height = 15.0          # Height of the profile
thickness = 6.0        # Thickness of the material
flange_length = 10.0   # Length of the small mounting tabs
hole_diameter = 4.0    # Diameter of the mounting holes

# Create the main path for the sweep or simple extrusion
# We can model this as a U-shape with flanges.
# Let's use a simple box subtraction method or union of boxes for clarity.

# Center section
center_beam = cq.Workplane("XY").box(width_overall, thickness, height)

# Side arms (depth)
# We position them at the ends of the center beam
left_arm = (
    cq.Workplane("XY")
    .workplane(offset=-width_overall/2 + thickness/2)
    .center(0, depth_overall/2 - thickness/2)
    .box(thickness, depth_overall - thickness, height)
)

right_arm = (
    cq.Workplane("XY")
    .workplane(offset=width_overall/2 - thickness/2)
    .center(0, depth_overall/2 - thickness/2)
    .box(thickness, depth_overall - thickness, height)
)

# Flanges (mounting tabs)
# They extend outwards from the ends of the arms
# The arms end at y = depth_overall - thickness/2 relative to center beam y=0
# Actually, let's rethink coordinates to be simpler. Let's build from a sketch.

# Alternative Approach: 2D Sketch Extrusion
# Looking from top-down (XY plane), the shape is like a U with feet.
#  __
# |  |______________________|  |
# |___|                    |___|
#  ^  ^                    ^  ^
# tab arm                 arm tab

# Let's trace the outer and inner perimeter.
# Or simpler: Union of rectangular blocks.

# 1. Main cross bar
main_bar = cq.Workplane("XY").box(width_overall, thickness, height)

# 2. Side legs
# Position: Z centered on 0 (height/2 to -height/2)
# X: +/- (width_overall/2 - thickness/2)
# Y: Moving "back" or "forward". In the image, the main bar is "front".
# Let's say main bar is at Y=0. Legs go to Y positive.
leg_length = depth_overall - thickness # Length of the leg excluding the main bar thickness overlap
leg_center_y = thickness/2 + leg_length/2
leg_center_x = width_overall/2 - thickness/2

right_leg = cq.Workplane("XY").center(leg_center_x, leg_center_y).box(thickness, leg_length, height)
left_leg = cq.Workplane("XY").center(-leg_center_x, leg_center_y).box(thickness, leg_length, height)

# 3. Mounting Flanges (Tabs)
# They stick out sideways from the end of the legs.
# End of leg is at Y = thickness/2 + leg_length = depth_overall - thickness/2
# Tabs go outwards in X.
tab_y = thickness/2 + leg_length - thickness/2 # Center of the tab in Y (aligning with end of leg)
# Actually, the tab seems to be an extension of the leg's end face but perpendicular?
# Looking at the image:
# - There is a long front face.
# - Two sides go back.
# - At the back, there are tabs going OUTWARDS.

# Correct dimensions calculation:
# Main bar: width=width_overall, depth=thickness
# Legs: depth=depth_overall - thickness
# Tabs: width=flange_length

# Re-assembling with specific coordinates to ensure clean geometry
result = (
    cq.Workplane("XY")
    # Main front bar
    .box(width_overall - 2*thickness, thickness, height) 
    # Move to absolute coordinates for legs to ensure perfect corners
    .union(
        cq.Workplane("XY")
        .center(width_overall/2 - thickness/2, depth_overall/2 - thickness/2)
        .box(thickness, depth_overall, height)
    )
    .union(
        cq.Workplane("XY")
        .center(-(width_overall/2 - thickness/2), depth_overall/2 - thickness/2)
        .box(thickness, depth_overall, height)
    )
    # Flanges going outward at the back
    .union(
        cq.Workplane("XY")
        .center(width_overall/2 + flange_length/2, depth_overall - thickness/2)
        .box(flange_length, thickness, height)
    )
    .union(
        cq.Workplane("XY")
        .center(-(width_overall/2 + flange_length/2), depth_overall - thickness/2)
        .box(flange_length, thickness, height)
    )
)

# Add holes on the flanges
# We select faces on the X axis extremes
# The image shows a hole on the visible left tab. We assume symmetry.

result = (
    result
    .faces(">X")
    .workplane()
    .center(0, 0) # Center on the face
    .hole(hole_diameter)
    .faces("<X")
    .workplane()
    .center(0, 0)
    .hole(hole_diameter)
)
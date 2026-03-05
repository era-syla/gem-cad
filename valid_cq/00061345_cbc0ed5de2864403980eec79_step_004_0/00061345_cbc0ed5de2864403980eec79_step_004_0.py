import cadquery as cq

# -----------------------------------------------------------------------------
# Parameter Definitions
# -----------------------------------------------------------------------------
# Dimensions estimated from the image to recreate the proportions
shaft_diameter = 30.0
shaft_height = 80.0
thread_pitch = 16.0
groove_radius = 6.0  # Radius of the semi-circular cut

# -----------------------------------------------------------------------------
# Geometry Construction
# -----------------------------------------------------------------------------

# 1. Create the base cylindrical shaft
#    We create a cylinder centered on the origin, extruded along the Z-axis.
shaft_radius = shaft_diameter / 2.0
shaft = cq.Workplane("XY").circle(shaft_radius).extrude(shaft_height)

# 2. Create the helical cutter tool
#    To ensure a clean cut through the top and bottom faces of the cylinder,
#    we extend the cutter geometry slightly beyond the shaft's dimensions.
extension = thread_pitch
cutter_height = shaft_height + (2 * extension)

#    Calculate the total rotation angle for the helix based on the height and pitch
num_turns = cutter_height / thread_pitch
rotation_angle = num_turns * 360.0

#    Generate the helical coil solid using twistExtrude.
#    - Start on a workplane offset below the shaft (-extension).
#    - Move the drawing pen to the shaft's radius (moveTo).
#    - Draw the circular profile of the groove.
#    - Extrude upwards while rotating to form the helix.
cutter = (
    cq.Workplane("XY")
    .workplane(offset=-extension)
    .moveTo(shaft_radius, 0)
    .circle(groove_radius)
    .twistExtrude(cutter_height, rotation_angle)
)

# 3. Boolean Operation
#    Subtract the helical cutter from the main shaft to form the groove.
result = shaft.cut(cutter)
import cadquery as cq

# Parametric Dimensions
base_diameter = 12.0
base_height = 3.0
shaft_diameter = 6.0
shaft_height = 10.0  # Height above the base
hole_diameter = 3.0  # Inner bore
slit_width = 1.0     # Width of the cross slits
slit_depth = 4.0     # Depth of the slit from the top
num_instances = 6    # Number of items in the array
spacing = 15.0       # Distance between centers

# 1. Create a single standoff unit
# Start with the base
standoff = cq.Workplane("XY").circle(base_diameter / 2).extrude(base_height)

# Add the shaft on top of the base
standoff = (
    standoff.faces(">Z")
    .workplane()
    .circle(shaft_diameter / 2)
    .extrude(shaft_height)
)

# Create the central hole (through the shaft, partially or fully)
# Assuming a through-hole for typical snap-fit/mounting pins
standoff = (
    standoff.faces(">Z")
    .workplane()
    .hole(hole_diameter, depth=shaft_height + base_height)
)

# Create the cross slits (making it a split pin)
# We create a cutting box and rotate it
slit_cutter = (
    cq.Workplane("XY")
    .rect(slit_width, shaft_diameter * 2) # Make it wide enough to cross the whole shaft
    .extrude(slit_depth)
)

# Position the cutter at the top of the shaft
# The cutter is extruded in Z, so we move it up
top_z = base_height + shaft_height
slit_cutter_translated = slit_cutter.translate((0, 0, top_z - slit_depth))

# Cut the first slit
standoff = standoff.cut(slit_cutter_translated)

# Cut the second slit (rotated 90 degrees)
# Note: The image looks like it might have a single slit or a cross slit. 
# Looking closely at the top of the pins in the image, it appears to be a single slit 
# dividing the top into two halves, not four. 
# Let's stick to a single slit as that matches the visual best.
# If a cross slit were needed, we would just cut again with a rotated cutter.

# 2. Create the linear array
# We will create a list of points for the array centers
points = [(i * spacing, 0, 0) for i in range(num_instances)]

# Use pushPoints to place the generated solid at each location
# Since 'standoff' is a solid, we can union them all together.
result = (
    cq.Workplane("XY")
    .pushPoints(points)
    .eachpoint(lambda loc: standoff.val().moved(loc), combine="a")
)

# If individual objects are preferred over one unioned object, we could leave them separate,
# but 'result' usually expects a single compound object in these prompts.
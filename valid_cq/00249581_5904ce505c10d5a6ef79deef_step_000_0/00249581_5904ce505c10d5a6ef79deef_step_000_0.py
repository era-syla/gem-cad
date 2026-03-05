import cadquery as cq

# Parameters derived from visual estimation
length = 80.0
width = 44.0
height = 14.0
plate_thickness = 4.0
rail_width = 8.0       # Thickness of the side walls
arch_radius = 5.0      # Radius of the cutouts in the legs
arch_spacing = 40.0    # Distance between the two leg cutouts
hole_diameter = 8.0    # Central hole diameter
keyway_width = 3.0     # Width of the keyway slot
keyway_depth = 2.0     # Depth of the keyway into the material from hole edge

# 1. Create the base block
# Positioned so the top face is at Z=0
result = cq.Workplane("XY").workplane(offset=-height/2).box(length, width, height)

# 2. Create the U-channel by removing material from the bottom
# This defines the top plate and the two side rails
cutout_width = width - 2 * rail_width
cutout_height = height - plate_thickness

result = result.faces("<Z").workplane() \
    .rect(length, cutout_width) \
    .cutBlind(cutout_height)

# 3. Cut the arches into the side rails
# Select the side face (+Y) to sketch the cut profile
# The arches are located at the bottom edge of the rails
result = result.faces(">Y").workplane() \
    .center(-arch_spacing / 2.0, -height / 2.0) \
    .circle(arch_radius) \
    .cutThruAll() \
    .center(arch_spacing, 0) \
    .circle(arch_radius) \
    .cutThruAll()

# 4. Create the central hole with a keyway notch
# Select the top face (+Z)
result = result.faces(">Z").workplane() \
    .circle(hole_diameter / 2.0) \
    .cutThruAll()

# Cut the keyway notch (rectangular slot on the hole edge)
# Positioned on the -X side of the hole
result = result.faces(">Z").workplane() \
    .center(-hole_diameter / 2.0, 0) \
    .rect(keyway_depth * 2, keyway_width) \
    .cutThruAll()
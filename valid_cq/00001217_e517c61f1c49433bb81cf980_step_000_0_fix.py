import cadquery as cq

# Dimensions
width = 60      # X direction (depth of part)
height = 70     # Z direction
base_width = 80 # Y direction (width of base)
base_height = 30 # height of rectangular base portion
radius = 25     # radius of the arch top
hole_radius = 12 # radius of the through hole

# Create the profile in XZ plane, then extrude in Y direction
# The shape is: rectangular base + arch top (semicircle)

# Base rectangle bottom: from z=0 to z=base_height
# Arch: semicircle centered at z=base_height, radius=radius

# Build the 2D profile as a closed wire
import math

# The arch center is at x=0, z=base_height
# The arch top goes from (-radius, base_height) up and over to (radius, base_height)
# But we need the overall width to be 'width' in X

# Let's make the profile:
# - Base is width x base_height rectangle
# - Top is a semicircle of radius = width/2

half_w = width / 2
arch_r = half_w  # radius of arch equals half width so it fits perfectly

# Profile points (in XZ plane, extruding along Y)
# Bottom-left -> bottom-right -> up right side -> arch -> down left side -> close

pts = [
    (-half_w, 0),
    (half_w, 0),
    (half_w, base_height),
]

# Build using CadQuery workplane
# Create the profile by drawing lines and an arc

result = (
    cq.Workplane("XZ")
    .moveTo(-half_w, 0)
    .lineTo(half_w, 0)
    .lineTo(half_w, base_height)
    .threePointArc((0, base_height + arch_r), (-half_w, base_height))
    .lineTo(-half_w, 0)
    .close()
    .extrude(base_width)
)

# Move so it's centered in Y
result = result.translate((0, -base_width/2, 0))

# Add the through hole - horizontal hole through the arch in Y direction
# Hole center at x=0, z=base_height (center of arch), going through Y
hole_z = base_height + arch_r * 0.45  # position hole in middle of arch

result = (
    result
    .faces(">Y")
    .workplane()
    .center(0, -(hole_z))
    .circle(hole_radius)
    .cutThruAll()
)

# Re-examine: the hole should be centered at arch center
# Let me redo with proper positioning

import cadquery as cq

half_w = 30.0
base_height = 30.0
arch_r = half_w  # = 30
extrude_depth = 60.0  # Y depth
hole_r = 10.0
hole_center_z = base_height + arch_r * 0.5  # z=45

# Build the profile shape
profile = (
    cq.Workplane("XZ")
    .moveTo(-half_w, 0)
    .lineTo(half_w, 0)
    .lineTo(half_w, base_height)
    .threePointArc((0, base_height + arch_r), (-half_w, base_height))
    .close()
    .extrude(extrude_depth)
)

# Center it along Y
profile = profile.translate((0, -extrude_depth/2, 0))

# Cut the through hole - along Y axis through arch center
result = (
    profile
    .faces(">Y")
    .workplane()
    .transformed(offset=cq.Vector(0, -hole_center_z, 0))
    .circle(hole_r)
    .cutThruAll()
)
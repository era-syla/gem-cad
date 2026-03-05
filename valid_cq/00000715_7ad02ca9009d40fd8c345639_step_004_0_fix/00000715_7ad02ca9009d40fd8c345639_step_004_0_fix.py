import cadquery as cq
import math

# Create a curved arc panel/trim piece
# The shape appears to be a curved flat panel - like an arc segment

# Parameters
length = 200  # total arc length along x
height = 12   # height of the panel
thickness = 3  # thickness

# Create the curved panel using a profile swept along an arc path
# The panel curves upward in the middle (arch shape)

# Arc parameters
arc_width = 200  # span width
arc_rise = 20    # how much it rises in the middle

# Build the shape as a loft or extrusion of an arc profile
# Use a 2D profile and sweep approach

# Create the arc path in the XZ plane (the arch shape viewed from side)
# The panel is thin (Y direction) and arches in Z while spanning X

# Build using a wire for the path
# The arch: starts at (-100, 0, 0), peaks at (0, 0, arc_rise), ends at (100, 0, 0)

# Create the panel cross-section (rectangle in YZ plane)
# Then sweep along the arch path

# Define the arch path points
half_span = 100

# Create path as an arc
# Using three points: start, mid, end
start_pt = (-half_span, 0, 0)
mid_pt = (0, 0, arc_rise)
end_pt = (half_span, 0, 0)

# Build the path wire
path = (
    cq.Workplane("XZ")
    .moveTo(-half_span, 0)
    .threePointArc((0, arc_rise), (half_span, 0))
    .wire()
)

# Create cross section - a thin rectangle (thickness x height)
# The cross-section should be perpendicular to path
profile = (
    cq.Workplane("YZ")
    .rect(thickness, height)
)

# Sweep the profile along the path
result = profile.sweep(path)

# Add small notches/tabs at the ends (visible in image)
# Small rectangular cutouts at bottom of each end

# Get bounding box to position notches
bbox = result.val().BoundingBox()

# Add small tabs visible at ends
notch_w = 3
notch_h = 3
notch_d = thickness + 2

# Left end notch cut
result = (
    result
    .faces(">X")
    .workplane()
    .center(0, -(height/2 - notch_h/2))
    .rect(notch_d, notch_h)
    .cutBlind(-notch_w)
)

result = (
    result
    .faces("<X")
    .workplane()
    .center(0, -(height/2 - notch_h/2))
    .rect(notch_d, notch_h)
    .cutBlind(-notch_w)
)

# Apply slight chamfer to the long edges
try:
    result = result.edges("|Y").chamfer(0.5)
except:
    pass
import cadquery as cq

# -- Parametric Dimensions --
length = 140.0   # Total length of the bench
width = 45.0     # Total width
height = 50.0    # Total height
thickness = 5.0  # Uniform thickness of the material

# -- Modeling Process --

# 1. Create the base solid block
# We create a box centered at the origin.
# Z range is [-height/2, height/2]
base = cq.Workplane("XY").box(length, width, height)

# 2. Create the longitudinal hollow (Rectangular Tube)
# Sketch a rectangle on the end face and cut through the entire length.
# This creates a tube with walls of 'thickness'.
# Hole dimensions are reduced by 2*thickness to keep the outer dimensions constant.
result = (
    base
    .faces(">X")
    .workplane()
    .rect(width - 2 * thickness, height - 2 * thickness)
    .cutThruAll()
)

# 3. Cut out the central section (The "Bridge")
# We remove the bottom and side walls in the middle, leaving the top surface and the end frames.
# Cut Dimensions:
#   Length: Total length minus the thickness of the two legs (one at each end).
#   Width: Wider than the object to ensure side walls are completely removed.
#   Height: Total height minus the top thickness.
cut_len = length - 2 * thickness
cut_wid = width * 1.1 
cut_h = height - thickness

# Calculate the vertical shift for the cutter.
# The cutter needs to be aligned with the bottom of the object (Z = -height/2)
# and extend up to (Z = height/2 - thickness).
# The geometric center of this target volume is at Z = -thickness/2.
cutter = (
    cq.Workplane("XY")
    .box(cut_len, cut_wid, cut_h)
    .translate((0, 0, -thickness / 2))
)

# Subtract the cutter from the tube to finalize the shape
result = result.cut(cutter)
import cadquery as cq

# Parameters used for parametric modeling
length = 60.0    # Total length of the block
width = 50.0     # Total width of the block
height_back = 40.0   # Height at the tall end
height_front = 15.0  # Height at the short end

# V-groove parameters
v_groove_depth = 20.0  # Depth from the top surface
v_groove_angle = 90.0  # Angle of the V (degrees)

# Create the base block shape with the sloped top
# We will create a profile on the side (YZ plane) and extrude it along X (width)
# Coordinates for the side profile:
# (0,0) -> (length, 0) -> (length, height_front) -> (0, height_back) -> close
pts = [
    (0, 0),
    (length, 0),
    (length, height_front),
    (0, height_back)
]

# Create the base solid
base = (
    cq.Workplane("YZ")
    .polyline(pts)
    .close()
    .extrude(width)
)

# To center the extrusion, we might want to move it or just work relative to it.
# The current extrusion puts the shape in +X. Let's center it for easier groove cutting.
base = base.translate((-width / 2.0, 0, 0))

# Create the V-Groove Cutter
# The V-groove runs along the length (Y-axis in our current orientation, 
# but Z in local Workplane terms if we pick a face).
# Since the top surface is sloped, it's actually easier to cut the V-groove 
# relative to the horizontal plane and project it down, or sweep a V-shape.
# However, looking at the image, the V-groove seems to be cut perpendicular 
# to the base, not perpendicular to the slope. The "V" profile is visible 
# on the front and back faces.

# Let's verify the orientation relative to the image.
# If looking at the front face (short height):
# It has a V-notch.
# If looking at the back face (tall height):
# It has a deeper V-notch relative to the bottom, but consistent relative to the top edge if the depth is constant.
# Actually, usually V-blocks have the V cut parallel to the base. 
# Looking at the shading in the image, the V-channel runs "downhill".

# Strategy: 
# 1. Create a V-profile sketch on the Front (or Back) face.
# 2. But wait, the top is sloped. If we just cut a horizontal V, the depth will vary.
#    Looking at the image, the "shoulders" (flat parts next to the V) seem to maintain 
#    a relatively consistent width, or the V-groove depth looks like it follows the slope.
#    Let's assume the V-groove is cut *vertically* down from the top surface, 
#    meaning the bottom of the V is parallel to the top slope.

# Let's try a different approach:
# Create the solid block first.
# Then create a V-shape cutter that is also a wedge, or simply sweep a triangle along the top edge path.

# Alternative (and likely robust) Strategy:
# 1. Create the main block.
# 2. Create a sketch on the XZ plane (front view in standard CAD, but here side view) 
#    that represents the "bottom of the valley" line.
# 3. Use a Sweep or Loft? 
# Simplest Strategy for this specific geometry:
# The top faces look planar. The V-groove faces are planar.
# We can construct this by intersecting a prism with the sloped top, 
# or simpler: Cut a triangular prism that is rotated to match the slope.

# Let's recalculate the slope angle to align the cut.
import math
slope_drop = height_back - height_front
slope_angle = math.degrees(math.atan2(slope_drop, length))

# We will cut a V-shape that runs along the top center.
# We can create a sketch on the back face (tall side) and extrude/cut towards the front.
# But we need the cut to follow the slope.

# Let's define the V-shape on the Back Face (plane at X=0 in our previous setup, 
# but we centered it. The back face is at X=0 in the YZ plane logic, but 
# let's reorient to standard "Front/Right/Top" for clarity).

# Re-orienting for standard "Front View" being the side profile:
# X-axis: Length
# Y-axis: Width
# Z-axis: Height

result = (
    cq.Workplane("XY")
    # Base rectangle
    .box(length, width, 1.0) # Dummy height, we will replace it
)

# Let's build from a side profile on XZ plane and extrude Y
# Side profile points (Length x Height)
p_side = [
    (0, 0),
    (length, 0),
    (length, height_front),
    (0, height_back)
]

base_solid = (
    cq.Workplane("XZ")
    .polyline(p_side)
    .close()
    .extrude(width/2.0, both=True) # Extrude symmetrically along Y
)

# Now we need to cut the V-groove.
# The groove runs along the top slope.
# We define a workplane on the slanted top surface?
# Or we define a V-profile on the Back face (X=0) and sweep it along the top edge?
# Let's try defining the V-profile on the back face and making a "Cut" that follows the slope.

# Find the top edge on the back face (X=0)
# Height is height_back.
# We want a V-shape centered on Y=0 at Z=height_back.

# Calculate width of V at the top based on depth and angle
# tan(angle/2) = (width/2) / depth
# width = 2 * depth * tan(angle/2)
half_width_v = v_groove_depth * math.tan(math.radians(v_groove_angle / 2.0))

# Create a triangular cutter
# It needs to be long enough to cover the whole slope.
# Length of slope = sqrt(length^2 + (h_back - h_front)^2)
slope_length = math.sqrt(length**2 + (height_back - height_front)**2)
cutter_length = slope_length * 1.2 # Oversize it slightly

# We will construct the cutter at the origin then rotate and move it
cutter = (
    cq.Workplane("YZ")
    .moveTo(0, 0)
    .lineTo(half_width_v, v_groove_depth)
    .lineTo(-half_width_v, v_groove_depth)
    .close()
    .extrude(cutter_length)
)

# The cutter is currently pointing UP (positive Z for the flat part), extruded in X.
# We need to rotate it so the point faces DOWN (-Z generally) 
# and the extrusion aligns with the slope.

# 1. Rotate 180 around X to point V down.
cutter = cutter.rotate((0,0,0), (1,0,0), 180)

# 2. Rotate around Y to match the slope.
# The slope goes down from X=0 to X=length.
# The angle is 'slope_angle' calculated earlier.
cutter = cutter.rotate((0,0,0), (0,1,0), -slope_angle)

# 3. Position the cutter.
# The point of the V (before rotation) was at (0,0).
# We want this point to start at the top-back edge: (0, 0, height_back).
# Because we extruded in +X initially (before rotation), the start face is at X=0.
# We need to be careful about the pivot point of rotation.
# The previous rotations were around (0,0,0).
# So the tip is still at (0,0,0).
# We move it to (0, 0, height_back).
cutter = cutter.translate((0, 0, height_back))

# Perform the cut
result = base_solid.cut(cutter)

# Export or Render helper (not strictly required by prompt but good practice)
# result.export("v_block.step")
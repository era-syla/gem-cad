import cadquery as cq

# Parametric dimensions
width = 50.0       # Width of the square base
length = 50.0      # Length of the square base
base_height = 10.0 # Height of the vertical base section
pyramid_height = 15.0 # Height of the pyramidal top section

# Create the base box
# We extrude a square to create the base prism
base = cq.Workplane("XY").box(width, length, base_height)

# Create the top pyramid
# We can create a pyramid by creating a rectangle on top of the base
# and lofting it to a point, or simpler: create a wedge/pyramid primitive.
# However, a robust way in CadQuery for a square pyramid is to extrude a rectangle with a taper,
# or to loft two sketches. Let's use the loft approach for clarity or a simple wedge.
# Since it is a regular pyramid on top of a box, we can also think of it as a loft 
# from the top face of the box to a center point.

# Method: Loft from the top face to a point
# 1. Select top face of the base
# 2. Draw the base rectangle (implied by face)
# 3. Offset workplane for the tip
# 4. Draw a very small rectangle or point (CadQuery lofts usually require similar topology, 
#    so a tiny rectangle is safer than a point, but let's try a ruled surface or just constructing the geometry differently).

# Alternative Method: Extrude with Taper (Draft)
# If we extrude the top face with a draft angle, it forms a pyramid.
# We need to calculate the draft angle. 
# tan(angle) = (width / 2) / pyramid_height
# But this only works if width == length. The image looks square.
# Let's stick to a constructive approach that is guaranteed to work:
# Create the base. Create a pyramid on top. Union them.

# Creating a pyramid from scratch:
# 1. Draw square on a plane at Z = base_height/2 (top of the centered box)
# 2. Extrude to a point? No, standard extrude is linear.
# 3. Use `rect` and `extrude(taper=...)`.
#    If we want a specific height, `taper` needs an angle.
#    Angle calculation: alpha = atan((width/2)/height) in degrees.
#    Wait, `extrude(taper=...)` is tricky with exact meeting at a point.

# Best Method: Lofting
# Workplane at top of base -> Rectangle
# Workplane at top of pyramid -> Point (or tiny rectangle) -> Loft

# Let's adjust coordinate system so Z=0 is bottom.
# Base goes from Z=0 to Z=base_height.
result = (
    cq.Workplane("XY")
    .box(width, length, base_height, centered=(True, True, False)) # Base box, Z 0 to base_height
    .faces(">Z").workplane()  # Workplane on top of the box
    .rect(width, length)      # Draw rectangle matching the top
    .workplane(offset=pyramid_height) # Move up by pyramid height
    .rect(0.001, 0.001)       # Draw a tiny rectangle (effectively a point)
    .loft(combine=True)       # Loft from base rect to tip rect
)

# Note: Using a tiny rectangle instead of a point is a common trick in CAD kernels 
# to ensure loft stability, as lofting to a singular point can sometimes cause issues 
# depending on the kernel version.

# Export or visualization handling is done by the caller, we just return 'result'
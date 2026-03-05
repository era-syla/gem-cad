import cadquery as cq

# --- Parameters ---
# Dimensions based on standard Robotics C-Channel (1x2x1 configuration)
pitch = 0.5           # Distance between hole centers (inches)
hole_size = 0.182     # Side length of square holes (inches)
thickness = 0.046     # Material thickness (inches)
length_holes = 35     # Length of channel in hole units
web_holes = 2         # Height of the web in hole units
flange_holes = 1      # Width of the flange in hole units

# Derived dimensions
total_length = length_holes * pitch
web_height = web_holes * pitch       # 1.0 inch
flange_width = flange_holes * pitch  # 0.5 inch

# --- Modeling ---

# 1. Create the C-Channel Profile
# Drawn on YZ plane, Web along Y, Flanges along Z, Extruded along X
profile = (
    cq.Workplane("YZ")
    .moveTo(0, 0)
    .lineTo(0, web_height)                         # Outer Web
    .lineTo(flange_width, web_height)              # Outer Top Flange
    .lineTo(flange_width, web_height - thickness)  # Inner Top Flange Tip
    .lineTo(thickness, web_height - thickness)     # Inner Top Corner
    .lineTo(thickness, thickness)                  # Inner Bottom Corner
    .lineTo(flange_width, thickness)               # Inner Bottom Flange Tip
    .lineTo(flange_width, 0)                       # Outer Bottom Flange
    .close()
)

# Extrude to create the base solid
channel = profile.extrude(total_length)

# 2. Cut Holes in the Web (Side Face)
# Select the back face of the web (at Z=0 in local profile coords)
# We use cutThruAll to punch through the web thickness
channel_with_web_holes = (
    channel.faces("<Z")
    .workplane(centerOption="CenterOfBoundBox")
    .rarray(
        xSpacing=pitch,
        ySpacing=pitch,
        xCount=length_holes,
        yCount=web_holes,
        center=True
    )
    .rect(hole_size, hole_size)
    .cutThruAll()
)

# 3. Cut Holes in the Flanges (Top and Bottom Faces)
# Select the top outer face. Cutting through all will pierce both the top
# and bottom flanges due to vertical alignment.
result = (
    channel_with_web_holes.faces(">Y")
    .workplane(centerOption="CenterOfBoundBox")
    .rarray(
        xSpacing=pitch,
        ySpacing=pitch,
        xCount=length_holes,
        yCount=flange_holes,
        center=True
    )
    .rect(hole_size, hole_size)
    .cutThruAll()
)
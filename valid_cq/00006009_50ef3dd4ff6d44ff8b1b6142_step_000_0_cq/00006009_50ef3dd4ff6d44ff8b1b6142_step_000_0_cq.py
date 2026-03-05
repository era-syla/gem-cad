import cadquery as cq

# Parametric dimensions
length = 200.0       # Total length of the part
width = 20.0         # Width of the top/bottom flanges
thickness_top = 2.0  # Thickness of the top flange
thickness_bot = 4.0  # Thickness of the bottom flange
gap = 4.0            # Gap between the flanges
web_thickness = 2.0  # Thickness of the connecting web
web_inset = 5.0      # How far the web is set back from the edge (if it's a C-channel)
                     # Looking at the image, it looks like a C-channel or U-profile on its side.
                     # Let's assume a C-channel shape where the web connects the two flanges at the back.

# More precise interpretation:
# It looks like a long rail. There are two horizontal flat sections parallel to each other.
# They are connected by a vertical section.
# The top section is thinner than the bottom section.
# There seem to be small holes or divots along the bottom section's top face, inside the channel.

# Revised Parameters
length = 300.0
base_width = 15.0
base_height = 5.0
top_width = 15.0
top_height = 2.0
web_width = 2.0
web_height = 4.0 # The gap distance

# Create the profile sketch
# We will draw the cross-section on the YZ plane and extrude along X.
# Origin at the bottom-left corner of the cross-section.

# Points for a C-channel like shape:
# (0,0) -> (base_width, 0) -> (base_width, base_height) -> (web_width, base_height) 
# -> (web_width, base_height + web_height) -> (top_width, base_height + web_height)
# -> (top_width, base_height + web_height + top_height) -> (0, base_height + web_height + top_height)
# -> close

# Let's adjust based on visual proportions:
# The "web" seems to be at the back.
# The bottom block is thicker.
# The top plate is thinner.
# There are holes drilled through the bottom block.

# Final set of parameters for the model
L = 250.0  # Length
W = 20.0   # Width of the strip
H_base = 6.0 # Height of the bottom block
H_gap = 4.0  # Height of the gap
H_top = 2.0  # Height of the top plate
Web_T = 2.0  # Thickness of the connecting wall (at the back)

# Holes
hole_spacing = 40.0
hole_diameter = 2.5
num_holes = 5

# Start building
# Draw cross-section on YZ plane
# (0,0) is bottom-rear corner
# Z is up, Y is forward (width), X is length

# Profile points (Y, Z)
pts = [
    (0, 0),                       # Bottom-rear
    (W, 0),                       # Bottom-front
    (W, H_base),                  # Top of base-front
    (Web_T, H_base),              # Top of base, start of web
    (Web_T, H_base + H_gap),      # Bottom of top plate, end of web
    (W, H_base + H_gap),          # Bottom of top plate-front
    (W, H_base + H_gap + H_top),  # Top of top plate-front
    (0, H_base + H_gap + H_top),  # Top of top plate-rear
    (0, 0)                        # Close
]

# Create the extrusion
profile = cq.Workplane("YZ").polyline(pts).close().extrude(L)

# Add holes
# The holes appear to be in the gap area, likely going through the base part or the web.
# Looking closely at the image, there are small black dots on the top surface of the bottom flange, inside the channel.
# These look like tapped holes or counterbores. Let's assume simple holes through the base.
# Location: Centered in the open area of the base flange? 
# The open area width is W - Web_T. 
# Center Y would be Web_T + (W - Web_T)/2.
# Z level for sketch: on top of the base flange (Z = H_base).

center_y = Web_T + (W - Web_T) / 2
hole_start_x = L / 2 - ( (num_holes - 1) * hole_spacing ) / 2

# Create points for the holes
hole_locs = [(hole_start_x + i * hole_spacing, center_y) for i in range(num_holes)]

# Cut holes. Since the workplane will be defined relative to the object, we need to orient correctly.
# We want to drill down into the base (-Z direction).
# Face selection: The top face of the bottom flange is tricky to select by string selector because there are multiple horizontal faces.
# Let's use coordinates. Workplane on XY plane offset by H_base.

result = (
    profile
    .faces(">Z[1]") # Select the top face of the bottom flange (index 1 might be needed if index 0 is top of top flange or vice versa)
    # Actually, let's just define a workplane explicitly to be safe
    .workplane(centerOption="CenterOfBoundBox")
    .transformed(offset=cq.Vector(0, 0, -H_gap/2 - H_top)) # This is getting messy with relative selections
)

# Cleaner approach for holes:
# Define a workplane at Z = H_base
result = profile.faces(cq.NearestToPointSelector((L/2, W/2, H_base))).workplane()

# Use pushPoints to place holes. Note: X axis of profile is X axis of workplane.
# The face selector puts the origin somewhere. It's safer to use absolute coordinates on a fresh workplane.
result = profile.workplane(offset=H_base).pushPoints(hole_locs).hole(hole_diameter)

# Refine hole placement to match image
# The holes look evenly spaced along the length.
# The solid is aligned along +X.
hole_locs = []
for i in range(5):
    # Distribute 5 holes along the length
    # Padding from ends
    x_pos = L * (i + 1) / 6.0 
    y_pos = - (W/2 + Web_T/2) # This depends on where the origin is after extrusion. 
                              # Extruding a YZ sketch creates a shape where Y is "width".
                              # The standard workplane usually has X aligned with global X.

# Let's restart the construction to ensure coordinate clarity.
# X: Length
# Y: Width
# Z: Height

result = (
    cq.Workplane("YZ")
    .polyline(pts)
    .close()
    .extrude(L)
)

# Now define holes
# We want holes on the surface at Z = H_base.
# The holes are centered in the channel width-wise.
# Channel open width starts at Y=Web_T and ends at Y=W. Center is (W+Web_T)/2.

hole_y = (W + Web_T) / 2
hole_xs = [L * (i + 1) / 6.0 for i in range(5)] # 5 holes distributed
hole_pts = [(x, hole_y) for x in hole_xs]

# Cut the holes
# We select the face at Z=H_base.
# Since we drew on YZ and extruded X, the default XY workplane is at Z=0.
# We create a workplane at Z=H_base.
result = result.faces(cq.NearestToPointSelector((L/2, hole_y, H_base))).workplane(centerOption="ProjectedOrigin").pushPoints(hole_pts).hole(hole_diameter)

# This looks complete based on the prompt.
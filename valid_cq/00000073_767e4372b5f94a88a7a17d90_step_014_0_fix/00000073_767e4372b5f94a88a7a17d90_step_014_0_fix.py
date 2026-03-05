import cadquery as cq

# Dimensions based on image analysis
# A rectangular box/enclosure with an open front face and a channel/slot on the left side

length = 80  # depth (front to back)
width = 40   # height
depth = 60   # width (left to right)

wall = 3     # wall thickness

# Create the outer box
outer = cq.Workplane("XY").box(length, depth, width)

# Create the inner cutout (open on the front face - along X axis)
# The box is hollow inside, open on the front
inner_length = length - wall  # keep back wall
inner_width = depth - 2 * wall
inner_height = width - wall   # keep top, open bottom? 

# Looking at image: box is open on front face, has walls on back, top, and sides
# with a flange/channel on the left side

# Build as shell with open front
# Start with solid box
base = cq.Workplane("XY").box(length, depth, width)

# Cut the interior - open from front (negative X direction)
# Interior cut leaves back wall, two side walls, top wall, bottom wall but open front
interior = (cq.Workplane("XY")
    .center(wall/2, 0)  # shift so we leave back wall
    .box(length - wall, depth - 2*wall, width - wall)
    .translate((wall/2, 0, wall/2))
)

result = base.cut(interior)

# Now add the left side flange/channel feature
# On the left face there appears to be a protruding frame/channel
flange_thickness = 2
flange_depth = 5

# Left face is at y = -depth/2
# Add a U-channel frame on the left face
left_x = -length/2
right_x = length/2 - wall

# Create a frame on the front-left edge
# The flange appears as a rectangular frame protruding from the left side
frame_outer = (cq.Workplane("YZ")
    .workplane(offset=-length/2 - flange_depth)
    .rect(depth + flange_depth*2, width + flange_depth)
    .extrude(flange_depth)
)

frame_inner = (cq.Workplane("YZ")
    .workplane(offset=-length/2 - flange_depth)
    .rect(depth - 2*wall, width - wall)
    .extrude(flange_depth + 1)
)

# Simpler approach: just create the main enclosure shell
# Main box shell
result = (cq.Workplane("XY")
    .box(length, depth, width)
)

# Cut interior cavity (open front)
cavity = (cq.Workplane("XY")
    .box(length - wall, depth - 2*wall, width - wall)
)
# Move cavity to leave back wall and align top/bottom
cavity = cavity.translate((-wall/2, 0, wall/2))

result = result.cut(cavity)

# Add front flange frame on the front face
# Front face at x = -length/2
flange_w = 4
flange_h = 4

front_frame = (cq.Workplane("YZ")
    .workplane(offset=length/2)
    .rect(depth + 2*flange_w, width + flange_h)
    .extrude(flange_w)
)

front_frame_cut = (cq.Workplane("YZ")
    .workplane(offset=length/2)
    .rect(depth - 2*wall, width - wall)
    .extrude(flange_w + 1)
)

front_frame = front_frame.cut(front_frame_cut)

result = result.union(front_frame)
import cadquery as cq

# Main frame dimensions
frame_width = 80
frame_height = 50
frame_depth = 50
wall_thickness = 5

# Build the main rectangular frame (open box - like a picture frame extruded)
outer = (
    cq.Workplane("XY")
    .rect(frame_width, frame_depth)
    .extrude(frame_height)
)

inner = (
    cq.Workplane("XY")
    .rect(frame_width - 2*wall_thickness, frame_depth - 2*wall_thickness)
    .extrude(frame_height - wall_thickness)
)

frame = outer.cut(inner)

# Add top plate (cap on top)
top_plate = (
    cq.Workplane("XY")
    .workplane(offset=frame_height)
    .rect(frame_width, frame_depth)
    .extrude(wall_thickness)
)

# Actually let's rebuild this as a U-channel open on one side (front open)
# Looking at the image: it's a rectangular frame open in the front/back
# with a top bar, bottom bar, left side and right side

# Rebuild from scratch as proper frame
result = (
    cq.Workplane("XY")
    .rect(frame_width, frame_depth)
    .extrude(frame_height)
)

# Cut the inner rectangle to make it hollow (open front and back)
result = result.faces(">X").workplane().rect(frame_depth - 2*wall_thickness, frame_height - 2*wall_thickness).cutThruAll()

# Now add the left arm extending out
left_arm = (
    cq.Workplane("XY")
    .workplane(offset=frame_height/2 - wall_thickness/2)
    .center(-frame_width/2, 0)
    .rect(30, wall_thickness)
    .extrude(wall_thickness)
)

# Let me restart with a clearer approach
# The object appears to be: rectangular frame/bracket with a cylindrical clamp on top-right
# and a rod/pin on the left side

# Base frame - rectangular hollow box open on two sides
w, h, d = 80, 45, 55
t = 5  # wall thickness

# Create outer box
outer_box = cq.Workplane("XY").box(w, d, h)

# Cut inner opening (open on front and back faces in Y direction)
inner_cut = cq.Workplane("XY").box(w - 2*t, d + 10, h - 2*t)
frame = outer_box.cut(inner_cut)

# Add left horizontal arm
left_arm = (
    cq.Workplane("YZ")
    .center(0, 0)
    .workplane(offset=-w/2 - 20)
    .rect(d, h)
    .extrude(20)
)
frame = frame.union(
    cq.Workplane("XY")
    .workplane(offset=-h/2 + t/2)
    .center(-w/2 - 10, 0)
    .box(20, t, t)
)

# Left pin/rod
left_pin = (
    cq.Workplane("YZ")
    .center(0, -h/2 + t/2)
    .circle(4)
    .extrude(15)
    .translate((-w/2 - 10, 0, 0))
)

# Cylindrical clamp on top
clamp_body = (
    cq.Workplane("XY")
    .workplane(offset=h/2)
    .center(w/4, -d/4)
    .cylinder(15, 10)
)

clamp_hole = (
    cq.Workplane("XY")
    .workplane(offset=h/2)
    .center(w/4, -d/4)
    .circle(6)
    .extrude(20)
)

clamp = clamp_body.cut(clamp_hole)

# Clamp slot
clamp_slot = (
    cq.Workplane("YZ")
    .center(-d/4, h/2 + 7)
    .rect(3, 15)
    .extrude(5)
    .translate((w/4, 0, 0))
)

clamp = clamp.cut(clamp_slot)

# Combine everything
result = frame.union(left_pin).union(clamp)

# Small screws/holes on the side
result = (
    result
    .faces(">Y")
    .workplane()
    .pushPoints([(w/4, 0), (-w/4, 0)])
    .hole(3, 4)
)
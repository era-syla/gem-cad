import cadquery as cq

# --- Dimensions and Parameters ---
length = 600.0
height = 60.0
width = 30.0
wall_thickness = 3.0

# Feature Dimensions
slot_len = 70.0
slot_wid = 20.0
large_hole_dia = 22.0
small_hole_dia = 3.5
pin_dia = 5.0
bracket_protrusion = 10.0

# --- 1. Base Geometry: Hollow Rectangular Tube ---
# Create a solid box and shell the X faces (ends) to create the hollow tube
base = (cq.Workplane("XY")
        .box(length, height, width)
        .faces("|X")
        .shell(-wall_thickness))

# --- 2. Top Face Features (Slots and Mounting Holes) ---
# Define positions relative to center
slot_positions_x = [-220, -110, 110, 220]
hole_group_centers_x = [-265, -165, -55, 55, 165, 265]
hole_group_spacing = 16.0

# Generate points for 2x2 hole clusters
top_hole_pts = []
for cx in hole_group_centers_x:
    hs = hole_group_spacing / 2.0
    top_hole_pts.extend([
        (cx - hs, -hs), (cx + hs, -hs),
        (cx - hs, hs), (cx + hs, hs)
    ])

# Select Top Face and Cut
top_workplane = base.faces(">Z").workplane()

# Cut Rectangular Slots
base = (top_workplane
        .pushPoints([(x, 0) for x in slot_positions_x])
        .rect(slot_len, slot_wid)
        .cutBlind(-wall_thickness * 2))

# Cut Small Pattern Holes
base = (base.faces(">Z").workplane()
        .pushPoints(top_hole_pts)
        .circle(small_hole_dia / 2.0)
        .cutBlind(-wall_thickness * 2))

# --- 3. Front Face Features (Large Holes and Mounting Pattern) ---
large_hole_centers_x = [-240, -180, -120, -60, 60, 120, 180, 240]
mount_offset = 18.0

# Generate mounting holes around large holes
front_mount_pts = []
for lx in large_hole_centers_x:
    front_mount_pts.extend([
        (lx - mount_offset, -mount_offset), 
        (lx + mount_offset, -mount_offset),
        (lx - mount_offset, mount_offset), 
        (lx + mount_offset, mount_offset)
    ])

# Add extra mounting holes near center for mechanism bracket
front_mount_pts.extend([(-15, 15), (-15, -15), (15, 15), (15, -15)])

# Select Front Face and Cut
front_workplane = base.faces(">Y").workplane()

# Cut Large Holes
base = (front_workplane
        .pushPoints([(x, 0) for x in large_hole_centers_x])
        .circle(large_hole_dia / 2.0)
        .cutBlind(-wall_thickness * 2))

# Cut Small Mounting Holes
base = (base.faces(">Y").workplane()
        .pushPoints(front_mount_pts)
        .circle(small_hole_dia / 2.0)
        .cutBlind(-wall_thickness * 2))

# --- 4. Center Pin Mechanism ---
# Dimensions
bracket_w = 15.0
bracket_h = 12.0
bracket_gap = 15.0
pin_axis_y = width/2.0 + bracket_protrusion/2.0

# Create Mounting Brackets (Lugs) on Front Face
lugs = (base.faces(">Y").workplane()
        .pushPoints([(0, bracket_gap/2.0 + bracket_h/2.0), 
                     (0, -(bracket_gap/2.0 + bracket_h/2.0))])
        .rect(bracket_w, bracket_h)
        .extrude(bracket_protrusion))

# Combine lugs with base
result = base.union(lugs)

# Cut vertical hole for the pin through the lugs
# Create a cutter cylinder
pin_hole_cutter = (cq.Workplane("XY")
                   .circle(pin_dia/2.0 + 0.5) # Clearance
                   .extrude(height + 20)
                   .translate((0, pin_axis_y, -height/2.0 - 10)))

result = result.cut(pin_hole_cutter)

# Create the Pin
pin_len = 90.0
pin = (cq.Workplane("XY")
       .circle(pin_dia / 2.0)
       .extrude(pin_len)
       .translate((0, pin_axis_y, -pin_len/2.0 - 15))) # Shift down

# Create Pin Handle (Horizontal bar)
handle_len = 25.0
handle = (cq.Workplane("YZ") # Creates cylinder along X
          .circle(2.5 / 2.0)
          .extrude(handle_len)
          .translate((-handle_len/2.0, pin_axis_y, 10)))

# Final Union
result = result.union(pin).union(handle)
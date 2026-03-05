import cadquery as cq

# Main flat bar/strap with slotted holes and center hub
# Overall dimensions: long flat bar ~160mm x 20mm x 4mm
# Center hub is raised in the middle

L = 160  # total length
W = 20   # width
T = 4    # thickness

# Slot dimensions
slot_w = 6
slot_l = 25
slot_offset = 45  # distance from center to slot center

# Center hub dimensions
hub_w = 24
hub_l = 30
hub_h = 8

# Build the base flat bar
base = (
    cq.Workplane("XY")
    .rect(L, W)
    .extrude(T)
)

# Add the center hub on top
hub = (
    cq.Workplane("XY")
    .workplane(offset=T)
    .rect(hub_l, hub_w)
    .extrude(hub_h)
)

result = base.union(hub)

# Cut slots in the flat bar - left slot
result = (
    result
    .workplane(offset=0)
    .center(-slot_offset, 0)
    .slot2D(slot_l, slot_w, 0)
    .cutThruAll()
)

# Cut slots in the flat bar - right slot
result = (
    result
    .workplane(offset=0)
    .center(slot_offset, 0)
    .slot2D(slot_l, slot_w, 0)
    .cutThruAll()
)

# Add a small notch/groove on the center hub sides (the waist/narrowing in center)
# Cut a narrowing groove from front and back of center hub
groove_depth = 4
groove_w = 6
groove_h = hub_h + T

# Front groove
result = (
    result
    .workplane(offset=0)
    .center(0, hub_w/2 - groove_depth/2)
    .rect(groove_w, groove_depth)
    .cutBlind(-(hub_h + T))
)

# Back groove  
result = (
    result
    .workplane(offset=0)
    .center(0, -(hub_w/2 - groove_depth/2))
    .rect(groove_w, groove_depth)
    .cutBlind(-(hub_h + T))
)

# Add small side walls/fins on center block
fin_h = hub_h + T
fin_t = 3
fin_l = hub_l

fin_left = (
    cq.Workplane("XY")
    .center(0, (hub_w/2 + fin_t/2))
    .rect(fin_l, fin_t)
    .extrude(fin_h)
)

fin_right = (
    cq.Workplane("XY")
    .center(0, -(hub_w/2 + fin_t/2))
    .rect(fin_l, fin_t)
    .extrude(fin_h)
)

result = result.union(fin_left).union(fin_right)

# Apply chamfers to the ends of the bar for the tapered look
# Select edges at the ends
result = (
    result
    .edges("|Z")
    .edges(cq.selectors.BoxSelector((-L/2-1, -W/2-1, -1), (-L/2+15, W/2+1, T+1)))
    .chamfer(1.5)
)
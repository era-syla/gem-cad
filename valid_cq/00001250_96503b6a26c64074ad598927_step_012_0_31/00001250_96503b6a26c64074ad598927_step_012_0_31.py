import cadquery as cq

# Overall dimensions and parameters
T = 1.5          # Base plate thickness
feat_H = 1.5     # Height of raised features
hole_depth = 10  # Depth for through-all cuts

# 1. Create the main base plate with an irregular polygon shape
pts = [
    (-75, 17.5),
    (60, 17.5),
    (75, 2.5),
    (75, -17.5),
    (-75, -17.5)
]
base_sketch = cq.Sketch().polygon(pts).vertices().fillet(3)
base = cq.Workplane("XY").placeSketch(base_sketch).extrude(T)

# 2. Add mounting tabs along the top and bottom edges
tabs_locs = [
    (-70, 17.5), (-25, 17.5), (15, 17.5), (55, 17.5),
    (-70, -17.5), (-10, -17.5), (35, -17.5), (70, -17.5)
]

for x, y in tabs_locs:
    tab = cq.Workplane("XY").center(x, y).circle(3.5).extrude(T)
    base = base.union(tab)

# Create a reference plane at the top surface of the base plate
top_ref = cq.Workplane("XY").workplane(offset=T)

# 3. Add raised solid features
# Circular boss
boss = top_ref.center(-25, 8).circle(6).extrude(feat_H)
base = base.union(boss)

# U-Shape block (will be hollowed out later)
u_sketch = cq.Sketch().rect(8, 10).vertices().fillet(2)
u_shape = top_ref.center(-1, 3).placeSketch(u_sketch).extrude(feat_H)
base = base.union(u_shape)

# Small rectangular slot feature block on the right
slot_sketch = cq.Sketch().rect(10, 6).vertices().fillet(2)
slot = top_ref.center(65, 0).placeSketch(slot_sketch).extrude(feat_H)
base = base.union(slot)

# Diagonal channel rib
angle_deg = -15
wp_ribs = top_ref.center(-35, 5).transformed(rotate=(0, 0, angle_deg))
rib_sketch = cq.Sketch().rect(70, 5).vertices().fillet(2.4)
rib = wp_ribs.placeSketch(rib_sketch).extrude(feat_H)
base = base.union(rib)

# 4. Perform partial-depth cuts on the raised features
# Reference plane at the top of the raised features
cut_plane = cq.Workplane("XY").workplane(offset=T + feat_H)

# Shallow groove in the diagonal rib
wp_groove = cut_plane.center(-35, 5).transformed(rotate=(0, 0, angle_deg))
groove_sketch = cq.Sketch().rect(68, 2.5).vertices().fillet(1.2)
base = base.cut(wp_groove.placeSketch(groove_sketch).extrude(-1.0))

# Open the inside of the U-shape (creates a C-shape opening to the right)
u_cut_sketch = cq.Sketch().rect(8, 6).vertices().fillet(1)
base = base.cut(cut_plane.center(2, 3).placeSketch(u_cut_sketch).extrude(-feat_H))

# 5. Perform through-all cuts
# Reference plane well above the part
holes_plane = cq.Workplane("XY").workplane(offset=T + 5)

# Cut slot through hole
slot_cut_sketch = cq.Sketch().rect(6, 3).vertices().fillet(1)
base = base.cut(holes_plane.center(65, 0).placeSketch(slot_cut_sketch).extrude(-hole_depth))

# Cut small holes in the mounting tabs
for x, y in tabs_locs:
    base = base.cut(holes_plane.center(x, y).circle(1.5).extrude(-hole_depth))

# Cut central hole through the boss
base = base.cut(holes_plane.center(-25, 8).circle(4).extrude(-hole_depth))

# Cut large central hole (this will also trim the open ends of the U-shape)
base = base.cut(holes_plane.center(15, -2).circle(14).extrude(-hole_depth))

# Final geometry assigned to 'result'
result = base
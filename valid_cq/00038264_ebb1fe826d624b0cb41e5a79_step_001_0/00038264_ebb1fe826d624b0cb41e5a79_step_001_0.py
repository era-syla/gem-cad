import cadquery as cq

# --- Parameters ---
# Bed dimensions
bed_w = 60
bed_l = 80
bed_h = 15
hb_h = 35
hb_th = 5

# Table dimensions
table_w = 30
table_d = 15
table_h = 18
leg_th = 4
top_th = 3

# Cabinet dimensions
cab_w = 20
cab_d = 40
cab_h = 30
hole_diam = 10
hole_depth = 5

# Sink dimensions
sink_w = 35
sink_d = 20
sink_h = 12
sink_elevation = 25

# Toilet dimensions
tank_w = 15
tank_d = 10
tank_h = 25
bowl_rad = 7
bowl_h = 15
bowl_ext = 15

# --- Modeling Functions ---

def create_bed():
    # Base mattress
    base = cq.Workplane("XY").box(bed_w, bed_l, bed_h).translate((0, 0, bed_h/2))
    # Headboard
    headboard = (
        cq.Workplane("XY")
        .box(bed_w, hb_th, hb_h)
        .translate((0, -bed_l/2 + hb_th/2, hb_h/2))
    )
    return base.union(headboard)

def create_table():
    # Top surface
    top = (
        cq.Workplane("XY")
        .box(table_w, table_d, top_th)
        .translate((0, 0, table_h - top_th/2))
    )
    # Legs (side panels)
    leg_geo = (
        cq.Workplane("XY")
        .box(leg_th, table_d, table_h - top_th)
        .translate((0, 0, (table_h - top_th)/2))
    )
    left_leg = leg_geo.translate((-table_w/2 + leg_th/2, 0, 0))
    right_leg = leg_geo.translate((table_w/2 - leg_th/2, 0, 0))
    
    return top.union(left_leg).union(right_leg)

def create_cabinet():
    # Main block
    block = cq.Workplane("XY").box(cab_w, cab_d, cab_h).translate((0, 0, cab_h/2))
    # Cut holes on top
    result = (
        block.faces(">Z")
        .workplane()
        .pushPoints([(0, -cab_d/4), (0, cab_d/4)])
        .hole(hole_diam, hole_depth)
    )
    return result

def create_sink():
    # Outer block
    outer = cq.Workplane("XY").box(sink_w, sink_d, sink_h)
    # Basin cutout
    cutout = (
        cq.Workplane("XY")
        .box(sink_w - 6, sink_d - 6, sink_h)
        .edges("|Z")
        .fillet(3)
        .translate((0, 0, 2)) # Offset up to create bottom thickness
    )
    return outer.cut(cutout).translate((0, 0, sink_elevation + sink_h/2))

def create_toilet():
    # Tank
    tank = (
        cq.Workplane("XY")
        .box(tank_w, tank_d, tank_h)
        .translate((0, tank_d/2, tank_h/2))
    )
    # Bowl
    bowl = (
        cq.Workplane("XY")
        .center(0, -bowl_ext/2)
        .circle(bowl_rad)
        .extrude(bowl_h)
    )
    # Connector/Base
    base = (
        cq.Workplane("XY")
        .box(tank_w, tank_d + bowl_ext, bowl_h//2)
        .translate((0, (tank_d - bowl_ext)/2, bowl_h//4))
    )
    return tank.union(bowl).union(base)

# --- Assembly / Layout ---

# 1. Bed (Bottom Left)
bed = create_bed().translate((-70, -30, 0))

# 2. Tables (Bottom Middle)
table1 = create_table().translate((-10, -60, 0))
table2 = create_table().translate((30, -50, 0))

# 3. Cabinets (Top Right)
# Arranged side-by-side or staggered slightly to match image feel
cab1 = create_cabinet().translate((30, 40, 0))
cab2 = create_cabinet().translate((60, 60, 0))

# 4. Sink (Middle Right)
sink = create_sink().translate((70, 0, 0))

# 5. Toilet (Below Sink)
toilet = create_toilet().translate((70, -30, 0))

# --- Final Composition ---
# Combine all parts into a single Compound
parts = [bed, table1, table2, cab1, cab2, sink, toilet]
compound_geometry = cq.Compound.makeCompound([p.val() for p in parts])

# Wrap in a CadQuery object
result = cq.Workplane("XY").newObject([compound_geometry])
import cadquery as cq

# Pipe clamp / double saddle clamp
# Two cylindrical saddles connected by a bridge, with a bolt hole on top

# Parameters
saddle_radius = 8.0        # radius of the pipe saddles
saddle_thickness = 3.0     # wall thickness of saddles
saddle_width = 12.0        # width (depth) of each saddle
center_dist = 18.0         # distance between saddle centers
bridge_height = 6.0        # height of connecting bridge
bridge_width = 8.0         # width of bridge between saddles
bolt_boss_r = 4.5          # boss radius around bolt hole
bolt_hole_r = 2.0          # bolt hole radius
boss_height = 3.5          # height of boss above bridge

outer_r = saddle_radius + saddle_thickness

# Create the left saddle (half-cylinder clamp shape)
# Each saddle is a cylinder shell arc (C-shape wrapping around a pipe)
def make_saddle(cx):
    # Outer cylinder solid
    outer = (cq.Workplane("XY")
             .center(cx, 0)
             .circle(outer_r)
             .extrude(saddle_width))
    
    # Inner cutout (the pipe hole)
    inner = (cq.Workplane("XY")
             .center(cx, 0)
             .circle(saddle_radius)
             .extrude(saddle_width))
    
    saddle = outer.cut(inner)
    
    # Cut away the bottom half to make a C-clamp (open at bottom)
    # Cut a box from the bottom
    cut_box = (cq.Workplane("XY")
               .center(cx, -outer_r - saddle_width/2)
               .box(outer_r*2 + 2, outer_r*2 + saddle_width, saddle_width + 2))
    
    saddle = saddle.cut(cut_box)
    return saddle

# Left saddle center
left_cx = -center_dist / 2
right_cx = center_dist / 2

left_saddle = make_saddle(left_cx)
right_saddle = make_saddle(right_cx)

# Bridge connecting the two saddles on top
# A flat box connecting them at the top
bridge_z_bottom = 0
bridge_z_top = saddle_width

bridge = (cq.Workplane("XY")
          .center(0, outer_r - bridge_height/2)
          .box(center_dist + outer_r * 2, bridge_height, bridge_z_top))

# Actually let's create a simpler bridge as a rectangular block
bridge_block = (cq.Workplane("XY")
                .box(center_dist - outer_r * 0.5, bridge_height + 2, saddle_width)
                .translate((0, outer_r - 1, saddle_width / 2)))

# Combine saddles
combined = left_saddle.union(right_saddle)
combined = combined.union(bridge_block)

# Add boss on top for bolt
boss = (cq.Workplane("XY")
        .workplane(offset=saddle_width)
        .center(0, outer_r - 1)
        .circle(bolt_boss_r)
        .extrude(boss_height))

combined = combined.union(boss)

# Drill the bolt hole through boss and bridge
bolt_hole = (cq.Workplane("XY")
             .center(0, outer_r - 1)
             .circle(bolt_hole_r)
             .extrude(saddle_width + boss_height + 2))

combined = combined.cut(bolt_hole)

# Also add a through hole from bottom (the pipe clearance hole visible in image)
bottom_hole = (cq.Workplane("XY")
               .center(0, outer_r - 1)
               .circle(bolt_hole_r)
               .extrude(saddle_width + boss_height + 2)
               .translate((0, 0, -1)))

# Cut the lower hole visible through center
lower_cut = (cq.Workplane("XY")
             .center(0, -(outer_r - 2))
             .circle(bolt_hole_r * 1.2)
             .extrude(saddle_width))

combined = combined.cut(lower_cut)

# Add fillets to smooth edges
try:
    result = combined.edges("|Z").fillet(1.0)
except:
    result = combined
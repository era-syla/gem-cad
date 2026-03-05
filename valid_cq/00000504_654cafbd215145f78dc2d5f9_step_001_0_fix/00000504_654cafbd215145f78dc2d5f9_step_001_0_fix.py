import cadquery as cq

# Create individual components of a bolt/fastener assembly

def make_bolt(shaft_r, shaft_l, head_r, head_h):
    """Create a bolt with cylindrical head"""
    shaft = cq.Workplane("XY").cylinder(shaft_l, shaft_r)
    head = cq.Workplane("XY").workplane(offset=shaft_l/2).cylinder(head_h, head_r)
    return shaft.union(head)

def make_rivet(shaft_r, shaft_l, head_r, head_h):
    """Create a rivet/bolt shape"""
    shaft = (cq.Workplane("XY")
             .cylinder(shaft_l, shaft_r))
    head = (cq.Workplane("XY")
            .workplane(offset=shaft_l/2)
            .cylinder(head_h, head_r))
    return shaft.union(head)

def make_washer(outer_r, inner_r, thickness):
    """Create a washer"""
    return (cq.Workplane("XY")
            .cylinder(thickness, outer_r)
            .cut(cq.Workplane("XY").cylinder(thickness * 2, inner_r)))

def make_nut(outer_r, inner_r, height):
    """Create a hex nut approximated as hexagonal prism with hole"""
    hex_nut = (cq.Workplane("XY")
               .polygon(6, outer_r * 2)
               .extrude(height))
    hole = cq.Workplane("XY").cylinder(height * 2, inner_r)
    return hex_nut.cut(hole)

def make_large_wheel(outer_r, inner_r, height, flange_r, flange_h):
    """Create a wheel/pulley shape"""
    body = (cq.Workplane("XY")
            .cylinder(height, outer_r))
    hole = cq.Workplane("XY").cylinder(height * 2, inner_r)
    flange_top = (cq.Workplane("XY")
                  .workplane(offset=height/2)
                  .cylinder(flange_h, flange_r))
    flange_bot = (cq.Workplane("XY")
                  .workplane(offset=-height/2)
                  .cylinder(flange_h, flange_r))
    result = body.cut(hole).union(flange_top).union(flange_bot)
    return result

# Assembly - position components along a diagonal line
# Scale factor
s = 1.0

# Component 1: Small washer (top-left)
washer1 = make_washer(3*s, 1.2*s, 0.8*s)
washer1 = washer1.rotate((0,0,0),(1,0,0), 90).translate((-35, 8, 0))

# Component 2: Small bolt/rivet (left)
bolt1 = (cq.Workplane("XY")
         .cylinder(8*s, 1.5*s)
         .union(cq.Workplane("XY").workplane(offset=4*s).cylinder(2*s, 4*s)))
bolt1 = bolt1.rotate((0,0,0),(0,1,0), 90).translate((-25, 0, 0))

# Component 3: Medium bolt
bolt2 = (cq.Workplane("XY")
         .cylinder(10*s, 2*s)
         .union(cq.Workplane("XY").workplane(offset=5*s).cylinder(2.5*s, 5*s)))
bolt2 = bolt2.rotate((0,0,0),(0,1,0), 90).translate((-12, -3, 0))

# Component 4: Large central wheel/bushing
wheel_body = cq.Workplane("XY").cylinder(6*s, 8*s)
wheel_hole = cq.Workplane("XY").cylinder(10*s, 3*s)
wheel_flange1 = cq.Workplane("XY").workplane(offset=3*s).cylinder(1.5*s, 10*s)
wheel_flange2 = cq.Workplane("XY").workplane(offset=-3*s).cylinder(1.5*s, 10*s)
wheel = wheel_body.cut(wheel_hole).union(wheel_flange1).union(wheel_flange2)
wheel = wheel.rotate((0,0,0),(0,1,0), 90).translate((0, -1, 0))

# Component 5: Washer medium
washer2 = make_washer(4*s, 2*s, 1*s)
washer2 = washer2.rotate((0,0,0),(1,0,0), 90).translate((11, -4, 0))

# Component 6: Small nut
nut1 = make_nut(3.5*s, 1.5*s, 2.5*s)
nut1 = nut1.rotate((0,0,0),(1,0,0), 90).translate((18, -6, 0))

# Component 7: Large rivet/bolt right
bolt3 = (cq.Workplane("XY")
         .cylinder(12*s, 2.5*s)
         .union(cq.Workplane("XY").workplane(offset=6*s).cylinder(3*s, 6*s)))
bolt3 = bolt3.rotate((0,0,0),(0,1,0), 90).translate((30, -9, 0))

# Component 8: Another large rivet
bolt4 = (cq.Workplane("XY")
         .cylinder(12*s, 2.5*s)
         .union(cq.Workplane("XY").workplane(offset=6*s).cylinder(3*s, 6*s)))
bolt4 = bolt4.rotate((0,0,0),(0,1,0), 90).translate((38, -12, 0))

# Combine all components
result = (washer1
          .union(bolt1)
          .union(bolt2)
          .union(wheel)
          .union(washer2)
          .union(nut1)
          .union(bolt3)
          .union(bolt4))
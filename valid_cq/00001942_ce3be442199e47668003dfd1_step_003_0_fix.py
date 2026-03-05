import cadquery as cq

# Build the assembly - a camera/sensor mount with base, pole, and head

def make_base():
    # Oval/rounded rectangle base
    base = (cq.Workplane("XY")
            .ellipse(30, 20)
            .extrude(4))
    
    # Add rim/edge detail
    base = (base
            .faces(">Z")
            .shell(-2))
    
    return base

def make_base_simple():
    # Simple rounded rectangle base
    base = (cq.Workplane("XY")
            .rect(55, 38, forConstruction=False)
            .extrude(5))
    
    # Round the corners
    base = base.edges("|Z").fillet(15)
    
    # Hollow slightly on top
    base = (base
            .faces(">Z")
            .workplane()
            .rect(48, 31)
            .cutBlind(-2))
    
    return base

def make_pole():
    pole = (cq.Workplane("XY")
            .circle(5)
            .extrude(35))
    return pole

def make_support_arms():
    # Two diagonal support arms
    arm1 = (cq.Workplane("XZ")
            .rect(4, 20)
            .extrude(3)
            .translate((8, 0, 10)))
    
    arm2 = (cq.Workplane("XZ")
            .rect(4, 20)
            .extrude(3)
            .translate((-8, 0, 10)))
    
    return arm1.union(arm2)

def make_head_mount():
    # Main head bracket - rectangular plate
    head = (cq.Workplane("XY")
            .rect(28, 20)
            .extrude(3)
            .translate((0, 0, 40)))
    
    # Add rail/grooves on top
    head = (head
            .faces(">Z")
            .workplane()
            .rarray(6, 1, 4, 1)
            .rect(2, 18)
            .cutBlind(-1))
    
    return head

def make_ring():
    # Circular ring at top
    ring_outer = (cq.Workplane("XY")
                  .circle(10)
                  .extrude(3))
    ring_inner = (cq.Workplane("XY")
                  .circle(7)
                  .extrude(3))
    ring = ring_outer.cut(ring_inner)
    return ring

# Build main assembly piece 1 (left - full assembly)
base1 = make_base_simple()

# Pole on base
pole1 = (cq.Workplane("XY")
         .workplane(offset=5)
         .circle(5)
         .extrude(30))

# Support structure at top of pole
support_top = (cq.Workplane("XY")
               .workplane(offset=35)
               .rect(30, 5)
               .extrude(3))

# Side walls of bracket
wall_left = (cq.Workplane("XY")
             .workplane(offset=35)
             .transformed(offset=cq.Vector(-12, 0, 0))
             .rect(3, 5)
             .extrude(20))

wall_right = (cq.Workplane("XY")
              .workplane(offset=35)
              .transformed(offset=cq.Vector(12, 0, 0))
              .rect(3, 5)
              .extrude(20))

# Ring at top
ring_top = (cq.Workplane("XY")
            .workplane(offset=55)
            .circle(9)
            .extrude(2)
            .cut(
                cq.Workplane("XY")
                .workplane(offset=55)
                .circle(6)
                .extrude(2)
            ))

# Rail mount head
rail_head = (cq.Workplane("XY")
             .workplane(offset=35)
             .rect(28, 18)
             .extrude(4))

# Combine left assembly
left_assembly = (base1
                 .union(pole1)
                 .union(support_top)
                 .union(wall_left)
                 .union(wall_right)
                 .union(ring_top)
                 .union(rail_head))

# Build right assembly (base with two cylinders)
base2 = (cq.Workplane("XY")
         .rect(55, 38)
         .extrude(5)
         .edges("|Z").fillet(15)
         .translate((80, 0, 0)))

cyl1 = (cq.Workplane("XY")
        .workplane(offset=5)
        .center(80 - 8, 0)
        .circle(6)
        .extrude(28))

cyl2 = (cq.Workplane("XY")
        .workplane(offset=5)
        .center(80 + 8, 0)
        .circle(6)
        .extrude(28))

right_assembly = base2.union(cyl1).union(cyl2)

# Small detached rail piece (top right in image)
rail_piece = (cq.Workplane("XY")
              .rect(24, 16)
              .extrude(8)
              .translate((80, 50, 0)))

rail_piece = rail_piece.edges("|Z").fillet(3)

# Combine everything
result = left_assembly.union(right_assembly).union(rail_piece)
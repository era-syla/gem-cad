import cadquery as cq
import math

def make_blade(length=40, width=8, thickness=2):
    """Create a single propeller blade using extrusion and tapering."""
    # Create blade profile - elliptical shape
    blade = (
        cq.Workplane("XY")
        .ellipse(length/2, width/2)
        .extrude(thickness)
    )
    return blade

def make_propeller():
    """Create a two-blade propeller."""
    # Central hub
    hub = (
        cq.Workplane("XY")
        .cylinder(4, 5)
    )
    
    # Blade 1 - elongated ellipsoid shape
    blade1 = (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(20, 0, 1))
        .ellipse(22, 5)
        .extrude(1.5)
    )
    
    # Blade 2 - opposite direction
    blade2 = (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(-20, 0, 1))
        .ellipse(22, 5)
        .extrude(1.5)
    )
    
    # Combine hub and blades
    prop = hub.union(blade1).union(blade2)
    
    # Add center hole
    prop = (
        prop
        .faces(">Z")
        .workplane()
        .circle(1.5)
        .cutThruAll()
    )
    
    return prop

# Create one propeller
prop = make_propeller()

# Create 4 propellers arranged like in the image (2x2 grid, slightly rotated)
# Propeller 1 - bottom left
p1 = prop.translate((-35, -20, 0))

# Propeller 2 - top left  
p2 = prop.translate((-35, 20, 0))

# Propeller 3 - bottom right
p3 = prop.translate((35, -20, 0))

# Propeller 4 - top right
p4 = prop.translate((35, 20, 0))

# Combine all propellers
result = (
    cq.Workplane("XY")
    .add(p1)
    .add(p2)
    .add(p3)
    .add(p4)
)

# Rebuild as compound
r1 = make_propeller().translate((-35, -20, 0))
r2 = make_propeller().translate((-35, 20, 0))
r3 = make_propeller().translate((35, -20, 0))
r4 = make_propeller().translate((35, 20, 0))

result = r1.union(r2).union(r3).union(r4)
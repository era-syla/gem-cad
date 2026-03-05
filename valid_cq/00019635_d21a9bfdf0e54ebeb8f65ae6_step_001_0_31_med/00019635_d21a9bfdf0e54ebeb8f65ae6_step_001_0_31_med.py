import cadquery as cq

# Parameters for the propeller
hub_radius = 4.0
hub_height = 6.0
shaft_radius = 1.0
blade_length = 45.0

# 1. Create the central hub
hub = cq.Workplane("XY").cylinder(hub_height, hub_radius)
hub = hub.faces(">Z").hole(shaft_radius * 2)

# 2. Create a single blade using lofted cross-sections
# The blade is built along the X-axis (using YZ workplanes)
blade1 = (
    cq.Workplane("YZ")
    # Root (inside the hub)
    .workplane(offset=hub_radius * 0.5)
    .transformed(rotate=cq.Vector(0, 0, 45))
    .ellipse(2.5, 0.8)
    
    # Station 1 (Inner blade)
    .workplane(offset=blade_length * 0.2)
    .transformed(rotate=cq.Vector(0, 0, -10))
    .ellipse(5.5, 1.1)
    
    # Station 2 (Max chord / widest part)
    .workplane(offset=blade_length * 0.4)
    .transformed(rotate=cq.Vector(0, 0, -15))
    .ellipse(7.5, 0.9)
    
    # Station 3 (Outer blade tapering)
    .workplane(offset=blade_length * 0.3)
    .transformed(rotate=cq.Vector(0, 0, -10))
    .ellipse(4.0, 0.5)
    
    # Tip
    .workplane(offset=blade_length * 0.1)
    .transformed(rotate=cq.Vector(0, 0, -5))
    .ellipse(0.5, 0.15)
    
    .loft()
)

# 3. Create the second blade by rotating the first one 180 degrees around the Z-axis
blade2 = blade1.rotate((0, 0, 0), (0, 0, 1), 180)

# 4. Combine all parts into the final result
result = hub.union(blade1, clean=True).union(blade2, clean=True)
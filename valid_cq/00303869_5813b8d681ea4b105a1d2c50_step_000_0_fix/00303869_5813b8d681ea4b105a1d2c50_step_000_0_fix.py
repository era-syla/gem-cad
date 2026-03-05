import cadquery as cq

# Base platform
base = (cq.Workplane("XY")
        .rect(60, 40)
        .extrude(10))

# Upper platform
upper_platform = (base.faces(">Z")
                  .workplane()
                  .rect(50, 30)
                  .extrude(5))

# Jaws
jaw1 = (upper_platform.faces(">Z")
        .workplane(offset=5)
        .rect(45, 8, forConstruction=True)
        .vertices("<Y")
        .rect(10, 8)
        .extrude(10))

jaw2 = (upper_platform.faces(">Z")
        .workplane(offset=5)
        .rect(45, 8, forConstruction=True)
        .vertices(">Y")
        .rect(10, 8)
        .extrude(10))

# Combine components
result = base.union(upper_platform).union(jaw1).union(jaw2)
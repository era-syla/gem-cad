import cadquery as cq

# Define the blade path
blade_path = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(0, 50)
    .threePointArc((5, 60), (0, 70))
    .lineTo(0, 120)
)

# Define the blade profile
blade_profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(2, 0)
    .lineTo(1, 0.5)
    .close()
)

# Loft the blade
blade = blade_profile.sweep(blade_path)

# Create the handle
handle = (
    cq.Workplane("XY")
    .circle(5)
    .extrude(30)
)

# Create a guard
guard = (
    cq.Workplane("XY", origin=(0, 0, 30))
    .rect(15, 5)
    .extrude(2)
)

result = handle.union(guard).union(blade)
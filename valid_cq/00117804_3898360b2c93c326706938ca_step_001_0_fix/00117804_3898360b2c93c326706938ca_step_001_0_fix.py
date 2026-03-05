import cadquery as cq

# Define basic parameters
rod_diameter = 2.0
rod_radius = rod_diameter / 2
base_length = 20.0
arch_height = 25.0
arch_radius = 5.0

# Create the base rod
base_rod = cq.Workplane("XY").circle(rod_radius).extrude(base_length)

# Create the upward arch
arch_path = cq.Workplane("YZ").moveTo(0, 0).threePointArc((arch_height/2, arch_radius), (arch_height, 0))
arch = base_rod.union(
    cq.Workplane("XY").circle(rod_radius).sweep(arch_path)
)

# Create the cross rods
cross_rod_path = cq.Workplane("XZ").moveTo(0, 0).lineTo(arch_height, 0)
cross_rod1 = cq.Workplane("YZ").circle(rod_radius).sweep(cross_rod_path)
cross_rod2 = cross_rod1.mirror(mirrorPlane="XZ")

# Assemble the structures
result = arch.union(cross_rod1).union(cross_rod2)
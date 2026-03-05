import cadquery as cq

# Parametric dimensions
ring_od = 100.0          # Outer diameter of the ring
ring_width = 3.0         # Radial thickness of the ring wall
ring_height = 5.0        # Axial height of the ring
notch_count = 12         # Number of notches around the perimeter
notch_radius = 2.0       # Radius of the semi-circular cutouts

# Derived dimensions
ring_id = ring_od - (2 * ring_width)

# 1. Create the base ring (hollow cylinder)
# Using two concentric circles and extruding creates a tube
base = (
    cq.Workplane("XY")
    .circle(ring_od / 2.0)
    .circle(ring_id / 2.0)
    .extrude(ring_height)
)

# 2. Create the cutting tool for the notches
# We create a long cylinder oriented radially (along the X-axis).
# Positioning the center at Z = ring_height creates a semi-circular scallop on the top rim.
# Extruding with both=True ensures it cuts through both sides of the ring (0 and 180 degrees).
cutter_geo = (
    cq.Workplane("YZ")
    .center(0, ring_height)
    .circle(notch_radius)
    .extrude(ring_od * 1.5, both=True)
)

# 3. Create the pattern of cutters
# Since one cutter handles two opposite notches, we rotate it notch_count/2 times.
# We union all rotated cutters into a single object for a cleaner cut operation.
cutters = cutter_geo
for i in range(1, int(notch_count / 2)):
    angle = i * (360.0 / notch_count)
    cutters = cutters.union(cutter_geo.rotate((0, 0, 0), (0, 0, 1), angle))

# 4. Subtract the cutters from the base ring
result = base.cut(cutters)
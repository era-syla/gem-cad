import cadquery as cq

# --- Parameters ---

# Plug (Top Object) dimensions
plug_diameter = 20.0
plug_height = 25.0
hole_diameter = 2.5
hole_spacing = 8.0  # Distance between hole centers
hole_depth = 6.0

# Ring (Bottom Object) dimensions
ring_od = 50.0
ring_id = 34.0
ring_height = 8.0
ring_chamfer = 2.0

# Positioning
vertical_separation = 20.0  # Gap between top of ring and bottom of plug

# --- Geometry Generation ---

# 1. Create the Plug
# Calculate starting Z height to place the plug above the ring
plug_start_z = ring_height + vertical_separation

plug = (
    cq.Workplane("XY")
    .workplane(offset=plug_start_z)
    .circle(plug_diameter / 2.0)
    .extrude(plug_height)
    # Select the top face to add the holes
    .faces(">Z")
    .workplane()
    # Create two points centered on the face
    .pushPoints([(hole_spacing / 2.0, 0), (-hole_spacing / 2.0, 0)])
    .hole(hole_diameter, hole_depth)
)

# 2. Create the Ring
ring = (
    cq.Workplane("XY")
    .circle(ring_od / 2.0)
    .circle(ring_id / 2.0)
    .extrude(ring_height)
)

# Apply chamfer to the inner top edge of the ring
# We select the top face, then find the edge closest to the inner radius
ring = (
    ring.faces(">Z")
    .edges(cq.NearestToPointSelector((ring_id / 2.0, 0, ring_height)))
    .chamfer(ring_chamfer)
)

# 3. Combine into final result
result = plug.union(ring)
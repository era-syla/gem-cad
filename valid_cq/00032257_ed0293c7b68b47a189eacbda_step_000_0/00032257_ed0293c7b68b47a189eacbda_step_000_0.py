import cadquery as cq

# --- Parameters ---
hub_diameter = 40.0
hub_length = 30.0
pivot_diameter = 32.0
pivot_length = 10.0
arm_diameter = 18.0
arm_horizontal_len = 150.0
arm_vertical_len = 100.0
arm_return_len = 30.0
bend_radius = 25.0

# --- Hub Construction ---
# Create the main hub cylinder oriented along the Y-axis
hub_main = (
    cq.Workplane("XZ")
    .workplane(offset=hub_length / 2.0)
    .circle(hub_diameter / 2.0)
    .extrude(-hub_length)
)

# Create the smaller pivot cylinder at the back (-Y side)
hub_pivot = (
    cq.Workplane("XZ")
    .workplane(offset=-hub_length / 2.0)
    .circle(pivot_diameter / 2.0)
    .extrude(-pivot_length)
)

# Combine hub parts
hub = hub_main.union(hub_pivot)

# Chamfer the front face and back face for detail
hub = hub.faces(">Y").chamfer(1.5)
hub = hub.faces("<Y").chamfer(1.0)

# --- Arm Construction ---
# Define the path points
# P0: Center of hub
# P1: End of horizontal section
# P2: End of vertical drop
# P3: End of inward return (towards the wall/back)
p0 = cq.Vector(0, 0, 0)
p1 = cq.Vector(arm_horizontal_len, 0, 0)
p2 = cq.Vector(arm_horizontal_len, 0, -arm_vertical_len)
p3 = cq.Vector(arm_horizontal_len, -arm_return_len, -arm_vertical_len)

# Create the path edges
e1 = cq.Edge.makeLine(p0, p1)
e2 = cq.Edge.makeLine(p1, p2)
e3 = cq.Edge.makeLine(p2, p3)

# Assemble edges into a wire and apply fillets to the corners
path_wire = cq.Wire.assembleEdges([e1, e2, e3])
path = path_wire.fillet(bend_radius)

# Create the arm by sweeping a circle profile along the path
# Profile is on YZ plane (perpendicular to the start direction X)
arm = (
    cq.Workplane("YZ")
    .circle(arm_diameter / 2.0)
    .sweep(path)
)

# --- Final Assembly ---
result = hub.union(arm)

# Fillet the junction where the arm meets the hub
# Select edges near the intersection point on the hub surface
junction_point = (hub_diameter / 2.0, 0, 0)
result = result.edges(cq.selectors.NearestToPointSelector(junction_point)).fillet(3.0)

# Fillet the tip of the handle arm
result = result.faces(cq.selectors.NearestToPointSelector(p3)).fillet(2.0)
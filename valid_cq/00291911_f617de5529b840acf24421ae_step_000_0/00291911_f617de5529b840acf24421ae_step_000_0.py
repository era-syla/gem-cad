import cadquery as cq

# -- Parameters --
thickness = 4.0

# -- Geometry Definition --
# Coordinates defined counter-clockwise starting from bottom-left tip
# These points define the outer hull which will be smoothed with fillets
p_tip = (-40, -32)      # Bottom-Left Tip
p_heel = (12, -12)      # Bottom-Right Corner (Heel)
p_bulge = (28, 55)      # Middle-Right (Bulge)
p_top_r = (18, 118)     # Top-Right
p_top_l = (4, 118)      # Top-Left
p_waist = (4, 55)       # Middle-Left (Waist)
p_crook = (-18, -2)     # Inner Corner (Crook)

points = [p_tip, p_heel, p_bulge, p_top_r, p_top_l, p_waist, p_crook]

# -- Create Base Solid --
base = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(thickness)
)

# -- Apply Fillets to define the shape --
# Using NearestToPointSelector to robustly target specific vertical edges
result = base

# Top: Create a full round by filleting the corners
result = result.edges(cq.selectors.NearestToPointSelector(p_top_r)).fillet(7.0)
result = result.edges(cq.selectors.NearestToPointSelector(p_top_l)).fillet(7.0)

# Mid Sections: Large radii for smooth organic transitions
result = result.edges(cq.selectors.NearestToPointSelector(p_bulge)).fillet(40.0)
result = result.edges(cq.selectors.NearestToPointSelector(p_waist)).fillet(30.0)

# Bottom Section: Define the leg and heel
result = result.edges(cq.selectors.NearestToPointSelector(p_tip)).fillet(8.0)
result = result.edges(cq.selectors.NearestToPointSelector(p_heel)).fillet(10.0)
result = result.edges(cq.selectors.NearestToPointSelector(p_crook)).fillet(15.0)

# -- Create Holes --
# List of (Center_XY, Diameter)
holes_data = [
    ((-33, -25), 6.0),    # Tip Hole
    ((4, 0), 6.0),        # Heel Hole
    ((15, 60), 6.0),      # Middle Hole
    ((11, 105), 5.0),     # Top Lower Hole
    ((14, 112), 5.0),     # Top Upper Hole
]

# Perform cuts
wp = result.faces(">Z").workplane()
for pos, dia in holes_data:
    wp = wp.pushPoints([pos]).circle(dia / 2.0)
    
result = wp.cutThruAll()
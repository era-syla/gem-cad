import cadquery as cq

# --- Parametric Dimensions ---
# Main Flange Dimensions
flange_diameter = 120.0  # Outer diameter of the flange base
flange_thickness = 15.0  # Thickness of the flange base

# Hub (Neck) Dimensions
hub_diameter = 60.0      # Outer diameter of the cylindrical neck
hub_length = 80.0        # Length of the neck extending from the flange

# Bore (Internal Hole) Dimensions
bore_diameter = 40.0     # Inner diameter of the through-hole

# Bolt Hole Dimensions
bolt_circle_diameter = 95.0 # Diameter of the circle on which bolt holes are placed
num_bolt_holes = 6          # Number of bolt holes
bolt_hole_diameter = 10.0   # Diameter of each bolt hole

# Fillet Radius (optional aesthetic touch seen in similar parts)
fillet_radius = 5.0

# --- Geometry Construction ---

# 1. Create the base flange disk
base_flange = cq.Workplane("XY").circle(flange_diameter / 2.0).extrude(flange_thickness)

# 2. Create the central hub
# We extrude from the top face of the flange
hub = (
    base_flange.faces(">Z")
    .workplane()
    .circle(hub_diameter / 2.0)
    .extrude(hub_length)
)

# 3. Add the fillet between the flange and the hub
# This strengthens the transition and matches the visual style
hub_with_fillet = hub.faces(">Z").edges().fillet(fillet_radius) 
# Note: The fillet needs to be applied to the edge connecting the hub and flange. 
# Let's re-select the proper edge. The edge is at the base of the hub extrusion.
# A more robust way is to select edges based on Z coordinate.
transition_edge_z = flange_thickness
hub_with_fillet = hub.edges(cq.selectors.NearestToPointSelector((hub_diameter/2, 0, transition_edge_z))).fillet(fillet_radius)


# 4. Create the main central bore (through-hole)
# We cut through the entire object
part_with_bore = hub_with_fillet.faces(">Z").workplane().hole(bore_diameter)

# 5. Create the bolt hole pattern on the flange
# We select the back face (or front face of the flange ring) to drill the holes
result = (
    part_with_bore.faces("<Z")  # Select the bottom face of the flange
    .workplane()
    .polarArray(bolt_circle_diameter / 2.0, 0, 360, num_bolt_holes)
    .circle(bolt_hole_diameter / 2.0)
    .cutThruAll()
)

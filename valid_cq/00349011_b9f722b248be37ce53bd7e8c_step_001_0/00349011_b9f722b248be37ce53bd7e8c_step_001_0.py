import cadquery as cq

# --- Geometric Parameters ---
# Standard 608 Bearing dimensions (mm)
bearing_od = 22.0
bearing_id = 8.0
body_thickness = 7.0

# Spinner Body Configuration
lobe_radius = 15.0       # Radius of the outer circular lobes
center_dist = 28.0       # Distance from center to lobe center
neck_fillet = 10.0       # Radius of the smooth curve connecting lobes to center
edge_fillet = 3.0        # Radius for rounding top and bottom edges

# Cap Configuration
cap_diam = 22.0          # Diameter of the cap cover
cap_thick = 2.0          # Thickness of the main cap disk
btn_diam = 10.0          # Diameter of the button/boss on top
btn_height = 2.0         # Height of the button
shaft_len = 4.0          # Length of the pin inserting into bearing
cap_z_pos = 25.0         # Vertical position for the exploded view

# --- 1. Create the Main Spinner Body ---

# Construct the central hub
center_geo = cq.Workplane("XY").circle(lobe_radius).extrude(body_thickness)

# Construct the three lobes arranged radially
lobes_geo = (
    cq.Workplane("XY")
    .polarArray(center_dist, 0, 360, 3)
    .circle(lobe_radius)
    .extrude(body_thickness)
)

# Combine hub and lobes into a single solid
body = center_geo.union(lobes_geo)

# Apply fillets to the vertical intersections (the "necks") to create the web
body = body.edges("|Z").fillet(neck_fillet)

# Apply fillets to the top and bottom edges for a rounded, ergonomic feel
# We do this before cutting holes to keep the bearing seats sharp
body = body.edges("not |Z").fillet(edge_fillet)

# Cut the central bearing hole
body = body.faces(">Z").workplane().hole(bearing_od)

# Cut the lobe bearing holes
body = body.faces(">Z").workplane().polarArray(center_dist, 0, 360, 3).hole(bearing_od)


# --- 2. Create the Bearing Cap ---

# Create the main disk of the cap, floating above the body
cap = (
    cq.Workplane("XY")
    .workplane(offset=cap_z_pos)
    .circle(cap_diam / 2)
    .extrude(cap_thick)
)

# Add the button/boss on the top face
cap = (
    cap.faces(">Z").workplane()
    .circle(btn_diam / 2)
    .extrude(btn_height)
)

# Add the shaft on the bottom face (pointing downwards into the bearing)
# Selecting <Z puts the workplane normal pointing down, so positive extrude adds material down
cap = (
    cap.faces("<Z").workplane()
    .circle(bearing_id / 2 - 0.1)  # Slight clearance for fit
    .extrude(shaft_len)
)

# --- 3. Final Assembly ---
# Combine the body and the cap into the result variable
result = body.union(cap)
import cadquery as cq

# Parametric dimensions for the model
total_height = 100.0
base_radius = 25.0
top_radius = 18.0
base_height = 15.0
shoulder_height = 10.0
neck_bottom_radius = 12.0
neck_top_radius = 9.0  # Radius just before the ribs
rib_start_height = 60.0
rib_protrusion = 4.0
rib_thickness = 5.0
rib_gap = 4.0
wedge_angle = 45.0

# Define the profile points (Radius, Height) corresponding to the outer silhouette
# Starting from the center bottom
points = []
points.append((0, 0))

# Base section
points.append((base_radius, 0))
points.append((base_radius, base_height))

# Tapered shoulder transition
points.append((neck_bottom_radius, base_height + shoulder_height))

# Long tapered neck up to the first rib
points.append((neck_top_radius, rib_start_height))

# --- Detail Section (Ribs) ---
current_h = rib_start_height
current_r = neck_top_radius

# Lower Rib
points.append((current_r + rib_protrusion, current_h))       # Step Out
current_h += rib_thickness
points.append((current_r + rib_protrusion, current_h))       # Vertical Up
points.append((current_r, current_h))                        # Step In

# Gap between ribs
current_h += rib_gap
points.append((current_r, current_h))                        # Vertical Up

# Upper Rib
points.append((current_r + rib_protrusion, current_h))       # Step Out
current_h += rib_thickness
points.append((current_r + rib_protrusion, current_h))       # Vertical Up
# Step In, but slightly wider to start the top flare smoothly
flare_start_r = current_r + 2.0
points.append((flare_start_r, current_h))

# --- Top Section ---
# Flare out to the top
points.append((top_radius, total_height))

# Close the profile back to the axis
points.append((0, total_height))
points.append((0, 0))

# Create the geometry
# We draw on the XZ plane: X corresponds to Radius, Z corresponds to Height (Y in local 2D plane)
# Revolve creates the solid by rotating around the Z-axis (default for XZ plane revolve)
result = (
    cq.Workplane("XZ")
    .polyline(points)
    .close()
    .revolve(wedge_angle)
)
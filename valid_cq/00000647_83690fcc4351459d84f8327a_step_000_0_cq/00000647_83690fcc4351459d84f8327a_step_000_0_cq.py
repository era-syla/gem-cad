import cadquery as cq
import math

# --- Parameters ---
# Overall dimensions to keep proportions similar to the image
main_length = 120.0

# Bell/Nozzle Section
bell_outer_radius = 45.0
bell_length = 30.0
bell_wall_thickness = 3.0

# Central Body Section
body_radius_start = 25.0
body_radius_end = 15.0
body_length = 50.0

# Rear Pod/Cap Section
pod_radius = 25.0
pod_length = 40.0

# Fin/Wing parameters
fin_length = 35.0
fin_height = 20.0
fin_thickness = 3.0
fin_offset = 10.0

# --- Geometry Construction ---

# 1. The Large Bell/Nozzle (Front)
# Create a solid cone and shell it
bell = (
    cq.Workplane("XY")
    .circle(bell_outer_radius)
    .workplane(offset=bell_length)
    .circle(body_radius_start)
    .loft(combine=True)
)

# Hollow out the bell to make it nozzle-like
bell_hollow = (
    cq.Workplane("XY")
    .circle(bell_outer_radius - bell_wall_thickness)
    .workplane(offset=bell_length - 2) # Slightly less deep to keep a solid back
    .circle(body_radius_start - bell_wall_thickness)
    .loft(combine=True)
)
bell = bell.cut(bell_hollow)

# Add mounting holes inside the bell
mounting_holes = (
    cq.Workplane("XY")
    .workplane(offset=bell_length/2)
    .pushPoints([(15, 0), (-15, 0)])
    .circle(4.0)
    .extrude(20) # Extrude through the back wall
)
bell = bell.cut(mounting_holes)


# 2. Central Body (Tapered Cylinder)
body = (
    cq.Workplane("XY")
    .workplane(offset=bell_length)
    .circle(body_radius_start)
    .workplane(offset=body_length)
    .circle(body_radius_end)
    .loft(combine=True)
)

# Add complex surface details to the body (simulating the organic/paneled look)
# We'll use a subtractive pipe or cuts to create grooves
groove_path = (
    cq.Workplane("XZ")
    .workplane(offset=0)
    .moveTo(bell_length + 5, body_radius_start)
    .spline([(bell_length + body_length/2, body_radius_start * 0.9), 
             (bell_length + body_length - 5, body_radius_end)], includeCurrent=True)
)
# This part is simplified; true organic texture requires complex surface modeling not easily done with basic primitives.
# Instead, we will add a box-like "tech" protrusion on top.

tech_box = (
    cq.Workplane("XY")
    .workplane(offset=bell_length + 5)
    .transformed(rotate=(0, 0, 0))
    .rect(20, 20)
    .extrude(body_length - 15)
    .translate((0, body_radius_start * 0.8, 0)) # Move it up
)
# Intersect with a slightly larger cylinder to curve the bottom or just let it merge
# We will just merge it.
body = body.union(tech_box)

# Add a side circular port
side_port = (
    cq.Workplane("YZ")
    .workplane(offset=10) # Offset from center
    .moveTo(0, bell_length + body_length/2)
    .circle(6)
    .extrude(20)
)
# We want to cut this into the body
body = body.cut(side_port)
# And add a rim
side_port_rim = (
    cq.Workplane("YZ")
    .workplane(offset=body_radius_start - 5)
    .moveTo(0, bell_length + body_length/2)
    .circle(7)
    .circle(5)
    .extrude(5)
)
body = body.union(side_port_rim)


# 3. Rear Pod/Cap (Rounded end)
# This looks like a loft from the body end to a rounded shape
rear_start_z = bell_length + body_length

rear_pod = (
    cq.Workplane("XY")
    .workplane(offset=rear_start_z)
    .circle(body_radius_end)
    .workplane(offset=pod_length * 0.6)
    .circle(pod_radius) # Expands
    .workplane(offset=pod_length * 0.4)
    .circle(5) # Tapers to a point/small circle
    .loft(combine=True)
)

# Cut the rear pod to look more like the "helmet" shape in the image
cutout_plane = (
    cq.Workplane("YZ")
    .workplane(offset=0)
    .moveTo(0, rear_start_z + pod_length/2)
    .rect(pod_radius*2.5, pod_length)
    .extrude(pod_radius*2)
    .translate((-pod_radius*2 - 5, 0, 0)) # Move to side to slice off a cheek
)
# Mirror the cut for symmetry? The image looks asymmetric or side view.
# Let's add a "visor" cut.
visor_cut = (
    cq.Workplane("XY")
    .workplane(offset=rear_start_z + pod_length * 0.5)
    .transformed(rotate=(45, 0, 0))
    .rect(pod_radius*2, 15)
    .extrude(20)
)
rear_pod = rear_pod.cut(visor_cut)


# 4. Fins / Wings
# The image shows angled fins sticking out near the junction of the bell and body.

def make_fin(angle):
    fin = (
        cq.Workplane("XY")
        .workplane(offset=bell_length + 5)
        .transformed(rotate=(0, 0, angle))
        .moveTo(body_radius_start - 2, 0)
        .lineTo(body_radius_start + fin_height, 0)
        .lineTo(body_radius_start + fin_height - 5, fin_length)
        .lineTo(body_radius_start - 2, fin_length)
        .close()
        .extrude(fin_thickness)
    )
    # Rotate the fin to align with the body axis better? 
    # The extrusion is currently along Z (axis of body), which creates a plate.
    # The image shows plates standing up radially.
    
    # Let's try a different approach for the fin: extrude a profile along the body
    fin_shape = (
        cq.Workplane("XZ")
        .workplane(offset=0)
        .moveTo(bell_length + 5, body_radius_start - 2)
        .lineTo(bell_length + 5, body_radius_start + fin_height)
        .lineTo(bell_length + 5 + fin_length, body_radius_start + fin_height * 0.5)
        .lineTo(bell_length + 5 + fin_length, body_radius_start - 2)
        .close()
        .extrude(fin_thickness/2, both=True)
    )
    
    # Rotate this fin around the Z axis
    return fin_shape.rotate((0,0,0), (0,0,1), angle)

fin1 = make_fin(45)
fin2 = make_fin(-45) # Symmetric fin
fin3 = make_fin(135) # Rear/bottom fins maybe?
fin4 = make_fin(-135)

# 5. Top Detail (The rectangular boxy structure on top of the bell/body junction)
top_detail = (
    cq.Workplane("XY")
    .workplane(offset=bell_length - 5)
    .moveTo(0, body_radius_start + 2)
    .rect(20, 15)
    .extrude(25)
)
# Add a hole through it
top_detail_hole = (
    cq.Workplane("YZ")
    .workplane(offset=0)
    .moveTo(0, bell_length + 7)
    .circle(5)
    .extrude(50) # Cut through
)
top_detail = top_detail.cut(top_detail_hole)


# 6. "Webbing" or reinforcement at the back of the bell
# The image shows a complex structure behind the bell. We can approximate with a polar array of ribs.
rib = (
    cq.Workplane("XZ")
    .moveTo(bell_length, body_radius_start)
    .lineTo(bell_length, bell_outer_radius * 0.8)
    .lineTo(bell_length + 10, body_radius_start)
    .close()
    .extrude(2, both=True)
)
ribs = rib
for i in range(1, 6):
    ribs = ribs.union(rib.rotate((0,0,0), (0,0,1), i * 60))


# --- Combine All Parts ---
result = bell.union(body).union(rear_pod)
result = result.union(fin1).union(fin2)
result = result.union(top_detail)
result = result.union(ribs)

# Apply some fillets to smooth transitions (simulating organic modeling)
# Selecting edges is tricky without specific IDs, so we'll use a general approach cautiously
try:
    result = result.edges("|Z").fillet(1.0)
except:
    pass # Fillets often fail on complex unions, skip if necessary

# Rotate to match image orientation roughly (Image shows it pointing somewhat towards left-viewer)
result = result.rotate((0,0,0), (0,1,0), -90).rotate((0,0,0), (0,0,1), -30)

# Export or display
if "show_object" in locals():
    show_object(result)
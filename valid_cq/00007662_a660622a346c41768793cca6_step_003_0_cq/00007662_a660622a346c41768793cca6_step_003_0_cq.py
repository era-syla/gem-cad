import cadquery as cq
import math

# --- Parameters ---
length = 200.0  # Total length of the vehicle body
width = 80.0    # Total width at the widest point
height = 50.0   # Approximate height of the side walls

# Front section parameters
front_nose_length = 50.0
front_width = 60.0

# Rear section parameters
rear_length = 60.0
rear_height = 60.0

# Chassis parameters
floor_thickness = 5.0
wall_thickness = 4.0

# --- Helper Functions ---

def create_hull_profile(pts):
    """Creates a smooth profile from points using splines."""
    return (
        cq.Workplane("XY")
        .spline(pts)
        .close()
    )

# --- Building the Model ---

# 1. Base shape (the overall volume)
# We will create a lofted shell to approximate the organic curves.

# Define cross-sections along the length
# Front section (narrower, split look)
s1 = cq.Workplane("YZ").workplane(offset=-length/2).rect(front_width * 0.6, height * 0.4)
s2 = cq.Workplane("YZ").workplane(offset=-length/2 + 20).rect(front_width * 0.8, height * 0.7)

# Middle section (wider, flatter floor)
s3 = cq.Workplane("YZ").workplane(offset=-20).rect(width, height * 0.6)
s4 = cq.Workplane("YZ").workplane(offset=20).rect(width, height * 0.65)

# Rear section (taller, boxier)
s5 = cq.Workplane("YZ").workplane(offset=length/2 - 20).rect(width * 0.9, rear_height)
s6 = cq.Workplane("YZ").workplane(offset=length/2).rect(width * 0.7, rear_height * 0.8)

# Lofting the main body
# Since basic lofting can be tricky with differing vertex counts, we'll model the 
# main hull as a central block with carving operations for robustness, 
# or use a simplified extrusion with fillets which is safer for generated code.

# Let's try a "Block and Carve" approach which is more reliable for this specific shape
# than a complex multi-section loft without precise point control.

# Start with a main block representing the bounding box
main_body = cq.Workplane("XY").box(length, width, height)

# 2. Shaping the Hull (Side Profile)
# We cut away the bottom to give it the curvature
side_cut_pts = [
    (-length/2, -height/2),
    (-length/3, -height/2 + 10),
    (0, -height/2 + 5),
    (length/3, -height/2 + 8),
    (length/2, -height/2 + 15),
    (length/2, height),
    (-length/2, height)
]
side_cutter = (
    cq.Workplane("XZ")
    .polyline(side_cut_pts)
    .close()
    .extrude(width + 20, both=True)
)

# Apply side cut (actually, we want to keep the intersection or cut away the inverse)
# Let's sculpt the outer shape first.

# Create the top-down silhouette
top_pts = [
    (-length/2, width/4),
    (-length/4, width/2),
    (length/4, width/2),
    (length/2, width/2.5),
    (length/2, -width/2.5),
    (length/4, -width/2),
    (-length/4, -width/2),
    (-length/2, -width/4),
]
top_silhouette = (
    cq.Workplane("XY")
    .polyline(top_pts)
    .close()
    .extrude(height * 2)
    .translate((0, 0, -height))
)

# Create a side silhouette for the rocker/bottom curve
side_pts = [
    (-length/2, height/2), # Top front
    (length/2, rear_height), # Top rear
    (length/2, -rear_height/2 + 10), # Bottom rear
    (length/4, -height/2), # Bottom mid
    (-length/4, -height/2), # Bottom mid
    (-length/2, -height/2 + 15), # Bottom front
    (-length/2, height/2) # Close
]
side_silhouette = (
    cq.Workplane("XZ")
    .polyline(side_pts)
    .close()
    .extrude(width * 2, both=True)
)

# Intersect to get the rough blank
hull = top_silhouette.intersect(side_silhouette)

# 3. Hollowing out the interior (The "Cockpit" and rear bay)
# We shell the object or cut a smaller version from the inside.
# Given the complex dividers, cutting is better.

inner_cutout = (
    cq.Workplane("XY")
    .polyline([
        (-length/2 + 10, width/4 - wall_thickness),
        (-length/4, width/2 - wall_thickness),
        (length/4, width/2 - wall_thickness),
        (length/2 - 5, width/2.5 - wall_thickness),
        (length/2 - 5, -(width/2.5 - wall_thickness)),
        (length/4, -(width/2 - wall_thickness)),
        (-length/4, -(width/2 - wall_thickness)),
        (-length/2 + 10, -(width/4 - wall_thickness)),
    ])
    .close()
    .extrude(height * 2)
    .translate((0, 0, -height + floor_thickness + 10)) # Move up to leave floor
)

hull = hull.cut(inner_cutout)

# 4. Creating the "Split" in the front nose
# The image shows a deep channel running down the center front.
front_split = (
    cq.Workplane("XY")
    .rect(length/2, 15)
    .extrude(height * 2)
    .translate((-length/4 - 10, 0, -height))
)
hull = hull.cut(front_split)

# 5. Adding the structural ribs/bulkheads
# The image shows vertical plates dividing the sections.

# Bulkhead 1 (Front/Mid transition)
bulkhead1 = (
    cq.Workplane("YZ")
    .rect(width - 2*wall_thickness, height)
    .extrude(2)
    .translate((-length/4, 0, 0))
    .intersect(side_silhouette) # Trim to outer shape
)
# Cut a U-shape out of the bulkhead for pass-through
pass_through = (
    cq.Workplane("YZ")
    .rect(width/3, height)
    .extrude(10, both=True)
    .translate((-length/4, 0, 10))
)
bulkhead1 = bulkhead1.cut(pass_through)

# Bulkhead 2 (Mid/Rear transition)
bulkhead2 = (
    cq.Workplane("YZ")
    .rect(width - 2*wall_thickness, height * 1.5)
    .extrude(2)
    .translate((length/4, 0, 10))
    .intersect(side_silhouette)
)
# Cut a circular pass-through
rear_hole = (
    cq.Workplane("YZ")
    .circle(15)
    .extrude(10, both=True)
    .translate((length/4, 0, 10))
)
bulkhead2 = bulkhead2.cut(rear_hole)

# Add bulkheads to hull
hull = hull.union(bulkhead1).union(bulkhead2)

# 6. Side Vents / Gills details
# The image shows angled slots on the front flanks.

def create_gills(x_pos, y_side, angle):
    gills = cq.Workplane("XY")
    for i in range(3):
        gill = (
            cq.Workplane("XY")
            .rect(5, 20)
            .extrude(20)
            .rotate((0,0,0), (0,0,1), angle)
            .rotate((0,0,0), (1,0,0), 45 if y_side > 0 else -45) # Tilt inward
            .translate((x_pos - i*8, y_side * (width/2 - 2), 0))
        )
        gills = gills.union(gill)
    return gills

front_gills_left = create_gills(-length/3, 1, 20)
front_gills_right = create_gills(-length/3, -1, -20)

hull = hull.cut(front_gills_left).cut(front_gills_right)

# 7. Rear side details (vertical slots)
# The image has some rectangular cutouts in the rear sidewalls.

rear_slots_left = (
    cq.Workplane("YZ")
    .rect(5, 20)
    .extrude(10)
    .translate((length/2 - 15, width/2 - 2, 10))
)
rear_slots_right = (
    cq.Workplane("YZ")
    .rect(5, 20)
    .extrude(10)
    .translate((length/2 - 15, -width/2 + 2, 10))
)
# Cut them through the walls
hull = hull.cut(rear_slots_left).cut(rear_slots_right)


# 8. Refine the nose
# The nose has a distinct scoop shape. We'll chamfer/fillet the front edges.
# Note: Filleting complex BRep intersections can be fragile in kernels, 
# so we will use a boolean subtraction to shape the nose tips.

nose_shaper = (
    cq.Workplane("YZ")
    .moveTo(0, -height)
    .lineTo(width, height)
    .lineTo(-width, height)
    .close()
    .extrude(20)
    .translate((-length/2, 0, 0))
)
hull = hull.cut(nose_shaper)

# 9. Wheel wells / Undercut
# The image suggests open areas at the bottom for wheels or propulsion.
wheel_cutout_front = (
    cq.Workplane("XZ")
    .circle(15)
    .extrude(width + 10, both=True)
    .translate((-length/3, -height/2, 0))
)
wheel_cutout_rear = (
    cq.Workplane("XZ")
    .circle(18)
    .extrude(width + 10, both=True)
    .translate((length/3, -height/2, 0))
)

hull = hull.cut(wheel_cutout_front).cut(wheel_cutout_rear)

# 10. Final Polish
# Add the vertical fins/antennas seen on the front corners
fin = (
    cq.Workplane("YZ")
    .polyline([(0,0), (2,0), (1, 25), (0, 25)])
    .close()
    .extrude(2)
)

left_fin = fin.translate((-length/2 + 5, width/2 - 5, 0))
right_fin = fin.translate((-length/2 + 5, -width/2 + 3, 0))

result = hull.union(left_fin).union(right_fin)

# Rotate to match image orientation roughly (Iso view is standard, but let's align logic)
# No rotation needed, standard Isometric view will show it well.
import cadquery as cq

# --- Parameters ---
# Back plate dimensions
plate_length = 60.0
plate_height = 20.0
plate_thickness = 2.0

# Clip dimensions
clip_outer_radius = 8.0
clip_wall_thickness = 2.0
clip_height = 20.0  # Matches plate height
clip_opening_angle = 60.0  # Degrees
clip_distance_from_plate = 15.0 # Center of clip to face of plate

# Rib/Support dimensions
rib_thickness = 2.0

# --- Modeling ---

# 1. Create the Back Plate
# We'll center it on the YZ plane, extruded along X
plate = cq.Workplane("YZ").rect(plate_length, plate_height).extrude(plate_thickness)

# 2. Create the C-Clip
# Center of the clip relative to the origin (assuming plate front face is at X=plate_thickness/2)
clip_center_x = plate_thickness/2 + clip_distance_from_plate

# Create the profile of the C-clip
# We draw a full tube first, then cut the opening
clip = (cq.Workplane("XY")
        .workplane(offset=-clip_height/2) # Start at bottom
        .center(clip_center_x, 0)
        .circle(clip_outer_radius)
        .circle(clip_outer_radius - clip_wall_thickness)
        .extrude(clip_height)
        )

# Create a cutout wedge for the "C" shape opening
# The opening faces towards the plate (negative X direction relative to clip center) or away?
# Looking at the image, the opening faces AWAY from the plate (positive X).
# Wait, let's look closer. The curve is attached to the plate via ribs. 
# The opening is on the side *opposite* the plate.
# Actually, looking at the crop, the opening is facing towards the "left" of the image relative to the plate.
# Let's re-orient.
# Let's assume Plate is in XZ plane. Y is depth.
# Let's stick to the previous coordinate system: Plate in YZ plane. X is normal to plate.
# Plate is at X=0 to X=2.
# Clip center is at X=17.
# The supports connect the plate to the *back* of the clip.
# The opening of the clip is facing +X direction (away from plate).

cutout_size = clip_outer_radius * 2
cutout = (cq.Workplane("XY")
          .workplane(offset=-clip_height/2)
          .center(clip_center_x, 0)
          .moveTo(0, 0)
          .lineTo(cutout_size, cutout_size) # Large enough to cut through
          .lineTo(cutout_size, -cutout_size)
          .close()
          .extrude(clip_height)
          )

# Rotate cutout to face the correct direction (away from plate, +X)
# The wedge defined above points roughly +X. Let's refine the cutout geometry for a specific angle.
# Better way: define a wedge shape for subtraction.
wedge = (cq.Workplane("XY")
         .workplane(offset=-clip_height/2)
         .center(clip_center_x, 0)
         .moveTo(0,0)
         .lineTo(clip_outer_radius*1.5, clip_outer_radius) # Arbitrary large coord
         .lineTo(clip_outer_radius*1.5, -clip_outer_radius)
         .close()
         .extrude(clip_height)
         )

# Apply the cut to make the 'C' shape
# We want a specific opening width or angle. Let's use a simple box cut for the opening 
# if it's a parallel opening, or a wedge for an angular one. 
# The image shows a gap. Let's assume a straight cut for the gap.
gap_width = (clip_outer_radius - clip_wall_thickness) * 1.0 # Heuristic
gap_cut = (cq.Workplane("XY")
           .workplane(offset=-clip_height/2)
           .center(clip_center_x + clip_outer_radius, 0) # Position at the front edge
           .box(clip_outer_radius, gap_width, clip_height)
           )

# Let's rebuild the clip with a cleaner approach: Arc
clip_wire = (cq.Workplane("XY")
             .workplane(offset=-clip_height/2)
             .center(clip_center_x, 0)
             .threePointArc((clip_outer_radius, 0), (0, clip_outer_radius)) # Just to init arc mode correctly? No.
             # Let's use 2D boolean to make the shape profile
             )
             
# Solid modeling approach usually safer
clip_solid = (cq.Workplane("XY")
        .workplane(offset=-clip_height/2)
        .center(clip_center_x, 0)
        .circle(clip_outer_radius)
        .circle(clip_outer_radius - clip_wall_thickness)
        .extrude(clip_height)
        )

# Cut the opening. The opening faces Positive X (away from plate).
# We cut a slot through the +X side.
opening_cut = (cq.Workplane("XY")
               .workplane(offset=-clip_height/2)
               .center(clip_center_x, 0)
               .moveTo(0, 0)
               .lineTo(clip_outer_radius*2, gap_width/2)
               .lineTo(clip_outer_radius*2, -gap_width/2)
               .close()
               .extrude(clip_height)
               )

clip_final = clip_solid.cut(opening_cut)

# 3. Create the Supports (Ribs)
# Looking at the image, there is a central rib and angled side ribs, forming a triangle shape
# connecting the tangent of the clip to the plate.
# Actually, it looks like two walls extending from the plate tangentially to the clip.
# Let's make a sketch on the Top (XY) plane and extrude it.

# Calculate tangent points or just connect comfortably.
# It looks like a "V" shape coming from the plate center to the sides of the clip.
# Or a "T" shape rib. Let's look at the junction.
# It seems there is a central rib perpendicular to the plate, and two side walls 
# that are tangent to the clip circle.
# Let's interpret it as a trapezoidal volume or two ribs.
# Image shows: A flat rib in the middle? No, it looks like a hollow triangle.
# It looks like two ribs starting from the plate center-line and going to the clip tangent.
# But there is also a rib perpendicular to the plate in the middle? No, that looks like the back of the clip circle.
# Let's assume two ribs forming a triangle with the plate.

# Points for the support polygon
# P1: On plate, slightly offset from center (Y+)
# P2: On plate, slightly offset from center (Y-)
# P3: Tangent to clip (Y-)
# P4: Tangent to clip (Y+)

# Let's simply draw a triangle and cut out the inside, or draw the walls.
# The support connects the flat face of the plate to the cylindrical back of the clip.
support_sketch = (cq.Workplane("XY")
                  .workplane(offset=-clip_height/2)
                  .moveTo(plate_thickness/2, 0) # Start at plate center face
                  .lineTo(plate_thickness/2, plate_height/3) # Go up along plate
                  .lineTo(clip_center_x, clip_outer_radius) # Go to clip tangent (approx)
                  .lineTo(clip_center_x, -clip_outer_radius) # Go to other tangent
                  .lineTo(plate_thickness/2, -plate_height/3) # Back to plate
                  .close()
                  .extrude(clip_height)
                  )

# Now we need to hollow this out or boolean it.
# The image shows a "web" structure. A central rib and two side ribs? 
# It looks like a simplified extrusion of a shape that includes the clip and the connector.

# Let's try a merged profile approach.
# 1. Circle for clip
# 2. Trapezoid connecting clip to plate
# 3. Subtract inner circle
# 4. Subtract inner triangle

final_profile_sketch = (cq.Workplane("XY")
    .workplane(offset=-plate_height/2)
    
    # Outer hull
    .moveTo(plate_thickness/2, 0)
    .lineTo(plate_thickness/2, 6.0) # Base on plate
    .lineTo(clip_center_x, clip_outer_radius) # Connect to clip side
    .radiusArc((clip_center_x, -clip_outer_radius), clip_outer_radius) # Arc around clip front
    .lineTo(plate_thickness/2, -6.0) # Back to plate base
    .close()
    
    # Inner Cutout for Clip
    .moveTo(clip_center_x, 0)
    .circle(clip_outer_radius - clip_wall_thickness)
    
    # Inner Cutout for Support (Triangular void)
    .moveTo(plate_thickness/2 + rib_thickness, 0) # Start near plate
    .lineTo(plate_thickness/2 + rib_thickness, 6.0 - rib_thickness*1.5) 
    .lineTo(clip_center_x - (clip_outer_radius - clip_wall_thickness) + 1, 0) # Tip of triangle near clip
    .lineTo(plate_thickness/2 + rib_thickness, -(6.0 - rib_thickness*1.5))
    .close()
)

# This is getting complex with automatic booleans in 2D. 
# Let's stick to constructive solid geometry (CSG) which is more robust in CQ.

# Step A: Plate
part_plate = cq.Workplane("YZ").rect(plate_length, plate_height).extrude(plate_thickness)
# Move plate to have face at X=0
part_plate = part_plate.translate((-plate_thickness/2, 0, 0))

# Step B: The Clip (Cylinder)
part_clip = (cq.Workplane("XY")
             .workplane(offset=-clip_height/2)
             .center(clip_distance_from_plate, 0)
             .circle(clip_outer_radius)
             .extrude(clip_height)
             )

# Step C: The Connector (Trapezoid extrude)
# Vertices for the connector
p1 = (0, 7.0) # On plate
p2 = (clip_distance_from_plate, clip_outer_radius * 0.8) # On clip
p3 = (clip_distance_from_plate, -clip_outer_radius * 0.8)
p4 = (0, -7.0)

connector = (cq.Workplane("XY")
             .workplane(offset=-clip_height/2)
             .polyline([p1, p2, p3, p4])
             .close()
             .extrude(clip_height)
             )

# Step D: Fuse basic shapes
combined = part_plate.union(part_clip).union(connector)

# Step E: Hollow out the clip
hollow_cylinder = (cq.Workplane("XY")
             .workplane(offset=-clip_height/2)
             .center(clip_distance_from_plate, 0)
             .circle(clip_outer_radius - clip_wall_thickness)
             .extrude(clip_height)
             )

# Step F: Cut the clip opening
opening_box = (cq.Workplane("XY")
               .workplane(offset=-clip_height/2)
               .center(clip_distance_from_plate + clip_outer_radius, 0)
               .box(clip_outer_radius, 8.0, clip_height) # Width 8.0 for the gap
               )

# Step G: Hollow out the connector (The triangular void)
# We create a smaller trapezoid inside
t_gap = rib_thickness
void_p1 = (t_gap, 7.0 - t_gap)
void_p2 = (clip_distance_from_plate - clip_outer_radius + clip_wall_thickness, 0) # Point towards clip
void_p3 = (t_gap, -(7.0 - t_gap))

connector_void = (cq.Workplane("XY")
                  .workplane(offset=-clip_height/2)
                  .polyline([void_p1, void_p2, void_p3])
                  .close()
                  .extrude(clip_height)
                  )

# Step H: Add the central stiffener rib shown in image?
# Looking closely at the image, inside the triangular void, there is a vertical line.
# It looks like the support is actually split into two separate compartments or there is a rib.
# Wait, looking at the crop, the void is a single triangle. 
# The line visible is the tangent edge of the cylinder inside the void.
# So a single triangular cut is sufficient.

# Perform Boolean Operations
result = combined.cut(hollow_cylinder).cut(opening_box).cut(connector_void)

# Re-centering the whole object for better presentation
# Currently X starts at -1. Y is centered. Z is 0 to 20.
result = result.translate((0, 0, -clip_height/2)) # Center Z
result = result.rotate((0,0,0), (0,0,1), -90) # Rotate to match image view (Plate along X roughly)
# Actually, image view: Plate runs along X/Y diagonal, Z is up. 
# Default view in generic CAD is usually Isometric.
# Let's leave orientation standard. Plate in YZ plane, Extrusion along X.

# Refinement on the "C" opening lips
# The image shows rounded lips on the C-clamp.
# Let's add fillets to the opening edges.
try:
    result = result.edges("|Z").select(lambda e: e.center().x > clip_distance_from_plate).fillet(0.5)
except:
    pass # Skip if geometry is tricky


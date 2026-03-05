import cadquery as cq

# --- Parameters ---
# Main large plate
main_plate_length = 150.0
main_plate_width = 60.0
main_plate_thickness = 10.0

# Secondary mounting plate
mount_plate_length = 120.0  # Slightly narrower than main plate
mount_plate_width = 40.0
mount_plate_thickness = 10.0

# Triangular Gussets
gusset_thickness = 6.0
gusset_height = mount_plate_width  # Full width of the mount plate
gusset_base_len = 30.0  # How far they extend on the mount plate

# Holes
hole_diameter = 8.0
cbore_diameter = 14.0
cbore_depth = 3.0

# --- Geometry Construction ---

# 1. Create the Main Plate
main_plate = (
    cq.Workplane("XY")
    .box(main_plate_length, main_plate_width, main_plate_thickness)
)

# Add holes to Main Plate
main_plate = (
    main_plate
    .faces(">Z")
    .workplane()
    .pushPoints([(main_plate_length/2 - 25, 0), (-main_plate_length/2 + 25, 0)])
    .cboreHole(hole_diameter, cbore_diameter, cbore_depth)
)

# 2. Create the Mounting Plate
# It is attached to the side of the main plate.
# We position it centered relative to the main plate's length, but offset in Y.
mount_plate = (
    cq.Workplane("XY")
    .box(mount_plate_length, mount_plate_width, mount_plate_thickness)
    .translate((0, (main_plate_width/2 + mount_plate_width/2), 0)) # Position it adjacent
)

# Add holes to Mounting Plate
# 3 holes visible in the image on the back plate
mount_plate = (
    mount_plate
    .faces(">Z")
    .workplane()
    .pushPoints([(0, 0), (mount_plate_length/2 - 20, 0), (-mount_plate_length/2 + 20, 0)])
    .cboreHole(hole_diameter, cbore_diameter, cbore_depth)
)

# 3. Create Triangular Gussets (Ribs)
# These connect the two plates for stiffness.
# There appear to be two gussets located between the holes on the mount plate.

def create_gusset():
    # Sketch a triangle on the YZ plane (side view relative to the plates)
    # The triangle connects the top of the main plate to the top of the mount plate
    # or slopes down. Based on image, it looks like a flat connection with a slope.
    
    # Let's model it as a wedge shape.
    pts = [
        (0, 0),
        (mount_plate_width, 0),
        (0, main_plate_thickness/2 + 5) # Slight height above surface or flush? 
        # Actually, looking closer at the image, the ribs are triangular prisms
        # sitting on top of the mounting plate, butting against the main plate.
    ]
    
    # Revised strategy for gussets:
    # They are triangular ribs.
    # Height = thickness of plates roughly.
    # Base = width of mount plate.
    
    return (
        cq.Workplane("YZ")
        .moveTo(main_plate_width/2, main_plate_thickness/2) # Start at edge of main plate, top surface
        .lineTo(main_plate_width/2 + mount_plate_width, -mount_plate_thickness/2) # Go to far edge, bottom corner?
        # Let's try a simpler shape fitting the visual
        .polyline([
            (main_plate_width/2, main_plate_thickness/2), # Top edge of main plate
            (main_plate_width/2 + mount_plate_width * 0.8, main_plate_thickness/2), # Top surface of mount plate
            (main_plate_width/2, -mount_plate_thickness/2) # Bottom corner of join
        ])
        .close()
        .extrude(gusset_thickness/2, both=True) # Extrude symmetric
    )

# Actually, the image shows the ribs are tapering *away* from the main plate.
# The thickest part is at the junction between the two plates.
gusset_shape = (
    cq.Workplane("YZ")
    .polyline([
        (main_plate_width/2, main_plate_thickness/2), # Top corner at junction
        (main_plate_width/2, -main_plate_thickness/2), # Bottom corner at junction
        (main_plate_width/2 + mount_plate_width, -mount_plate_thickness/2) # Far corner bottom
    ])
    .close()
    .extrude(gusset_thickness)
    # Rotate to orient correctly
    # The extrusion happened along X, centered at origin? No, workplane YZ extrudes along X.
)

# Let's build the gusset in place using the coordinate system
# The gap between holes on mount plate is roughly 40mm each side of center.
# We'll place gussets at +/- 25mm X.

gusset_l = (
    cq.Workplane("XY")
    .workplane(offset=main_plate_thickness/2) # Top surface
    .moveTo(-25, main_plate_width/2)
    .lineTo(-25 - gusset_thickness, main_plate_width/2)
    .lineTo(-25 - gusset_thickness/2, main_plate_width/2 + mount_plate_width)
    .close()
    .extrude(-main_plate_thickness) # Extrude downwards
    # Wait, the gusset in the image is a vertical rib, triangular in profile (side view).
)

# Third attempt at Gussets - simplest geometric approach
# It's a wedge.
gusset_pts = [
    (0, 0),
    (mount_plate_width, 0),
    (0, main_plate_thickness)
]

base_rib = (
    cq.Workplane("YZ")
    .polyline(gusset_pts)
    .close()
    .extrude(gusset_thickness)
    # Position: The 90 deg corner is at (0,0).
    # We need to rotate and move it.
    .rotate((0,0,0), (1,0,0), -90) # Rotate to lay flat? No.
    .rotate((0,0,0), (0,0,1), 180) # Flip around Z
    .translate((0, main_plate_width/2 + mount_plate_width, -main_plate_thickness/2))
)

# Create specific left and right ribs
rib_offset = 35.0
rib_left = base_rib.translate((-rib_offset, 0, 0))
rib_right = base_rib.translate((rib_offset - gusset_thickness, 0, 0))


# 4. Refined approach using a single UNION operation for cleanliness
# Let's rebuild the assembly as a single object from the start or union them.

final_part = main_plate.union(mount_plate)

# Add the triangular ribs
# Define the rib profile on the side (YZ plane)
# The rib starts at the junction (Y = main_plate_width/2) and goes to Y = main_plate_width/2 + mount_plate_width
# The rib height is Z = main_plate_thickness/2 down to something?
# Looking at the image: The rib connects the side wall of the large plate to the top face of the small plate.
# Wait, the plates are likely flush on the BOTTOM.
# If they are flush on bottom, the rib is on TOP of the secondary plate.

# Let's assume bottom flush.
# Main plate Z: 0 to 10
# Mount plate Z: 0 to 10
# Rib sits on Mount plate Z=10.
# Rib connects to Main plate side wall.

rib_height = 8.0 # Height of rib at the main plate wall
rib_len = mount_plate_width * 0.7

rib_geo = (
    cq.Workplane("YZ")
    .polyline([
        (main_plate_width/2, main_plate_thickness/2), # Top edge of mount plate at junction
        (main_plate_width/2, main_plate_thickness/2 + rib_height), # Up the wall of main plate?
        # The image shows the main plate is THICKER or the ribs are flush with top of main plate?
        # The image implies both plates are same thickness.
        # The ribs appear to reinforce the corner.
        # Let's look really closely.
        # It looks like a T-joint. The narrower plate butts into the wider plate.
        # The ribs are triangular fillets in the corner.
    ])
)

# Correct Interpretation:
# Two rectangular plates forming a T-shape. They are likely same thickness.
# The "Mount Plate" is attached to the SIDE of the "Main Plate".
# The ribs are triangular stiffeners on the top surface.

# Re-establishing dimensions
t = 12.0 # Thickness
w1 = 60.0 # Main plate width
l1 = 160.0 # Main plate length
w2 = 50.0 # Mount plate width (extension length)
l2 = 100.0 # Mount plate length (along the main plate)

# Base T-shape
part = (
    cq.Workplane("XY")
    .box(l1, w1, t)
)

extension = (
    cq.Workplane("XY")
    .box(l2, w2, t)
    .translate((0, w1/2 + w2/2, 0))
)
part = part.union(extension)

# Holes
# Main plate holes
part = (
    part.faces(">Z").workplane()
    .pushPoints([(l1/2 - 25, 0), (-l1/2 + 25, 0)])
    .cboreHole(8, 14, 4)
)

# Extension plate holes
# Image shows 3 holes in a line or pattern on the extension?
# Actually, looking at the crop, it looks like:
# One big plate (foreground), one smaller plate (background/left).
# Let's stick to the T-shape interpretation, it matches best.
# Holes on extension:
part = (
    part.faces(">Z").workplane()
    # Shift workplane origin to center of extension
    .center(0, w1/2 + w2/2)
    .pushPoints([(0, 0), (35, 0), (-35, 0)])
    .cboreHole(8, 14, 4)
)

# Ribs
# Triangular ribs placed on top of the extension, against the main plate side.
# They are between the holes.
rib_spacing = 22.0 # Offset from center
rib_width = 8.0

def make_rib(x_pos):
    # Draw on YZ plane
    return (
        cq.Workplane("YZ")
        .moveTo(w1/2, t/2) # Start at junction top corner
        .lineTo(w1/2 + w2*0.8, -t/2 + t) # Slope down to surface of extension
        .lineTo(w1/2, -t/2 + t) # Back to junction at surface level
        .close()
        .extrude(rib_width/2, both=True) # Center the extrusion
        .translate((x_pos, 0, t)) # Move up to sit on top surface? No.
        # The points were defined relative to global origin.
        # (w1/2, t/2) is top-right corner of main plate cross section.
        # We need the rib to sit ON TOP of the extension plate (z=t/2)
        # And against the side of the main plate?
        # NO, looking at shading, the whole assembly is flat on top mostly?
        # Actually, the rib connects the vertical face of the Main Plate to the top face of the Extension.
        # But wait, if they are the same thickness (t), there is no vertical face above the extension.
        
        # ALTERNATE INTERPRETATION: Step-down or L-bracket.
        # The "Main Plate" is thicker or higher.
        # The image shows a continuous top surface on the left...
        # Let's assume the Main Plate (front right in image) is THICKER than the back plate? 
        # Or it's a LAP JOINT.
        
        # Let's go with the most standard CAD exercise interpretation:
        # A T-bracket where the back plate is thinner or lower, allowing ribs.
        # OR: Both are same thickness, but the ribs are actually part of the casting/molding 
        # that taper down.
    )

# Let's try "Ribs as fillets" interpretation on a flat T-plate. 
# It doesn't make sense unless there is height difference.
# Let's look at the shadows. The ribs cast shadows. They protrude upwards.
# This means the Main Plate must be TALLER (in Z) than the extension, 
# OR the Main Plate is the vertical part of an L-bracket? 
# No, it looks flat.
# The most logical geometric interpretation for this specific render style:
# It is a flat T-plate. The ribs are simple extruded triangles sitting on top of the surface. 
# While mechanically weird (stress concentrations), it matches the visual of "triangular prism on a plate".

rib_shape = (
    cq.Workplane("YZ")
    .polyline([(0,0), (w2*0.6, 0), (0, 15)]) # 15mm high against main plate
    .close()
    .extrude(rib_width/2, both=True)
    .translate((0, w1/2, t/2)) # Position: On top surface (t/2), at edge (w1/2)
)

part = part.union(rib_shape.translate((rib_spacing, 0, 0)))
part = part.union(rib_shape.translate((-rib_spacing, 0, 0)))

result = part
import cadquery as cq

# --- Parameters ---

# General Plate Thickness
plate_thickness = 5.0

# --- NEMA 17 Style Square Motor Mount (Right Part) ---
nema_side = 42.0          # Typical NEMA 17 width
nema_corner_rad = 3.0     # Radius of the corners
nema_center_hole = 22.0   # Center pilot hole diameter
nema_bolt_spacing = 31.0  # Center-to-center hole distance
nema_mount_hole = 3.5     # M3 clearance hole

# Secondary small holes on the square plate (looks like endstop mounting)
small_hole_dia = 2.5
small_hole_offset_x = 12.0
small_hole_offset_y = 12.0 # Just inside the corner

# --- T-Shaped / Carriage Plate (Left Part) ---
# This part seems to combine a NEMA mount pattern with linear bearing blocks or similar attachment points.
# It shares the central NEMA 17 pattern.

carriage_width_total = 85.0
carriage_height = 45.0  # Main body height
carriage_center_y = 0.0

# The NEMA mount section is often slightly lower or centered. 
# Based on image, the large hole is central to a square-ish area.
nema_mount_center_x = 0.0 

# Wing/Flange dimensions
wing_width = (carriage_width_total - nema_side) / 2.0
wing_hole_dia = 5.5 # M5 clearance (likely for V-wheels or mounting)
wing_hole_spacing_x = 65.0 # Distance between outer wing holes

# Notch cutout on the right side of the T-plate
notch_width = 15.0
notch_height = 15.0

# --- Geometry Construction ---

# 1. Create the Square Motor Mount (Right Part)
square_mount = (
    cq.Workplane("XY")
    .box(nema_side, nema_side, plate_thickness)
    .edges("|Z").fillet(nema_corner_rad)
    # Center pilot hole
    .faces(">Z").workplane().circle(nema_center_hole / 2).cutThruAll()
    # Mounting holes (NEMA 17 standard pattern)
    .faces(">Z").workplane()
    .rect(nema_bolt_spacing, nema_bolt_spacing, forConstruction=True)
    .vertices()
    .hole(nema_mount_hole)
    # Extra small holes (as seen in image on one side)
    .faces(">Z").workplane()
    .pushPoints([(-15, 15), (-10, 15)]) # Approximate locations based on visual
    .hole(small_hole_dia)
)

# 2. Create the T-Shaped Carriage Plate (Left Part)
# We will build this using a 2D sketch and extruding

# Base rectangle
base_sketch = (
    cq.Sketch()
    .rect(carriage_width_total, nema_side) # Main width, NEMA height
    .vertices().fillet(nema_corner_rad)
)

# Cutout for the "step" on the right side
# The image shows the right side is stepped down or cut out
# Let's subtract a rectangle from the top right corner area
# Actually, looking closer, it looks like a T-shape where the right side has a notch.
# Let's model it as a union of shapes or a subtractive process.

carriage_plate = (
    cq.Workplane("XY")
    # Start with the full bounding box
    .box(carriage_width_total, nema_side, plate_thickness)
    # Round corners
    .edges("|Z").fillet(nema_corner_rad)
    # Cut the notch on the top right
    .faces(">Z").workplane()
    .moveTo(carriage_width_total/2, nema_side/2)
    .rect(20, 20, centered=True) # Cut corner
    .cutBlind(-plate_thickness)
)

# Refine the shape: It's more of a wide plate with a cutout
# Let's rebuild the specific shape more accurately
# Center part is NEMA 17 size. Wings extend left and right.
# Right wing has a cutout.

# Simplified approach: Create base shape, drill holes.
carriage_plate = (
    cq.Workplane("XY")
    .rect(carriage_width_total, nema_side)
    .extrude(plate_thickness)
    .edges("|Z").fillet(nema_corner_rad)
)

# Create the notch on the right side
notch = (
    cq.Workplane("XY")
    .moveTo(carriage_width_total/2, nema_side/2)
    .rect(25, 25, centered=True) # Over-sized rect to cut corner
    .extrude(plate_thickness)
)
carriage_plate = carriage_plate.cut(notch)

# Add Holes to Carriage Plate
carriage_plate = (
    carriage_plate
    # Center Large Hole
    .faces(">Z").workplane()
    .circle(nema_center_hole / 2).cutThruAll()
    # NEMA Mounting Holes
    .faces(">Z").workplane()
    .rect(nema_bolt_spacing, nema_bolt_spacing, forConstruction=True)
    .vertices()
    .hole(nema_mount_hole)
    # Outer Wing Holes (Likely for wheels/eccentric spacers)
    .faces(">Z").workplane()
    .pushPoints([(-30, 0), (28, -10)]) # Asymmetric placement based on image
    .hole(wing_hole_dia)
    # Extra small mounting holes
    .faces(">Z").workplane()
    .pushPoints([(-15, 0)]) 
    .hole(3.0)
)


# --- Assembly ---
# Move the square mount to the right to match the image layout
square_mount_moved = square_mount.translate((70, 20, 0))

# Combine into one result for visualization
result = carriage_plate.union(square_mount_moved)

if __name__ == "__main__":
    # If running in CQ-editor, this will show the model
    try:
        show_object(result)
    except NameError:
        pass # Not in CQ-editor
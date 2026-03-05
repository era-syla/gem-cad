import cadquery as cq

# Parametric dimensions
plate_width = 120.0
plate_height = 60.0
plate_thickness = 2.0

# Slit parameters
slit_width = 1.0
slit_height = plate_height * 0.5  # Slits go halfway up
slit_spacing = plate_width / 3.0  # Divide plate into thirds

# Calculate positions
# Local Y coordinate for the center of the slit rectangle (sketch plane)
# The slit starts at the bottom (-plate_height/2) and extends up by slit_height
slit_center_y = -plate_height / 2 + slit_height / 2

# X coordinates for the two slits relative to center
slit_pos_x = slit_spacing / 2.0

# Generate 3D model
result = (
    cq.Workplane("XZ")  # Create plate standing vertically
    .box(plate_width, plate_height, plate_thickness)
    .faces(">Y")        # Select the front face
    .workplane()
    .pushPoints([(-slit_pos_x, slit_center_y), (slit_pos_x, slit_center_y)])
    .rect(slit_width, slit_height)
    .cutThruAll()       # Cut the slots through the plate
)
import cadquery as cq

# --- Parametric Dimensions ---

# Main Face Dimensions
face_radius = 50.0
plate_thickness = 5.0

# Facial Features Dimensions
eye_radius = 12.0
eye_offset_x = 22.0
eye_offset_y = 15.0

nose_radius = 8.0
nose_offset_y = -10.0

mouth_width = 40.0
mouth_height = 8.0
mouth_offset_y = -35.0

# Ear Dimensions
# Left Ear (Viewer's Left: Shorter and wider)
ear_l_width_radius = 18.0
ear_l_height_radius = 26.0
ear_l_center_x = -32.0
ear_l_center_y = 42.0
ear_l_rotation = 20.0  # Degrees, tilts top to the left

# Right Ear (Viewer's Right: Taller and narrower)
ear_r_width_radius = 15.0
ear_r_height_radius = 52.0
ear_r_center_x = 28.0
ear_r_center_y = 55.0
ear_r_rotation = -15.0 # Degrees, tilts top to the right

# --- Geometry Construction ---

# 1. Base Face
# Create the main circular face
face = cq.Workplane("XY").circle(face_radius).extrude(plate_thickness)

# 2. Ears
# Construct the Left Ear
ear_l = (
    cq.Workplane("XY")
    .ellipse(ear_l_width_radius, ear_l_height_radius)
    .extrude(plate_thickness)
    .rotate((0, 0, 0), (0, 0, 1), ear_l_rotation)
    .translate((ear_l_center_x, ear_l_center_y, 0))
)

# Construct the Right Ear
ear_r = (
    cq.Workplane("XY")
    .ellipse(ear_r_width_radius, ear_r_height_radius)
    .extrude(plate_thickness)
    .rotate((0, 0, 0), (0, 0, 1), ear_r_rotation)
    .translate((ear_r_center_x, ear_r_center_y, 0))
)

# Union the ears to the face to create the main solid body
body = face.union(ear_l).union(ear_r)

# 3. Create Cutting Tools
# We create separate solids for the features and subtract them from the body

# Eyes Tool
eyes_tool = (
    cq.Workplane("XY")
    .pushPoints([(-eye_offset_x, eye_offset_y), (eye_offset_x, eye_offset_y)])
    .circle(eye_radius)
    .extrude(plate_thickness * 2) # Extrude extra to ensure clean cut
    .translate((0, 0, -plate_thickness / 2)) # Center vertically relative to plate
)

# Nose Tool
nose_tool = (
    cq.Workplane("XY")
    .center(0, nose_offset_y)
    .circle(nose_radius)
    .extrude(plate_thickness * 2)
    .translate((0, 0, -plate_thickness / 2))
)

# Mouth Tool
mouth_tool = (
    cq.Workplane("XY")
    .center(0, mouth_offset_y)
    .rect(mouth_width, mouth_height)
    .extrude(plate_thickness * 2)
    .translate((0, 0, -plate_thickness / 2))
)

# 4. Final Boolean Operations
result = body.cut(eyes_tool).cut(nose_tool).cut(mouth_tool)
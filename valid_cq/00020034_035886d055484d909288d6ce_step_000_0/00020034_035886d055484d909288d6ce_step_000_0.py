import cadquery as cq

# --- Parameters ---
length = 90.0
height = 25.0
width = 20.0          # Total depth of the top section
top_thickness = 12.0  # Thickness (height) of the top section
flange_thickness = 5.0 # Thickness of the front vertical flange
tab_width = 10.0
tab_protrusion = 5.0
cutout_radius = 2.5
feature_spacing = 45.0 # Center-to-center distance of tabs/cutouts

# --- 1. Main Body ---
# Create the L-shaped profile on the YZ plane and extrude along X.
# The back face is aligned with Y=0.
# The top surface is at Z=height.
profile_pts = [
    (0, 0),                          # Bottom-Back
    (0, height),                     # Top-Back
    (width, height),                 # Top-Front
    (width, height - top_thickness), # Bottom of Top section (Front)
    (flange_thickness, height - top_thickness), # Inner Corner
    (flange_thickness, 0),           # Bottom of Flange (Front)
    (0, 0)                           # Close
]

result = (
    cq.Workplane("YZ")
    .polyline(profile_pts)
    .close()
    .extrude(length / 2.0, both=True)
)

# --- 2. Back Tabs ---
# Add the rectangular tabs to the back face (Y=0).
# The tabs are flush with the top surface.
# The workplane center on the back face is at Z = height / 2.
# We need to shift the tabs up so they align with the top section.
tab_z_center = height - (top_thickness / 2.0)
face_z_center = height / 2.0
offset_z = tab_z_center - face_z_center

result = (
    result.faces("<Y")
    .workplane()
    .pushPoints([
        (-feature_spacing / 2.0, offset_z), 
        (feature_spacing / 2.0, offset_z)
    ])
    .rect(tab_width, top_thickness)
    .extrude(tab_protrusion)
)

# --- 3. Relief Cutouts ---
# Create semi-circular cutouts on the underside of the top overhang.
# We create a workplane at the step level and cut upwards.
# The cut is centered on the step edge (Y = flange_thickness), creating a notch.
result = (
    result.cut(
        cq.Workplane("XY")
        .workplane(offset=height - top_thickness)
        .pushPoints([
            (-feature_spacing / 2.0, flange_thickness), 
            (feature_spacing / 2.0, flange_thickness)
        ])
        .circle(cutout_radius)
        .extrude(top_thickness) # Cut upwards through the top section
    )
)
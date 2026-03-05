import cadquery as cq

# --- Parametric Dimensions ---
# Main plate dimensions
plate_height = 100.0
plate_width = 40.0
plate_thickness = 2.0

# Top T-feature dimensions
t_stem_height = 15.0     # Height of the vertical part of the T
t_stem_thickness = 2.0   # Thickness of the vertical part
t_top_width = 8.0        # Width of the horizontal top bar of the T
t_top_thickness = 2.0    # Thickness of the horizontal top bar
t_depth = 10.0           # Depth (extrusion length) of the T feature

# --- Modeling ---

# 1. Create the main rectangular plate
# Oriented in the XZ plane for "vertical" look, extruded in Y
plate = (
    cq.Workplane("XY")
    .box(plate_width, plate_thickness, plate_height)
)

# 2. Create the T-shaped feature on top
# We will draw the T-profile on the top face of the plate or relative to it.
# Let's construct the profile on the XZ plane centered above the plate.

# Calculate the center Z position for the T-feature relative to the global origin
# The plate is centered at Z=0, so its top is at plate_height/2
# We want the T-feature to sit on top of that.

# Alternative approach: Build the T-profile sketch and extrude it.
# The T-profile is viewed from the "front" (XZ plane in local coords relative to the top).
# However, looking at the image, the "T" shape is extruded along the Z-axis (vertical) 
# or maybe it's a rib on top.
# Let's look closer. The image shows a long vertical plate. On the top edge, there is a small extrusion going UP.
# The cross-section of that extrusion seems to be a "T" shape when viewed from the top? 
# No, looking at the shading, it looks like a T-profile extruded vertically upwards from the center of the top edge.
# Wait, let me re-examine the image.
# It looks like a flat plate. On the top edge, there is a smaller piece sticking up.
# This smaller piece has a cross-section. The cross-section looks like a T. The "top" of the T is parallel to the plate's thickness? No.
# Let's assume the plate is width (X) and height (Z). The thickness is Y.
# The feature on top is centered on the top edge.
# It looks like a "T" where the stem connects to the plate, and the cross-bar is at the very top.
# The orientation of the T: The cross-bar is parallel to the plate width? Or perpendicular?
# In the image, the T-top is perpendicular to the wide face of the plate. 
# So if plate is wide in X, the T-top is wide in Y.
# Actually, looking at the perspective:
# The main plate is facing us.
# The feature on top: The stem is aligned with the plate. The top bar of the T overhangs perpendicular to the plate face.
# So if plate is in XZ plane (thin in Y):
# The T-stem is in XZ plane.
# The T-bar runs along Y.
# But wait, usually these are aluminum extrusions or similar.
# Let's try a different interpretation.
# Maybe the T-shape is the cross section extruded vertically?
# If I look at the top of the object, I see a T-shape profile.
# So the object is a T-profile extruded downwards? No, the bottom part is just a rectangular plate.
# So it's a transition? No, it looks like two distinct shapes unioned.
# Shape 1: The large plate.
# Shape 2: The T-feature on top.
# Let's look at the junction. The width of the T-stem seems to match the width of the feature on top, but is much narrower than the plate width.
# The T-stem is centered on the plate width.
# The T-feature seems to have a specific depth (along the plate width direction).
# Let's assume:
# Plate: Width=40, Height=100, Thickness=2.
# Feature on top: Centered. Width=10 (along plate width direction). Height=15.
# Cross-section of feature (viewed from side/edge of plate): T-shape.
# Stem thickness = plate thickness (2). 
# Top bar width = 8 (wider than plate thickness).
# Top bar thickness = 2.

# Let's refine the dimensions based on visual proportions.
# Plate W/H ratio ~ 1:2.5 or 1:3. Let's say 40x100.
# Top feature height is about 1/6th of plate height ~ 15mm.
# Top feature width (along the top edge of plate) is small, maybe 1/4 of plate width ~ 10mm.
# The T-profile shape: The "top" of the T is perpendicular to the plate's large face.
# So the T cross-section is visible from the SIDE view (YZ plane).

# Let's build it.
# 1. Main Plate.
# 2. T-feature on top.

# Adjusting orientation to match standard views usually preferred in CAD.
# Let X be the width of the plate.
# Let Y be the thickness of the plate.
# Let Z be the vertical height.

plate = cq.Workplane("XY").box(plate_width, plate_thickness, plate_height)

# Create the T-feature.
# It sits on the top face (Z = plate_height/2).
# It is centered in X and Y.
# It is extruded upwards by t_depth (which corresponds to the visual "width" of the tab along the top edge).
# Wait, the "T" shape is the profile. Which way is it extruded?
# Looking at the image, the small part has a constant cross-section along the X-axis (along the plate width).
# So we sketch the T on the YZ plane (Side view) and extrude it in X.
# The "stem" of the T sits on the plate. The "crossbar" is at the top.
# The stem width matches the plate thickness?
# It looks like the stem is the same thickness as the plate, so they merge smoothly.
# The crossbar makes it wider than the plate thickness at the very top.

# Dimensions for the T-profile (on YZ plane):
# Stem width (in Y) = plate_thickness (2.0)
# Stem height (in Z) = t_stem_height (15.0)
# Top bar width (in Y) = t_top_width (6.0 - making it wider than thickness)
# Top bar height/thickness (in Z) = t_top_thickness (2.0)
# Total height of feature = stem height? Or stem + top? Let's say total height added is ~15-20.

# The extrusion length (in X) is smaller than the plate width. It's a "tab" in the middle.
# Let's call the extrusion length `tab_width`.

tab_width = 10.0   # Width of the tab along the top edge
tab_height = 20.0  # Total height of the tab feature
flange_width = 6.0 # Width of the top T-bar (thickness direction of plate)
flange_thick = 3.0 # Thickness of the top T-bar

# Constructing the T-profile on the side plane (YZ), centered on the top of the plate.
# We need to create a workplane on the top of the plate, or rotated.
# Easier to just define the sketch on the YZ plane, move it up to the top of the plate, and extrude symmetrically in X.

def t_profile(stem_w, stem_h, flange_w, flange_th):
    """
    Creates a T-shape sketch.
    Origin is at the bottom center of the stem.
    """
    pts = [
        (stem_w/2, 0),
        (stem_w/2, stem_h - flange_th),
        (flange_w/2, stem_h - flange_th),
        (flange_w/2, stem_h),
        (-flange_w/2, stem_h),
        (-flange_w/2, stem_h - flange_th),
        (-stem_w/2, stem_h - flange_th),
        (-stem_w/2, 0)
    ]
    return cq.Workplane("YZ").polyline(pts).close()

# Create the profile
t_sketch = t_profile(plate_thickness, tab_height, flange_width, flange_thick)

# Move the profile to the top of the plate
# Plate top is at Z = plate_height/2
# The sketch is currently at Z=0. We need to move it up.
# CadQuery sketches/wires can be moved. 
# Alternatively, create the Workplane at the correct offset.

t_feature = (
    cq.Workplane("YZ")
    .workplane(offset=0) # Center
    .center(0, plate_height/2) # Move origin of sketch to top of plate
    .polyline([
        (plate_thickness/2, 0),
        (plate_thickness/2, tab_height - flange_thick),
        (flange_width/2, tab_height - flange_thick),
        (flange_width/2, tab_height),
        (-flange_width/2, tab_height),
        (-flange_width/2, tab_height - flange_thick),
        (-plate_thickness/2, tab_height - flange_thick),
        (-plate_thickness/2, 0)
    ])
    .close()
    .extrude(tab_width/2, both=True) # Extrude symmetrically along X
)

# Combine the plate and the T-feature
result = plate.union(t_feature)
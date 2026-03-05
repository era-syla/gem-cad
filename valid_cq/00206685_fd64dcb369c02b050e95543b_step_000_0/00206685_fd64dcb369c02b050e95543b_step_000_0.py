import cadquery as cq

# --- Parametric Dimensions ---
# Flange (Base Plate)
flange_width = 40.0        # Width of the stadium shape (and diameter of rounded ends)
hole_spacing = 60.0        # Center-to-center distance of mounting holes
flange_thickness = 12.0    # Thickness of the flange plate

# Central Hub (Top Boss)
top_hub_od = 34.0          # Outer diameter of the raised boss on top
top_hub_height = 4.0       # Height of the boss above the flange

# Central Hub (Bottom Extension)
bottom_hub_od = 34.0       # Outer diameter of the cylinder extending downwards
bottom_hub_len = 25.0      # Length of the cylinder extending downwards

# Bore
center_hole_dia = 16.0     # Diameter of the central through-hole

# Mounting Holes
mount_hole_dia = 6.5       # Diameter of mounting screw holes
cbore_dia = 12.0           # Diameter of the counterbore
cbore_depth = 5.0          # Depth of the counterbore

# --- Modeling ---

# 1. Create the base flange
# Using slot2D to create the stadium shape. 
# length in slot2D is the total length (hole_spacing + flange_width).
result = (
    cq.Workplane("XY")
    .slot2D(length=hole_spacing + flange_width, diameter=flange_width)
    .extrude(flange_thickness)
)

# 2. Add Mounting Holes (Counterbored)
# We perform this before adding the top boss to easily select the flange top face.
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(-hole_spacing/2, 0), (hole_spacing/2, 0)])
    .cboreHole(mount_hole_dia, cbore_dia, cbore_depth)
)

# 3. Add Bottom Hub Extension
# Extrude from the bottom face of the flange downwards.
result = (
    result.faces("<Z")
    .workplane()
    .circle(bottom_hub_od / 2)
    .extrude(bottom_hub_len)
)

# 4. Add Top Hub Boss
# Extrude from the top face of the flange upwards.
# faces(">Z") selects the highest Z face, which is the top of the flange.
result = (
    result.faces(">Z")
    .workplane()
    .circle(top_hub_od / 2)
    .extrude(top_hub_height)
)

# 5. Create Central Through Hole
# Drill through the entire part from the very top face.
result = (
    result.faces(">Z")
    .workplane()
    .hole(center_hole_dia)
)
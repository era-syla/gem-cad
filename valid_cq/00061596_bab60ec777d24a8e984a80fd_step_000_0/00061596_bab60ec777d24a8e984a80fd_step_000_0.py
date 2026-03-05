import cadquery as cq

# --- Parametric Dimensions ---

# Top Cylinder Section
cyl_diameter = 24.0
cyl_height = 40.0

# Middle Rectangular Section
# Width matches the cylinder diameter to align with the curve
rect_width = 24.0  
rect_thickness = 14.0
rect_upper_height = 22.0
rect_lower_height = 10.0

# Flange Section
flange_diameter = 48.0
flange_thickness = 3.0

# --- Geometry Construction ---

# The model is built from the bottom up along the Z-axis
result = (
    cq.Workplane("XY")
    
    # 1. Create the bottom rectangular tab
    .rect(rect_width, rect_thickness)
    .extrude(rect_lower_height)
    
    # 2. Create the circular flange on top of the bottom tab
    .faces(">Z").workplane()
    .circle(flange_diameter / 2.0)
    .extrude(flange_thickness)
    
    # 3. Create the upper rectangular block on top of the flange
    .faces(">Z").workplane()
    .rect(rect_width, rect_thickness)
    .extrude(rect_upper_height)
    
    # 4. Create the top cylindrical shaft
    .faces(">Z").workplane()
    .circle(cyl_diameter / 2.0)
    .extrude(cyl_height)
)
import cadquery as cq

# Parametric dimensions
shaft_diameter = 10.0
flange_diameter = 15.0
total_length = 80.0
end_length = 12.0      # Length of the shaft from end to flange
flange_thickness = 3.0 # Width of the flange

# Derived dimensions
shaft_radius = shaft_diameter / 2.0
flange_radius = flange_diameter / 2.0
# Calculate the length of the middle section based on total length
center_length = total_length - 2 * (end_length + flange_thickness)

# Create the model using a stack of extrusions along the Z-axis
result = (
    cq.Workplane("XY")
    # 1. Bottom shaft end
    .circle(shaft_radius)
    .extrude(end_length)
    
    # 2. Bottom flange
    .faces(">Z").workplane()
    .circle(flange_radius)
    .extrude(flange_thickness)
    
    # 3. Center shaft section
    .faces(">Z").workplane()
    .circle(shaft_radius)
    .extrude(center_length)
    
    # 4. Top flange
    .faces(">Z").workplane()
    .circle(flange_radius)
    .extrude(flange_thickness)
    
    # 5. Top shaft end
    .faces(">Z").workplane()
    .circle(shaft_radius)
    .extrude(end_length)
)
import cadquery as cq

# Parametric dimensions
total_length = 300.0  # Total length of the shaft
main_diameter = 10.0  # Diameter of the main shaft body

# Left end features (simple step down)
left_end_length = 10.0
left_end_diameter = 6.0

# Right end features (stepped profile)
# Section 1: Immediate step down
right_step1_length = 15.0
right_step1_diameter = 8.0
# Section 2: Groove/Undercut area
right_groove_length = 5.0
right_groove_diameter = 6.0
# Section 3: Final tip
right_tip_length = 10.0
right_tip_diameter = 7.0

# Calculate main body length
# We build from left to right
# Total length = left_end + main_body + right_features
right_total_feature_length = right_step1_length + right_groove_length + right_tip_length
main_body_length = total_length - left_end_length - right_total_feature_length

# Create the model using a workplane and extruding sections
result = (
    cq.Workplane("XY")
    # 1. Left end tip
    .circle(left_end_diameter / 2.0)
    .extrude(left_end_length)
    
    # 2. Main Shaft Body
    .faces(">Z").workplane()
    .circle(main_diameter / 2.0)
    .extrude(main_body_length)
    
    # 3. Right End - Step 1
    .faces(">Z").workplane()
    .circle(right_step1_diameter / 2.0)
    .extrude(right_step1_length)
    
    # 4. Right End - Groove
    .faces(">Z").workplane()
    .circle(right_groove_diameter / 2.0)
    .extrude(right_groove_length)
    
    # 5. Right End - Tip
    .faces(">Z").workplane()
    .circle(right_tip_diameter / 2.0)
    .extrude(right_tip_length)
)

# Optional: Add chamfers to the main body ends for realism
# Select edges at the transition from main body to ends
result = result.edges(
    cq.selectors.NearestToPointSelector((0, 0, left_end_length))
).chamfer(0.5)

result = result.edges(
    cq.selectors.NearestToPointSelector((0, 0, left_end_length + main_body_length))
).chamfer(0.5)

# Add a small chamfer to the very tip of the right end
result = result.edges(">Z").chamfer(0.5)

# Add a small chamfer to the very start of the left end
result = result.edges("<Z").chamfer(0.5)
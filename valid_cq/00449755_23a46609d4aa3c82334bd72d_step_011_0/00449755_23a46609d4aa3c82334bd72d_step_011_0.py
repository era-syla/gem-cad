import cadquery as cq

# --- Parametric Dimensions ---
# Based on typical 12g CO2 cartridge dimensions
total_length = 83.0
body_diameter = 18.6
neck_diameter = 7.0
neck_height = 8.0
shoulder_height = 14.0

# Derived parameters
body_radius = body_diameter / 2.0
neck_radius = neck_diameter / 2.0
# The bottom is a hemisphere, so its height equals its radius
bottom_height = body_radius
# Calculate the length of the straight cylindrical section
straight_height = total_length - bottom_height - shoulder_height - neck_height

# --- Modeling ---

# Create a profile in the XZ plane to revolve around the Z axis
# Starting from the bottom pole at (0, 0)
result = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    
    # 1. Bottom Hemisphere
    # Create a quarter-circle arc from the pole (0,0) to the full radius (r, r).
    # Using threePointArc with a calculated midpoint for a perfect circular profile.
    # Midpoint offset factor for 45 degrees: sin(45) ~= 0.7071
    .threePointArc(
        (body_radius * 0.7071, body_radius * (1 - 0.7071)), 
        (body_radius, body_radius)
    )
    
    # 2. Straight Body Cylinder
    # Draw a vertical line up to the start of the shoulder
    .lineTo(body_radius, body_radius + straight_height)
    
    # 3. Shoulder Transition
    # Create a smooth convex curve connecting the body to the neck.
    # tangentArcPoint ensures the arc is tangent to the previous vertical line,
    # resulting in a smooth G1 continuity at the body-shoulder junction.
    .tangentArcPoint((neck_radius, body_radius + straight_height + shoulder_height))
    
    # 4. Neck Cylinder
    # Draw the straight vertical neck section
    .lineTo(neck_radius, total_length)
    
    # 5. Top Face
    # Close the geometry by drawing a line to the center axis
    .lineTo(0, total_length)
    
    # 6. Close Profile
    # Draw a line back to the origin (implicitly or explicitly via close)
    .close()
    
    # 7. Generate Solid
    # Revolve the profile 360 degrees around the Z axis
    .revolve()
)
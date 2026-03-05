import cadquery as cq
import math

# --- Parameters ---
# Overall dimensions and key sizes
overall_width = 80.0    # Distance between outer faces of the legs
leg_thickness = 10.0    # Thickness of the curved legs
leg_angle = 45.0        # Angle of the legs relative to vertical
leg_length_horizontal = 40.0 # Approximate horizontal span of one leg from center
leg_drop = 30.0         # Vertical drop from top platform to leg ends

# Top Platform parameters
platform_length = 40.0
platform_width = 25.0
platform_thickness = 5.0
top_hole_diameter = 6.0

# Leg parameters
leg_end_radius = 5.0    # Rounding at the end of the legs
leg_hole_diameter = 4.0

# Arch parameters
arch_radius = 45.0      # Radius of the under-arch

# --- Modeling Strategy ---
# 1. Create the main profile in the XZ plane. This profile will represent the side view
#    of the bracket (the "V" shape with the arch).
# 2. Extrude this profile to create the main body.
# 3. Create the top platform.
# 4. Add the mounting holes on the legs.
# 5. Add the mounting hole on the top platform.
# 6. Apply fillets to smooth transitions if necessary (though the image shows fairly sharp transitions except for the arch).

# --- Geometry Construction ---

# 1. Base Profile Construction (XZ Plane)
# We will draw half of the profile and mirror it, or draw the whole thing.
# Let's draw the full symmetric profile.

# Calculate points
# Top center point is origin (0,0) relative to the sketch, but let's shift it down 
# so the top of the legs is at Z=0 for easier platform placement.
# Actually, let's put the top surface of the leg intersection at Z=0.

# End of leg X coordinate
leg_end_x = leg_length_horizontal
# End of leg Z coordinate (downwards)
leg_end_z = -leg_drop

# Create the main V-shape body
# We define the outer shape and the inner arch.

# Function to build the main bracket body
def create_bracket_body():
    # Helper points
    p_top_left = (-platform_length/2, 0)
    p_top_right = (platform_length/2, 0)
    
    # Outer leg endpoints
    p_leg_left_outer = (-leg_end_x - leg_end_radius, leg_end_z)
    p_leg_right_outer = (leg_end_x + leg_end_radius, leg_end_z)
    
    # Inner arch construction is tricky without exact specs, 
    # so we'll use a 3-point arc or a radius tangent.
    # Let's approximate the leg shape.
    
    pts = [
        (0, 0), # Top center
        (leg_end_x, leg_end_z), # Right leg end center
    ]
    
    # We will construct this by creating a sketch and extruding.
    # The shape looks like an extrusion along Y, but the legs angle out.
    # Looking closely at the image, the legs have constant thickness in the extrusion direction.
    # It looks like a linear extrusion of a specific profile.
    
    sketch = (
        cq.Workplane("XZ")
        .moveTo(-platform_length/2, 0)
        .lineTo(platform_length/2, 0) # Top flat part under the platform
        # Right outer leg edge
        .lineTo(leg_end_x, leg_end_z + leg_end_radius)
        .tangentArcPoint((leg_end_x, leg_end_z - leg_end_radius), relative=False) # Rounded end
        # Inner arch
        .lineTo(leg_end_x - leg_thickness, leg_end_z - leg_end_radius/2) # slight return
        .radiusArc((-leg_end_x + leg_thickness, leg_end_z - leg_end_radius/2), arch_radius) # The big arch
        # Left outer leg edge
        .lineTo(-leg_end_x, leg_end_z - leg_end_radius)
        .tangentArcPoint((-leg_end_x, leg_end_z + leg_end_radius), relative=False) # Rounded end
        .close()
    )
    
    # Extrude the main body
    # The image shows the body has a specific width.
    body = sketch.extrude(leg_thickness)
    
    # Center the extrusion on Y
    body = body.translate((0, -leg_thickness/2, 0))
    
    return body

main_body = create_bracket_body()

# 2. Create the Top Platform
# The platform sits on top of the main body, wider than the leg thickness.
platform = (
    cq.Workplane("XY")
    .workplane(offset=0) # Base at Z=0
    .rect(platform_length, platform_width)
    .extrude(platform_thickness)
)

# 3. Combine parts
result = main_body.union(platform)

# 4. Add Holes

# Top hole
result = (
    result.faces(">Z")
    .workplane()
    .hole(top_hole_diameter)
)

# Leg holes
# We need to find the centers of the rounded ends of the legs.
# Based on our sketch logic:
# Right leg center: (leg_end_x, -leg_thickness/2 (y), leg_end_z)
# Left leg center: (-leg_end_x, -leg_thickness/2 (y), leg_end_z)

# We can drill these perpendicular to the leg face (Y-axis)
result = (
    result.faces(">Y")
    .workplane()
    .pushPoints([
        (leg_end_x, leg_end_z),
        (-leg_end_x, leg_end_z)
    ])
    .hole(leg_hole_diameter)
)

# Refinement: The image shows the top platform has rounded undersides or fillets where it meets the legs?
# Actually, the image shows the platform is just a rectangular block sitting on the V-shape.
# However, the V-shape profile at the top seems to match the platform length.
# In my sketch, I used platform_length for the top of the V, so it aligns perfectly.

# Refinement: Filleting the transition between the vertical sides of the V-body and the horizontal wings of the platform?
# The image shows a sharp corner there, or a very small fillet.
# However, the "neck" where the platform meets the legs looks seamless.
# There is a distinct feature: The platform overhangs the legs in the Y direction (width).
# The legs are `leg_thickness` (10mm), the platform is `platform_width` (25mm).
# This creates the T-shape look.

# Optional: Add fillets to the leg roots if desired, but the image is quite sharp/geometric.
# Let's just ensure the coordinate system makes sense.

# Code Cleanup for generation
# Re-assembling into the clean script format.
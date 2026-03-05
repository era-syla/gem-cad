import cadquery as cq

# ==========================================
# Parameter Definitions
# ==========================================
# Dimensions estimated based on standard robotics U-channel (e.g., goBILDA)
length = 384.0          # Total length of the channel (approx 15")
width = 48.0            # Outer width
height = 48.0           # Flange height
thickness = 2.5         # Wall thickness
grid_spacing = 8.0      # Standard spacing for mounting holes
pattern_pitch = 32.0    # Distance between repeating pattern centers
large_hole_dia = 14.0   # Diameter of central large holes
small_hole_dia = 4.0    # Diameter of smaller mounting holes

# ==========================================
# Geometry Construction
# ==========================================

# 1. Create Base U-Channel Profile
# Drawn on XY plane with origin (0,0) at the bottom-left corner
# Extruded along the Z axis (vertical in the image)
def create_u_profile():
    return (cq.Workplane("XY")
            .moveTo(0, height)                  # Start at top of left flange
            .lineTo(0, 0)                       # Down to bottom-left
            .lineTo(width, 0)                   # Across bottom to bottom-right
            .lineTo(width, height)              # Up to top of right flange
            .lineTo(width - thickness, height)  # Inner top right
            .lineTo(width - thickness, thickness) # Inner bottom right
            .lineTo(thickness, thickness)       # Inner bottom left
            .lineTo(thickness, height)          # Inner top left
            .close()
           )

# Extrude to create the base solid
base_solid = create_u_profile().extrude(length)

# 2. Generate Hole Pattern Coordinates
# The pattern consists of:
# - A large central hole
# - 4 surrounding small holes in a cross pattern (offset by grid_spacing)
# - An intermediate small hole halfway between pattern centers

large_hole_pts = []
small_hole_pts = []

num_patterns = int(length // pattern_pitch)
cross_center = width / 2.0  # Center position across the face width (24mm)

for i in range(num_patterns):
    # Z coordinate for the center of the large hole (starts at half pitch, 16mm)
    z_center = pattern_pitch / 2.0 + i * pattern_pitch
    
    # 1. Large Hole Center
    large_hole_pts.append((cross_center, z_center))
    
    # 2. Surrounding Small Holes (Cross layout)
    # Top
    small_hole_pts.append((cross_center, z_center + grid_spacing))
    # Bottom
    small_hole_pts.append((cross_center, z_center - grid_spacing))
    # Left (relative to face)
    small_hole_pts.append((cross_center - grid_spacing, z_center))
    # Right (relative to face)
    small_hole_pts.append((cross_center + grid_spacing, z_center))
    
    # 3. Intermediate Small Hole
    # Placed between this pattern and the next (offset by 16mm)
    z_intermediate = z_center + pattern_pitch / 2.0
    
    # Only add intermediate hole if it fits within the part length with a small margin
    if z_intermediate < (length - small_hole_dia/2): 
        small_hole_pts.append((cross_center, z_intermediate))

# 3. Apply Holes to Faces
# We use centerOption="ProjectedOrigin" so that the Workplane's (0,0) matches the 
# Global (0,0,0) projected onto the face. This aligns the Z-coordinates of our points
# with the Z-axis of the extrusion.

# Helper function to maintain clean code
def apply_pattern_to_face(solid, face_selector):
    return (solid
            .faces(face_selector)
            .workplane(centerOption="ProjectedOrigin")
            .pushPoints(large_hole_pts)
            .hole(large_hole_dia, depth=thickness)
            .faces(face_selector)
            .workplane(centerOption="ProjectedOrigin")
            .pushPoints(small_hole_pts)
            .hole(small_hole_dia, depth=thickness)
           )

# Apply to Back Face (Web) - Normal pointing -Y
result = apply_pattern_to_face(base_solid, "<Y")

# Apply to Left Flange - Normal pointing -X
result = apply_pattern_to_face(result, "<X")

# Apply to Right Flange - Normal pointing +X
result = apply_pattern_to_face(result, ">X")

# The variable 'result' now contains the finished 3D model
import cadquery as cq
import math

# Parameters
center_size = 30  # central polygon size
arm_length = 60   # length of each arm from center
arm_width = 8     # width of each arm
boss_radius = 8   # radius of end boss cylinders
boss_height = 8   # height of end bosses
hole_radius = 3   # hole radius in bosses
plate_thickness = 4  # thickness of main plate
arm_thickness = 6  # thickness of arms

# Arm angles (4 arms, not symmetric - roughly 3 at bottom and 1 at top)
# Looking at image: one arm goes up-right, one goes right, one goes down-left, one goes down
arm_angles = [90, 210, 330, 0]  # degrees - like a 3-arm star plus one more
# Actually from image it looks like: top, bottom-left, bottom-right, and left
arm_angles_deg = [75, 195, 315, 0]

# Let me use 4 arms at specific angles based on the image
# Image shows: top-right arm, right arm, bottom-left arm, bottom arm
arm_angles_deg = [80, 170, 260, 350]

# Simpler approach: build the frame
# Central octagon plate
# 4 arms extending outward
# Cylindrical bosses at arm ends

def make_model():
    # Start with central plate as a polygon
    center = (
        cq.Workplane("XY")
        .polygon(8, center_size * 2)
        .extrude(plate_thickness)
    )
    
    # Add 4 arms at different angles
    arm_angles = [80, 170, 260, 350]
    
    result = center
    
    for angle in arm_angles:
        angle_rad = math.radians(angle)
        
        # Arm end position
        end_x = arm_length * math.cos(angle_rad)
        end_y = arm_length * math.sin(angle_rad)
        
        # Create arm as a box, then rotate and position
        # Arm along X axis, then rotate
        arm = (
            cq.Workplane("XY")
            .box(arm_length, arm_width, arm_thickness, centered=False)
            .translate((0, -arm_width/2, 0))
        )
        
        # Rotate arm
        arm = arm.rotate((0, 0, 0), (0, 0, 1), angle)
        
        result = result.union(arm)
        
        # Add boss cylinder at arm end
        boss = (
            cq.Workplane("XY")
            .circle(boss_radius)
            .extrude(boss_height)
            .translate((end_x, end_y, 0))
        )
        
        result = result.union(boss)
        
        # Cut hole through boss
        hole = (
            cq.Workplane("XY")
            .circle(hole_radius)
            .extrude(boss_height + 1)
            .translate((end_x, end_y, -0.5))
        )
        
        result = result.cut(hole)
    
    return result

result = make_model()

# Clean up by centering vertically
result = result.translate((0, 0, -plate_thickness/2))
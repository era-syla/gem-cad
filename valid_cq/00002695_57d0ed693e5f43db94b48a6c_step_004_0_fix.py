import cadquery as cq
import math

# Parameters
center_size = 20        # central hub size
arm_length = 35         # length of each arm from center
arm_width = 12          # width of arm
end_radius = 12         # radius of circular end piece
hole_radius = 6         # radius of hole in end piece
thickness = 6           # overall thickness
num_arms = 4            # 4 arms at 90 degree intervals

# Build center hub (octagonal/square rotated 45 degrees)
center_hex = (
    cq.Workplane("XY")
    .polygon(8, center_size * 1.5)
    .extrude(thickness)
)

# Build each arm and end circle
arms = cq.Workplane("XY").box(0.001, 0.001, 0.001)  # dummy start

# Create a single arm unit (arm + circular end)
def make_arm(angle_deg):
    angle_rad = math.radians(angle_deg)
    
    # Arm rectangle - pointing outward
    arm_cx = math.cos(angle_rad) * (arm_length / 2 + center_size * 0.4)
    arm_cy = math.sin(angle_rad) * (arm_length / 2 + center_size * 0.4)
    
    # Arm: a rectangle oriented along the angle
    arm = (
        cq.Workplane("XY")
        .transformed(rotate=cq.Vector(0, 0, angle_deg))
        .rect(arm_length, arm_width)
        .extrude(thickness)
        .translate((arm_cx * 0, arm_cy * 0, 0))
    )
    
    # End circle position
    end_x = math.cos(angle_rad) * (arm_length + center_size * 0.3)
    end_y = math.sin(angle_rad) * (arm_length + center_size * 0.3)
    
    end_circle = (
        cq.Workplane("XY")
        .circle(end_radius)
        .extrude(thickness)
        .translate((end_x, end_y, 0))
    )
    
    return arm, end_circle

# Build complete shape by union
result = center_hex

for i in range(num_arms):
    angle = i * 90  # 0, 90, 180, 270 degrees
    angle_rad = math.radians(angle)
    
    # End circle position
    end_x = math.cos(angle_rad) * (arm_length + 8)
    end_y = math.sin(angle_rad) * (arm_length + 8)
    
    # Arm: oriented along angle
    arm = (
        cq.Workplane("XY")
        .transformed(rotate=cq.Vector(0, 0, angle))
        .rect(arm_length + 10, arm_width)
        .extrude(thickness)
    )
    
    end_circle = (
        cq.Workplane("XY")
        .workplane()
        .center(end_x, end_y)
        .circle(end_radius)
        .extrude(thickness)
    )
    
    result = result.union(arm).union(end_circle)

# Cut holes in each end circle
for i in range(num_arms):
    angle = i * 90
    angle_rad = math.radians(angle)
    
    end_x = math.cos(angle_rad) * (arm_length + 8)
    end_y = math.sin(angle_rad) * (arm_length + 8)
    
    hole = (
        cq.Workplane("XY")
        .center(end_x, end_y)
        .circle(hole_radius)
        .extrude(thickness)
    )
    
    result = result.cut(hole)

# Add chamfers/notches between arms (V-shaped cuts)
# Cut triangular notches between each arm pair
for i in range(num_arms):
    angle = i * 90 + 45  # diagonal angles between arms
    angle_rad = math.radians(angle)
    
    notch_x = math.cos(angle_rad) * (center_size * 0.5)
    notch_y = math.sin(angle_rad) * (center_size * 0.5)
    
    notch = (
        cq.Workplane("XY")
        .transformed(rotate=cq.Vector(0, 0, angle))
        .rect(14, 14)
        .extrude(thickness)
        .translate((notch_x, notch_y, 0))
    )
    
    result = result.cut(notch)
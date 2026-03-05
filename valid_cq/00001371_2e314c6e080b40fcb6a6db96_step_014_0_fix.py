import cadquery as cq
import math

# Main plate - star/gear shaped hub with 6 arms
# Base parameters
base_thickness = 6
arm_thickness = 4
center_radius = 18
arm_length = 35
arm_width = 12
outer_radius = 42

# Create the base hexagonal/star shaped plate
# Start with a central disk
base = cq.Workplane("XY").circle(center_radius).extrude(base_thickness)

# Add 6 arms at 60 degree intervals
for i in range(6):
    angle = i * 60
    angle_rad = math.radians(angle)
    
    # Arm rectangle
    arm = (cq.Workplane("XY")
           .transformed(rotate=(0, 0, angle))
           .rect(arm_width, arm_length, centered=True)
           .extrude(arm_thickness))
    
    # Shift arm to extend outward
    arm = (cq.Workplane("XY")
           .transformed(offset=(math.cos(angle_rad) * (arm_length/2 - 2), 
                                math.sin(angle_rad) * (arm_length/2 - 2), 0),
                        rotate=(0, 0, angle))
           .rect(arm_width, arm_length)
           .extrude(arm_thickness))
    
    base = base.union(arm)

# Add outer connection pads at end of every other arm (3 larger pads)
for i in range(3):
    angle = i * 120
    angle_rad = math.radians(angle)
    cx = math.cos(angle_rad) * (outer_radius - 4)
    cy = math.sin(angle_rad) * (outer_radius - 4)
    
    pad = (cq.Workplane("XY")
           .transformed(offset=(cx, cy, 0), rotate=(0, 0, angle))
           .rect(14, 10)
           .extrude(base_thickness))
    
    base = base.union(pad)

# Add small cylindrical bosses at alternate arm ends
for i in range(3):
    angle = i * 120 + 60
    angle_rad = math.radians(angle)
    cx = math.cos(angle_rad) * (outer_radius - 6)
    cy = math.sin(angle_rad) * (outer_radius - 6)
    
    boss = (cq.Workplane("XY")
            .transformed(offset=(cx, cy, 0))
            .circle(5)
            .extrude(base_thickness))
    
    base = base.union(boss)

# Add central raised hub
hub = (cq.Workplane("XY")
       .circle(14)
       .extrude(base_thickness + 4))

base = base.union(hub)

# Central through hole
base = (base
        .faces(">Z")
        .workplane()
        .hole(10))

# Add ring groove on hub
base = base.cut(
    cq.Workplane("XY")
    .transformed(offset=(0, 0, base_thickness - 1))
    .circle(12)
    .circle(10.5)
    .extrude(3)
)

# Add bolt holes around center
for i in range(6):
    angle = i * 60
    angle_rad = math.radians(angle)
    cx = math.cos(angle_rad) * 22
    cy = math.sin(angle_rad) * 22
    
    hole = (cq.Workplane("XY")
            .transformed(offset=(cx, cy, 0))
            .circle(2)
            .extrude(20))
    
    base = base.cut(hole)

# Add rectangular slots at arm ends (every other arm)
for i in range(3):
    angle = i * 120
    angle_rad = math.radians(angle)
    cx = math.cos(angle_rad) * (outer_radius - 8)
    cy = math.sin(angle_rad) * (outer_radius - 8)
    
    slot = (cq.Workplane("XY")
            .transformed(offset=(cx, cy, 0), rotate=(0, 0, angle))
            .rect(6, 8)
            .extrude(20))
    
    base = base.cut(slot)

# Add small holes at boss positions
for i in range(3):
    angle = i * 120 + 60
    angle_rad = math.radians(angle)
    cx = math.cos(angle_rad) * (outer_radius - 6)
    cy = math.sin(angle_rad) * (outer_radius - 6)
    
    hole = (cq.Workplane("XY")
            .transformed(offset=(cx, cy, 0))
            .circle(2)
            .extrude(20))
    
    base = base.cut(hole)

result = base
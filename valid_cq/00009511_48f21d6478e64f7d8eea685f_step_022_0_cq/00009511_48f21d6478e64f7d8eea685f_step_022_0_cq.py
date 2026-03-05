import cadquery as cq
import math

# --- Parameters ---
# Central hub dimensions
hub_od = 60.0
hub_id = 40.0
hub_height = 10.0
fillet_radius = 2.0

# Arm dimensions
num_arms = 4
arm_length = 65.0  # From center
arm_width = 15.0
arm_thickness = 10.0
arm_end_fillet = 5.0

# Motor mount / Arm end details
mount_hole_spacing = 25.0
mount_hole_dia = 3.2
mount_plate_thickness = 4.0
mount_width = 40.0

# Vertical tower/housing dimensions
tower_width = 50.0
tower_depth = 40.0
tower_height = 45.0
tower_wall_thickness = 4.0
arch_radius = 12.0
arch_height_offset = 15.0 # From top

# Cable guide / rectangular protrusion
cable_guide_width = 18.0
cable_guide_depth = 10.0
cable_guide_height = 12.0
cable_guide_wall = 1.5

# --- Helper Functions ---

def create_arm(length, width, thickness, end_width, end_thickness):
    """Creates a single arm with a mounting plate at the end."""
    # Main arm strut
    arm = (
        cq.Workplane("XY")
        .box(length, width, thickness)
        .translate((length / 2.0, 0, thickness / 2.0))
    )
    
    # End mounting plate (wider section)
    plate = (
        cq.Workplane("XY")
        .box(end_width, length * 0.25, end_thickness) # Approximate length of plate
        .translate((length - (length * 0.125), 0, end_thickness / 2.0))
        .rotate((0,0,0), (0,0,1), 90) # Rotate to be perpendicular
    )
    
    # Combine and fillet
    full_arm = arm.union(plate)
    
    # Add mounting holes
    full_arm = (
        full_arm.faces(">Z").workplane()
        .pushPoints([(length - 10, -mount_hole_spacing/2.0), 
                     (length - 10, mount_hole_spacing/2.0)])
        .hole(mount_hole_dia)
    )
    
    return full_arm

# --- Main Geometry Construction ---

# 1. Central Base Ring
base = (
    cq.Workplane("XY")
    .circle(hub_od / 2.0)
    .circle(hub_id / 2.0)
    .extrude(hub_height)
)

# 2. Arms (X-style quadcopter layout)
arms = cq.Workplane("XY")

for i in range(num_arms):
    angle = 45 + (i * 90)  # X configuration
    
    # Create a generic arm shape
    # We construct it along X then rotate
    arm_geo = (
        cq.Workplane("XY")
        .moveTo(hub_od/2.0 - 5, -arm_width/2.0)
        .lineTo(arm_length, -arm_width/2.0)
        .lineTo(arm_length + 5, -mount_width/2.0) # Flare out
        .lineTo(arm_length + 15, -mount_width/2.0)
        .lineTo(arm_length + 15, mount_width/2.0)
        .lineTo(arm_length + 5, mount_width/2.0) # Flare in
        .lineTo(arm_length, arm_width/2.0)
        .lineTo(hub_od/2.0 - 5, arm_width/2.0)
        .close()
        .extrude(arm_thickness)
    )
    
    # Add holes to the arm ends
    # Transform coordinates to the rotated frame
    hole_dist = arm_length + 10
    
    arm_geo = (
        arm_geo.faces(">Z").workplane()
        .pushPoints([(hole_dist, -mount_hole_spacing/2.0), 
                     (hole_dist, mount_hole_spacing/2.0)])
        .hole(mount_hole_dia)
    )

    # Rotate into position
    arm_geo = arm_geo.rotate((0,0,0), (0,0,1), angle)
    
    if i == 0:
        arms = arm_geo
    else:
        arms = arms.union(arm_geo)

# Combine base and arms
structure = base.union(arms)

# Fillet the junctions between arms and hub
try:
    structure = structure.edges("|Z").fillet(fillet_radius)
except:
    pass # Fillets can fail on complex unions, proceed if so

# 3. Vertical Tower Housing
# Create the outer block
tower_outer = (
    cq.Workplane("XY")
    .rect(tower_width, tower_depth)
    .extrude(tower_height)
    .translate((0, 0, 0)) # Centered
)

# Create the inner cutout (hollow)
tower_inner = (
    cq.Workplane("XY")
    .rect(tower_width - 2*tower_wall_thickness, tower_depth - 2*tower_wall_thickness)
    .extrude(tower_height)
    .translate((0, 0, 0))
)

# Create the arch cutouts on the sides
arch_cutout = (
    cq.Workplane("YZ")
    .workplane(offset=tower_width/2.0 + 1)
    .moveTo(-tower_depth/2.0, tower_height - arch_height_offset)
    .threePointArc((0, tower_height - arch_height_offset + arch_radius), 
                   (tower_depth/2.0, tower_height - arch_height_offset))
    .lineTo(tower_depth/2.0, 0)
    .lineTo(-tower_depth/2.0, 0)
    .close()
    .extrude(-(tower_width + 2))
)

# Top U-shape cutout
top_cutout = (
    cq.Workplane("XZ")
    .workplane(offset=tower_depth/2.0 + 1)
    .moveTo(-tower_width/4.0, tower_height)
    .lineTo(-tower_width/4.0, tower_height - 15)
    .threePointArc((0, tower_height - 15 - 5), (tower_width/4.0, tower_height - 15))
    .lineTo(tower_width/4.0, tower_height)
    .close()
    .extrude(-(tower_depth + 2))
)

# Form the tower shell
tower = tower_outer.cut(tower_inner).cut(arch_cutout).cut(top_cutout)

# Add side holes to the tower (as seen in image)
tower = (
    tower.faces(">X").workplane()
    .pushPoints([(0, tower_height - 10)])
    .hole(3.0, depth=10) # Blind hole or through wall
)
tower = (
    tower.faces("<X").workplane()
    .pushPoints([(0, tower_height - 10)])
    .hole(3.0, depth=10)
)

# Fillet tower edges
try:
    tower = tower.edges("|Z").fillet(3.0)
    tower = tower.edges(">Z").fillet(1.0)
except:
    pass

# Combine tower with base structure
result = structure.union(tower)

# 4. Rectangular Cable Guide
# Located at one of the "open" sides between arms (0 degrees in our setup)
cable_guide = (
    cq.Workplane("XY")
    .rect(cable_guide_width, cable_guide_depth)
    .extrude(cable_guide_height)
)

cable_guide_hole = (
    cq.Workplane("XY")
    .rect(cable_guide_width - 2*cable_guide_wall, cable_guide_depth - 2*cable_guide_wall)
    .extrude(cable_guide_height)
)

cable_guide_final = cable_guide.cut(cable_guide_hole)
# Position it. Image shows it offset from center, sticking up from base.
cable_guide_final = cable_guide_final.translate((hub_od/2.0 + 5, 0, 0))

# Union the cable guide
result = result.union(cable_guide_final)

# 5. Final clean up and large fillets to smooth the organic shape
# The image shows very smooth transitions between the hub and the arms.
# We apply a large fillet to the bottom edges of the arms connecting to the hub.
try:
    # Select bottom edges roughly
    result = result.edges("<Z").fillet(1.0)
    
    # Select vertical edges of the arm-hub junction
    # This is often tricky in CAD kernels without precise selection
    # We will attempt a general fillet
    pass
except:
    pass

# Ensure the center bore is clear (re-cut to be safe after unions)
center_bore = (
    cq.Workplane("XY")
    .circle(hub_id / 2.0)
    .extrude(tower_height + 10) # Through everything
    .translate((0,0,-5))
)

result = result.cut(center_bore)

# Rotate to match image orientation roughly (Isometric view is standard, but let's align)
result = result.rotate((0,0,0), (1,0,0), 0)

if __name__ == "__main__":
    # If running in CQ-Editor, this renders the model
    # show_object(result) 
    pass
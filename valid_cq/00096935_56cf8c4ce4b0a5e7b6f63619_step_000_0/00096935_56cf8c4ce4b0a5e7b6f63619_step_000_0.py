import cadquery as cq

# --- Parameters ---
# Main housing dimensions
mh_w, mh_d, mh_h = 30.0, 16.0, 45.0

# Front plate dimensions
fp_w, fp_d, fp_h = 40.0, 32.0, 5.0

# Cylindrical component dimensions
cyl_r = 5.0
cyl_h = 35.0

# Side rail dimensions
sr_w, sr_d, sr_h = 14.0, 45.0, 10.0

# --- Geometry Construction ---

# 1. Main Housing Block (Tall Rectangular Prism)
# A tall block with cutouts on the top corners
main_housing = (
    cq.Workplane("XY")
    .box(mh_w, mh_d, mh_h, centered=(True, True, False))
    # Cutout top-front-left corner
    .faces(">Z").workplane()
    .moveTo(-mh_w/2 + 5, -mh_d/2 + 5)
    .rect(10, 10)
    .cutBlind(-8)
    # Notch top-front-right corner
    .faces(">Z").workplane()
    .moveTo(mh_w/2 - 3, -mh_d/2 + 3)
    .rect(6, 6)
    .cutBlind(-5)
    .translate((10, 15, 0)) # Position: Back-Right
)

# 2. Front Base Plate (Flat housing cover)
# A flat plate with a rim and internal details
front_plate = (
    cq.Workplane("XY")
    .box(fp_w, fp_d, fp_h, centered=(True, True, False))
    # Hollow out center to create rim
    .faces(">Z").workplane()
    .rect(fp_w - 4, fp_d - 4)
    .cutBlind(-3)
    # Add internal raised details
    .faces(">Z").workplane(offset=-3)
    .rect(15, 6).extrude(3)
    .faces(">Z").workplane()
    .moveTo(10, -5).rect(4, 12).extrude(3)
    .translate((-5, -18, 0)) # Position: Front-Center
)

# 3. Cylindrical Components (Solenoids/Capacitors)
# Helper function to create one unit
def create_cylinder():
    return (
        cq.Workplane("XY")
        .circle(cyl_r).extrude(cyl_h * 0.55)
        .faces(">Z").workplane().circle(cyl_r + 1.5).extrude(2) # Middle Flange
        .faces(">Z").workplane().circle(cyl_r).extrude(cyl_h * 0.3) # Upper body
        .faces(">Z").workplane().circle(1.0).extrude(6) # Top Pin
    )

solenoid1 = create_cylinder().translate((36, 8, 0))
solenoid2 = create_cylinder().translate((36, 22, 0))

# 4. Left Side Rail/Module
# Elongated block with a stepped profile
side_rail = (
    cq.Workplane("XY")
    .box(sr_w, sr_d, sr_h, centered=(True, True, False))
    # Create the step/rail profile
    .faces(">Z").workplane()
    .moveTo(-sr_w/4, 0)
    .rect(sr_w/2, sr_d)
    .cutBlind(-5)
    .translate((-32, 5, 0))
)

# 5. Small Connector (Front Left)
connector = (
    cq.Workplane("XY")
    .box(12, 10, 9, centered=(True, True, False))
    # Connector pocket
    .faces(">Z").workplane()
    .rect(10, 8).cutBlind(-5)
    # Internal pins
    .faces(">Z").workplane(offset=-5)
    .pushPoints([(2, 0), (-2, 0)])
    .circle(0.6).extrude(4)
    .translate((-32, -25, 0))
)

# 6. Far Left Block (Chamfered Cap)
cap_block = (
    cq.Workplane("XY")
    .box(16, 14, 7, centered=(True, True, False))
    # Chamfer the top-back edge to form a ramp shape
    .faces(">Z").edges(">Y").chamfer(4)
    .translate((-52, -30, 0))
)

# --- Final Assembly ---
result = (
    main_housing
    .union(front_plate)
    .union(solenoid1)
    .union(solenoid2)
    .union(side_rail)
    .union(connector)
    .union(cap_block)
)
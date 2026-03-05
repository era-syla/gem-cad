import cadquery as cq
import math

# --- Parameters ---
# Axle dimensions
axle_length = 300.0
axle_diameter = 12.0
axle_end_stub_length = 15.0  # Length sticking out past the flange/wheel
axle_end_stub_diameter = 10.0 # Slightly smaller diameter for the ends

# Flange/Bushing dimensions (Left side)
flange_diameter = 25.0
flange_thickness = 5.0
flange_fillet = 1.0

# Wheel dimensions (Right side)
wheel_diameter = 80.0
wheel_rim_width = 15.0
wheel_rim_thickness = 5.0
wheel_hub_diameter = 20.0
wheel_hub_length = 20.0  # Slightly longer than rim width
spoke_count = 12
spoke_width = 4.0
spoke_thickness = 4.0

# --- Geometry Construction ---

# 1. Main Axle Shaft
# Create the main long rod
axle = cq.Workplane("XY").circle(axle_diameter / 2).extrude(axle_length)

# 2. Left End (Stub + Flange)
# Create the smaller stub on the left end
left_stub = (
    cq.Workplane("XY")
    .workplane(offset=-axle_end_stub_length)
    .circle(axle_end_stub_diameter / 2)
    .extrude(axle_end_stub_length)
)

# Create the flange near the left end
flange = (
    cq.Workplane("XY")
    .workplane(offset=10.0) # Position slightly inward from the start of the main axle
    .circle(flange_diameter / 2)
    .extrude(flange_thickness)
)

# 3. Right End (Wheel Assembly)
# Create the stub on the right end (protruding through the wheel)
right_stub = (
    cq.Workplane("XY")
    .workplane(offset=axle_length)
    .circle(axle_end_stub_diameter / 2)
    .extrude(axle_end_stub_length)
)

# --- Wheel Construction ---
# Center the wheel relative to the right end of the main axle
wheel_center_offset = axle_length - (wheel_hub_length / 2)

# Wheel Hub
hub = (
    cq.Workplane("XY")
    .workplane(offset=wheel_center_offset - wheel_hub_length/2)
    .circle(wheel_hub_diameter / 2)
    .extrude(wheel_hub_length)
)

# Wheel Rim
# The rim is often centered with the hub, or slightly offset. We'll center it.
rim_outer_r = wheel_diameter / 2
rim_inner_r = rim_outer_r - wheel_rim_thickness
rim = (
    cq.Workplane("XY")
    .workplane(offset=wheel_center_offset - wheel_rim_width/2)
    .circle(rim_outer_r)
    .circle(rim_inner_r)
    .extrude(wheel_rim_width)
)

# Add grooves/treads to the rim (simulated by cutting thin rings)
num_grooves = 4
groove_depth = 0.5
groove_width = 1.0
groove_spacing = wheel_rim_width / (num_grooves + 1)

grooves = cq.Workplane("XY")
for i in range(num_grooves):
    z_pos = (wheel_center_offset - wheel_rim_width/2) + (i + 1) * groove_spacing
    groove = (
        cq.Workplane("XY")
        .workplane(offset=z_pos - groove_width/2)
        .circle(rim_outer_r + 0.1) # Start outside
        .circle(rim_outer_r - groove_depth)
        .extrude(groove_width)
    )
    # Since we can't easily union an empty workplane loop, we subtract directly from rim later
    # For now, let's just make the rim geometry with cuts applied
    rim = rim.cut(groove)

# Wheel Spokes
# Create a single spoke and rotate it
spoke_length = (rim_inner_r - (wheel_hub_diameter / 2)) 
# Position spoke in the middle of the rim width
spoke_z_center = wheel_center_offset 

def create_spoke(angle):
    s = (
        cq.Workplane("XY")
        .workplane(offset=spoke_z_center - spoke_thickness/2)
        .transformed(rotate=(0, 0, angle))
        .moveTo((wheel_hub_diameter / 2) - 1, -spoke_width/2) # Start slightly inside hub
        .rect(spoke_length + 2, spoke_width, centered=False) # +2 to ensure overlap
        .extrude(spoke_thickness)
    )
    return s

all_spokes = create_spoke(0)
for i in range(1, spoke_count):
    all_spokes = all_spokes.union(create_spoke(i * (360 / spoke_count)))

# Combine Wheel Components
wheel = hub.union(rim).union(all_spokes)

# --- Final Assembly ---
result = axle.union(left_stub).union(right_stub).union(flange).union(wheel)

# Apply some fillets for realism
# Fillet the flange connection
result = result.edges(
    cq.selectors.NearestToPointSelector((0, flange_diameter/2, 10))
).fillet(flange_fillet)

result = result.edges(
    cq.selectors.NearestToPointSelector((0, flange_diameter/2, 10 + flange_thickness))
).fillet(flange_fillet)

# Fillet where spokes meet rim (optional, can be computationally expensive but looks good)
# result = result.edges("|Z").fillet(0.5) 

# Ensure the bore hole goes through everything
final_bore = (
    cq.Workplane("XY")
    .workplane(offset=-axle_end_stub_length - 1)
    .circle(axle_end_stub_diameter / 2 - 2.0) # Inner hole diameter
    .extrude(axle_length + axle_end_stub_length*2 + 2)
)

# Hollow out the axle if intended to be a tube, or just add center holes at ends
# Based on the image, it looks solid, but usually axles have center drills or are tubes.
# We will leave it solid as per typical simple CAD representations, 
# but adding a small chamfer to the very ends makes it look finished.

result = result.faces("<Z").chamfer(0.5)
result = result.faces(">Z").chamfer(0.5)
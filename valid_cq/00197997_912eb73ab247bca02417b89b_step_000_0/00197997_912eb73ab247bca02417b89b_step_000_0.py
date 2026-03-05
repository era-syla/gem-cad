import cadquery as cq

# Model parameters
outer_diameter = 10.0
inner_diameter = 7.5
length = 50.0
cut_angle = 50.0  # Degrees of tilt for the cut

# Create the hollow tube geometry
# Step 1: Draw concentric circles and extrude to create the pipe
tube = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(length)
)

# Step 2: Create a cutting solid (negative volume) to slice the tip
# We create a workplane at the top of the tube, rotate it, 
# and create a large block to subtract from the tube.
cutter = (
    cq.Workplane("XY")
    .workplane(offset=length)
    .transformed(rotate=(cut_angle, 0, 0))
    .rect(outer_diameter * 4, outer_diameter * 4)  # Ensure cutter covers the whole diameter
    .extrude(length) # Extrude 'up' relative to the angled plane
)

# Step 3: Subtract the cutter from the tube to get the final result
result = tube.cut(cutter)
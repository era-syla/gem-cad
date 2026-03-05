import cadquery as cq

# --- Parametric Dimensions ---
total_height = 100.0        # Total height of the object
main_od = 24.0              # Outer diameter of the main upper body
main_id = 18.0              # Inner diameter (through-hole)
neck_od = 21.0              # Outer diameter of the bottom neck section
neck_height = 15.0          # Height of the neck section
ring_height = 4.0           # Height of the solid ring at the very bottom
window_height = 7.0         # Vertical height of the cutout windows
window_width = 10.0         # Width of the cutout windows

# --- Modeling Steps ---

# 1. Create the Neck (Bottom Cylinder)
# Centered at Z=0
neck = cq.Workplane("XY").circle(neck_od / 2.0).extrude(neck_height)

# 2. Create the Main Body (Top Cylinder)
# Starts where the neck ends and extends to total height
main_body = (
    cq.Workplane("XY")
    .workplane(offset=neck_height)
    .circle(main_od / 2.0)
    .extrude(total_height - neck_height)
)

# 3. Combine the base cylinders
result = neck.union(main_body)

# 4. Create the Central Bore
# Cut a hole through the entire length of the part
result = result.faces(">Z").workplane().hole(main_id)

# 5. Create the Windows
# We define a "cutter" object: a rectangular bar that passes through the diameter.
# This cuts two opposing windows at once.
cutter = (
    cq.Workplane("XY")
    .rect(neck_od * 2.0, window_width)  # Width long enough to pass through, Height is window width
    .extrude(window_height)             # Extrude to window vertical height
    .translate((0, 0, ring_height))     # Lift Z to start above the bottom ring
)

# Subtract the cutter from the main body (0 and 180 degrees)
result = result.cut(cutter)

# Rotate the cutter 90 degrees and subtract again (90 and 270 degrees)
result = result.cut(cutter.rotate((0, 0, 0), (0, 0, 1), 90))

# 6. Finishing Touches
# Add a small chamfer to the top rim edges for realism
result = result.faces(">Z").edges().chamfer(0.5)
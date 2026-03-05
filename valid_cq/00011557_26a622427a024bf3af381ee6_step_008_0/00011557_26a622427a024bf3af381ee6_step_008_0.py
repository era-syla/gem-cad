import cadquery as cq

# --- Parameters ---
# Dimensions based on visual estimation to match the image proportions
pipe_od = 10.0          # Outer diameter of the pipe
pipe_id = 8.0           # Inner diameter (for hollow pipe)
main_length = 300.0     # Length of the bottom horizontal pipe
riser_height = 80.0     # Height of the vertical section
offset_length = 40.0    # Length of the perpendicular offset (depth)
top_run_length = 100.0  # Length of the top horizontal return
bend_radius = 15.0      # Radius of the pipe bends

# Fitting parameters for the Tee junction
tee_scale = 1.2
tee_length = 25.0

# --- 1. Main Horizontal Pipe ---
# Modeled as a cylinder centered at the origin aligned with the X-axis
main_pipe = (
    cq.Workplane("YZ")
    .circle(pipe_od / 2.0)
    .circle(pipe_id / 2.0)
    .extrude(main_length)
    .translate((-main_length / 2.0, 0, 0))
)

# --- 2. Branch Pipe Geometry ---
# Define the 3D path: Start -> Up -> Offset(Y) -> Return(-X)
# Points: Origin -> Top of Riser -> End of Offset -> End of Top Run
p0 = cq.Vector(0, 0, 0)
p1 = cq.Vector(0, 0, riser_height)
p2 = cq.Vector(0, offset_length, riser_height)
p3 = cq.Vector(-top_run_length, offset_length, riser_height)

# Create edges connecting the points
e1 = cq.Edge.makeLine(p0, p1)
e2 = cq.Edge.makeLine(p1, p2)
e3 = cq.Edge.makeLine(p2, p3)

# Assemble edges into a wire and apply fillets to create elbows
branch_path_wire = cq.Wire.assembleEdges([e1, e2, e3])
branch_path_filleted = branch_path_wire.fillet(bend_radius)

# Sweep the pipe profile along the filleted path
branch_pipe = (
    cq.Workplane("XY")
    .circle(pipe_od / 2.0)
    .circle(pipe_id / 2.0)
    .sweep(branch_path_filleted, isFrenet=True)
)

# --- 3. Tee Junction Detail ---
# Add a slightly thicker fitting at the intersection to resemble a Tee connector
tee_horizontal = (
    cq.Workplane("YZ")
    .circle(pipe_od * tee_scale / 2.0)
    .circle(pipe_id / 2.0)
    .extrude(tee_length)
    .translate((-tee_length / 2.0, 0, 0))
)

tee_vertical = (
    cq.Workplane("XY")
    .circle(pipe_od * tee_scale / 2.0)
    .circle(pipe_id / 2.0)
    .extrude(tee_length / 1.5)
    .translate((0, 0, -pipe_od/2.0)) # Sink slightly to blend
)

tee_fitting = tee_horizontal.union(tee_vertical)

# --- 4. Final Assembly ---
# Combine the main pipe, the branch, and the tee fitting
result = main_pipe.union(branch_pipe).union(tee_fitting)
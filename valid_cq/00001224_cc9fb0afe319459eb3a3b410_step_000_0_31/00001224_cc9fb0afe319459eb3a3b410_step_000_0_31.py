import cadquery as cq
import math

# --- Parameters ---
R_pipe_out = 10.0
R_pipe_in = 9.0
H_main = 100.0

R_ring_out = 13.5
H_ring = 3.0
ring_fillet = 1.0

angle_deg = 20.0
L1 = 15.0
R_bend = 25.0
drop_len = 35.0
start_z = 8.0

# --- Calculations ---
A = math.radians(angle_deg)

p1_x = L1 * math.cos(A)
p1_z = start_z + L1 * math.sin(A)

# Center of the tangent arc
cx = p1_x + R_bend * math.sin(A)
cz = p1_z - R_bend * math.cos(A)

# End point of the arc (tangent straight down)
p2_x = cx + R_bend
p2_z = cz

end_x = p2_x
end_z = p2_z - drop_len

# --- Outer Geometry ---
main_outer = (
    cq.Workplane("XY")
    .circle(R_pipe_out)
    .extrude(H_main)
    .translate((0, 0, -H_main/2))
)

ring = (
    cq.Workplane("XY", origin=(0, 0, -H_ring/2))
    .circle(R_ring_out)
    .extrude(H_ring)
    .edges("%CIRCLE")
    .fillet(ring_fillet)
)

# Tangent vector at the start of the side path
dx = math.cos(A)
dz = math.sin(A)

path = (
    cq.Workplane("XZ")
    .moveTo(0, start_z)
    .lineTo(p1_x, p1_z)
    .tangentArcPoint((p2_x, p2_z))
    .lineTo(end_x, end_z)
    .wire()
)

profile_plane = cq.Plane(origin=(0, 0, start_z), xDir=(0, 1, 0), normal=(dx, 0, dz))

side_outer = cq.Workplane(profile_plane).circle(R_pipe_out).sweep(path)

# Combine all outer parts
outer = main_outer.union(ring).union(side_outer)

# --- Inner Geometry (for hollowing) ---
main_inner = (
    cq.Workplane("XY")
    .circle(R_pipe_in)
    .extrude(H_main + 10.0)
    .translate((0, 0, -(H_main + 10.0)/2))
)

# Extend the inner path slightly at the end to ensure a clean boolean cut
path_inner = (
    cq.Workplane("XZ")
    .moveTo(0, start_z)
    .lineTo(p1_x, p1_z)
    .tangentArcPoint((p2_x, p2_z))
    .lineTo(end_x, end_z - 5.0)
    .wire()
)

side_inner = cq.Workplane(profile_plane).circle(R_pipe_in).sweep(path_inner)

# Combine all inner hollow parts
inner = main_inner.union(side_inner)

# --- Final Object ---
result = outer.cut(inner)
import cadquery as cq

# Base chassis
base = cq.Workplane("XY").box(60, 30, 10)

# Wheels
wheel = cq.Workplane("XY").circle(5).extrude(4)
wheel_positions = [(25,15), (-25,15), (25,-15), (-25,-15)]
wheels = None
for x, y in wheel_positions:
    w = wheel.translate((x, y, -2))
    wheels = w if wheels is None else wheels.union(w)

# Main body
body = cq.Workplane("XY").transformed(offset=(0,0,5)).box(40, 30, 30)

# Side hydraulic cylinder
cylinder = cq.Workplane("XY").transformed(offset=(20,0,25)).circle(5).extrude(20)

# Mast beams
mast1 = cq.Workplane("XY").transformed(offset=(0,8,10)).box(2, 2, 40)
mast2 = cq.Workplane("XY").transformed(offset=(0,-8,10)).box(2, 2, 40)

# Fork carriage
carriage = cq.Workplane("XY").transformed(offset=(10,0,12)).box(12, 2, 4)

# Forks
fork_left = cq.Workplane("XY").transformed(offset=(16,4,10)).box(30, 1, 1)
fork_right = cq.Workplane("XY").transformed(offset=(16,-4,10)).box(30, 1, 1)

# Overhead canopy supports
support1 = cq.Workplane("XY").transformed(offset=(-20,10,10)).box(2, 2, 35)
support2 = cq.Workplane("XY").transformed(offset=(-20,-10,10)).box(2, 2, 35)

# Canopy grid
grid = None
grid_thk = 1
grid_len_x = 40
grid_len_y = 25
num_bars = 5
spacing_x = grid_len_x / (num_bars-1)
spacing_y = grid_len_y / (num_bars-1)
z_grid = 45
for i in range(num_bars):
    # bars along X
    bx = cq.Workplane("XZ").transformed(offset=(-grid_len_x/2, -grid_len_y/2 + i*spacing_y, z_grid)).box(grid_len_x, grid_thk, grid_thk)
    # bars along Y
    by = cq.Workplane("YZ").transformed(offset=(-grid_len_x/2 + i*spacing_x, 0, z_grid)).box(grid_thk, grid_len_y, grid_thk)
    grid = bx if grid is None else grid.union(bx)
    grid = grid.union(by)

# Assemble all parts
result = base.union(wheels).union(body).union(cylinder).union(mast1).union(mast2)\
    .union(carriage).union(fork_left).union(fork_right).union(support1).union(support2).union(grid)
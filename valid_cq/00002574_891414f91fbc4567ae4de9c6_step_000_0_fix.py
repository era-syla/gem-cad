import cadquery as cq

# Building parameters
wall_thickness = 0.3
height = 3.0
outer_x = 10.0
outer_y = 8.0

# The building has an L-shape footprint (main section minus a corner cutout)
# Main rectangle minus upper-right corner cutout
main_x = outer_x
main_y = outer_y
cutout_x = 3.0
cutout_y = 3.0

# Create L-shaped floor plan using a polyline
# Coordinates for L-shape (missing upper-right corner)
pts = [
    (0, 0),
    (main_x, 0),
    (main_x, main_y - cutout_y),
    (main_x - cutout_x, main_y - cutout_y),
    (main_x - cutout_x, main_y),
    (0, main_y),
    (0, 0),
]

# Create the outer shell as L-shape
outer_shell = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(height)
)

# Create inner cutout (hollow interior) - also L-shaped but inset by wall_thickness
wt = wall_thickness
inner_pts = [
    (wt, wt),
    (main_x - wt, wt),
    (main_x - wt, main_y - cutout_y - wt),
    (main_x - cutout_x - wt, main_y - cutout_y - wt),
    (main_x - cutout_x - wt, main_y - wt),
    (wt, main_y - wt),
    (wt, wt),
]

inner_cut = (
    cq.Workplane("XY")
    .polyline(inner_pts)
    .close()
    .extrude(height)
)

# Subtract inner from outer to get walls
walls = outer_shell.cut(inner_cut)

# Add interior wall dividing the space (vertical partition)
# Interior wall running parallel to Y axis (creating a room on the right)
interior_wall_x = main_x - cutout_x - wt
int_wall1 = (
    cq.Workplane("XY")
    .transformed(offset=(interior_wall_x, wt, 0))
    .rect(wall_thickness, main_y - cutout_y - 2 * wt, centered=False)
    .extrude(height)
)

walls = walls.union(int_wall1)

# Add windows - cut rectangular holes in walls
# Window on front wall (Y=0 face)
def add_window_front(shape, x_pos, w, h, z_pos):
    cut = (
        cq.Workplane("XY")
        .transformed(offset=(x_pos, 0, z_pos))
        .rect(w, wall_thickness * 2, centered=False)
        .extrude(h)
    )
    return shape.cut(cut)

def add_window_back(shape, x_pos, w, h, z_pos):
    cut = (
        cq.Workplane("XY")
        .transformed(offset=(x_pos, main_y - wall_thickness * 2, z_pos))
        .rect(w, wall_thickness * 2, centered=False)
        .extrude(h)
    )
    return shape.cut(cut)

def add_window_left(shape, y_pos, w, h, z_pos):
    cut = (
        cq.Workplane("XY")
        .transformed(offset=(0, y_pos, z_pos))
        .rect(wall_thickness * 2, w, centered=False)
        .extrude(h)
    )
    return shape.cut(cut)

def add_window_right(shape, y_pos, w, h, z_pos):
    cut = (
        cq.Workplane("XY")
        .transformed(offset=(main_x - wall_thickness * 2, y_pos, z_pos))
        .rect(wall_thickness * 2, w, centered=False)
        .extrude(h)
    )
    return shape.cut(cut)

win_w = 1.5
win_h = 1.2
win_z = 0.8

# Front wall windows
walls = add_window_front(walls, 1.5, win_w, win_h, win_z)
walls = add_window_front(walls, 5.5, win_w, win_h, win_z)

# Back wall windows (only up to where cutout begins)
walls = add_window_back(walls, 1.5, win_w, win_h, win_z)
walls = add_window_back(walls, 4.0, win_w, win_h, win_z)

# Left wall windows
walls = add_window_left(walls, 1.5, win_w, win_h, win_z)
walls = add_window_left(walls, 4.5, win_w, win_h, win_z)

# Right wall windows (lower part only)
walls = add_window_right(walls, 1.0, win_w, win_h, win_z)

result = walls
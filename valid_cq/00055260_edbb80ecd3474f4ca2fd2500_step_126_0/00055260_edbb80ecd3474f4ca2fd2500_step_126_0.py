import cadquery as cq

# Dimensions
od = 20.0
length = 25.0
id = 6.0
hub_length = 6.0
helix_pitch = 2.0
cut_width = 0.8
hole_dia = 2.5
hole_offset = 3.0

# 1. Base Cylinder with Bore
result = (
    cq.Workplane("XY")
    .circle(od / 2.0)
    .extrude(length)
    .faces(">Z")
    .workplane()
    .hole(id)
)

# 2. Helical Cut
# Calculate helix parameters
helix_height = length - 2 * hub_length
helix_radius = od / 2.0

# Create the helix path wire
# makeHelix creates a wire centered at origin, we translate it to the hub start
helix_wire = cq.Wire.makeHelix(
    pitch=helix_pitch,
    height=helix_height,
    radius=helix_radius
).translate(cq.Vector(0, 0, hub_length))

# Create the cutting profile
# We define a plane perpendicular to the start of the helix
p0 = helix_wire.startPoint()
t0 = helix_wire.tangentAt(0)
# Define radial inward vector at the start point (assuming start is at angle 0)
# makeHelix starts at (r, 0, 0), so inward is (-1, 0, 0)
rad_in = cq.Vector(-1, 0, 0)

# Construct plane: Normal=Tangent, X-Axis=Radial Inward
profile_plane = cq.Plane(origin=p0, normal=t0, xDir=rad_in)

# Determine cut depth (through the wall)
cut_depth = (od - id) / 2.0 + 1.0

# Create the sweep cutter
# Draw a rectangle on the profile plane.
# X-axis is inward. We center at depth/2 so it cuts from surface (0) to depth.
cutter = (
    cq.Workplane(profile_plane)
    .center(cut_depth / 2.0, 0)
    .rect(cut_depth, cut_width)
    .sweep(cq.Workplane(obj=helix_wire), isFrenet=True)
)

# Apply the cut
result = result.cut(cutter)

# 3. Set Screw Holes
# Helper function to cut radial holes
def add_radial_hole(part, z, angle):
    # Create a cylindrical cutter
    # Orient along X, rotate to angle, move to Z
    c = (
        cq.Workplane("YZ")
        .circle(hole_dia / 2.0)
        .extrude(od + 5.0)  # Length sufficient to cross the wall
        .translate(cq.Vector(-od / 2.0 - 2.5, 0, 0)) # Position outside
        .rotate((0, 0, 0), (0, 0, 1), angle)
        .translate(cq.Vector(0, 0, z))
    )
    return part.cut(c)

# Add holes at bottom hub
result = add_radial_hole(result, hole_offset, 0)
result = add_radial_hole(result, hole_offset, 90)

# Add holes at top hub
result = add_radial_hole(result, length - hole_offset, 0)
result = add_radial_hole(result, length - hole_offset, 90)
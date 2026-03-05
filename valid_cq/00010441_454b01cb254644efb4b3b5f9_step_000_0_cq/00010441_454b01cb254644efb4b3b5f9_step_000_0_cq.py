import cadquery as cq
import math

# ------------------------------------------------------------------
# Parametric definitions
# ------------------------------------------------------------------
radius = 50.0  # Overall radius of the sphere
thickness = 2.0  # Thickness of the spiral arms
num_spirals = 6  # Number of arms in each swirl pattern
arm_angle = 120.0  # How much an arm wraps around in degrees
inner_gap = 5.0  # Gap in the center of the swirl

# The pattern is distributed on the faces of a Dodecahedron (12 faces)
# or an Icosahedron (20 faces). Looking at the symmetries, this looks
# like an Icosahedral layout, but the 6-way symmetry of the swirls 
# suggests vertices of an icosahedron (where 5 triangles meet) or 
# faces of a dodecahedron (which are pentagons). 
# Wait, the swirls clearly have 6 arms? Let's recount.
# Looking closely at the image, there are points where arms converge.
# It looks like 5 arms converging at some points and maybe 6 at others?
# Actually, the most prominent features are "swirls".
# Let's count arms on one swirl. It looks like 5 or 6 curved blades.
# Standard geodesic patterns usually map to icosahedrons (5-fold symmetry vertices)
# or dodecahedrons (5-sided faces).
# If it's a Rhombic Triacontahedron or similar, it gets complex.
# Let's assume a layout based on the vertices of a regular Icosahedron.
# An Icosahedron has 12 vertices. At each vertex, 5 triangles meet.
# This implies 5-fold symmetry. The image shows swirls that look somewhat like 5-fold.
# Let's try to model a single 5-arm spiral unit and place it on the 12 vertices of an Icosahedron.

# ------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------

def create_spiral_arm(r_outer, r_inner, thick):
    """
    Creates a single curved, saw-toothed arm for the spiral.
    This is a 2D profile that will be extruded.
    """
    # Define points for a curved, saw-toothed shape
    # We'll use a spline for the back and a zigzag for the front
    
    # Outer curve points (smooth back)
    pts_outer = [
        (r_inner, 0),
        (r_inner + (r_outer-r_inner)*0.3, 5),
        (r_inner + (r_outer-r_inner)*0.6, 15),
        (r_outer, 35)
    ]
    
    # Inner curve points (saw-toothed front)
    # We will construct this as a series of lines relative to the curve
    pts_inner = [
        (r_outer, 35),
        (r_outer - 5, 25), # tooth 1 down
        (r_outer - 2, 28), # tooth 1 up
        (r_outer - 8, 18), # tooth 2 down
        (r_outer - 5, 21), # tooth 2 up
        (r_outer - 12, 10), # tooth 3 down
        (r_outer - 9, 13), # tooth 3 up
        (r_inner, 0)       # close loop
    ]
    
    # Create the face
    # Note: This is a rough approximation of the aesthetic in the image
    arm = (
        cq.Workplane("XY")
        .moveTo(*pts_outer[0])
        .spline(pts_outer[1:])
        .lineTo(*pts_inner[1])
        .lineTo(*pts_inner[2])
        .lineTo(*pts_inner[3])
        .lineTo(*pts_inner[4])
        .lineTo(*pts_inner[5])
        .lineTo(*pts_inner[6])
        .close()
    )
    
    return arm

def create_swirl_unit(radius, thickness):
    """
    Creates one complete swirl unit consisting of 5 interlocking arms.
    """
    # Dimensions for the arm
    r_outer = radius * 0.55  # Radius of the swirl unit on the sphere surface (approx)
    r_inner = radius * 0.1
    
    # Create one arm profile
    arm_profile = create_spiral_arm(r_outer, r_inner, thickness)
    
    # Extrude it to give it 3D thickness
    # We extrude slightly and will project/cut later, or just extrude straight for now
    arm_solid = arm_profile.extrude(thickness)
    
    # Pattern the arm 5 times (for icosahedral vertex symmetry)
    swirl = cq.Workplane("XY")
    for i in range(5):
        angle = i * (360.0 / 5.0)
        rotated_arm = arm_solid.rotate((0,0,0), (0,0,1), angle)
        swirl = swirl.union(rotated_arm)
        
    return swirl

# ------------------------------------------------------------------
# Main Geometry Construction
# ------------------------------------------------------------------

# 1. Generate the base swirl pattern centered at origin
swirl_unit = create_swirl_unit(radius, thickness)

# 2. Define Icosahedron Vertices
# Golden ratio
phi = (1 + math.sqrt(5)) / 2
# Normalized vertices of an icosahedron
verts = [
    (0, 1, phi), (0, -1, phi), (0, 1, -phi), (0, -1, -phi),
    (1, phi, 0), (-1, phi, 0), (1, -phi, 0), (-1, -phi, 0),
    (phi, 0, 1), (phi, 0, -1), (-phi, 0, 1), (-phi, 0, -1)
]

# 3. Place the swirl unit on the sphere at each vertex
result = cq.Workplane("XY")

# To project onto a sphere properly, we would ideally intersect with a spherical shell.
# However, placing flat units tangent to the sphere surface is a good approximation
# for this kind of "ball of parts" aesthetic.

sphere_shell = cq.Workplane("XY").sphere(radius).cut(cq.Workplane("XY").sphere(radius - thickness*2))

for v in verts:
    # Normalize vector
    mag = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    vn = (v[0]/mag, v[1]/mag, v[2]/mag)
    
    # Position for the swirl (slightly embedded in the sphere radius)
    pos = (vn[0]*radius, vn[1]*radius, vn[2]*radius)
    
    # Orientation logic:
    # We need to rotate the swirl (which is in XY plane) so its Z axis points along the normal 'vn'
    # Default Z is (0,0,1). We need rotation from (0,0,1) to vn.
    
    # Axis of rotation is cross product of Z and vn
    z_axis = (0, 0, 1)
    
    # Handle the case where vn is parallel to Z
    if abs(vn[2]) > 0.999:
        # Just translate, maybe flip if opposite
        if vn[2] > 0:
            rotated_swirl = swirl_unit.translate(pos)
        else:
            rotated_swirl = swirl_unit.rotate((0,0,0),(1,0,0), 180).translate(pos)
    else:
        # Cross product
        rot_axis = (
            z_axis[1]*vn[2] - z_axis[2]*vn[1],
            z_axis[2]*vn[0] - z_axis[0]*vn[2],
            z_axis[0]*vn[1] - z_axis[1]*vn[0]
        )
        
        # Dot product for angle
        dot = z_axis[0]*vn[0] + z_axis[1]*vn[1] + z_axis[2]*vn[2]
        rot_angle = math.degrees(math.acos(dot))
        
        # Apply rotation and translation
        rotated_swirl = swirl_unit.rotate((0,0,0), rot_axis, rot_angle).translate(pos)
    
    result = result.union(rotated_swirl)

# 4. Refine the shape to match the sphere curvature
# The flat swirls stick out. We intersect the whole assembly with a hollow sphere (shell)
# to curve the outer and inner surfaces of the blades.
outer_sphere = cq.Workplane("XY").sphere(radius)
inner_sphere = cq.Workplane("XY").sphere(radius - thickness * 1.5)
spherical_shell_cutter = outer_sphere.cut(inner_sphere)

# Intersecting the accumulated swirls with the spherical shell forces them into the spherical shape
result = result.intersect(spherical_shell_cutter)

# Optional: Add an inner core if needed (image shows hollow-ish but maybe a dark core)
# We will leave it as the shell structure which matches the visual "cage" look.
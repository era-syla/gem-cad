import cadquery as cq

# --- Parameters ---

# Cage parameters
cage_radius = 30.0    # Approximate radius of the outer structure
strut_thickness = 3.0 # Thickness of the cage bars

# Inner core parameters
core_radius = 12.0
core_thickness = 8.0
hub_radius = 5.0
hub_length = 8.0
axle_radius = 2.0
axle_length = cage_radius * 0.9  # Axle spans most of the cage

# Text parameters
text_string = "CadQuery"
text_size = 5.0
text_depth = 1.0

# --- Helper Functions ---

def create_wireframe_cage(radius, thickness):
    """
    Creates a wireframe structure resembling the truncated octahedron 
    or rhombicuboctahedron-like cage seen in the image.
    Simplified approach: Create a solid shape and hollow it out with framing.
    """
    # Create the base solid: A box intersected with a rotated box to approximate the polyhedral shape
    # The image looks like a Rhombic Dodecahedron or similar dual-polyhedron wireframe.
    # Let's approximate it by creating a skeletal structure based on a cube with chamfered corners (Truncated Hexahedron/Octahedron).
    
    # Strategy: Build a solid block that represents the envelope, then subtract the faces.
    
    # 1. Create a base Platonic/Archimedean solid. 
    # The shape in the image has square faces and hexagonal faces. This is a Truncated Octahedron.
    
    # A truncated octahedron can be made by intersecting a cube and an octahedron (or simply cutting corners off an octahedron).
    # Let's construct it manually using intersecting planes/solids or hulling vertices.
    
    # Alternative Strategy (easier in CQ for wireframes): 
    # Create a solid, shell it, then cut holes in the faces.
    
    L = radius * 1.5 
    
    # Start with a Cube
    base = cq.Workplane("XY").box(L, L, L)
    
    # Cut the corners to create the 14-sided polyhedron (Truncated Octahedron)
    # A truncated octahedron is formed by cutting the corners of a cube such that the cut creates an equilateral triangle.
    # Cut depth needs to be specific.
    
    # Actually, looking closely at the image, it looks like a Rhombic Dodecahedron or simply a cube with very large chamfers.
    # Let's look at the symmetry. It has 4-fold symmetry around the axes.
    # It looks like 6 square faces and 8 hexagonal faces.
    
    # Let's try the intersection method: Cube intersected with Octahedron.
    cube = cq.Workplane("XY").box(L, L, L)
    octahedron = cq.Workplane("XY").box(L*1.2, L*1.2, L*1.2).rotate((0,0,0), (1,1,0), 45).rotate((0,0,0), (1,0,1), 45) 
    # Creating a perfect truncated octahedron via intersection is tricky with just boxes.
    
    # Let's use the standard "make a solid and cut faces" approach on a simple chamfered cube.
    # The shape in the image is specifically a Truncated Octahedron.
    # Vertices of a truncated octahedron permutation of (0, ±1, ±2)
    
    pts = []
    # Generate vertices for Truncated Octahedron
    # Permutations of (0, +/- 1, +/- 2) scaled
    scale = radius / 2.2
    for x in [0]:
        for y in [-1, 1]:
            for z in [-2, 2]:
                pts.append((x*scale, y*scale, z*scale))
                pts.append((x*scale, z*scale, y*scale))
                pts.append((y*scale, x*scale, z*scale))
                pts.append((y*scale, z*scale, x*scale))
                pts.append((z*scale, x*scale, y*scale))
                pts.append((z*scale, y*scale, x*scale))
    
    # Create a convex hull from these points to get the solid
    solid_poly = cq.Workplane("XY").polyhedron(pts)
    
    # Now we convert this solid into a wireframe.
    # We can do this by selecting faces and cutting/shelling, but a robust way for arbitrary 
    # polyhedra in CQ is to intersect the solid with a shelled version of itself? No.
    # The standard way: For each face, draw a shape on it and cut it through.
    
    # Since the faces are planar, we can iterate over them.
    # However, detecting face types (square vs hexagon) automatically can be verbose.
    
    # Simplified wireframe construction:
    # 1. Create the solid.
    # 2. Hollow it out completely (shell).
    # 3. Cut holes in the center of every face.
    
    shelled = solid_poly.faces().shell(thickness)
    
    # Cut holes
    # We need to act on each face of the original solid to find normal and center
    faces = solid_poly.faces().vals()
    cutter = cq.Workplane("XY")
    
    for f in faces:
        # Get center and normal
        center = f.Center()
        normal = f.normalAt(center)
        
        # Determine face type by number of vertices/edges
        num_edges = len(f.Edges())
        
        # Offset for the cut (leave material for struts)
        # We need a workplane on this face
        wp = cq.Workplane(obj=f).workplaneFromTagged("f") # This is pseudo-code logic, let's use direct WP construction
        
        wp = cq.Workplane(plane=cq.Plane(origin=center, zDir=normal))
        
        # Determine size of cut based on face bounding box
        bbox = f.BoundingBox()
        dim = max(bbox.xlen, bbox.ylen, bbox.zlen)
        
        # Create a polygon to cut. 
        # If square (4 edges), cut a square. If Hex (6 edges), cut hex.
        # To be safe and generic, we can use an offset of the face wire, but 2D offset on arbitrary 3D face is complex in pure CQ api without OCP.
        
        # Approximate method: Cut a circle/polygon
        cut_radius = dim * 0.35 # Tuning parameter
        
        if num_edges == 4:
            # It's a square face
            cutter = cutter.union(wp.rect(dim*0.6, dim*0.6).extrude(thickness*3, both=True))
        else:
             # It's a hexagonal face
            cutter = cutter.union(wp.polygon(6, dim*0.7).extrude(thickness*3, both=True))

    # Apply the cuts
    cage = shelled.cut(cutter)
    
    return cage

# --- Build the Inner Mechanism ---

def create_inner_assembly():
    # Central flattened sphere/disc
    core = cq.Workplane("YZ").circle(core_radius).extrude(core_thickness, both=True)
    
    # Add fillets to make it look like the smooth pebble in the image
    core = core.edges().fillet(core_thickness/2.0 - 0.1)
    
    # Add Text on the face
    # We need to orient to the face of the disc
    # The disc was extruded along X axis (YZ plane extrusion).
    text_wp = cq.Workplane("YZ").workplane(offset=core_thickness/2.0)
    text = text_wp.text(text_string, fontsize=text_size, distance=text_depth)
    
    # Add the text to the core
    core = core.union(text)
    
    # Create the axle hubs (cylinders on the sides)
    hub_wp = cq.Workplane("YZ")
    hubs = hub_wp.circle(hub_radius).extrude(hub_length + core_thickness/2.0, both=True)
    
    # Axle connecting to the cage
    axle_wp = cq.Workplane("YZ")
    axle = axle_wp.circle(axle_radius).extrude(axle_length/2.0, both=True)
    
    # End caps on the axle (where it meets the cage)
    cap_dist = axle_length/2.0
    cap_wp = cq.Workplane("YZ").workplane(offset=cap_dist)
    cap1 = cap_wp.circle(hub_radius).extrude(2)
    cap_wp2 = cq.Workplane("YZ").workplane(offset=-cap_dist-2)
    cap2 = cap_wp2.circle(hub_radius).extrude(2)
    
    # Combine internal parts
    assembly = core.union(hubs).union(axle).union(cap1).union(cap2)
    
    # Rotate assembly to match image orientation (Text usually reads upright)
    # The image shows the text reading roughly along X/Y
    assembly = assembly.rotate((0,0,0), (0,0,1), 45) # slight twist
    
    return assembly

# --- Build the Wireframe Cage (Geometric Approach) ---
# Since the helper function above with `polyhedron` might be complex to get perfect normals for 2D sketches,
# let's build the cage using constructive solid geometry with simple primitives which is more robust for a generated script.

def create_robust_cage():
    # A truncated octahedron cage can be approximated by intersecting a hollow cube and a hollow octahedron,
    # or by building the struts directly.
    
    # Let's use the "Lattice" approach: Define vertices and connect them with cylinders/rectangles.
    # Vertices of Truncated Octahedron: Permutations of (0, ±1, ±2)
    
    points = []
    scale = cage_radius / 2.0
    
    # Generate vertices
    perms = [
        (0, 1, 2), (0, 1, -2), (0, -1, 2), (0, -1, -2),
        (0, 2, 1), (0, 2, -1), (0, -2, 1), (0, -2, -1),
        (1, 0, 2), (1, 0, -2), (-1, 0, 2), (-1, 0, -2),
        (2, 0, 1), (2, 0, -1), (-2, 0, 1), (-2, 0, -1),
        (1, 2, 0), (1, -2, 0), (-1, 2, 0), (-1, -2, 0),
        (2, 1, 0), (2, -1, 0), (-2, 1, 0), (-2, -1, 0)
    ]
    
    vertices = []
    for p in perms:
        vertices.append(cq.Vector(p[0]*scale, p[1]*scale, p[2]*scale))

    # Define edges based on distance. In a truncated octahedron, edges have length sqrt(2).
    # With our (0,1,2) basis, edge length is sqrt((1-0)^2 + (2-1)^2 + (0-0)^2) = sqrt(2).
    # Any two vertices with distance approx sqrt(2)*scale are connected.
    
    struts = cq.Assembly()
    
    edges_drawn = set()
    
    cage_geo = cq.Workplane("XY")
    
    # Tolerance for distance check
    target_dist_sq = (scale**2) * 2
    tol = scale * 0.1
    
    for i, v1 in enumerate(vertices):
        for j, v2 in enumerate(vertices):
            if i >= j: continue
            
            diff = v1 - v2
            dist_sq = diff.Length**2
            
            if abs(dist_sq - target_dist_sq) < (target_dist_sq * 0.1):
                # This is an edge
                # Create a rectangular strut connecting v1 and v2
                
                # We create a path and sweep a rectangle
                path = cq.Workplane("XY").polyline([v1.toTuple(), v2.toTuple()])
                
                # To orient the rectangular profile correctly is hard without a reference plane perpendicular to path.
                # Easiest valid geometry: Cylinders, or square pipes using `sweep`.
                
                # Constructing a plane perpendicular to the edge
                midpoint = (v1 + v2) * 0.5
                direction = (v2 - v1).normalized()
                
                # Make a generic plane for the profile
                plane = cq.Plane(origin=v1, normal=direction)
                
                # Create strut
                strut = cq.Workplane(plane).rect(strut_thickness, strut_thickness).extrude((v2-v1).Length)
                
                cage_geo = cage_geo.union(strut)
                
    return cage_geo

# --- Execution ---

# 1. Create the cage
cage = create_robust_cage()

# 2. Create the inner spinner
spinner = create_inner_assembly()

# 3. Combine
# The image shows the spinner axle aligned with two opposing square faces of the cage.
# The truncated octahedron has vertices at (0, +/-1, +/-2).
# The square faces are perpendicular to the coordinate axes (X, Y, Z).
# The current spinner is aligned along X (extruded YZ).
# We need to ensure it fits inside. The cage radius is approx 30.
# The robust cage logic generates vertices. The square faces are at distance 2*scale = 30.
# The axle length is 27. It should fit.

# Rotate the whole result to a nice isometric view similar to the image
result = cage.union(spinner)
result = result.rotate((0,0,0), (1,0,0), -20).rotate((0,0,0), (0,1,0), 20)
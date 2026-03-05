import cadquery as cq
import math

def create_star_tetrahedron():
    # --- Parameters ---
    # Radius of the circumscribed sphere for the tetrahedrons
    radius = 20.0  
    # Thickness of the structural bars
    bar_thickness = 2.5
    # Dimensions for the hanging loop
    loop_outer_radius = 2.0
    loop_inner_radius = 1.0
    loop_thickness = 1.0
    
    # --- Helper Calculation ---
    # Calculate vertices of a regular tetrahedron based on radius
    # A tetrahedron has 4 vertices.
    # We need two tetrahedrons, one inverted relative to the other.
    
    # Vertices for Tetrahedron A (pointing up)
    # Using standard geometric formulas for a tetrahedron inscribed in a sphere
    angle_step = 2 * math.pi / 3
    
    # Top vertex
    t1_v1 = (0, 0, radius)
    # Base vertices
    base_z = -radius / 3.0
    base_r = math.sqrt(radius**2 - base_z**2)
    
    t1_v2 = (base_r * math.cos(0), base_r * math.sin(0), base_z)
    t1_v3 = (base_r * math.cos(angle_step), base_r * math.sin(angle_step), base_z)
    t1_v4 = (base_r * math.cos(2*angle_step), base_r * math.sin(2*angle_step), base_z)
    
    tet1_vertices = [t1_v1, t1_v2, t1_v3, t1_v4]
    
    # Vertices for Tetrahedron B (pointing down) - simply inverted coordinates of A
    tet2_vertices = [(-v[0], -v[1], -v[2]) for v in tet1_vertices]

    # --- Frame Generation Function ---
    def create_tetrahedron_frame(vertices, thickness):
        frame = cq.Assembly()
        
        # Combinations of vertices for edges (4 vertices, 6 edges)
        # 0-1, 0-2, 0-3, 1-2, 2-3, 3-1
        indices = [(0,1), (0,2), (0,3), (1,2), (2,3), (3,1)]
        
        frame_geo = None
        
        for start_idx, end_idx in indices:
            p1 = vertices[start_idx]
            p2 = vertices[end_idx]
            
            # Vector math to orient the bar
            v1 = cq.Vector(p1)
            v2 = cq.Vector(p2)
            direction = v2 - v1
            length = direction.Length
            
            # Create a bar. We create it along Z and rotate/move it.
            # Using a rectangular profile, but extruded along a path is easier in CQ
            # Or creating a cylinder/box and locating it.
            
            # Method: Make a box at origin, rotate and translate.
            # Center of the edge
            midpoint = (v1 + v2) * 0.5
            
            # Create the edge geometry
            # We use a path sweep to ensure cleaner joints if we were careful, 
            # but simple union of boxes usually works for this aesthetic.
            # Let's use a box oriented along Z, then rotated.
            
            # Create a box along Z axis
            edge = (
                cq.Workplane("XY")
                .rect(thickness, thickness)
                .extrude(length)
                .translate((0, 0, -length / 2)) # Center vertically
            )
            
            # Rotate to align with the edge vector
            # Current vector is (0,0,1)
            target_vector = direction.normalized()
            
            # Compute rotation axis and angle
            z_axis = cq.Vector(0, 0, 1)
            rotation_axis = z_axis.cross(target_vector)
            
            # If vectors are parallel (e.g. vertical edge), cross product is zero
            if rotation_axis.Length < 1e-6:
                # If pointing down, flip 180 (though for a symmetric box it doesn't matter much)
                 if z_axis.dot(target_vector) < 0:
                     edge = edge.rotate((0,0,0), (1,0,0), 180)
            else:
                rotation_angle = math.degrees(math.acos(z_axis.dot(target_vector)))
                edge = edge.rotate((0,0,0), rotation_axis, rotation_angle)
            
            # Move to midpoint
            edge = edge.translate(midpoint)
            
            if frame_geo is None:
                frame_geo = edge
            else:
                frame_geo = frame_geo.union(edge)
                
        return frame_geo

    # --- Build Geometry ---
    
    # 1. Create the two tetrahedron frames
    tet1_frame = create_tetrahedron_frame(tet1_vertices, bar_thickness)
    tet2_frame = create_tetrahedron_frame(tet2_vertices, bar_thickness)
    
    # 2. Combine them
    star_tetrahedron = tet1_frame.union(tet2_frame)
    
    # 3. Add the Loop
    # We need to find a suitable vertex to attach the loop.
    # Looking at the image, the loop is on one of the outer points.
    # Let's pick t1_v2 (one of the base vertices of the "up" tetrahedron)
    attach_point = cq.Vector(t1_v2)
    
    # The loop needs to be oriented correctly. The image shows it standing up 
    # relative to the edge, or aligned with the radial vector.
    # Let's align the loop plane normal to the tangent of the sphere (radius vector).
    
    # Create the loop geometry at origin first
    loop = (
        cq.Workplane("XY")
        .circle(loop_outer_radius)
        .circle(loop_inner_radius)
        .extrude(loop_thickness)
        .translate((0, 0, -loop_thickness/2)) # Center thickness
    )
    
    # Orient the loop. It looks like the hole axis is roughly tangential to the structure.
    # Let's rotate it so the "face" of the ring is facing the viewer or sideways.
    # A simple approach: Rotate it 90 degrees on X to stand it up.
    loop = loop.rotate((0,0,0), (1,0,0), 90)
    
    # Move loop to the attachment point.
    # We want the loop to sit *on* the corner, slightly offset outward.
    offset_dist = loop_outer_radius * 0.8
    loop_pos = attach_point + attach_point.normalized() * offset_dist
    
    # Rotate loop to face outward radially
    # Current normal of the loop plane is Y (after the 90 deg rotation above).
    # We want to align that Y axis with the tangent or just position it.
    # Let's try simply translating first, then rotating to look "natural".
    
    # Vector from center to attach point
    radial_vec = attach_point.normalized()
    z_axis = cq.Vector(0,0,1)
    
    # Calculate rotation to align the loop's "up" with Z, and position radially
    # This is aesthetic. In the image, the loop is on a left-side vertex.
    
    # Move the loop
    loop = loop.translate(loop_pos)
    
    # Align loop orientation roughly with the corner
    # Calculate angle of the attach point in XY plane
    angle_xy = math.degrees(math.atan2(attach_point.y, attach_point.x))
    loop = loop.rotate((0,0,0), (0,0,1), angle_xy)
    
    # 4. Create a small connector/fillet blob between loop and frame
    # A small sphere or loft is usually used. Here a small sphere unioned works well.
    connector = (
        cq.Workplane("XY")
        .sphere(bar_thickness * 0.8)
        .translate(attach_point)
    )

    # Final union
    final_shape = star_tetrahedron.union(loop).union(connector)
    
    # Optional: Apply small fillets to edges to make it look manufactured/cast
    # This can be computationally expensive, so use a small value or skip if speed is needed.
    # final_shape = final_shape.edges().fillet(0.2)

    return final_shape

# Generate the model
result = create_star_tetrahedron()
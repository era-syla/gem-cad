import cadquery as cq
import math

def create_scroll_compressor_part():
    # Parameters for the scroll geometry
    # These parameters control the size and shape of the scroll
    base_radius = 50.0       # Radius of the circular base plate
    base_height = 5.0        # Thickness of the base plate
    
    wall_height = 40.0       # Height of the scroll wall
    wall_thickness = 8.0     # Thickness of the scroll wall
    
    start_angle = 0          # Starting angle of the spiral (in degrees)
    end_angle = 360 * 2.2    # Ending angle (e.g., 2.2 turns)
    pitch = 18.0             # Distance between successive turns of the spiral
    
    center_hole_radius = 5.0 # Radius of the central hole

    # Function to generate points for an involute of a circle or Archimedean spiral
    # Here we use an Archimedean-like spiral approximation which is easier to parameterize directly with pitch
    # Formula: r = a + b * theta
    def spiral_points(r_start, r_end_offset, angle_start, angle_end, num_points=200):
        points = []
        # Calculate b based on pitch: pitch = b * 2 * pi
        # So b = pitch / (2 * pi)
        b = pitch / (2 * math.pi)
        
        # We need two curves: inner and outer wall surfaces.
        # But CadQuery's sweep works best with a single path and a profile, 
        # or constructing a custom face. 
        # For a scroll, extruding a 2D sketch of the spiral area is usually most robust.
        
        # Let's define the center-line spiral and then offset it.
        # Or better, define inner and outer spiral paths explicitly.
        
        # Let's use a parametric approach to build the 2D face directly.
        
        # Convert degrees to radians for math
        rad_start = math.radians(angle_start)
        rad_end = math.radians(angle_end)
        
        # Base radius parameter 'a' determines the starting distance from center
        # For a tight center, 'a' is small.
        a = 10.0 
        
        pts_inner = []
        pts_outer = []
        
        step = (rad_end - rad_start) / num_points
        
        for i in range(num_points + 1):
            theta = rad_start + i * step
            
            # Archimedean spiral equation: r = a + b * theta
            # Centerline radius
            r_center = a + b * theta
            
            # Inner and outer radii
            r_in = r_center - wall_thickness / 2.0
            r_out = r_center + wall_thickness / 2.0
            
            # Convert polar to cartesian
            x_in = r_in * math.cos(theta)
            y_in = r_in * math.sin(theta)
            
            x_out = r_out * math.cos(theta)
            y_out = r_out * math.sin(theta)
            
            pts_inner.append((x_in, y_in))
            pts_outer.append((x_out, y_out))
            
        # To close the shape, we go forward along outer, then connect to inner (reversed)
        # We also need to close the tips.
        
        # Reversing inner points to form a continuous loop
        pts_combined = pts_outer + pts_inner[::-1]
        
        # Connect the last inner point to the first outer point to close the loop?
        # CadQuery makePolygon will close start to end automatically.
        
        return pts_combined

    # 1. Create the base plate
    # The base plate is usually a disk, but often follows the spiral shape or is a bounding circle.
    # Looking at the image, there is a base that tapers upwards (a fillet or chamfer) into the wall?
    # Actually, looking closely, the image shows the spiral wall sitting on a conical/curved hub surface.
    # The base itself isn't just a flat cylinder, it's a domed/conical shape.
    
    # Let's model the central hub/base first.
    # It looks like a shallow cone or spherical segment.
    base = cq.Workplane("XY").circle(base_radius).extrude(base_height)
    
    # Let's add a "dome" on top of the base, which creates the smooth transition in the center.
    # We can revolve a profile.
    dome_height = 15.0
    dome_profile = (
        cq.Workplane("XZ")
        .moveTo(0, base_height)
        .lineTo(base_radius, base_height)
        .spline([(center_hole_radius * 1.5, base_height + dome_height * 0.8), (0, base_height + dome_height)], includeCurrent=True)
        .close()
    )
    dome = dome_profile.revolve(360, (0,0,0), (0,1,0))
    
    # Combine base and dome
    base_structure = base.union(dome)
    
    # 2. Create the Spiral Wall
    # Generate the points for the 2D spiral profile
    spiral_pts = spiral_points(0, 0, start_angle, end_angle, num_points=300)
    
    # Create the 2D face for the spiral
    spiral_face = cq.Workplane("XY").polyline(spiral_pts).close().extrude(wall_height)
    
    # Now we need to handle the interaction between the spiral wall and the domed base.
    # The spiral wall should emerge from the domed surface.
    # The extrusion goes from Z=0 up to Z=wall_height.
    # We need to position it correctly. Let's move it so it sits properly.
    
    # In a real scroll, the wall height is constant relative to the base plane, 
    # but in the image, the center looks deeper.
    # However, usually the top of the scroll is flat (planar).
    # The extrusion `spiral_face` creates a flat top and flat bottom.
    
    # Let's shift the spiral up so its bottom is embedded in the base structure,
    # and its top is at the desired total height.
    spiral_wall = spiral_face.translate((0, 0, base_height))
    
    # The image shows the spiral wall extending downwards to meet the curved surface of the hub.
    # Since we extruded from a flat plane, the bottom of our spiral is flat.
    # To make it match the hub perfectly, we can union them.
    # If the spiral extrusion starts below the dome surface, the union will be seamless.
    # Let's move the spiral down slightly into the base.
    spiral_wall = spiral_wall.translate((0, 0, -2.0)) 
    # And ensure it's tall enough to extend above
    
    # 3. Create the center hole
    # A simple cut through the center
    
    # Assemble the parts
    # Union the base and the spiral
    model = base_structure.union(spiral_wall)
    
    # Cut the hole
    final_model = model.faces(">Z").workplane().circle(center_hole_radius).cutThruAll()

    # Optional: Fillets for better realism (computationally expensive, maybe skip for robustness or keep small)
    # The image shows smooth transitions, particularly at the root of the spiral.
    # In CadQuery, filleting complex intersections like a spiral on a dome can be fragile.
    # We will skip the root fillet to ensure script execution reliability, 
    # but the dome shape provides a visual approximation of that smooth rise.
    
    return final_model

# Generate the result
result = create_scroll_compressor_part()
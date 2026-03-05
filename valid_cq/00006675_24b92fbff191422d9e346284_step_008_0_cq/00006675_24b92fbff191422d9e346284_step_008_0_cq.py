import cadquery as cq

# Parameters
width = 80.0          # Overall width/height of the square base
thickness = 4.0       # Thickness of the base frame
corner_radius = 6.0   # Radius of the exterior corners
hole_spacing = 64.0   # Distance between mounting holes (center-to-center)
hole_diameter = 4.5   # Diameter of mounting holes
dome_height = 15.0    # Height of the domed section above the base
dome_diameter = 74.0  # Diameter of the dome base (slightly smaller than width)
grill_thickness = 2.0 # Thickness of the grill ribs

# Create the base frame
# Start with a rectangle and fillet corners
base = (cq.Workplane("XY")
    .rect(width, width)
    .extrude(thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# Add mounting holes
base = (base
    .faces(">Z")
    .workplane()
    .rect(hole_spacing, hole_spacing, forConstruction=True)
    .vertices()
    .cboreHole(hole_diameter, hole_diameter + 3.0, 1.0) # Simple counterbore or just a hole
)

# Create the dome shape for intersection
# We create a solid sphere and cut off the bottom to make a dome
sphere_radius = (dome_diameter**2 + (2*dome_height)**2) / (8*dome_height)
# Calculate center Z offset to position the dome correctly
center_z = thickness - (sphere_radius - dome_height)

dome = (cq.Workplane("XY")
    .workplane(offset=center_z)
    .sphere(sphere_radius)
)

# Create the grill pattern (The Biohazard Symbol)
# The biohazard symbol consists of circles and specific cutouts.
# We will draw this in 2D and then extrude it to intersect with the dome.

def biohazard_shape():
    # Primary setup
    outer_circle_radius = 28.0
    inner_cutout_radius = 20.0
    gap_width = 3.0
    
    # Base sketch
    s = cq.Sketch()
    
    # 1. The three main circular arcs (claws)
    # We create a full circle and then cut away parts
    
    # Center circle ring
    s = s.circle(outer_circle_radius)
    
    # The inner "cutting" circles that form the sharp points
    # These are shifted from the center.
    # The biohazard symbol has 3-fold symmetry.
    
    # Using a boolean approach on 2D geometry is often easier for complex symbols
    # Let's build the "positive" shape of the symbol first
    
    # The logic:
    # 1. Start with 3 main rings overlapping.
    # 2. Cut out the center.
    # 3. Cut out the gaps.
    
    # Alternative strategy: Construct explicit 2D faces using CadQuery Workplane logic
    # which is often more robust for simple geometric logos than pure Sketch
    
    wp = cq.Workplane("XY")
    
    # The 3 main rings
    ring_radius = 18.0
    ring_offset = 12.0
    ring_thickness = 4.0 # Visual estimate
    
    # Create the three rings at 0, 120, 240 degrees
    rings = wp.polarArray(ring_offset, 0, 360, 3).circle(ring_radius).extrude(1)
    
    # The inner cutout circles for the rings
    rings_inner = wp.polarArray(ring_offset, 0, 360, 3).circle(ring_radius - 4.5).extrude(1)
    
    # The central circular cutout
    center_cut = wp.circle(6.0).extrude(1)
    
    # The linear gaps
    # We need rectangles rotated at 0, 120, 240 + offset
    gap_rect = wp.rect(4.0, 40.0).extrude(1)
    gaps = (wp.polarArray(0, 0, 360, 1).union(gap_rect)
              .rotate((0,0,0), (0,0,1), 60).union(gap_rect)
              .rotate((0,0,0), (0,0,1), 60).union(gap_rect))
              
    # Let's try a different, more constructive CSG approach for the symbol on a Workplane
    # 1. Three large circles
    shapes = []
    cutouts = []
    
    # Radius of the three main circles making the loops
    r_main = 16.0
    # Distance from center to center of main circles
    d_offset = 11.0 
    
    for i in range(3):
        angle = 90 + i * 120
        # Main circles (Solids for boolean ops)
        main_cyl = (cq.Workplane("XY")
                    .transformed(rotate=(0,0,angle))
                    .center(d_offset, 0)
                    .circle(r_main).extrude(100))
        shapes.append(main_cyl)
        
        # Inner cutouts of the main circles
        inner_cyl = (cq.Workplane("XY")
                     .transformed(rotate=(0,0,angle))
                     .center(d_offset, 0)
                     .circle(r_main - 4.0).extrude(100))
        cutouts.append(inner_cyl)
        
        # The gaps between the loops
        gap_box = (cq.Workplane("XY")
                   .transformed(rotate=(0,0,angle+60)) # Gaps are between the circles
                   .center(18, 0) # Offset outwards
                   .rect(40, 3.0) # Length, Width (gap size)
                   .extrude(100))
        cutouts.append(gap_box)

    # The center circle element
    center_ring_outer = cq.Workplane("XY").circle(7.0).extrude(100)
    center_ring_inner = cq.Workplane("XY").circle(5.0).extrude(100)
    
    # Combine the main circles
    symbol = shapes[0].union(shapes[1]).union(shapes[2])
    
    # Intersect with a bounding circle to keep it neat (optional, but typical for grilles)
    # The image shows concentric rings.
    # Let's add the outer circular frame of the grill
    outer_ring = (cq.Workplane("XY")
                  .circle(dome_diameter/2.0 - 1.0)
                  .circle(dome_diameter/2.0 - 3.0)
                  .extrude(100))
    
    symbol = symbol.union(outer_ring).union(center_ring_outer)
    
    # Subtract the inner definitions
    for cut in cutouts:
        symbol = symbol.cut(cut)
        
    symbol = symbol.cut(center_ring_inner)
    
    # Create the concentric arcs often seen in these designs or just refine the shape
    # Looking at the image, it's strictly the biohazard symbol projected.
    # The "bars" are just the symbol shape extruded.
    
    return symbol

# Generate the 2D extrusion of the pattern
pattern_extrusion = biohazard_shape()

# Move the pattern down so it covers the dome height range
pattern_extrusion = pattern_extrusion.translate((0, 0, -20))

# Intersect the dome with the pattern to get the curved grill
# We create a shell of the dome first to give the grill thickness
dome_outer = dome
dome_inner = (cq.Workplane("XY")
    .workplane(offset=center_z)
    .sphere(sphere_radius - grill_thickness)
)

# The solid shell of the dome
dome_shell = dome_outer.cut(dome_inner)

# Intersect shell with the pattern
grill_structure = dome_shell.intersect(pattern_extrusion)

# Cut the hole in the base for airflow
base_cutout = (cq.Workplane("XY")
    .circle(dome_diameter / 2.0 - 2.0)
    .extrude(thickness)
)
base_frame = base.cut(base_cutout)

# Combine the base frame and the dome grill
result = base_frame.union(grill_structure)

# Optional: slight chamfer on the top edge of the base for aesthetics
# result = result.edges("|Z").fillet(1.0) # Depending on specific need

if __name__ == "__main__":
    try:
        from cadquery.vis import show_object
        show_object(result)
    except ImportError:
        pass
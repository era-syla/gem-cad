import cadquery as cq
import math

# ------------------------------------------------------------------
# Parametric Dimensions
# ------------------------------------------------------------------

# Lead screw parameters
screw_diameter = 12.0
screw_length = 150.0
pitch = 3.0
thread_depth = 1.2
thread_angle = 30.0 # ACME or Trapezoidal angle (degrees)

# Nut/Flange parameters
flange_diameter = 30.0
flange_thickness = 5.0
barrel_diameter = 16.0
barrel_length = 15.0 # Length of the non-threaded cylindrical part behind the flange
num_mounting_holes = 4
mounting_hole_diameter = 3.5
mounting_hole_circle_dia = 22.0

# ------------------------------------------------------------------
# Helper Function: Create the Thread Profile
# ------------------------------------------------------------------
def create_trapezoidal_thread(length, diameter, pitch, depth, angle):
    """
    Creates a simplified threaded rod representation using a helical sweep.
    Note: Generating true helical threads is computationally expensive.
    This creates a solid cylinder first, then cuts the thread groove.
    """
    
    # 1. Base Cylinder
    rod = cq.Workplane("XY").circle(diameter / 2).extrude(length)
    
    # 2. Thread Profile Calculation
    # We define a trapezoidal profile to sweep
    # Width at the bottom of the groove
    groove_bottom_width = (pitch / 2) - (depth * math.tan(math.radians(angle / 2)))
    groove_top_width = pitch / 2
    
    # 3. Create the helix path
    # CadQuery helix creation can be tricky. A robust way is to use the `helix` method.
    # However, cutting a true helix is complex. 
    # For visualization purposes in code generation, often a stack of discs or a simplified 
    # visual representation is preferred if performance is key, but the prompt asks for the model.
    # Let's try to make a proper single-start thread cut.
    
    # Define the wire for the thread cross-section (the material to remove)
    # Positioned at the outer edge of the rod
    
    p1 = (diameter/2, -groove_top_width/2)
    p2 = ((diameter/2) - depth, -groove_bottom_width/2)
    p3 = ((diameter/2) - depth, groove_bottom_width/2)
    p4 = (diameter/2, groove_top_width/2)
    
    # We need to perform a helical cut.
    # In pure CQ, `twistExtrude` creates an additive shape, so we create the thread volume
    # and subtract it, or create the core and add the thread ridges.
    # Let's add thread ridges to a core cylinder for better stability.
    
    core_radius = (diameter / 2) - depth
    core = cq.Workplane("XY").circle(core_radius).extrude(length)
    
    # Profile for the thread ridge (Trapezoidal)
    ridge_bottom_width = pitch - groove_top_width # Base on core
    ridge_top_width = pitch - groove_bottom_width # Top of thread
    
    # Define points for the ridge cross-section on XZ plane
    # Centered on X-axis, offset by radius
    
    # Calculate number of turns
    turns = length / pitch
    
    # Create the thread coil
    # This is a computationally intensive operation. 
    # We will construct a profile and twist extrude it.
    
    thread_profile = (
        cq.Workplane("XZ")
        .center(core_radius, 0)
        .polyline([
            (0, -ridge_bottom_width/2),
            (depth, -ridge_top_width/2),
            (depth, ridge_top_width/2),
            (0, ridge_bottom_width/2),
            (0, -ridge_bottom_width/2)
        ])
        .close()
    )
    
    # Parametric helical sweep
    threads = thread_profile.twistExtrude(length, 360 * turns)
    
    # Combine core and threads
    threaded_rod = core.union(threads)
    
    return threaded_rod

# ------------------------------------------------------------------
# Main Geometry Construction
# ------------------------------------------------------------------

# 1. Create the Threaded Rod part
# Note: Since twistExtrude can be slow/complex, if the script fails in some viewers,
# a simple cylinder is often used as a fallback. Here we implement the thread.
# To keep the script robust and fast for 'visual' match without needing a 2-minute compute,
# I will create the distinct visual 'ribs' using a stack of discs if twistExtrude is too heavy,
# but `twistExtrude` is the correct CAD way.

# Constructing the screw shaft
# We start the screw at Z=0 and go positive.
screw_shaft = create_trapezoidal_thread(screw_length, screw_diameter, pitch, thread_depth, thread_angle)

# 2. Create the Nut/Flange Assembly
# The flange sits at one end. Let's position it near the start.
# Based on the image, there is a smooth barrel section, then the flange, then the screw continues?
# Actually, the image looks like a lead screw nut assembly (the flange part) ON the screw.
# Or is it a lead screw with a machined end? 
# The image shows the screw extending out one side, and a smooth barrel on the other. 
# This is typical of a lead screw nut. I will model the whole object as a single union 
# representing the assembly shown.

# Position the flange relative to the screw
# It looks like the flange is at Z=0, barrel extends to negative Z, screw extends to positive Z.

# Create the Flange
flange = (cq.Workplane("XY")
          .circle(flange_diameter / 2)
          .extrude(flange_thickness)
          )

# Add mounting holes to flange
for i in range(num_mounting_holes):
    angle = (360.0 / num_mounting_holes) * i
    # Calculate x, y position
    x = (mounting_hole_circle_dia / 2) * math.cos(math.radians(angle))
    y = (mounting_hole_circle_dia / 2) * math.sin(math.radians(angle))
    
    flange = (flange.faces(">Z")
              .workplane()
              .moveTo(x, y)
              .hole(mounting_hole_diameter)
              )

# Create the Barrel (the smooth part sticking out the back)
barrel = (cq.Workplane("XY")
          .workplane(offset=-barrel_length)
          .circle(barrel_diameter / 2)
          .extrude(barrel_length)
          )

# Combine Flange and Barrel
nut_body = flange.union(barrel)

# Now combine the nut with the screw.
# In the image, the screw starts flush with the flange face or slightly inside.
# Let's align them.
final_assembly = nut_body.union(screw_shaft)

# 3. Add the characteristic 'cuts' at the end of the screw if present
# The image shows a chamfer and maybe some small slots on the tip of the screw.
# Let's add a chamfer to the end of the screw.
final_assembly = final_assembly.faces(">Z").chamfer(1.0)

# 4. Center bore
# Lead screw nuts have a hole through them.
# The screw itself is solid. 
# The image shows a solid object (Lead Screw Integrated with Flange/Nut or a Nut on a Screw).
# Assuming it's a solid assembly.

# 5. Optional: Cut the small slots on the screw tip seen in the image
# There appear to be 4 small notches on the very tip circumference.
tip_notch_width = 2.0
tip_notch_depth = 1.0

tip_face = final_assembly.faces(">Z").workplane()

for i in range(4):
    angle = 90 * i
    final_assembly = (
        final_assembly.faces(">Z")
        .workplane()
        .transformed(rotate=cq.Vector(0, 0, angle))
        .moveTo(screw_diameter/2, 0)
        .rect(tip_notch_depth * 2, tip_notch_width)
        .cutBlind(-2.0)
    )

result = final_assembly
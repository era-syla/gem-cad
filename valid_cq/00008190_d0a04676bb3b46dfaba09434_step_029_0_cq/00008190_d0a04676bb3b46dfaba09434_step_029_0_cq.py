import cadquery as cq
import math

def timing_pulley(tooth_count=40, 
                  tooth_pitch=2.0, 
                  pulley_width=7.0, 
                  bore_diameter=5.0, 
                  flange_diameter_offset=4.0, 
                  flange_thickness=1.0):
    """
    Generates a parametric timing belt pulley with flanges.
    
    :param tooth_count: Number of teeth
    :param tooth_pitch: Distance between teeth (e.g., 2mm for GT2)
    :param pulley_width: Width of the toothed section
    :param bore_diameter: Diameter of the central shaft hole
    :param flange_diameter_offset: How much larger the flanges are than the pulley pitch diameter
    :param flange_thickness: Thickness of the side flanges
    """
    
    # --- derived calculations ---
    # Pitch circumference = tooth_count * tooth_pitch
    # Pitch diameter = circumference / pi
    pitch_diameter = (tooth_count * tooth_pitch) / math.pi
    pitch_radius = pitch_diameter / 2.0
    
    # Tooth profile parameters (Approximate GT2-style profile)
    # The "root radius" is slightly smaller than pitch radius
    tooth_depth = 0.75  # Approximate depth for standard small pitch belts
    root_radius = pitch_radius - tooth_depth
    outer_radius = pitch_radius # The tops of the teeth are often near the pitch line or slightly outside
    
    # Flange dimensions
    flange_radius = outer_radius + (flange_diameter_offset / 2.0)
    total_width = pulley_width + 2 * flange_thickness

    # --- Geometry Creation ---

    # 1. Create the main toothed cylinder
    # We create a single tooth profile and polar array it
    
    # Define a trapezoidal/rounded tooth cutter
    # For simplicity in this general model, we cut away material from a cylinder
    # Tooth gap width is roughly half the pitch
    tooth_gap_width_top = tooth_pitch * 0.55
    tooth_gap_width_bottom = tooth_pitch * 0.35
    
    # Create the base cylinder for the pulley body
    pulley_body = cq.Workplane("XY").circle(outer_radius).extrude(pulley_width)
    
    # Create the cutter shape for the gap between teeth
    # We draw it on the top face and extrude down
    tooth_gap = (
        cq.Workplane("XY")
        .workplane(offset=pulley_width)
        .moveTo(outer_radius + 1.0, -tooth_gap_width_top/2.0)
        .lineTo(root_radius, -tooth_gap_width_bottom/2.0)
        .lineTo(root_radius, tooth_gap_width_bottom/2.0)
        .lineTo(outer_radius + 1.0, tooth_gap_width_top/2.0)
        .close()
        .extrude(-pulley_width)
    )
    
    # Subtract the gaps from the body to form teeth
    for i in range(tooth_count):
        angle = 360.0 / tooth_count * i
        rotated_gap = tooth_gap.rotate((0,0,0), (0,0,1), angle)
        pulley_body = pulley_body.cut(rotated_gap)

    # 2. Create the Bore
    pulley_body = pulley_body.faces(">Z").workplane().circle(bore_diameter / 2.0).cutThruAll()

    # 3. Create Flanges
    # Bottom Flange
    flange_bottom = (
        cq.Workplane("XY")
        .workplane(offset=-flange_thickness)
        .circle(flange_radius)
        .extrude(flange_thickness)
    )
    # Add bore to bottom flange
    flange_bottom = flange_bottom.faces(">Z").workplane().circle(bore_diameter / 2.0).cutThruAll()

    # Top Flange
    flange_top = (
        cq.Workplane("XY")
        .workplane(offset=pulley_width)
        .circle(flange_radius)
        .extrude(flange_thickness)
    )
    # Add bore to top flange
    flange_top = flange_top.faces(">Z").workplane().circle(bore_diameter / 2.0).cutThruAll()

    # Combine everything
    final_pulley = pulley_body.union(flange_bottom).union(flange_top)

    # Optional: Chamfer the bore for easier insertion
    try:
        final_pulley = final_pulley.faces("Z").edges(cq.selectors.RadiusNthSelector(0)).chamfer(0.5)
    except:
        pass # Skip if selection fails on complex geometry

    return final_pulley

# Generate the model
result = timing_pulley(
    tooth_count=36, 
    tooth_pitch=2.0, 
    pulley_width=8.0, 
    bore_diameter=8.0, 
    flange_diameter_offset=3.0,
    flange_thickness=1.0
)
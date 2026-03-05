import cadquery as cq
import math

def create_coexist_logo():
    # --- Parametric Dimensions ---
    height = 5.0      # Thickness of the model
    base_size = 20.0  # Approximate height/width of each symbol
    spacing = 22.0    # Distance between symbol centers
    
    # Common parameters for line widths and radii
    stroke_width = 2.5
    outer_radius = base_size / 2.0
    inner_radius = outer_radius - stroke_width

    # --- Symbol 1: 'C' - Crescent Moon and Star (Islam) ---
    def make_c():
        # Large moon body
        c_outer = cq.Workplane("XY").circle(outer_radius).extrude(height)
        c_inner = (cq.Workplane("XY")
                   .center(outer_radius * 0.4, 0)
                   .circle(inner_radius * 0.9)
                   .extrude(height))
        
        moon = c_outer.cut(c_inner)
        
        # Star
        star_pts = []
        star_outer_r = stroke_width * 1.5
        star_inner_r = star_outer_r * 0.4
        for i in range(10):
            angle = math.radians(i * 36 + 18) # Rotate slightly
            r = star_outer_r if i % 2 == 0 else star_inner_r
            star_pts.append((r * math.cos(angle), r * math.sin(angle)))
            
        star = (cq.Workplane("XY")
                .center(outer_radius * 0.4, 0)
                .polyline(star_pts).close()
                .extrude(height))
        
        # Combine moon and star, positioned as 'C'
        # The standard Coexist logo has the moon on the left open to the right
        return moon.union(star)

    # --- Symbol 2: 'O' - Peace Sign ---
    def make_o():
        # Outer ring
        outer = cq.Workplane("XY").circle(outer_radius).extrude(height)
        inner = cq.Workplane("XY").circle(inner_radius).extrude(height)
        ring = outer.cut(inner)
        
        # Vertical bar
        vert_bar = (cq.Workplane("XY")
                    .rect(stroke_width, outer_radius * 2)
                    .extrude(height))
        
        # Diagonals
        diag_len = outer_radius * 1.8
        diag1 = (cq.Workplane("XY")
                 .center(0, -outer_radius*0.2)
                 .rect(stroke_width, diag_len)
                 .rotate((0,0,0), (0,0,1), 45)
                 .extrude(height))
        diag2 = (cq.Workplane("XY")
                 .center(0, -outer_radius*0.2)
                 .rect(stroke_width, diag_len)
                 .rotate((0,0,0), (0,0,1), -45)
                 .extrude(height))
                 
        # For the peace sign specifically shown (often just vertical + diagonals downwards)
        # Let's clean it up to match the "Mercedes" style or standard peace sign
        # Standard peace sign: vertical line down, two diagonals down
        
        center_bar = (cq.Workplane("XY")
                      .rect(stroke_width, outer_radius*2)
                      .extrude(height))
        
        # Diagonal legs
        leg_len = outer_radius 
        leg = (cq.Workplane("XY")
               .rect(stroke_width, leg_len)
               .extrude(height))
        
        leg1 = leg.translate((0, -leg_len/2, 0)).rotate((0,0,0), (0,0,1), -45)
        leg2 = leg.translate((0, -leg_len/2, 0)).rotate((0,0,0), (0,0,1), 45)
        
        # Usually for 'O' in coexist, the peace sign is inverted or standard.
        # Based on image, it looks like standard peace sign.
        # Vertical line full height? No, usually top to bottom.
        
        full_peace = ring.union(center_bar).union(leg1).union(leg2)
        return full_peace

    # --- Symbol 3: 'e' - Male/Female Gender Symbol (Trans/Combined) ---
    def make_e():
        # Usually represented as 'e' = E=mc^2 or a symbol. 
        # In standard Coexist, 'e' is often the E=mc2 or Male/Female symbol.
        # Looking at the provided image (3rd from right), it looks like the 
        # male/female combined symbol (circle with cross below and arrow above-right).
        # Actually, looking closer at the specific image provided:
        # It looks like a lowercase 'e' formed by a symbol.
        # In the specific "Coexist" image provided, the 3rd letter is clearly the female/male symbol combination.
        
        # Circle
        ring = (cq.Workplane("XY")
                .circle(outer_radius*0.8)
                .circle(inner_radius*0.7)
                .extrude(height))
        
        # Cross (Female) - usually down
        v_cross = (cq.Workplane("XY")
                   .center(0, -outer_radius*0.8)
                   .rect(stroke_width, outer_radius*0.8)
                   .extrude(height))
        h_cross = (cq.Workplane("XY")
                   .center(0, -outer_radius*1.0)
                   .rect(outer_radius*0.8, stroke_width)
                   .extrude(height))
        
        # Arrow (Male) - usually up-right
        arrow_shaft = (cq.Workplane("XY")
                       .center(outer_radius*0.6, outer_radius*0.6)
                       .rect(stroke_width, outer_radius)
                       .rotate((0,0,0), (0,0,1), -45)
                       .extrude(height))
                       
        # Arrow head
        arrow_head_pts = [(0,0), (-4, -2), (0, 4), (4, -2)]
        arrow_head = (cq.Workplane("XY")
                      .center(outer_radius*0.9, outer_radius*0.9)
                      .polyline(arrow_head_pts).close()
                      .rotate((0,0,0), (0,0,1), -45)
                      .extrude(height))
        
        return ring.union(v_cross).union(h_cross).union(arrow_shaft).union(arrow_head)

    # --- Symbol 4: 'x' - Star of David (Judaism) ---
    def make_x():
        def triangle(r, angle_offset=0):
            pts = []
            for i in range(3):
                angle = math.radians(i * 120 + 90 + angle_offset)
                pts.append((r * math.cos(angle), r * math.sin(angle)))
            
            tri = (cq.Workplane("XY")
                   .polyline(pts).close()
                   .extrude(height))
            
            # Hollow it
            inner_pts = []
            inner_r = r - stroke_width*1.5 # Need thicker offset for acute angles
            for i in range(3):
                angle = math.radians(i * 120 + 90 + angle_offset)
                inner_pts.append((inner_r * math.cos(angle), inner_r * math.sin(angle)))
            
            tri_inner = (cq.Workplane("XY")
                   .polyline(inner_pts).close()
                   .extrude(height))
            
            return tri.cut(tri_inner)

        t1 = triangle(outer_radius * 1.1, 0)
        t2 = triangle(outer_radius * 1.1, 180)
        return t1.union(t2)

    # --- Symbol 5: 'i' - Pentagram/Pagan (Dot of 'i') and Stick ---
    # In the image provided, the 'i' looks like a vertical stick with a symbol on top.
    # The symbol looks like the Pagan Pentacle (star in circle) or just a Pentagram.
    def make_i():
        # Vertical stick
        stick = (cq.Workplane("XY")
                 .center(0, -outer_radius*0.5)
                 .rect(stroke_width*1.5, outer_radius*1.5)
                 .extrude(height))
        
        # Dot (Pentacle)
        center_y = outer_radius * 0.6
        
        # Ring
        dot_ring = (cq.Workplane("XY")
                    .center(0, center_y)
                    .circle(outer_radius * 0.45)
                    .circle(outer_radius * 0.45 - stroke_width/2)
                    .extrude(height))
        
        # Star inside
        star_pts = []
        r_outer = outer_radius * 0.45
        r_inner = r_outer * 0.4
        for i in range(10): # 5 points
            angle = math.radians(i * 36 + 18) # 90 deg start
            r = r_outer if i % 2 == 0 else r_inner
            star_pts.append((r * math.cos(angle), r * math.sin(angle) + center_y))
            
        # Creating a pentagram lines is tricky with just polyline fill.
        # Let's make a solid star
        star = (cq.Workplane("XY")
                .polyline(star_pts).close()
                .extrude(height))

        return stick.union(dot_ring).union(star)

    # --- Symbol 6: 's' - Yin Yang (Taoism) ---
    def make_s():
        r = outer_radius
        
        # Main circle
        main = cq.Workplane("XY").circle(r).extrude(height)
        
        # Cutout for 'S' shape separation
        # Construct S curve using two smaller circles
        top_sub = (cq.Workplane("XY")
                   .center(0, r/2)
                   .circle(r/2)
                   .extrude(height))
        
        bot_add = (cq.Workplane("XY")
                   .center(0, -r/2)
                   .circle(r/2)
                   .extrude(height))
                   
        # Left side (Yin) construction
        # Start with full circle, cut right half
        left_half = (cq.Workplane("XY")
                     .rect(r*2, r*2)
                     .translate((-r, 0, 0)) # Shift to keep left
                     .extrude(height))
        
        yin = main.intersect(left_half)
        yin = yin.cut(top_sub)
        yin = yin.union(bot_add)
        
        # Right side (Yang) construction
        right_half = (cq.Workplane("XY")
                      .rect(r*2, r*2)
                      .translate((r, 0, 0)) 
                      .extrude(height))
        
        yang = main.intersect(right_half)
        yang = yang.cut(bot_add)
        yang = yang.union(top_sub)
        
        # Hollow dots
        dot_r = r * 0.15
        top_dot = (cq.Workplane("XY")
                   .center(0, r/2)
                   .circle(dot_r)
                   .extrude(height))
        bot_dot = (cq.Workplane("XY")
                   .center(0, -r/2)
                   .circle(dot_r)
                   .extrude(height))
        
        yin = yin.cut(bot_dot)
        yang = yang.cut(top_dot)
        
        # Create an outer ring to hold them together if we want it to look like the letter S
        # Or usually in Coexist, it's just the yin yang. 
        # To make it printable/solid, we often put a ring around it.
        ring = (cq.Workplane("XY")
                .circle(r)
                .circle(r - stroke_width/2)
                .extrude(height))
                
        return yin.union(yang).union(ring)

    # --- Symbol 7: 't' - Cross (Christianity) ---
    def make_t():
        # Vertical beam
        v = (cq.Workplane("XY")
             .rect(stroke_width * 1.5, outer_radius * 2.5)
             .extrude(height))
        
        # Horizontal beam
        h = (cq.Workplane("XY")
             .center(0, outer_radius * 0.3)
             .rect(outer_radius * 1.8, stroke_width * 1.5)
             .extrude(height))
             
        return v.union(h)

    # --- Assembly ---
    
    # Note: The provided image order is reversed compared to standard reading (right to left or inverted view?)
    # The image shows: Cross (T), YinYang (S), Pentacle (I), Star of David (X), Gender (E), Peace (O), Moon (C)
    # But usually Coexist is C-O-E-X-I-S-T.
    # The image orientation seems to be: Left=T, Right=C. So it spells "TSIXEOC" ?
    # No, looking at the image: 
    # Leftmost is a Cross (T)
    # Next is Yin Yang (S)
    # Next is a Symbol (I)
    # Next is Star of David (X)
    # Next is Gender Symbol (E)
    # Next is Peace Sign (O)
    # Rightmost is Crescent (C)
    # It spells "COEXIST" backwards, or mirrored.
    
    # We will generate "COEXIST" in standard order, which matches the visual components 
    # of the prompt image, just ordered logically.
    
    symbols = [
        make_c(),
        make_o(),
        make_e(),
        make_x(),
        make_i(),
        make_s(),
        make_t()
    ]
    
    # Depending on interpretation, we can reverse to match the geometric position in the specific PNG 
    # (where T is left, C is right). Let's construct it T-S-I-X-E-O-C to match the visual block exactly.
    
    # Let's stick to standard reading left-to-right C-O-E-X-I-S-T to be safe, 
    # as the prompt says "based on the provided image" which implies the content, not necessarily the mirror state.
    # However, to replicate the shape *exactly* as displayed (T on left):
    
    final_obj = symbols[6] # T
    
    # Shift and union
    final_obj = final_obj.union(symbols[5].translate((spacing * 1, 0, 0))) # S
    final_obj = final_obj.union(symbols[4].translate((spacing * 2, 0, 0))) # I
    final_obj = final_obj.union(symbols[3].translate((spacing * 3, 0, 0))) # X
    final_obj = final_obj.union(symbols[2].translate((spacing * 4, 0, 0))) # E
    final_obj = final_obj.union(symbols[1].translate((spacing * 5, 0, 0))) # O
    final_obj = final_obj.union(symbols[0].translate((spacing * 6, 0, 0))) # C

    # If the user wants the standard reading order (C on left), uncomment below and comment above block:
    # final_obj = symbols[0]
    # for i, sym in enumerate(symbols[1:]):
    #     final_obj = final_obj.union(sym.translate((spacing * (i+1), 0, 0)))

    return final_obj

# Generate the result
result = create_coexist_logo()
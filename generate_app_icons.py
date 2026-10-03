import os
from PIL import Image, ImageDraw

def generate_icons():
    src_path = 'frontend/src/images/Nichole Agrivet.png'
    src = Image.open(src_path)

    # 1. Precise crop of the character (hat to hooves, stalk to waving hand)
    character = src.crop((35, 45, 830, 855))
    
    # Clean up the rogue green leaf speck at bottom right
    cw, ch = character.size
    for x in range(cw - 120, cw):
        for y in range(ch - 100, ch):
            r, g, b, a = character.getpixel((x, y))
            if a > 0 and (g > r + 15 or (x > cw - 80 and y > ch - 60)):
                character.putpixel((x, y), (0, 0, 0, 0))

    bbox = character.getbbox()
    mascot = character.crop(bbox)
    print(f"Mascot cropped cleanly: {mascot.size}")

    # Output directory base
    res_dir = 'frontend/src-capacitor/android/app/src/main/res'

    # Densities for Android:
    # (density_name, foreground_size, legacy_size)
    densities = [
        ('mipmap-mdpi', 108, 48),
        ('mipmap-hdpi', 162, 72),
        ('mipmap-xhdpi', 216, 96),
        ('mipmap-xxhdpi', 324, 144),
        ('mipmap-xxxhdpi', 432, 192),
    ]

    for name, fg_size, leg_size in densities:
        folder = os.path.join(res_dir, name)
        os.makedirs(folder, exist_ok=True)

        # -------------------------------------------------------------
        # A. ADAPTIVE FOREGROUND (ic_launcher_foreground.png)
        # Canvas: fg_size x fg_size, transparent
        # Safe zone: Mascot scaled to ~64% of fg_size, centered exactly
        # -------------------------------------------------------------
        fg_img = Image.new('RGBA', (fg_size, fg_size), (0, 0, 0, 0))
        target_h = int(fg_size * 0.64)
        aspect = mascot.width / mascot.height
        target_w = int(target_h * aspect)
        m_scaled = mascot.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        pos_x = (fg_size - target_w) // 2
        pos_y = (fg_size - target_h) // 2 + int(fg_size * 0.01) # optical center balance
        fg_img.paste(m_scaled, (pos_x, pos_y), m_scaled)
        
        fg_path = os.path.join(folder, 'ic_launcher_foreground.png')
        fg_img.save(fg_path, 'PNG')

        # -------------------------------------------------------------
        # B. LEGACY SQUIRCLE ICON (ic_launcher.png)
        # Crisp white background squircle with subtle border, centered mascot
        # -------------------------------------------------------------
        supersample = 4
        big_size = leg_size * supersample
        squircle = Image.new('RGBA', (big_size, big_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(squircle)
        radius = int(big_size * 0.22)
        margin = int(big_size * 0.02)
        
        draw.rounded_rectangle(
            [(margin, margin), (big_size - margin, big_size - margin)],
            radius=radius,
            fill=(255, 255, 255, 255),
            outline=(226, 232, 240, 255),
            width=max(1, int(supersample * 1.5))
        )
        
        target_m_h = int(big_size * 0.72)
        target_m_w = int(target_m_h * aspect)
        m_big = mascot.resize((target_m_w, target_m_h), Image.Resampling.LANCZOS)
        
        m_x = (big_size - target_m_w) // 2
        m_y = (big_size - target_m_h) // 2 + int(big_size * 0.01)
        squircle.paste(m_big, (m_x, m_y), m_big)
        
        leg_icon = squircle.resize((leg_size, leg_size), Image.Resampling.LANCZOS)
        leg_path = os.path.join(folder, 'ic_launcher.png')
        leg_icon.save(leg_path, 'PNG')

        # -------------------------------------------------------------
        # C. ROUND ICON (ic_launcher_round.png)
        # Crisp white background circle, centered mascot
        # -------------------------------------------------------------
        circle_img = Image.new('RGBA', (big_size, big_size), (0, 0, 0, 0))
        draw_c = ImageDraw.Draw(circle_img)
        draw_c.ellipse(
            [(margin, margin), (big_size - margin, big_size - margin)],
            fill=(255, 255, 255, 255),
            outline=(226, 232, 240, 255),
            width=max(1, int(supersample * 1.5))
        )
        circle_img.paste(m_big, (m_x, m_y), m_big)
        
        round_icon = circle_img.resize((leg_size, leg_size), Image.Resampling.LANCZOS)
        round_path = os.path.join(folder, 'ic_launcher_round.png')
        round_icon.save(round_path, 'PNG')

        print(f"Generated icons for {name}: FG={fg_size}x{fg_size}, LEG={leg_size}x{leg_size}")

    print("All Android launcher icons generated successfully!")

if __name__ == '__main__':
    generate_icons()

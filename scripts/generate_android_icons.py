import os
from PIL import Image, ImageDraw

def generate_icons():
    source_path = "frontend/src/images/Nichole Agrivet.png"
    if not os.path.exists(source_path):
        print(f"Error: {source_path} does not exist")
        return

    source = Image.open(source_path).convert("RGBA")
    res_dir = "frontend/src-capacitor/android/app/src/main/res"

    # Mipmap densities & sizes
    # (dir_name, icon_size, foreground_size)
    densities = [
        ("mipmap-mdpi", 48, 108),
        ("mipmap-hdpi", 72, 162),
        ("mipmap-xhdpi", 96, 216),
        ("mipmap-xxhdpi", 144, 324),
        ("mipmap-xxxhdpi", 192, 432),
    ]

    for dir_name, icon_size, fg_size in densities:
        target_dir = os.path.join(res_dir, dir_name)
        os.makedirs(target_dir, exist_ok=True)

        # 1. ic_launcher.png (Square / Rounded rectangle with white background)
        launcher_img = Image.new("RGBA", (icon_size, icon_size), (255, 255, 255, 255))
        # mascot scaled to fit inside with slight padding (88%)
        mascot_size = int(icon_size * 0.90)
        mascot_resized = source.resize((mascot_size, mascot_size), Image.Resampling.LANCZOS)
        offset = ((icon_size - mascot_size) // 2, (icon_size - mascot_size) // 2)
        launcher_img.paste(mascot_resized, offset, mascot_resized)
        launcher_img.save(os.path.join(target_dir, "ic_launcher.png"), "PNG")

        # 2. ic_launcher_round.png (Circular icon)
        round_bg = Image.new("RGBA", (icon_size, icon_size), (0, 0, 0, 0))
        # Draw filled white circle
        draw = ImageDraw.Draw(round_bg)
        draw.ellipse([(0, 0), (icon_size - 1, icon_size - 1)], fill=(255, 255, 255, 255))
        # Scale mascot to ~82% so it fits well inside circular mask
        round_mascot_size = int(icon_size * 0.82)
        round_mascot_resized = source.resize((round_mascot_size, round_mascot_size), Image.Resampling.LANCZOS)
        round_offset = ((icon_size - round_mascot_size) // 2, (icon_size - round_mascot_size) // 2)
        round_bg.paste(round_mascot_resized, round_offset, round_mascot_resized)
        
        # Apply circular alpha mask
        mask = Image.new("L", (icon_size, icon_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse([(0, 0), (icon_size - 1, icon_size - 1)], fill=255)
        round_final = Image.new("RGBA", (icon_size, icon_size), (0, 0, 0, 0))
        round_final.paste(round_bg, (0, 0), mask)
        round_final.save(os.path.join(target_dir, "ic_launcher_round.png"), "PNG")

        # 3. ic_launcher_foreground.png (Adaptive icon foreground: 108dp canvas, safe zone 72dp)
        fg_img = Image.new("RGBA", (fg_size, fg_size), (0, 0, 0, 0))
        # Safe zone is 66% of fg_size
        fg_mascot_size = int(fg_size * 0.70)
        fg_mascot_resized = source.resize((fg_mascot_size, fg_mascot_size), Image.Resampling.LANCZOS)
        fg_offset = ((fg_size - fg_mascot_size) // 2, (fg_size - fg_mascot_size) // 2)
        fg_img.paste(fg_mascot_resized, fg_offset, fg_mascot_resized)
        fg_img.save(os.path.join(target_dir, "ic_launcher_foreground.png"), "PNG")

        print(f"Generated launcher icons for {dir_name}")

    # 4. Generate splash screens
    splash_targets = [
        ("drawable/splash.png", (480, 320)),
        ("drawable-land-hdpi/splash.png", (800, 480)),
        ("drawable-land-mdpi/splash.png", (480, 320)),
        ("drawable-land-xhdpi/splash.png", (1280, 720)),
        ("drawable-land-xxhdpi/splash.png", (1600, 960)),
        ("drawable-land-xxxhdpi/splash.png", (1920, 1280)),
        ("drawable-port-hdpi/splash.png", (480, 800)),
        ("drawable-port-mdpi/splash.png", (320, 480)),
        ("drawable-port-xhdpi/splash.png", (720, 1280)),
        ("drawable-port-xxhdpi/splash.png", (960, 1600)),
        ("drawable-port-xxxhdpi/splash.png", (1280, 1920)),
    ]

    # Warm cream background color matching the login screen (#fcf1ea)
    bg_color = (252, 241, 234, 255)

    for rel_path, (width, height) in splash_targets:
        full_path = os.path.join(res_dir, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        splash_img = Image.new("RGBA", (width, height), bg_color)
        # Mascot scaled to fit ~50% of min dimension
        target_mascot_dim = int(min(width, height) * 0.55)
        mascot_splash = source.resize((target_mascot_dim, target_mascot_dim), Image.Resampling.LANCZOS)
        splash_offset = ((width - target_mascot_dim) // 2, (height - target_mascot_dim) // 2)
        splash_img.paste(mascot_splash, splash_offset, mascot_splash)
        splash_img.save(full_path, "PNG")
        print(f"Generated splash for {rel_path} ({width}x{height})")

    print("All icons and splash screens successfully generated!")

if __name__ == "__main__":
    generate_icons()

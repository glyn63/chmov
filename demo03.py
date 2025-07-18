import json
from PIL import Image, ImageDraw

# Piece type → square size mapping
PIECE_SIZE = {
    'p': 8,
    'n': 10,
    'b': 10,
    'r': 12,
    'q': 14,
    'k': 14
}

def load_chess_turns(filename):
    """Load a chmov.json file and return the turns array."""
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get("moves", [])

def sample_turns(turns, count=64):
    """Evenly sample `count` turns from the list."""
    total = len(turns)
    if total < count:
        raise ValueError("Not enough turns to sample 64.")
    step = total / count
    return [turns[int(i * step)] for i in range(count)]

def draw_xfen_block(xfen):
    """Render an 8x8 xfen board into a 128x128 Image block."""
    block = Image.new("RGB", (128, 128), (240, 240, 240))
    draw = ImageDraw.Draw(block)

    for row in range(8):
        for col in range(8):
            piece = xfen[row][col]
            if piece is None:
                continue  # empty square

            color_prefix = piece[0]  # 'w' or 'b'
            piece_type = piece[1]    # 'p', 'n', 'b', 'r', 'q', 'k'
            size = PIECE_SIZE.get(piece_type, 6)

            # Center inside 16x16 minor square
            cx = col * 16 + 8
            cy = row * 16 + 8
            half = size // 2

            fill = (0, 0, 0) if color_prefix == 'b' else (255, 255, 255)
            draw.rectangle([cx - half, cy - half, cx + half - 1, cy + half - 1], fill=fill)

    return block

def get_spiral_positions():
    """Hardcoded 1-based spiral positions from center of 8x8 board."""
    return [
        (4, 4), (4, 5), (5, 5), (5, 4),
        (5, 3), (4, 3), (3, 3), (3, 4), (3, 5), (3, 6),
        (4, 6), (5, 6), (6, 6), (6, 5), (6, 4), (6, 3),
        (6, 2), (5, 2), (4, 2), (3, 2), (2, 2), (2, 3),
        (2, 4), (2, 5), (2, 6), (2, 7), (3, 7), (4, 7),
        (5, 7), (6, 7), (7, 7), (7, 6), (7, 5), (7, 4),
        (7, 3), (7, 2), (7, 1), (6, 1), (5, 1), (4, 1),
        (3, 1), (2, 1), (1, 1), (1, 2), (1, 3), (1, 4),
        (1, 5), (1, 6), (1, 7), (1, 8), (2, 8), (3, 8),
        (4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (8, 7),
        (8, 6), (8, 5), (8, 4), (8, 3), (8, 2), (8, 1)
    ]

def create_full_image(sampled_turns):
    """Create the 1024x1024 image composed of 64 xfen blocks in spiral layout."""
    image = Image.new("RGB", (1024, 1024), (200, 200, 200))
    spiral_positions = get_spiral_positions()

    for idx, (turn, (row1, col1)) in enumerate(zip(sampled_turns, spiral_positions)):
        xfen = turn.get("xfen")
        if not xfen:
            print(f"Skipping turn {idx} — missing xfen")
            continue

        block = draw_xfen_block(xfen)

        # Convert from 1-based to pixel positions
        px = (col1 - 1) * 128
        py = (row1 - 1) * 128
        image.paste(block, (px, py))

    return image

def main():
    import sys
    if len(sys.argv) != 2:
        print("Usage: python chess_image_spiral.py path/to/chmov.json")
        return

    filename = sys.argv[1]
    turns = load_chess_turns(filename)
    sampled = sample_turns(turns, 64)
    image1024 = create_full_image(sampled)

    # Save both PNG and JPEG
    image1024.save("chess_visual.png", "PNG")
    image1024.save("chess_visual.jpg", "JPEG")
    print("Saved chess_visual.png and chess_visual.jpg")

if __name__ == "__main__":
    main()

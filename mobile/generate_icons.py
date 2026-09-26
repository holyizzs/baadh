"""Generate simple RAINFO alert icons (blue flood wave) as PNGs — stdlib only (zlib + struct)."""
import struct
import zlib
import os

OUT_DIR = os.path.join(os.path.dirname(__file__), "icons")


def make_png(size: int, path: str) -> None:
    """32x32-ish pixel art of a flood wave on dark navy, scaled to `size`."""
    art = [
        "................................",
        "................................",
        "................................",
        "..............####..............",
        ".............######.............",
        "............########............",
        "...........##########...........",
        "..........############..........",
        ".........##############.........",
        "........################........",
        ".......##################.......",
        "......####################......",
        ".....######################.....",
        "....########################....",
        "...##########################...",
        "..############################..",
        "..#########WWWWWWWWWW#########..",
        "..########WW#WW#WW#WW#########..",
        "..#########WWWWWWWWWW#########..",
        "..############################..",
        ".KK##########################KK.",
        ".KK##########################KK.",
        "KKKK########################KKKK",
        "KKKK########################KKKK",
        "KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK",
        "KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK",
        "KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK",
        "KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK",
        "KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK",
        "KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK",
        "................................",
        "................................",
    ]
    colors = {
        ".": (15, 23, 42, 255),      # slate-900 background
        "#": (37, 99, 235, 255),    # blue-600 wave
        "W": (255, 255, 255, 255),  # white warning band
        "K": (220, 38, 38, 255),    # red-600 flood base
    }

    px = size // 32
    raw = b""
    for row in art:
        line = b""
        for ch in row:
            c = colors[ch]
            line += bytes(c) * px
        raw += (b"\x00" + line * px) * px

    def chunk(tag: bytes, data: bytes) -> bytes:
        c = tag + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c))

    ihdr = struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)
    png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
           + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(png)
    print(f"  wrote {path} ({size}x{size}, {len(png)} bytes)")


if __name__ == "__main__":
    make_png(192, os.path.join(OUT_DIR, "icon-192.png"))
    make_png(512, os.path.join(OUT_DIR, "icon-512.png"))
    make_png(72, os.path.join(OUT_DIR, "badge-72.png"))
    print("Icons generated.")

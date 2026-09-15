from pathlib import Path

UPLOAD_DIR = Path(__file__).resolve().parents[1] / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


def save_file(file_content: bytes, filename: str) -> str:
    final_path = UPLOAD_DIR / filename
    final_path.write_bytes(file_content)
    return str(final_path)

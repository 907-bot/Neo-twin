"""Splat Compression"""
def compress_splat(ply_path: str, target_size_mb: int = 8) -> str:
    try:
        from gsplat import compress
        output_path = ply_path.replace(".ply", "_compressed.splat")
        compress(ply_path, output_path, target_size_mb=target_size_mb)
        return output_path
    except ImportError:
        print("gsplat not installed. Install with: pip install gsplat")
        return ply_path

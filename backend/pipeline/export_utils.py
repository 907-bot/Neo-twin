"""Export Utilities - .splat, .glb, .ply"""
import os

def export_splat(ply_path: str) -> str:
    from gsplat import compress
    output_path = ply_path.replace(".ply", ".splat")
    compress(ply_path, output_path, target_size_mb=8)
    return output_path

def export_glb(ply_path: str) -> str:
    output_path = ply_path.replace(".ply", ".glb")
    try:
        from sugar_scene import export_mesh
        export_mesh(ply_path, output_path)
    except ImportError:
        print("SuGaR not installed, skipping mesh export")
        output_path = None
    return output_path

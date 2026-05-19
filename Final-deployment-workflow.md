feature-extraction using colmap -> feature matching(SIFT) -> Sparse Reconstruction from SfM -> 3D gaussian splatting training (3DGS) -> Langsplat training(language embedding) -> Assest exporting

graph TD
    A[Start: Matched SIFT Features] --> B[1. Select Seed Image Pair]
    B --> C[2. Reconstruct Initial 3D Points]
    C --> D[3. Find Next Best Image]
    D --> E[4. Estimate Camera Pose of New Image]
    E --> F[5. Triangulate New 3D Points]
    F --> G[6. Bundle Adjustment: Global Optimization]
    G --> H{More Images?}
    H -- Yes --> D
    H -- No --> I[End: Final Sparse Point Cloud]
    
    style B fill:#e1f5fe,stroke:#0288d1
    style G fill:#efebe9,stroke:#5d4037
    style I fill:#e8f5e9,stroke:#2e7d32

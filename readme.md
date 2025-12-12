# Multimodal-Vision-Tactile-Integrated-AGI_Vision

### Objective

Developing AGI technologies that integrate tactile and visual information to simulate human-level haptic perception and generate immersive virtual haptic content

### Updates
- 2025.12.12
    - `develop_3dgs` branch를 `master (main)` branch로 merge
    - Segment Anything Model (SAM) 관련 folder 생성 및 segmentation baseline 구축
    - 각 2D-3D Object Reconstruction 방법 별로 folder 생성 (NeRF, 3DGS, Diffusion-based)
- 2025.10.24
    - `develop_3dgs` branch 생성 및 3DGS baseline 따로 구축
    - 3DGS 성능 재현 확인 $\rightarrow$ NeRF Synthetic Datasets 기준 `SSIM Score: 0.94`
- 2025.09.29
    - 시촉각 AGI 과제 github repository 생성
    - README.md 정리

### Directory Layout
- `unityassets` : Unity 3D object 제작에 사용된 코드 저장용.
    - 용량이 큰 3D asset들을 직접 업로드 하지 않도록 주의 부탁드립니다.
- `Hunyuan3D-2.1` : Diffusion 기반 image-to-3D model인 Hunyuan3D-2.1 관련 코드 저장.
    - 용량이 큰 `*.ckpt, *.pth` 등 모델 checkpoint 업로드 하지 않도록 주의 부탁드립니다.
- `GNT` : NeRF 기반 image-to-3D model인 GNT 관련 코드 저장.
    - 용량이 큰 `*.ckpt, *.pth` 등 모델 checkpoint 업로드 하지 않도록 주의 부탁드립니다.

### 작업시 권고 사항
- 작업 별 branch 생성
    - `develop_unity`, `develop_hunyuan` 등 작업별로 branch 생성하여 작업을 부탁드립니다.
    - 작업 내용끼리 충돌하는 등의 문제를 방지하기 위함입니다.
- `master` branch 업데이트 시에는 반드시 pull request 생성하고, 주변 동료에게 확인 받은 후 업데이트
    - `master` branch는 어느 정도 진행된 작업물을 업데이트 하는 곳입니다.
    - 반드시 모든 사람들이 공유 해야하는 내용들을 `master` branch에 push 해주세요.
    - 작업 별 branch 생성 --> 자유롭게 해당 branch push --> 최종 업데이트시 `master` 에 pull request



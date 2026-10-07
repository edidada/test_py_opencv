# OpenCV 主流版本功能点整理

> 本文按版本整理 OpenCV 主流版本的功能点（新 API、新后端、新编解码、性能优化等），数据来自官方 Change Logs（[OpenCV-Change-Logs wiki](https://github.com/opencv/opencv/wiki/OpenCV-Change-Logs)）。
> 本项目当前使用 `opencv-python 4.13`（见 `pyproject.toml`），对应下文 4.13 一节。
> 面向新手：每个功能点尽量用一句话说明"能干什么"，不必一次读完，可按版本按需查阅。

---

## 一、演进脉络（里程碑速览）

| 时期 | 版本 | 里程碑主题 |
|---|---|---|
| 2013 | 2.4.x | 经典 C/C++ API 时代，`IplImage` 风格仍可用，是教科书/老项目最常见的版本 |
| 2014–2016 | 3.0 / 3.4 (LTS) | 引入 `cv::Mat` 现代化重构、UMat/T-API 并行框架雏形；3.3/3.4 起 DNN 模块进入主线，可用 ONNX/TensorFlow 模型推理 |
| 2018 | 4.0 | 移除旧 C API；`text`、`clustering`、`structured_analysis` 等模块移入 opencv_contrib；全面转向 C++11 与模块化发布 |
| 2020–2021 | 4.5.x | G-API 计算图框架成熟（Python 绑定、状态化 kernel）、DNN 支持 YOLO 系列解析与 CUDA/OpenVINO 后端增强 |
| 2022 | 4.6 / 4.7 | NPU/异构后端扩展（TIM-VX、华为 CANN）、RISC-V RVV 可扩展 SIMD 后端、ONNX Runtime 后端进入 Python |
| 2023 | 4.8 / 4.9 | ARM FP16 全速推理、Transformer 算子（Attention/Einsum/LayerNorm）支持、自研 QR 解码器、Model Zoo 随版本发布 |
| 2024 | 4.10 / 4.11 | `cv::Mat` 原生 FP16 类型、全新 findContours 实现、C++20 支持、JPEG XL 实验性编解码、fisheye solvePnP |
| 2025 | 4.12 / 4.13 | GIF/动图编解码、OpenVINO NPU 支持、RISC-V RVV 1.0 新 HAL、迭代相位相关、16 位 LUT、FFmpeg 8.0、DLPACK 零拷贝 |
| 2026 | 4.14 / 5.0 | 多尺度 ECC 对齐、VideoWriter/VideoCapture 支持 alpha 通道、AVX VNNI；5.0 大版本重构（见官方 OpenCV-5 摘要与 4→5 迁移指南） |

> 说明：4.x 采用"奇偶无关"的滚动发布，每年约 2 个功能版本；LTS 分支（如 3.4）长期只修 bug。

---

## 二、各版本主要功能点

### 4.5.0（2020 年底）—— G-API 计算图时代开启

- **G-API Python 绑定**：用 Python 搭数据流计算图（`GIn`/`GOut`），把预处理+推理+后处理编排成一张图执行，而非逐函数调用。
- **G-API 图序列化**：计算图可导出为字节流再还原，便于部署时"离线构图、在线执行"。
- **NN 后处理算子**：`parseYolo`、`parseSSD` 进入 G-API，网络输出直接变成 `GArray<Rect>` 结构。
- **GFrame/MediaFrame**：图数据处理支持 NV12/YUV 等视频原生格式与外部内存，减少色彩转换拷贝。
- **状态化 kernel（`GAPI_OCV_KERNEL_ST`）**：kernel 可在视频流帧间保留状态，方便写跟踪、累积类算法。
- **视频向算子扩充**：`goodFeaturesToTrack`、`buildOpticalFlowPyramid`、`calcOpticalFlowPyrLK`（光流跟踪全家桶）可入图。
- CUDA/OpenVINO/TensorRT 后端在 DNN 模块持续增强，YOLOv4 等模型可直接跑。

### 4.6.0（2022 年中）—— NPU 与嵌入式后端扩展

- **TIM-VX NPU 后端**：可在 Vivante 类 NPU 上跑 DNN 推理。
- **OpenCV AI Kit (OAK) 后端（G-API，实验性）**：Camera+NN 流水线可下发到 OAK 板卡，支持 host 与设备端混合编排。
- **oneVPL + OpenVINO GPU 直通**：Windows 上硬件解码的 GPU 纹理可直接预处理+推理，零回传 host；oneVPL 同时支持了 Linux。
- **GStreamer pipeline source 暴露给 Python**。
- **Windows on ARM 的 NEON 构建支持**。
- Universal Intrinsics 大量内核补齐动态派发（Split4/Merge3/ConvertTo/加减除等），x86 各代指令集自动选优。

### 4.7.0（2022 年底）—— 可扩展 SIMD 与 Python 大暴露

- **通用可扩展 intrinsics 后端**：首个 RISC-V RVV 1.0 实现，为无固定向量长度的 CPU 写一次 SIMD 代码。
- **DNN 新算子**：ONNX reduce 系列、Tile；批量 NMS（多类别检测提速）；华为 CANN 后端加入。
- **OpenVINO 后端异步推理请求**；oneVPL 表面到 OpenCL/GPU 的零拷贝通路。
- **Python 绑定大扩容**：Stateful kernels、ONNX Runtime 后端、core/imgproc 的几乎全部 G-API 算子。
- **多页图像格式的新迭代式 API**（如 TIFF 多帧逐页读取）。

### 4.8.0（2023 年中）—— ARM FP16 提速

- **ARMv8 上完整 FP16 计算分支**：DNN 推理比 FP32 约快 1.5 倍（移动端/树莓派类设备显著受益）。
- RISC-V RVV 支持继续完善；DNN 支持更多层型，可跑更多主流模型。

### 4.9.0（2023 年底）—— Transformer 算子与自研 QR 解码

- **Core**：新增 `cv::broadcast`；NEON_FP16/NEON_BF16 指令运行时检测与派发；龙芯 LoongArch 128-bit SIMD 优化。
- **DNN 实验性 Transformer 支持**：ONNX Attention、Einsum、GatherElements、InstanceNorm、Expand 等层；LayerNorm 打通 OpenVINO/OpenCL/CUDA 后端；新 fastGEMM 实现与图融合优化（共享节点、可交换算子合并）。
- **OpenVINO 后端 INT8 模型**；ONNX Runtime 后端接入 DirectML/CUDA/TensorRT/CoreML/OpenVINO 四类 Execution Provider——Python 里用 ORT 换设备更简单。
- **Objdetect**：自研 QR 码解码器（替换 QUIRC）；ArUco 角点动态窗口精化。
- **G-API**：`QueueSource` 手动推帧、VAS Object Tracker 场景跟踪器；Fluid kernel 迁到通用 intrinsics。
- Android 开始经 Maven Central 发布 AAR；随版发布 [OpenCV Model Zoo](https://github.com/opencv/opencv_zoo) 4.9 分支。

### 4.10.0（2024 年中）—— Mat 原生 FP16 与新轮廓提取

- **Core**：`cv::Mat` 新增 `CV_FP16` 数据类型（半图像素可直接存 Mat，`convertTo` 支持 FP16 互转）；并行框架支持 cgroups v2（容器内 CPU 配额感知）。
- **Imgproc**：全新 `findContours` 实现（内存占用更低、更稳）；`remap` 支持相对位移场（光流/形变场景更自然）；`cartToPolar/polarToCart` 支持原地操作。
- **Calib3d**：fisheye 相机模型的 `solvePnP`；对称圆形标定板检测改进。
- **DNN**：TFLite 层扩充（GlobalPool2D/Transpose/HardSwish-INT8/Split/FC/Softmax/Cast）、ONNX Mod/GroupNorm；CuDNN 9+、OpenVINO 2024；Raft 光流模型支持；Vulkan 后端 N 路逐元素算子；Attention 层多轮优化。
- **Objdetect**：QR 码 Structured Append（分片拼长内容）解码模式。

### 4.11.0（2024 年底）—— C++20 与 JPEG XL 尝鲜

- **Core**：正式支持 **C++20** 标准；FileStorage 支持 int64；`Mat::reinterpret`（重解释像素类型不拷贝）。
- **Imgproc**：Weighted Hough Transform（加权霍夫直线）；`approxPolyN`（按边数约束的多边形逼近）；GaussianBlur/cvtColor 增加"更快但非位精确"选项；形态学新增菱形结构元（随后版本完善）。
- **DNN**：DepthToSpace/SpaceToDepth、Unflatten（Attention 需要）、ONNX TopK、TFLite LeakyReLU；Winograd 改运行时派发。
- **Imgcodecs**：**实验性 JPEG XL (jxl)** 编解码；`imencodeMulti()`（多帧编码）；图像编解码错误处理改进。
- **VideoIO**：`VideoCapture` 支持从内存流构造；GStreamer 后端支持 BGRA 流。
- **HighGUI**：新增基于 Framebuffer 的后端（无 X11 的嵌入式设备也能 `imshow`）。
- **平台**：高通 SoC 的 FastCV HAL（`-DWITH_FASTCV=ON`）；v_exp/v_log/v_erf/v_sin/v_cos 自有向量化实现；CUDA 增加 Blackwell 架构初步支持与 `haveCUDA` 运行时探测。

### 4.12.0（2025 年中）—— 动图编解码大年 + RISC-V 新 HAL

- **Imgcodecs**：**GIF 解码与编码**进主线 imgcodecs；**动图 WebP**、**APNG hidden frame**、内存中动画编解码；JPEG XL 支持 `IMREAD_UNCHANGED`、`imdecode()` 直读内存、无损压缩；GDAL 多通道支持。
- **平台/HAL**：**全新 RISC-V RVV 1.0 HAL 实现**（官方博客专题）；core 侧新增大量 HAL 入口（sum、DFT/DCT、norm、calcHist、pyrUp、remap 变体等）方便第三方替换加速。
- **Core**：用户自定义日志回调；`solveCubic` 精度改进；SIMD_SCALABLE 支持 exp/sqrt。
- **Imgproc**：`findContours` 优化降内存；椭圆拟合鲁棒性提升、新增 `getClosestEllipsePoints`；`threshold` 支持 mask 与 `THRESH_DRYRUN`（只取自适应阈值不实际阈值化）；非极大距离优化。
- **Calib3d**：fisheye 模型的 `solvePnPRansac`；fisheye undistortPoints 优化；新相机矩阵估计优化。
- **DNN**：OpenVINO **NPU** 支持；CANN 后端算子扩充；TFLite 导入新增 SUB/SQRT/DIV/NEG/SUM 等算子；conv+eltwise 融合处理多输出节点（Split）。
- **Photo**：`fastNlMeansDenoising` 支持 16-bit 图像。
- **Video**：跟踪器工厂可预载 DNN 模型（开箱用 learning-based tracker）；Android 原生摄像头捕获支持 zoom。
- **硬件**：Orbbec Gemini 330 深度相机支持；CUDA 初步支持 Nvidia Blackwell。
- **Python/Java**：Python 动画编码绑定；Java 增加 `VideoCapture` 内存流构造器。

### 4.13.0（2025 年底）—— 本项目当前版本（重点）

- **Core**：16-bit LUT（`LUT` 支持 CV_16U 查表）与对应 HAL 入口；`Mat::clone()` 深拷贝行为明确化；Input/OutputArray 向量长度校验；FileStorage 支持 JSON null 与反斜杠转义；**DLPACK 支持**——与 PyTorch/JAX/NumPy 等框架零拷贝互转张量。
- **Imgproc**：**迭代相位相关**（Iterative Phase Correlation，高精度图像对齐/配准新算法）；`minEnclosingConvexPolygon`（带边数约束的最小凸包多边形）；CLAHE 新增 BitShift 选项；`ThickLine` 远端点优化；滤波器/形态学无状态 HAL 入口。
- **Imgproc/平台**：Windows on ARM 多项性能优化（FAST/AGAST 等）；RISC-V RVV HAL 补 Canny/Scharr/Sobel/FAST； scalable-SIMD 分支支持 RVV。
- **Imgcodecs**：**OpenEXR 多光谱读写**；32bpp BI_BITFIELDS BMP；PNG `IMWRITE_PNG_ZLIBBUFFER_SIZE` 选项；AVIF 编解码安全检查。
- **VideoIO**：**FFmpeg 8.0 支持**；FFmpeg 后端可按索引打开摄像头、swscale 线程选项优化；**树莓派 4/5 V4L2 无状态 HEVC 硬件加速（配合 FFmpeg）**；macOS 支持 Orbbec Gemini330。
- **Features2D/Objdetect**：ArUco 检测新增**基于像素的置信度**输出、生成器支持索引偏移；`QRCodeDetector::detectAndDecodeMulti` 多码检测改进。
- **DNN**：ONNX randomNormalLike、TFLite Minimum/Maximum 层；NEON 版 fastGEMM1T；softmax_3d 展开优化；OpenVINO Params 新增 `cfgEnsureNamedTensors`/`cfgClampOutputs`，可动态设置 workload type（ONNX OVEP 同）。
- **Calib3d**：新增 `estimateTranslation2D()`（纯平移场景更快更稳的双点集对齐）；`stereoCalibrate` 可选 QR 分解；fisheye undistortPoints 收敛性改进。
- **Video**：背景减除器支持"已知前景掩码"（optional Known Foreground Mask）；`findTransformECC/computeECC` 支持多通道。
- **Photo**：merge 系列支持 16U/32F。
- **绑定/工具**：Python G-API 自定义流 source；Java 支持 `List<List<Mat>>`、Vec4i 包装、可选新 Cleaners 接口；contrib 模块也可打包进 JS；支持 MSVC 2026、CUDA 13.0；可复现构建（host 版本号可选）。

### 4.14.0（2026 年中，最新 4.x）

- **Core**：AVX VNNI 支持、`cv::reduce` SUM 平台 SIMD、transposeND 快路径、Universal SIMD 版 gemm、minMaxLoc/countNonZero 优化；IPP 数学函数迁入 HAL 层；RVV HAL 补 norm/convertScale/Laplacian/spatialGradient。
- **Imgproc**：**`findTRUContours`——无锁并行轮廓提取**（多核大图提速）；距离变换 SIMD；霍夫变换累加器并行优化；remap 插值、box filter、PyrDown、LUT/equalizeHist 优化；EMD（推土机距离）求解器提速。
- **Imgcodecs**：`imreadWithMetadata()` 支持 cICP 色彩管理元数据；EXIF profile 处理改进。
- **Features2D**：BFMatcher 交叉检查 OpenCL 加速；AKAZE OpenCL 支持；KAZE DIFF_CHARBONNIER 差异算子补全；RVV 版 FAST 优化；ArUco 正反标记一次遍历求边界误差。
- **Video**：**VideoWriter/VideoCapture 支持 alpha 通道**；`CAP_PROP_IMAGE_SEQ_START` 指定图像序列起始帧号。
- **Calib/Align**：**Multiscale ECC**（多尺度增强相关对齐）；InRange 通用 intrinsics。
- **DNN**：15 种超越函数激活层 SIMD；RVV convBlock 内核；ONNX DynamicQuantizeLinear 层支持。
- **平台**：Ubuntu 26.04 支持；Windows on ARM FP16 全开；可复现构建；RISC-V 支持继续加深。

### 5.0.0（2026 年年中，大版本）

- 官方摘要与迁移指南：[OpenCV-5](https://opencv.org/opencv-5/)、[4→5 migration guide](https://github.com/opencv/opencv/wiki/OpenCV-4-to-5-migration)。
- 大版本清理（Big OpenCV cleanup）、Core/Imgproc/HAL/DNN/3D-Calib 全面更新、样例重写——4.x API 迁移需对照指南。
- 发布注记：Android 包需注意 16KB page 对齐（用 `16kb-page-fix` 后缀包上 Google Play）；Windows-on-Arm 二进制在高通骁龙设备验证。

---

## 三、新手速查：常用功能是在哪个版本引入的？

| 你可能遇到的功能 | 引入版本 |
|---|---|
| DNN 模块跑 ONNX/TFLite 模型 | 主线 3.3/3.4 起，4.x 持续增强 |
| G-API Python 编程 | 4.5 |
| 华为 CANN 后端 / ONNX Runtime 后端进 Python | 4.7 |
| ARM FP16 推理提速 | 4.8 |
| Transformer 类模型（Attention/Einsum/LayerNorm） | 4.9 |
| `cv::Mat` 直接存半精度浮点（CV_FP16） | 4.10 |
| JPEG XL 编解码（实验） | 4.11 起，4.12 增强 |
| GIF / 动图 WebP / APNG 编解码 | 4.12 |
| OpenVINO NPU 推理 | 4.12 |
| DLPACK 与 PyTorch 张量零拷贝互转 | 4.13 |
| 迭代相位相关（图像配准） | 4.13 |
| FFmpeg 8.0 / 树莓派 HEVC 硬解 | 4.13 |
| 视频读写带透明通道（alpha） | 4.14 |
| 无锁并行轮廓提取 `findTRUContours` | 4.14 |

> 提示：`opencv-python` PyPI 包通常滞后主仓库数周~数月；本项目 `requirements`/`pyproject` 锁的是 4.13.x，升级前先查 [opencv-python releases](https://github.com/opencv/opencv-python/releases)。

---

## 四、参考

- 官方 Change Logs：<https://github.com/opencv/opencv/wiki/OpenCV-Change-Logs>（4.11+）与 [v2.2–v4.10](https://github.com/opencv/opencv/wiki/OpenCV-Change-Logs-v2.2%E2%80%90v4.10)
- GitHub Releases：<https://github.com/opencv/opencv/releases>
- OpenCV 官方博客：<https://opencv.org/blog/>
- OpenCV 5 概要与迁移指南：<https://opencv.org/opencv-5/>、<https://github.com/opencv/opencv/wiki/OpenCV-4-to-5-migration>

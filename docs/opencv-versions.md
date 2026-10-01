# OpenCV 版本功能点整理

本文按版本整理 OpenCV 主流版本的功能点，数据全部来自官方 wiki 的 Change Logs
（[https://github.com/opencv/opencv/wiki/OpenCV-Change-Logs](https://github.com/opencv/opencv/wiki/OpenCV-Change-Logs)
及其链接的历史页 OpenCV-Change-Logs-v2.2‐v4.10）。整理时优先保留"新增 API / 新模块 / 新后端 / 新编解码 / SIMD 与 HAL / 语言绑定 / 平台支持"这类功能点，
忽略琐碎 bugfix；条目后的 `#数字` 为官方 changelog 中的 PR/issue 编号，便于回溯。
本项目（test_py_opencv）当前使用 `opencv-python 4.13`（4.13.0.92），因此重点展开 4.11–4.14 与 5.0。

## 演进脉络

- **2.4.x（2.4.0 于 2012 年 5 月，官方 changelog 记至 2.4.9）**：延续 1.x/2.x 的 C API + `CvMat` 风格，`cv::getBuildInformation()` 提供完整构建信息，FFmpeg 视频读写成熟，MOG2 背景减除用 TBB 优化；作为"经典 API 保守分支"长期维护。
- **3.0（2015 年 6 月）/ 3.1（2015）**：主仓库模块化、C++ 接口成为一等公民，旧 C API 标记废弃；`opencv_contrib` 承载实验性模块（xfeatures2d 的 DAISY/BRISK/LATCH、aruco 的棋盘格+ArUco 标定等）；`parallel_for_` 新增 pthreads 后端，Android OpenCV Manager 用 Java 重写。
- **3.3（2017）**：`dnn` 模块从 contrib 进入主仓库，加入层融合与 AVX/AVX2/NEON 优化，并新增可选 Halide 后端；实现 SSE4.2/AVX/AVX2 运行时动态派发。
- **3.4（2017–2018）**：`dnn` 支持 faster R-CNN、OpenCL 加速与 JS 绑定；bit-exact resize（`INTER_LINEAR_EXACT`）；OpenCL 内核磁盘缓存。
- **4.0（2018）**：删除 1.x 遗留 C API（objdetect/photo/video/videoio/imgcodecs/calib3d），全面转向 C++11（`cv::String = std::string`）；引入 G-API 图执行模块；宽通用内在函数（universal intrinsics）重写数百内核；`objdetect` 加入 QR 码检测/解码；DIS 光流进入主仓库；Kinect Fusion 进 contrib。
- **4.1–4.4（2019–2020）**：DNN 持续演进（OpenVINO/Myriad X、Mask-RCNN、内存占用下降）、`dnn` 目标检测/分割高层 API、Python 绑定与类型提示改进、`calib3d` 手眼标定方法。
- **4.5.0（2020）**：许可证由 BSD 改为 **Apache 2**；GSoC 2020 成果集中落地（主仓库更好的 SIFT、USAC/RANSAC 重构、深度学习单目标跟踪、RISC-V 优化、Julia 绑定）。
- **4.5.1–4.5.5（2020–2021）**：DNN/CUDA/OpenVINO 持续改进为主：并行后端插件化（4.5.2）、IntelligentScissors、HighGUI 后端插件化与 FFmpeg 硬件编解码 UMat（4.5.3）、DNN 8-bit 量化与 RISC-V DNN 优化（4.5.4）、VideoCapture 音频支持与 OpenVINO 2021.4 LTS（4.5.5）。
- **4.6.0（2022）**：CI 迁移到 GitHub Actions；GCC 12 / Clang 15 / FFmpeg 5.0 支持；DNN 新增 TIM-VX NPU 后端与更多层；G-API 流式与 MediaFrame 能力扩展。
- **4.7.0（2022）**：通用内在函数新增"可变宽度可扩展向量"后端（首个实现为 RISC-V RVV 1.0）；CUDA 12.0；`objdetect` 主仓库内建 ArUco 标记与 AprilTag（含 ChArUco/diamond 板标定）；DNN 新增华为 CANN 后端与批量 NMS。
- **4.8.0（2023）**：DNN 支持 TFLite（含 int8 量化模型）并可脱离 Protobuf 构建；G-API 引入 OpenVINO API 2.0 后端；`objdetect` 收编条形码检测/解码并提供图形码统一 API；AVIF 解码（libavif）；Python 类型存根（typing stubs）。
- **4.9.0（2023）**：DNN 实验性 Transformer 支持（ONNX Attention / Einsum）；自研 QR 解码器替代 QUIRC；Android 改为 Maven 分发 AAR。
- **4.10.0（2024）**：`cv::Mat` 支持 FP16 数据类型；DNN 内存占用大幅下降；ARM KleidiCV 作为 HAL 引入；Wayland、zlib-ng、Apple VisionOS 与 Windows ARM64 实验支持。
- **4.11.0（2024/2025 跨年版）**：C++20 支持与 `algoHint`（近似/精确实现开关）；动画图像新 API 与 GIF、JPEG XL 起步；FastCV/RVV/KleidiCV 等 HAL 布局成型。
- **4.12.0（2025 夏季版）**：全新 RISC-V RVV 1.0 HAL 后端；GIF/动画 WebP/动画 PNG、JPEG XL 完善；Intel IPP 与 OpenVX 重构为 HAL。
- **4.13.0（2025 跨年版）**：图像元数据 API、OpenEXR 多光谱、FFmpeg 8.0、Python DLPACK、KleidiCV 0.7 默认启用、CUDA 13 / VS2026 支持。
- **4.14.0（2026 夏季版）**：IPP 大规模迁移到 HAL；Imgproc 无锁并行轮廓提取；视频读写 alpha 通道；DNN ONNX 层与 SIMD 激活函数扩展。
- **5.0（2026）**：5.0-alpha（2024-12）已公布技术预览要点（彻底清理 1.x C API、模块拆分、新增数据类型、新 DNN 引擎）；5.0 正式版于 2026 年 6 月发布，官方 changelog 段落仍标注 "ChangeLog is TBD"。

## 4.5 – 4.8（精简）

### 4.5.x 系列

- 许可证：4.5.0 起改为 Apache 2（3.x 分支仍为 BSD）。
- Core：支持可插拔并行后端（TBB/OpenMP/pthreads/std::thread），并可通过插件动态加载（4.5.2 [#19365]、[#19470]）。
- HighGUI：引入 UI 后端选择/插件化机制（4.5.3 [#20116]）。
- Imgproc：新增 IntelligentScissors 交互式分割（4.5.2 [#19194]）。
- VideoIO：FFmpeg 后端支持 UMat/OpenCL 硬件加速解码（4.5.3 [#19755]）；VideoCapture 音频轨支持（MSMF [#19721]、GStreamer [#21264]）。
- DNN：8-bit 量化推理与 ONNX 导入（4.5.4 [#20228]、[#20535]）；RISC-V 上 DNN 优化（[#20287]、[#20521]）；OpenVINO 后端跟进 2021.1 / 2021.4 LTS；CUDA 后端 MatMul 等层优化（[#20138]）。
- 其他：USAC 随机采样一致性框架重构、SIFT 改进、深度学习单目标跟踪（GSoC 2020）、Julia 绑定（contrib）。

### 4.6.0

- 构建与 CI：项目 CI/发布流程迁移至 GitHub Actions；新增 GCC 12、Clang 15、FFmpeg 5.0 支持。
- DNN：新增层与激活（LSTM(+CUDA)、resize(+ONNX)、Sign、Shrink、Reciprocal、depth2space、space2depth 等）；新增 **TIM-VX NPU 后端**；OpenVINO 2022.1 初始支持并移除 legacy API；音频语音识别 C++ 示例（[#21458]）。
- G-API：`cv::MediaFrame` 支持灰度格式（[#21511]）；CPU 后端支持 `.reshape()`；Fluid 后端大量内核 SIMD 化并接入动态派发（Resize/Split4/Merge3/Add/Sub/ConvertTo）。
- 通用：禁用浮点 denormal 处理以提升数值内核速度（[#21521]）。

### 4.7.0

- Core：通用内在函数新增"可扩展向量"后端，首个目标为 RISC-V RVV 1.0（[#22179]）；新增 N 维 `flip`；CUDA 12.0 支持。
- Imgproc：新增 `cv::stackBlur`（[#20379]）与多项性能优化。
- Objdetect：ArUco 标记与 AprilTag 支持（含 ChArUco、diamond 板检测与标定）进入主仓库（[#22986]）；QR 码检测/解码质量改进与对齐标记支持；提供 QR 基准测试。
- DNN：新增华为 **CANN 后端**（[#22634]）；多类目标检测的批量 NMS（[#22857]）；ARM 卷积加速、Winograd 优化；Nanotrack v2 神经网络跟踪器；Scatter/ScatterND/Tile/部分 reduce 层。
- 多媒体：FFmpeg 5.x；NVIDIA 现代 Video Codec SDK（NVCUVID/NVENC）硬件编解码；FFmpeg 读写 `CV_16UC1`；PNG 使用 libSPNG；自研 libJPEG-Turbo 的 SIMD 加速；Android H264/H265；多页图像格式的迭代器式 API。
- G-API：OpenVINO 后端异步推理请求；oneVPL/VAAPI 样本与测试；Python 暴露 stateful kernel、ONNX RT 后端与全部 core/imgproc 操作。

### 4.8.0 / 4.8.1

- DNN：支持 **TFLite 模型（含 int8 量化）**（[#23161]、[#23409]）；可关闭 Protobuf 依赖构建（[#23604]）；ONNX LayerNormalization/GELU/QLinearSoftmax；CANN 后端支持 Split/Slice/Clip/Sub/PRelu/ConvTranspose；ARMv8 全 FP16 计算分支（比 FP32 约快 1.5x [#22275]）；Vulkan 后端重构（约 4x 提速 [#23349]）；`blobFromImageParam` 预处理 API（[#22750]）；Meta SAM（Segment Anything）修复。
- Objdetect：`FaceDetectorYN` 升级（性能/精度/关键点 [#23020]）；基于 ArUco 思路的新 QR 检测算法（[#23264]）；条形码检测解码从 contrib 移入主仓库（[#23666]），并提供条码/QR 统一 API（[#23758]）。
- Core：`cv::reduce` 新增 `REDUCE_SUM2`（[#13879]）；新增 `cv::hasNonZero`（[#22947]）；RISC-V RVV v0.11（LLVM16/GCC13）与 T-Head 0.7.1/1.0 构建支持；IPP 二进制更新至 20230330。
- Imgproc：`IntelligentScissorsMB::buildMap` 局部代价优化（[#21959]）；`INTER_NEAREST_EXACT` 偶数尺寸修复；distanceTransform 大图修复。
- Calib3d：USAC 框架改进（[#23078]）；`icvGetRectangles` 像素网格修正，提升 `getOptimalNewCameraMatrix`/`stereoRectify` 精度；ChArUco 板进入标定工具与样本。
- 多媒体：通过 libavif 支持 **AVIF**（[#23596]）；Orbbec Femto Mega 相机；MSMF 后端 HEVC/H265 编码；TIFF `CV_32S` 编码；OBS 虚拟摄像头修复。
- Python/JS：Python typing stubs（[#20370]）、`np.float16` 支持、RotatedRect 等绑定；JS 可关闭 wasm inlining，扩展 ArUco/ChArUco/QR/条码绑定。
- 4.8.1：安全版本，修复 WebP **CVE-2023-4863**，并修复 5x5 depthwise 卷积性能回退。

## 4.9

### Core / SIMD
- 新增 `cv::broadcast`（[#23965]），并用于改进 ONNX `Expand` 层支持。
- 新增 NEON_FP16、NEON_BF16 等现代 NEON 指令的检测与运行时派发（[#24420]）。
- 新增 LoongArch 128-bit 向量优化与 CPU 特性检测/派发（[#23929]）。
- GSoC/暑期项目：跨模块重构 CPU 优化代码，使其适配可变宽度 SIMD（RISC-V RVV）。

### DNN
- 实验性 **Transformer 支持**：ONNX `Attention`（[#24476]）、`Einsum`（[#24037]）、`GatherElements`（[#24092]）、`InstanceNorm`（[#24378]）。
- 全新 **fastGEMM** 实现并基于其实现多个层（[#23897]、[#24694]、[#24509]）；ARM 上 Winograd FP16 优化（[#23654]）。
- OpenVINO 后端支持 **INT8 模型**（[#23987]）；`LayerNormalization` 扩展到 OpenVINO/OpenCL/CUDA 后端（[#24552]）；CANN 后端支持 HardSwish/LayerNorm/InstanceNorm。
- 图优化：共享节点与可交换运算的图融合改进（[#24463]、[#24577]、[#24483]）；Yolo 系列模型的测试与修复。

### Imgproc / Features2d
- 自有 QR 码解码器实现，替代第三方 QUIRC 库（[#24299]）；QR 编码器版本估计修复；Android QR 检测示例（[#24598]）。
- ArUco 角点动态窗口精细化，精度提升（[#24355]）。

### Video / VideoIO
- GSoC：新增基于 Vision Transformer 的跟踪 API `TrackerVit`（VitTrack，[#24201]）。
- `cv::VideoWriter`（CAP_FFMPEG）支持对原始编码流做封装（[#24363]）。

### Calib3d / Python / 平台
- `calibrateCamera` 在标定系统欠约束时抛异常（[#23025]）；棋盘点检测器多项修复；`cornerSubPix` 越界访问修复（[#24527]）。
- Python：为缺失与手工包装的类型补全类型存根（[#24023]、[#24022]、[#23910]）；NumPy 数组只读标志处理（[#24026]）。
- Android：改为 **AAR + Maven Central** 分发；移除 OpenCV Manager API，改用 `OpenCVLoader.initLocal()`；Gradle 7.6.3 与新样本。
- 平台：CMake 中把 CUDA 作为一等语言的实验支持（[#23021]）；实验性 Apple VisionOS 支持（[#24136]）；Orbbec Gemini2 / Gemini2 XL 相机（[#24666]）。

## 4.10

### Core
- `cv::Mat` 新增 **FP16 数据类型**（CV_FP16，[#24892]、[#24918]），废弃 `convertFp16`，`convertTo` 等支持 FP16。
- HAL API 扩展：`minMaxIdx`、`LUT`、`meanStdDev`、`moments`、`normHamming`、`transpose` 及部分算术函数（[#25563]、[#25554]、[#25483]、[#25491]、[#25342]）。
- FileStorage 以人类可读形式输出实数（[#25351]）；`cartToPolar`/`polarToCart` 支持原地操作（[#24893]）；并行框架支持 cgroups v2（[#25285]）。

### Imgproc
- 全新 `findContours` 实现（[#25146]、[#25680]、[#25385]）。
- `cv::remap` 新增相对位移场选项（[#24621]）。
- HAL 新增 `gaussianBlur`、`remap`、`bilateralFilter`，并扩展 `projectPoints`、`equalizeHist`、Otsu 阈值（[#25397]、[#25399]、[#25343]、[#25511]、[#25565]、[#25509]）。

### DNN
- 显著降低 DNN 内存占用（[#25181]）；新增 `Net::dumpToPbtxt` 便于用 Netron 查看优化后的图（[#25582]）。
- TFLite 层：GlobalPool2D、Transpose、HardSwishInt8、Split、FullyConnected、SoftMax、Cast（[#25613]、[#25297]、[#24985]、[#25273]）；ONNX 新层 Mod、GroupNorm（[#24765]、[#24610]）。
- Attention 层持续优化；scatter/scatterND 并行化（[#24813]）；Winograd 卷积使用策略调优（[#24709]）；RISC-V RVV 与 RISC-V P 扩展上的 depthwise 卷积优化（[#25361]、[#24556]）。
- 后端与模型：新增 Raft 光流模型支持与跟踪示例（[#24913]）；现代 YOLO 检测器支持完善与文档（[#24898]）；Vulkan 后端 NaryEltwise 层（[#24768]）；CuDNN 9+、OpenVINO 2024 支持（[#25412]、[#25199]）。

### Objdetect / Calib3d
- QR 码支持 Structured Append 解码模式（[#24548]）；ArUco 检测器线程安全与确定性改进（[#24807]、[#24829]）。
- 新增鱼眼相机模型的 `solvePnP` 实现（[#25028]）；`findChessboardCorners` 多项改进；鱼眼标定焦距初值策略调整（[#25030]）。

### 语言绑定 / 平台
- Python：实验性 **NumPy 2.0** 支持；`Rect2f`/`Point3i` 绑定（[#24919]）；文件路径参数支持 path-like 对象（[#24773]）。
- Android：JavaCameraView/JavaCamera2View/NativeCameraView 支持任意屏幕方向；AAR 加入 Kotlin 类；示例支持从 Maven 引入 OpenCV。
- 平台：CUDA 12.4+；Linux **Wayland** HighGUI 后端（[#25551]）；RISC-V P 扩展 HAL 初始版本（Andes，[#25167]）；ARM **KleidiCV** HAL（`-DWITH_KLEIDICV=ON`，[#25443]）；`zlib-ng` 替代 zlib（`-DWITH_ZLIB_NG=ON`）；OneAPI 2024；实验性 Apple VisionOS 与 Windows ARM64 支持。

## 4.11

- Generic：支持 C++20 标准（[#26590]）；为核心/Imgproc 部分函数引入 `algoHint` 参数，允许"更快但非 bit-exact"的实现；内部 C API 清理并为 5.x 回填。
- Core：FileStorage 支持 `int64` 数据类型（[#26434]）；LUT 扩展支持 FP16（[#25787]）；`cv::TickMeter` 扩展（[#26212]）；OpenCL-OpenGL interop 设备发现重写并支持 Apple（[#26281]）；`Mat` 全部实例校验 allocator 指针（[#25979]）。
- Imgproc：新增以指定边数近似凸包边界的多边形函数（[#25607]）；新增 **加权霍夫变换**（[#21407]）；`GaussianBlur`、`cvtColor` 增加"更快但非 bit-exact"标志（[#25792]、[#25932]）。
- DNN：GSoC 的 **blockwise（分块）量化**支持（[#25644]）；ONNX `TopK`（[#23279]）、`DepthToSpace`/`SpaceToDepth`（[#25779]）、`Unflatten`（Attention 层所需，[#25861]）；TFLite `LeakyReLU`（[#26132]）；**YOLO v10 支持**与示例（[#25794]）；Erf/GELU 激活与 `v_exp` 激活优化（[#25147]、[#25881]）；Winograd 改为运行时派发（[#26155]）；RISC-V RVV 上 DNN 优化（[#25883]）；`blobFromImages` CPU NCHW 输出加速（[#26127]）。
- Imgcodecs：GSoC 动画图像新 API，支持 **WebP / AVIF / 动画 PNG**（[#25608]、[#25715]）；GIF 编解码起步（[#25691]）；实验性 **JPEG XL** 支持（[#26379]）；新增 `imencodemulti()`（[#26211]）；`imread`/`imdecode` 支持 RGB 布局（[#25809]）。
- VideoIO：`VideoCapture` 支持从内存数据流构造（[#25584]）；GStreamer 后端支持 BGRA 流（[#25602]）；Orbbec 相机资料与代码更新；Android 原生相机与 NDK 像素格式增强（[#26627]、[#26656]）。
- HighGUI：新增基于 Framebuffer 的 HighGUI 后端（[#25661]）；GSoC：GTK3 下的 OpenGL 支持（[#25822]）。
- HAL / SIMD：Qualcomm SoC 的新 FastCV HAL（`-DWITH_FASTCV=ON`，[#26556]）；ARM **KleidiCV HAL 升级到 0.3 并在 Android 构建中默认启用**（[#26623]）；RISC-V RVV 1.0 / 0.7.1 HAL 初始版本（[#26216]、[#26624]）；通用内在函数 RVV 后端使用 LMUL=2（[#26318]）；NDSRVP（RISC-V P 扩展）HAL 覆盖更多函数；自研向量版 `v_exp`/`v_log`/`v_erf`/`v_sin`/`v_cos`（[#24941]、[#25781]、[#25872]、[#25892]）；内置 IPP 更新至 2021.12。
- Calib3d：棋盘点检测器多项改进；支持黑格中心/角点标记的棋盘格检测（[#25808]）；`fisheye::distort` 支持非单位投影矩阵（[#25943]）；SQPnP 求解器更新（[#26219]）。
- G-API：ONNX 后端 `onnx::Params` 可传任意 session options（[#25791]）；支持 I32/I64 数据类型（[#25817]）；ONNXRT 后端引入图优化 level 标志（[#26293]）。
- Python / JS：JS API 白名单按模块拆分并支持覆盖 opencv_contrib（[#25986]、[#26387]）；USAC 相关公共类型暴露（[#26638]）。
- 平台：Android HWAsan 支持（[#25746]）；QNX 支持（[#25832]）；CUDA 侧新增 `getStdAllocator()`、无 FP16 老 GPU 修复、NPP 使用新 `NppStreamContext` API、`haveCUDA` 运行时 GPU 检查。

## 4.12

- Core：新增用户自定义日志回调（[#27154]）；`cv::Mat` 新增 `reinterpret()` 方法（[#25394]）；`mean` 走 HAL、`normalize`/`norm`/`copyTo`（带掩码）向量化；`exp`/`sqrt` 启用 SIMD_SCALABLE；`UMat` 从 `std::vector` 构造时的 `copyData` 参数废弃（[#27408]）。
- Imgproc：`findContours` 性能与内存占用优化（[#26690]、[#26834]）；`threshold` 支持可选掩码（[#26842]）并新增 `THRESH_DRYRUN` 标志（[#26836]）；形态学新增菱形结构元（[#27441]）；新增 `cv::getClosestEllipsePoints`（[#26299]）；`WARP_INVERSE_MAP` 下 remap 多线程加速（[#27108]）；medianBlur 性能提升。
- Imgcodecs：图像 I/O API **扩展元数据支持**（[#27499]）；内存中动画编码/解码（[#27013]）；动画 PNG 隐藏帧支持（[#27127]）；GIF 编解码正式落地（[#25691] 等）；动画 WebP 支持（[#25608]、[#27457]）；JPEG XL 支持 `imdecode()` 直读内存、`IMREAD_UNCHANGED` 与无损压缩（[#26844]、[#26788]、[#27384]）；GDAL 多通道支持（[#27458]）。
- DNN：TFLite 解析器新增 SUB/SQRT/DIV/NEG/SQUARED_DIFFERENCE/SUM 等 op，并减少 NHWC↔NCHW 转换（[#27307]）；TFLite StridedSlice 与 TF 导入的 strides 支持（[#27273]）；conv+eltwise（Split 多输出）融合（[#27326]）；新增 **OpenVINO NPU 支持**（[#27363]）；CANN 后端扩充算子（[#24756]）。
- Objdetect：`ArUcoDetector` 支持高效运行**多字典**（[#26934]）；QR 码新增 **ECI 编码**支持（[#24426]、[#27486]）；ChArUco 板一致性检查改为可选（[#26824]）。
- Calib3d：鱼眼相机模型的 `solvePnPRansac` 实现（[#26669]）；鱼眼 `undistortPoints` 优化；`drawAxes` 投影轴出框时告警（[#27311]）。
- Video：新增带预置 DNN 模型的**跟踪器工厂**（[#26875]）。
- Photo：`cv::fastNlMeansDenoising` 支持 16-bit（[#26831]）。
- HAL：HAL 实现拆分为独立目录（[#27252]）；**全新 RISC-V RVV 1.0 HAL 后端**（见官方博客 introducing-hal-riscv-rvv）；OpenVX 与 Intel IPP 重构为 HAL（[#26903]、[#26880] 等）；KleidiCV 更新至 0.5；扩充 Qualcomm FastCV HAL；新增 `sum`、带掩码 `copyTo`、`DFT`/`DCT`、`convert` with scale、`norm` 变体、`calcHist`、`pyrUp`、更多 `remap` 变体等 HAL 入口。
- 绑定：Python/Java/JS 头文件解析器支持条件包含（[#27325]）；动画相关绑定（[#26813]）；NumPy 2.0 兼容（`np.ptp`，[#27133]）；Java 端扩展 DNN/Features2d 绑定与 `VideoCapture` 流构造（[#27228]、[#27245]、[#27284]）；修复 `imread` 类型提示。
- 平台：兼容 CMake 4（[#27192]）；NVIDIA Blackwell GPU 架构 CUDA 初始支持（[#26820]）；QNX 7.0 构建修复、Windows ARM64EC 构建修复、Power VSX 内在函数修复；CUDA 目标在 CUDA Toolkit ≥12.8 时强制 C++17。
- VideoIO：Android 原生相机采集支持缩放（[#26837]）；Orbbec Gemini 330 相机支持（[#27230]）；DShow 自定义选项下打开相机提速。

## 4.13

- CVBenchmark：OpenCV 官方发布无偏 CPU 基准 **CVBenchmark**（[https://github.com/opencv/cvbenchmark](https://github.com/opencv/cvbenchmark)），面向真实视觉与 AI 负载评估 CPU。
- Core：新增 16-bit LUT 及对应 HAL 入口（[#27890]）；新增 `cv::Mat::copyAt` 支持 ROI 拷贝操作（[#27318]）；`InputArray/OutputArray` 对 `std::vector<T>`、`std::vector<std::vector<T>>` 的处理更准确并加入长度校验（[#28242]、[#27817]）；FileStorage 的 JSON 支持扩展（解析 `null` [#27579]、反斜杠转义 [#27587]）；新增 `inRange` HAL 入口（[#27854]）；Windows on ARM 性能优化与 FP16 转换启用（[#27575]、[#27596]、[#27897]）。
- Imgproc：新增**迭代式相位相关**（Iterative Phase Correlation，[#28146]）；新增 `cv::minEnclosingConvexPolygon`（[#27369]）；`cv::CLAHE` 新增 `BitShift` 选项（[#28014]）；`minAreaRect` 角度范围按文档统一为 [-90, 0)（[#28051]，4.5.1–4.12.0 行为不同），并用 double 提升精度（[#28149]）；为滤波与形态学引入**无状态 HAL**（[#28208]）；GaussianBlur/blur/bilateralFilter 性能优化（含 AVX512，[#27795]、[#27822]、[#27433]）；RISC-V RVV HAL 新增 Canny、Scharr、Sobel（[#27378]）。
- Imgcodecs：JPEG（ICCP、XMP）、PNG/WebP、PNG 的 `cICP`、AVIF（XMP）元数据支持扩展（[#27583]、[#27503]、[#27741]、[#27506]）；OpenEXR **多光谱**读写（[#27485]）；PNG 支持 `IMWRITE_PNG_ZLIBBUFFER_SIZE`（[#27551]）；支持 32bpp BI_BITFIELDS BMP（[#27559]）；多种格式解码尺寸上限放宽到 1 GiB 以上（[#27811]）；编码参数严格校验（[#27621]）。
- VideoIO：**FFmpeg 8.0 支持**并可通过索引打开摄像头（[#27691]、[#27841]）；树莓派 4/5 上 V4L2 无状态 HEVC 硬件加速（配合 FFmpeg，[#27453]）；swscale 线程选项优化 FFmpeg 采集（[#27755]）；Orbbec SDK 扩展（时间戳、自定义 fps/分辨率、畸变系数 API）并支持 macOS 上的 Gemini 330（[#27610]、[#27629]、[#27663]、[#27930]）；Aravis SDK 支持系统级安装与默认像素格式（[#28090]、[#28086]）。
- Objdetect：ArUco 检测新增**基于像素的置信度**（[#23190]）；`QRCodeDetector::detectAndDecodeMulti` 多码检测改进（[#27787]）；ChArUco 通过避免临时拷贝提速（[#27820]）。
- DNN：新增 ONNX `RandomNormalLike`、TFLite `Minimum`/`Maximum`（[#28164]、[#28248]、[#28171]）；`fastGEMM1T` 新增 NEON 实现与 SVE 优化+派发（[#27785]、[#28055]）；protobuf 消息可用 `LITE_RUNTIME` 编译（[#27960]）；softmax_3d 循环展开优化。
- Calib3d：新增 `estimateTranslation2D()`（[#27950]）；P3P 由 Gao 算法替换为 **Ding P3P**（[#27736]）；`stereoCalibrate` 新增 QR 分解选项（[#27920]）；`fisheye::undistortPoints` 收敛性改进（[#27993]）。
- Video：`findTransformECC`/`computeECC` 支持多通道（[#27524]）与可选模板掩码（[#27952]）；背景减除器支持"已知前景掩码"（[#27810]）；`DISOpticalFlow` 新增 `setCoarsestScale`（[#28217]）。
- Photo：`merge` 系列函数支持 16U 与 32F（[#28168]）。
- G-API：Python 中支持自定义流输入源（[#27276]）；OpenVINO Params 新增 `cfgEnsureNamedTensors`、`cfgClampOutputs`（[#27549]、[#27600]）；OpenVINO 与 ONNX OVEP 支持动态设置 workload type（[#27460]）。
- 绑定：Python 新增 **DLPACK** 支持（[#27581]、[#27861]）；`CV_WRAP_FILE_PATH` 参数生成 PathLike 类型提示（[#27767]）；把 `distCoeffs`/`cameraMatrix` 等标注为可选；Java 提供 Cleaners 接口替代 `finalize()` 的生成选项（[#28159]）与 `List<List<Mat>>` 包装（[#27705]）；JS 支持包装 opencv_contrib 并让 `Mat.clone()` 深拷贝（[#27828]、[#28216]）。
- 构建与平台：集成 **KleidiCV 0.7**（支持 macOS/Linux 且默认启用，[#28220]）；IPP ICV 集成支持 AVX512；支持 **Visual Studio 2026**（[#28013]）与 **CUDA 13.0**（[#27636]）；可复现构建（主机系统版本可选，[#27979]）；OpenBLAS 探测修复。

## 4.14

- Core：新增 **AVX VNNI** 支持（[#28684]）；`rotate` 新增 NEON 实现（[#28609]）；`cv::reduce`（REDUCE_SUM）新增平台专用 SIMD 并整体向量化（[#28782]、[#27510]）；`sum` 启用 AVX-512 派发（[#29400]）；norm、距离与 Hamming API 的 SIMD 优化（[#29335]）；RVV HAL 优化 `norm` 与 `convertScale`（[#29057]、[#29174]）；ARMPL 支持 DFT（[#28664]）；`gemm` 使用通用 SIMD 优化（[#29242]）；`sort_` 改为 `parallel_for_` 并行（[#29192]）；`transposeND` 对单位置换与 2D 转置走快速路径（[#29172]）；`AutoBuffer` 扩展为类似 `std::vector`（[#28909]）；**废弃 `MatCommaInitializer_`**（[#29060]，原文拼写 "Deprecateed"）。
- Imgproc：新增 `findTRUContours` —— 无锁并行轮廓提取（[#28773]、[#29167]、[#29461]）；距离变换新增 SIMD 支持（[#28636]）；bilateralFilter 与 medianBlur 的 AVX512 优化（[#28401]、[#28394]）；颜色转换改进并加入 AVX512 派发、LUT 与 `equalizeHist` SIMD 优化（[#28992]、[#29250]）；Hough 变换累加器的并行性与内存访问优化（[#29059]）；`PyrDown`、`remap` 插值、EMD 求解器优化（[#28650]、[#29507]、[#29194]）；**大规模 IPP→HAL 抽取**：resize、cvtColor、calcHist、distanceTransform、threshold、Canny、filter2D、boxFilter、Sobel/Scharr（[#29374]、[#29397]、[#29511]、[#29463]、[#29491]、[#29434]、[#29427]、[#29420]、[#29417]）；RVV HAL 新增 Laplacian、spatialGradient，并让 8U `INTER_LINEAR` resize 位精确（[#28887]、[#29062]、[#29473]）。
- Imgcodecs：`imreadWithMetadata()` 支持 **cICP 元数据**（[#28615]）；TIFF 允许对 32F 使用压缩方案（[#28785]）；WebP `IMWRITE_WEBP_LOSSLESS_MODE` 支持精确无损压缩（[#28519]）；EXIF profile 处理改进（[#29295]）。
- Features2d：BFMatcher 交叉校验的 **OpenCL 加速**（[#28735]、[#28828]）；AKAZE 特征新增 OpenCL 支持（[#28879]）；KAZE 补齐 `DIFF_CHARBONNIER` 支持（[#28324]）；FAST 针对 RISC-V RVV 优化（[#28938]）。
- Objdetect：ArUco 依据阈值判定标记以降低误检（[#28289]）；普通与反色标记的边界误差单趟计算优化（[#29329]）；QR 码纠错重复计算消除（[#28460]）。
- DNN：新增 ONNX **DynamicQuantizeLinear** 层（[#29018]）；为 15 个超越函数激活层加入 SIMD 实现（[#2937]）；RISC-V rv64gcv 上 `convBlock_F32` 的 LMUL=1 RVV 卷积内核（[#29405]）；Resize 层与 Slice 层并行化（[#28510]、[#28511]）；Sigmoid 用通用内在函数向量化（[#28999]）；OpenVINO 2025.3 下支持 1D int8 AvgPool（[#28961]）。
- Calib3d：`calibrateCamera` 采用 Schur 补 LM + 并行 Jacobian 累加优化（[#28461]）；`findCirclesGrid` 的 `computeRNG` 改用 Delaunay 三角剖分（[#29117]）。
- Video：新增**多尺度 ECC**（Multiscale ECC，[#28802]）；`accumulate` 系列进一步优化（[#29094]）；ScharrDeriv 优化（[#28632]）。
- VideoIO：`VideoWriter`/`VideoCapture` 支持 **alpha 通道**（[#28751]、[#28788]）；新增只读打开参数 `CAP_PROP_IMAGE_SEQ_START`，可指定按模式打开图像序列时的起始帧号（[#28844]）。
- ML / G-API / Flann：KNN 暴力最近邻距离与 SVM 核函数归约的 SIMD 优化（[#29380]、[#29404]）；G-API 的 InRange 内核通用 SIMD 化、Fluid Select 内核优化（[#29008]、[#29115]）；Flann 堆池改为线程本地存储以消除锁竞争（[#29346]）。
- Python 绑定：`VideoCapture`/`VideoWriter` 支持 **with 上下文管理器**（[#28967]）；`inRange` 签名接受 Scalar；`ECCParameters` 包装补上 `itersPerLevel`（[#29148]）。
- 构建与平台：IPP ICV 集成更新至 **IPP 2026.0.0**（[#29437]）；KleidiCV 更新至 26.03（[#28744]）；Ubuntu 26.04 支持（[#28946]）；Windows on ARM 启用 FP16 转换（[#27897]）；3rdparty(itt) 支持 LOONGARCH64（[#28439]）；Apple 平台文档改用 Xcode DocC 并新增快速上手教程（[#28704]）；Power 架构 SIMD 构建修复（[#28345]）。

## 5.0

> 官方 changelog 中 `version:5.0` 段落（2026 年 6 月）仅给出发布博客
> [https://opencv.org/opencv-5/](https://opencv.org/opencv-5/)、汇总页 OpenCV-5 与 4→5 迁移指南，正文标注 "ChangeLog is TBD"；
> 以下要点来自 5.0-alpha（2024 年 12 月）的 "Release highlights"。
> 标注约定（沿用官方）：`5+4.x` 表示已进入较新 4.x 的重要特性；`5.0` 表示 5.0 正式版完成；`5.x` 表示后续 5.x 完善。

### 总体变化

- `5+4.x`：自 4.5.0 起与 5.0 均采用 **Apache 2 许可证**（替代 BSD，以更好地应对专利问题）。
- 最低要求 **C++17**，默认以 C++17 构建，并计划兼容 C++20/C++23。
- 移除 Python 2 支持，仅要求 Python 3（3.6+）并只构建 Python 3 绑定。

### 大规模清理

- **删除 C API**：`cvCreateMat()`、`CvMat` 等旧式函数与结构全部移除，仅保留 `CV_8U` 一类宏。
- 移除 OpenVX 支持；厂商若要用 OpenVX 内核加速，可自建"非 CPU"HAL。
- `G-API` 模块移入 `opencv_contrib`。
- 经典 `ML` 模块移入 `opencv_contrib`（官方建议 Python 用户改用 scikit-learn）。
- `Features2D` 更名为 **`Features`**，范围扩展到现代深度网络输出的特征向量；过时检测子/描述子移出，但 `SIFT`、`ORB`、`FAST`、`GoodFeaturesToTrack`、`MSER` 保留。
- `5.0`：`FLANN` 不再是独立模块，由已进入 `Features` 的 **Annoy 式近似最近邻（ANN）** 搜索替代。
- `objdetect` 清理：Haar 与 HOG 检测器移入 contrib 的 `xobjdetect`，改用基于深度学习的检测器。
- `Calib3d` 拆分为三个模块：`3d`（基础三维几何与三维视觉）、`calib`（相机标定）、`stereo`（立体匹配深度图估计）。
- 删除大量过时示例（约 50% 的 C++ 示例、5% 的 Python 示例）。

### Core 模块更新

- 数据类型集合扩展：新增 `bfloat`（`CV_16BF`）、`uint32_t`（`CV_32U`）、`uint64_t`（`CV_64U`）、`int64_t`（`CV_64S`）、`bool`（`CV_Bool`）；`hfloat`（`CV_16F`）纳入体系统一支持。
- `bool` 类型每值占 1 字节，`CV_Bool` 的 `Mat` 可直接作为原先需要 `uchar/int8` 掩码的函数的掩码。
- `hfloat`/`bfloat` 运算在硬件不原生支持时也始终可用（内部标量/向量转换内联函数）；新类型支持覆盖 `Mat`、`UMat`、`InputArray/OutputArray`、core/dnn/imgproc、`FileStorage` 与语言绑定。
- 支持低于二维的数组：1D 向量与 0D 标量（`std::vector<T>` 包装后是真正的 1D 数组，`dims/rows/cols/total()` 语义有明确定义；区分空矩阵与标量请用 `empty()`）。
- Lapack 现在总是可用（SVD、特征分解、USAC 用它加速），系统无外部 Lapack 时构建并使用内置子集。
- `5.x`：Core 的进一步重构计划见官方 issue #25011。

### Imgproc 模块更新

- 加速图像变形类函数 `warpAffine`、`warpPerspective`、`remap`，依平台/尺寸/类型/标志提速 10% 到 300%+。
- 文本渲染改用 **STB truetype 引擎 + 内嵌可变字体**，支持加载自定义字体与大量 Unicode 符号（限制：阿拉伯语/天城文等连字书写系统、部分复合符号未正确处理，需 HarfBuzz；不支持彩色 emoji，STB 为黑白引擎）。

### HAL 与 SIMD 更新

- `5+4.x`：新增大量 HAL 入口，便于厂商为 OpenCV 函数提供自定义加速实现；5.0 正式版还会追加。
- `5+4.x`：在关键位置引入可选 `AlgorithmHint hint` 参数，让用户在速度与精度之间取舍（默认 `ALGO_HINT_DEFAULT`；CMake 可用 `-DOPENCV_ALGO_HINT_DEFAULT=ALGO_HINT_APPROX`）。
- `5+4.x`：数学函数的通用内在函数版本 `v_exp`、`v_log`、`v_erf`、`v_sincos` 加入，用于加速深度学习推理与图像处理。
- ARMv8 NEON 与 RISC-V RVV 后端加入 **FP16 通用内在函数**（默认不启用 SIMD FP16 算术，需专门编译选项），配合运行时派发选择最佳内核。
- `5.x`：`UMat` 将扩展为可存放任意 CPU/非 CPU 数组与张量，从 OpenCL-only 的 T-API 演进为通用异构 API（"non-CPU HAL" / U-API）。

### DNN 模块更新

- 引入**全新的推理引擎**，与旧引擎并存：更好地支持动态形状与现代 ONNX 特性，5.0 正式版的 ONNX 规范覆盖度将显著高于旧引擎（当前相当）。
- `cv::dnn::readNet()` 新增 `int engine = ENGINE_AUTO` 参数选择引擎（默认先试新引擎、失败回退旧引擎；加载后不可切换）。
- ONNX、Caffe、TF、TFLite 解析器均更新以支持引擎选择。
- `5.x`：目前新引擎仅支持默认后端与 CPU 目标，后续将开放更多后端/目标（#26198）。

### 3D / 标定更新

- `5+4.x`：RANSAC 类算法（单应、本质矩阵、PnP 等）改用效率显著更高的 **USAC** 框架（含教程 tutorial_usac）。
- 新增 **Levenberg–Marquardt** 算法实现，更快也更精确。
- `calib` 模块新增**多相机标定框架**：智能初始化 + 基于 USAC 的优化流程，计算所有同时标定相机相对第一台相机的位姿，支持全针孔、全鱼眼与混合配置（含教程 tutorial_multiview_camera_calibration）。
- 启动基础网格处理与点云处理算法工作：TSDF、ICP 等。
- 新增流行点云格式的导入/导出器：`.ply`、`.obj`。

### 示例与其他

- 重写深度学习示例：分类、分割、目标检测、边缘检测、跟踪、行人重识别；模型可用 `samples/dnn/download_models.py` 统一下载。
- 新增实验性 **LLM（GPT-2）** 与 **扩散模型（LDM）** 示例。

## 参考

- 官方 Change Logs（4.11–4.14、5.0-alpha）：[https://github.com/opencv/opencv/wiki/OpenCV-Change-Logs](https://github.com/opencv/opencv/wiki/OpenCV-Change-Logs)
- 官方历史 Change Logs（v2.2–v4.10）：[https://github.com/opencv/opencv/wiki/OpenCV-Change-Logs-v2.2%E2%80%90v4.10](https://github.com/opencv/opencv/wiki/OpenCV-Change-Logs-v2.2%E2%80%90v4.10)
- OpenCV 5 汇总页与迁移指南：[https://github.com/opencv/opencv/wiki/OpenCV-5](https://github.com/opencv/opencv/wiki/OpenCV-5)、[https://github.com/opencv/opencv/wiki/OpenCV-4-to-5-migration](https://github.com/opencv/opencv/wiki/OpenCV-4-to-5-migration)
- OpenCV 官方博客（发布说明、RISC-V RVV HAL 等专题）：[https://opencv.org/blog/](https://opencv.org/blog/)、[https://opencv.org/opencv-5/](https://opencv.org/opencv-5/)
- GitHub Releases：[https://github.com/opencv/opencv/releases](https://github.com/opencv/opencv/releases)
- CVBenchmark（4.13 提到的官方 CPU 基准）：[https://github.com/opencv/cvbenchmark](https://github.com/opencv/cvbenchmark)

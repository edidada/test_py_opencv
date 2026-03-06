import cv2
import numpy as np
from moviepy import VideoFileClip, TextClip, CompositeVideoClip
import whisper
import os

def add_subtitles_and_watermark(
        input_video_path,
        output_video_path,
        watermark_text="© Cheng 2026",
        model_size="base",          # tiny/base/small/medium/large
        font_size_sub=40,
        font_size_water=30,
        subtitle_color='white',
        watermark_color='yellow',
        subtitle_position=('center', 'bottom'),
        watermark_position=('right', 'bottom')
):
    # 1. 加载 Whisper 模型
    print("加载 Whisper 模型...")
    model = whisper.load_model(model_size)

    # 2. 提取音频并转录（带时间戳）
    print("语音识别中...")
    result = model.transcribe(input_video_path, fp16=False)
    segments = result["segments"]  # 每个片段有 start, end, text

    # 3. 加载视频
    video = VideoFileClip(input_video_path)
    duration = video.duration

    # 4. 创建字幕 clips
    subtitle_clips = []
    for seg in segments:
        txt = seg["text"].strip()
        if not txt:
            continue

        clip = TextClip(
            txt,
            fontsize=font_size_sub,
            color=subtitle_color,
            font='Arial-Bold',          # 可换成支持中文的字体，如 'SimHei'
            stroke_color='black',
            stroke_width=1.5,
            method='caption',
            size=video.size,
            align='center'
        ).set_position(subtitle_position).set_start(seg["start"]).set_duration(seg["end"] - seg["start"])

        subtitle_clips.append(clip)

    # 5. 创建水印（全程显示）
    watermark = TextClip(
        watermark_text,
        fontsize=font_size_water,
        color=watermark_color,
        font='Arial',
        stroke_color='black',
        stroke_width=1
    ).set_position(watermark_position).set_duration(duration)

    # 6. 合成：原视频 + 字幕 + 水印
    final = CompositeVideoClip([video] + subtitle_clips + [watermark])

    # 7. 输出（保留原音频）
    print("正在写入视频...")
    final.write_videofile(
        output_video_path,
        codec='libx264',
        audio_codec='aac',
        threads=4,          # 多线程加速
        preset='medium',    # 平衡速度与质量
        fps=video.fps
    )
    print(f"完成！输出文件：{output_video_path}")

# 使用示例
if __name__ == "__main__":
    add_subtitles_and_watermark(
        input_video_path="input.mp4",
        output_video_path="output_with_subs_watermark.mp4",
        watermark_text="@myedidada | Tokyo 2026",
        model_size="small",          # small 比较准，速度也还行
        subtitle_position=('center', 0.85),  # 底部偏上一点
        watermark_position=('right', 'bottom')
    )
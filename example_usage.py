"""
Ví dụ sử dụng Character Replacement Tool
Example usage of Character Replacement Tool
"""

from character_replacement import CharacterReplacer
import sys


def example_basic():
    """Ví dụ cơ bản - Basic example"""
    print("=== Ví dụ 1: Thay thế cơ bản với blur ===\n")

    # Khởi tạo với video input
    replacer = CharacterReplacer("input.mp4")

    # Lấy thông tin video
    info = replacer.get_video_info()
    print(f"📹 Video: {info['filename']}")
    print(f"📐 Resolution: {info['resolution']}")
    print(f"⏱ FPS: {info['fps']:.1f}")
    print(f"⏳ Duration: {info['duration_seconds']:.1f}s")
    print()

    # Xử lý video với blur
    stats = replacer.process_video(
        output_path="output_blur.mp4",
        replacement_method="blur",
        show_bboxes=False,
        frame_skip=0
    )

    print(f"\n✓ Hoàn thành!")
    print(f"  Frames processed: {stats['frames_processed']}")
    print(f"  Characters replaced: {stats['characters_replaced']}")


def example_face_only():
    """Ví dụ chỉ thay thế khuôn mặt"""
    print("\n=== Ví dụ 2: Chỉ thay thế khuôn mặt với pixelate ===\n")

    replacer = CharacterReplacer("input.mp4")

    stats = replacer.process_video(
        output_path="output_face_pixelate.mp4",
        replacement_method="pixelate",
        character_filter="face",  # Chỉ xử lý face
        show_bboxes=True,
        frame_skip=0
    )

    print(f"\n✓ Hoàn thành!")
    print(f"  Characters replaced: {stats['characters_replaced']}")


def example_image_replacement():
    """Ví dụ thay thế bằng ảnh"""
    print("\n=== Ví dụ 3: Thay thế bằng ảnh khác ===\n")

    replacer = CharacterReplacer("input.mp4")

    stats = replacer.process_video(
        output_path="output_image_replaced.mp4",
        replacement_method="image",
        replacement_image="avatar.png",  # Ảnh thay thế
        character_filter="face",
        show_bboxes=False,
        frame_skip=0
    )

    print(f"\n✓ Hoàn thành!")
    print(f"  Characters replaced: {stats['characters_replaced']}")


def example_fast_processing():
    """Ví dụ xử lý nhanh với frame skip"""
    print("\n=== Ví dụ 4: Xử lý nhanh với frame skip ===\n")

    replacer = CharacterReplacer("input.mp4")

    stats = replacer.process_video(
        output_path="output_fast.mp4",
        replacement_method="blur",
        frame_skip=2,  # Bỏ qua 2 frames
        show_bboxes=False
    )

    print(f"\n✓ Hoàn thành!")
    print(f"  Frames processed: {stats['frames_processed']}")
    print(f"  Total frames: {replacer.total_frames}")
    print(f"  Speed up: ~{(replacer.total_frames / stats['frames_processed']):.1f}x")


def example_extract_info():
    """Ví dụ trích xuất thông tin nhân vật"""
    print("\n=== Ví dụ 5: Trích xuất thông tin nhân vật ===\n")

    replacer = CharacterReplacer("input.mp4")

    # Trích xuất thông tin
    info = replacer.extract_characters_info(
        output_json="characters_info.json",
        frame_step=30  # Phân tích mỗi 30 frames
    )

    print(f"\n✓ Hoàn thành!")
    print(f"  Timeline points: {len(info['characters_timeline'])}")

    # Hiển thị 1 vài điểm timeline
    if info['characters_timeline']:
        print(f"\n📊 Sample timeline:")
        for point in info['characters_timeline'][:3]:
            print(f"  Frame {point['frame_number']}: {point['characters_detected']} characters")


def example_custom_processing():
    """Ví dụ xử lý tùy chỉnh từng frame"""
    print("\n=== Ví dụ 6: Xử lý tùy chỉnh ===\n")

    import cv2

    replacer = CharacterReplacer("input.mp4")

    # Khởi tạo video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(
        "output_custom.mp4",
        fourcc,
        replacer.fps,
        (replacer.width, replacer.height)
    )

    frame_count = 0
    replaced_count = 0

    while True:
        ret, frame = replacer.cap.read()
        if not ret:
            break

        frame_count += 1

        # Phát hiện nhân vật
        characters = replacer.detect_characters(frame)

        # Xử lý custom: faces dùng pixelate, bodies dùng blur
        for char in characters:
            if char["type"] == "face":
                frame = replacer.replace_character_pixelate(frame, char, pixel_size=15)
            else:
                frame = replacer.replace_character_blur(frame, char, blur_strength=31)

            replaced_count += 1

        out.write(frame)

        if frame_count % 30 == 0:
            print(f"  Processed {frame_count} frames...")

    out.release()

    print(f"\n✓ Hoàn thành!")
    print(f"  Total frames: {frame_count}")
    print(f"  Characters replaced: {replaced_count}")


def main():
    """Main function"""
    print("=" * 60)
    print("CHARACTER REPLACEMENT TOOL - EXAMPLES")
    print("Ví dụ sử dụng công cụ thay thế nhân vật")
    print("=" * 60)

    print("\nChọn ví dụ để chạy:")
    print("1. Ví dụ cơ bản - Blur tất cả nhân vật")
    print("2. Chỉ thay thế khuôn mặt - Pixelate")
    print("3. Thay thế bằng ảnh")
    print("4. Xử lý nhanh với frame skip")
    print("5. Trích xuất thông tin nhân vật")
    print("6. Xử lý tùy chỉnh")
    print("0. Chạy tất cả (demo only)")

    try:
        choice = input("\nNhập lựa chọn (0-6): ").strip()

        if choice == "1":
            example_basic()
        elif choice == "2":
            example_face_only()
        elif choice == "3":
            example_image_replacement()
        elif choice == "4":
            example_fast_processing()
        elif choice == "5":
            example_extract_info()
        elif choice == "6":
            example_custom_processing()
        elif choice == "0":
            print("\n⚠ Demo mode - các ví dụ sẽ không chạy thực tế")
            print("Để chạy thực tế, bạn cần có file 'input.mp4' trong thư mục hiện tại")
        else:
            print("❌ Lựa chọn không hợp lệ!")
            return 1

    except FileNotFoundError as e:
        print(f"\n❌ Lỗi: File không tồn tại - {e}")
        print("\nHướng dẫn:")
        print("1. Đặt file video vào thư mục hiện tại với tên 'input.mp4'")
        print("2. Hoặc sửa đường dẫn trong code để trỏ đến file video của bạn")
        return 1
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

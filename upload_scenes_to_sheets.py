"""
Script để upload dữ liệu cảnh quay lên Google Sheets
Sử dụng Google Sheets API để thêm dòng mới vào spreadsheet
"""
import json
from datetime import datetime

def load_scenes_from_file(filepath):
    """Đọc file JSON chứa các cảnh quay"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def prepare_row_data(scenes_data):
    """
    Chuẩn bị dữ liệu để gửi lên Google Sheets
    Format theo yêu cầu của workflow:
    - id: unique identifier
    - scenes: JSON string với cấu trúc shots
    - status: "Ready" để trigger workflow xử lý
    """
    # Tạo cấu trúc shots theo đúng format workflow yêu cầu
    shots_data = {
        "shots": scenes_data.get("shots", [])
    }

    # Chuẩn bị row data
    row = {
        "id": scenes_data.get("id", f"scene_{datetime.now().strftime('%Y%m%d_%H%M%S')}"),
        "scenes": json.dumps(shots_data, ensure_ascii=False),
        "status": "Ready"
    }

    return row

def display_preview(row_data):
    """Hiển thị preview dữ liệu trước khi gửi"""
    print("=" * 80)
    print("PREVIEW DỮ LIỆU SẼ GỬI LÊN GOOGLE SHEETS")
    print("=" * 80)
    print(f"\nID: {row_data['id']}")
    print(f"Status: {row_data['status']}")
    print(f"\nScenes JSON:")
    print("-" * 80)

    # Parse và hiển thị đẹp hơn
    scenes_obj = json.loads(row_data['scenes'])
    print(f"Tổng số cảnh: {len(scenes_obj['shots'])}")
    print("\nDanh sách cảnh quay:")
    for idx, shot in enumerate(scenes_obj['shots'], 1):
        print(f"\n  Cảnh {idx}:")
        print(f"    Mô tả: {shot['scene']}")
        print(f"    Thời lượng: {shot['duration']}s")

    total_duration = sum(shot['duration'] for shot in scenes_obj['shots'])
    print(f"\n{'=' * 80}")
    print(f"TỔNG THỜI LƯỢNG VIDEO: {total_duration} giây ({total_duration/60:.1f} phút)")
    print(f"{'=' * 80}\n")

def main():
    """Main function"""
    # Đọc file scenes
    scenes_file = "scenes_trex_vs_pteranodon.json"

    print(f"Đang đọc file: {scenes_file}")
    scenes_data = load_scenes_from_file(scenes_file)

    # Chuẩn bị dữ liệu
    row_data = prepare_row_data(scenes_data)

    # Hiển thị preview
    display_preview(row_data)

    # Lưu dữ liệu đã format để sẵn sàng upload
    output_file = "ready_to_upload.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(row_data, f, ensure_ascii=False, indent=2)

    print(f"✓ Đã lưu dữ liệu sẵn sàng upload vào: {output_file}")
    print("\nLƯU Ý:")
    print("- Dữ liệu đã được format đúng theo yêu cầu của n8n workflow")
    print("- Status = 'Ready' sẽ trigger workflow xử lý tự động")
    print("- Để upload lên Google Sheets, bạn có thể:")
    print("  1. Sử dụng n8n workflow (AI Agent sẽ tự động thêm)")
    print("  2. Hoặc thêm thủ công vào Google Sheets")
    print("  3. Hoặc sử dụng Google Sheets API (cần credentials)")

if __name__ == "__main__":
    main()

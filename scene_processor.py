"""
Scene Processor - Xử lý cảnh quay với character consistency, VFX, và effects
"""
import json
import re
from typing import List, Dict, Any

class SceneProcessor:
    """Xử lý và enhancement các cảnh quay"""

    def __init__(self):
        self.character_profiles = {
            "T-Rex": {
                "description": "Tyrannosaurus Rex lớn, da xanh sẫm có vân nâu, mắt vàng sắc, răng nanh trắng bóng, cơ bắp cuồn cuộn",
                "consistent_details": [
                    "da có vân sần sùi màu xanh sẫm pha nâu đất",
                    "mắt vàng chanh với đồng tử đen sâu thẳm",
                    "răng nanh dài cong, màu trắng ngà bóng",
                    "cơ bắp chân sau cuồn cuộn, móng vuốt đen nhọn",
                    "đuôi dài khỏe, vảy lớn ở lưng"
                ],
                "scale": "15 mét chiều cao, 40 tấn"
            },
            "Pteranodon": {
                "description": "Pteranodon khổng lồ, cánh xương 7 mét, màu xám xanh, mỏ dài nhọn màu cam đậm, mào đầu đỏ sẫm",
                "consistent_details": [
                    "cánh xương dài 7 mét, da cánh mỏng màu xám xanh",
                    "mỏ dài nhọn màu cam đậm, không có răng",
                    "mào đầu đỏ sẫm hình mũi mác",
                    "vuốt chân sắc nhọn màu đen bóng",
                    "mắt lớn màu đỏ tía, nhìn sắc bén"
                ],
                "scale": "sải cánh 7 mét, cân nặng 200kg"
            }
        }

        self.vfx_library = {
            "dust_cloud": "đám bụi bay dày đặc, màu nâu đất, khuếch tán chậm trong không khí",
            "tree_shake": "cây cối rung lắc mạnh, lá rụng tung tóe",
            "ground_crack": "nứt đất lan tỏa hình tia chớp, sỏi đá bật lên",
            "impact_flash": "tia sáng trắng xanh thoáng qua khi va chạm mạnh",
            "motion_blur": "hình ảnh mờ động khi di chuyển tốc độ cao",
            "lens_flare": "chớp sáng mặt trời qua khe lá",
            "water_splash": "nước bắn tung tóe, giọt nước bay chậm",
            "debris": "mảnh vỡ cây cối, đá nhỏ bay trong không khí"
        }

        self.smoke_fire_effects = {
            "dust_impact": "bụi bay dày đặc từ chân T-Rex đạp xuống đất",
            "breathing_mist": "hơi thở ấm tạo sương mù nhẹ từ mũi",
            "friction_smoke": "khói nhẹ từ móng vuốt cọ vào đá",
            "battle_dust": "làn khói bụi dày bao trùm khu vực chiến đấu",
            "fire_sparks": "tia lửa nhỏ bắn từ va chạm răng nanh và vuốt",
            "heat_wave": "sóng nhiệt méo mó không khí ở gần T-Rex",
            "forest_particles": "hạt bụi, phấn hoa bay trong rừng",
            "impact_explosion": "vụ nổ nhỏ bụi đất khi va chạm mạnh"
        }

    def add_character_consistency(self, scene: str, scene_number: int) -> str:
        """Thêm chi tiết đồng bộ nhân vật vào mô tả cảnh"""
        enhanced = scene

        # Detect characters in scene
        has_trex = any(keyword in scene.lower() for keyword in ['t-rex', 'trex', 'khủng long', 'bạo chúa'])
        has_pteranodon = any(keyword in scene.lower() for keyword in ['pteranodon', 'bay', 'cánh'])

        details = []

        # Add T-Rex details
        if has_trex:
            trex = self.character_profiles["T-Rex"]
            # Rotate through details for variety
            detail_idx = scene_number % len(trex["consistent_details"])
            details.append(trex["consistent_details"][detail_idx])

        # Add Pteranodon details
        if has_pteranodon:
            ptero = self.character_profiles["Pteranodon"]
            detail_idx = scene_number % len(ptero["consistent_details"])
            details.append(ptero["consistent_details"][detail_idx])

        if details:
            enhanced = f"{scene} [{', '.join(details)}]"

        return enhanced

    def add_vfx_effects(self, scene: str, scene_number: int) -> str:
        """Thêm hiệu ứng VFX phù hợp với cảnh"""
        enhanced = scene
        vfx_to_add = []

        scene_lower = scene.lower()

        # Detect actions and add appropriate VFX
        if any(word in scene_lower for word in ['chạy', 'trốn', 'di chuyển']):
            vfx_to_add.append(self.vfx_library["dust_cloud"])
            vfx_to_add.append(self.vfx_library["motion_blur"])

        if any(word in scene_lower for word in ['nhảy', 'tránh', 'vung']):
            vfx_to_add.append(self.vfx_library["ground_crack"])
            vfx_to_add.append(self.vfx_library["debris"])

        if any(word in scene_lower for word in ['va chạm', 'đánh', 'tấn công']):
            vfx_to_add.append(self.vfx_library["impact_flash"])
            vfx_to_add.append(self.vfx_library["debris"])

        if any(word in scene_lower for word in ['rừng', 'cây']):
            vfx_to_add.append(self.vfx_library["tree_shake"])

        if any(word in scene_lower for word in ['ánh sáng', 'sáng lên', 'trời']):
            vfx_to_add.append(self.vfx_library["lens_flare"])

        if vfx_to_add:
            vfx_desc = "; ".join(vfx_to_add)
            enhanced = f"{enhanced} [VFX: {vfx_desc}]"

        return enhanced

    def add_smoke_fire(self, scene: str, scene_number: int) -> str:
        """Thêm hiệu ứng khói lửa"""
        enhanced = scene
        effects_to_add = []

        scene_lower = scene.lower()

        # Detect actions needing smoke/fire effects
        if any(word in scene_lower for word in ['chân', 'bước', 'đạp']):
            effects_to_add.append(self.smoke_fire_effects["dust_impact"])

        if any(word in scene_lower for word in ['gầm', 'tru', 'hàm']):
            effects_to_add.append(self.smoke_fire_effects["breathing_mist"])

        if any(word in scene_lower for word in ['va chạm', 'đụng', 'đánh']):
            effects_to_add.append(self.smoke_fire_effects["fire_sparks"])
            effects_to_add.append(self.smoke_fire_effects["impact_explosion"])

        if any(word in scene_lower for word in ['chiến', 'đấu', 'truy']):
            effects_to_add.append(self.smoke_fire_effects["battle_dust"])

        if 'cận cảnh' in scene_lower:
            effects_to_add.append(self.smoke_fire_effects["heat_wave"])

        if effects_to_add:
            effects_desc = "; ".join(effects_to_add)
            enhanced = f"{enhanced} [SFX: {effects_desc}]"

        return enhanced

    def summarize_scene(self, scene: str, scene_number: int, duration: int) -> Dict[str, Any]:
        """Tóm lược cảnh với đầy đủ thông tin sync"""

        # Phân tích cảnh
        scene_analysis = {
            "scene_number": scene_number,
            "original_description": scene,
            "duration": duration,
            "characters": [],
            "action_type": "",
            "environment": "",
            "camera_angle": "",
            "mood": "",
            "key_elements": []
        }

        scene_lower = scene.lower()

        # Detect characters
        if any(word in scene_lower for word in ['t-rex', 'trex', 'khủng long']):
            scene_analysis["characters"].append("T-Rex")
        if any(word in scene_lower for word in ['pteranodon', 'bay', 'cánh']):
            scene_analysis["characters"].append("Pteranodon")

        # Detect action type
        if any(word in scene_lower for word in ['chạy', 'trốn']):
            scene_analysis["action_type"] = "Chase"
        elif any(word in scene_lower for word in ['chiến', 'đấu', 'tấn công']):
            scene_analysis["action_type"] = "Combat"
        elif any(word in scene_lower for word in ['cận cảnh']):
            scene_analysis["action_type"] = "Close-up"
        elif any(word in scene_lower for word in ['toàn cảnh', 'rộng']):
            scene_analysis["action_type"] = "Wide shot"
        else:
            scene_analysis["action_type"] = "Transition"

        # Detect environment
        if 'rừng' in scene_lower:
            scene_analysis["environment"] = "Dense jungle"
        if 'trời' in scene_lower or 'bầu trời' in scene_lower:
            scene_analysis["environment"] = "Sky/aerial"

        # Detect camera angle
        if 'cận cảnh' in scene_lower:
            scene_analysis["camera_angle"] = "Close-up"
        elif 'toàn cảnh' in scene_lower or 'rộng' in scene_lower:
            scene_analysis["camera_angle"] = "Wide angle"
        else:
            scene_analysis["camera_angle"] = "Medium shot"

        # Detect mood
        if any(word in scene_lower for word in ['bí ẩn', 'tối']):
            scene_analysis["mood"] = "Mysterious"
        elif any(word in scene_lower for word in ['kịch tính', 'đe dọa']):
            scene_analysis["mood"] = "Intense"
        elif any(word in scene_lower for word in ['hoảng', 'lo sợ']):
            scene_analysis["mood"] = "Fearful"
        else:
            scene_analysis["mood"] = "Action"

        return scene_analysis

    def process_scenes(self, scenes_data: Dict[str, Any]) -> Dict[str, Any]:
        """Xử lý toàn bộ scenes với character consistency, VFX và effects"""

        shots = scenes_data.get("shots", [])
        processed_shots = []
        scene_summaries = []

        for idx, shot in enumerate(shots, 1):
            original_scene = shot["scene"]
            duration = shot["duration"]

            # Step 1: Add character consistency
            scene_with_characters = self.add_character_consistency(original_scene, idx)

            # Step 2: Add VFX
            scene_with_vfx = self.add_vfx_effects(scene_with_characters, idx)

            # Step 3: Add smoke/fire
            scene_enhanced = self.add_smoke_fire(scene_with_vfx, idx)

            # Step 4: Create summary
            summary = self.summarize_scene(original_scene, idx, duration)

            # Create processed shot
            processed_shot = {
                "scene_number": idx,
                "original": original_scene,
                "enhanced": scene_enhanced,
                "duration": duration,
                "summary": summary
            }

            processed_shots.append(processed_shot)
            scene_summaries.append(summary)

        # Create final output
        result = {
            "original_data": scenes_data,
            "processed_shots": processed_shots,
            "scene_summaries": scene_summaries,
            "metadata": {
                "total_scenes": len(processed_shots),
                "total_duration": sum(s["duration"] for s in processed_shots),
                "characters": ["T-Rex", "Pteranodon"],
                "processing_pipeline": [
                    "Character Consistency",
                    "VFX Enhancement",
                    "Smoke/Fire Effects",
                    "Scene Summarization"
                ]
            }
        }

        return result

def main():
    """Test the processor"""
    # Load scenes
    with open("scenes_trex_vs_pteranodon.json", "r", encoding="utf-8") as f:
        scenes_data = json.load(f)

    # Process
    processor = SceneProcessor()
    result = processor.process_scenes(scenes_data)

    # Save processed data
    with open("scenes_processed.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # Display summary
    print("=" * 100)
    print("SCENE PROCESSING COMPLETE")
    print("=" * 100)
    print(f"\nTotal Scenes: {result['metadata']['total_scenes']}")
    print(f"Total Duration: {result['metadata']['total_duration']}s ({result['metadata']['total_duration']/60:.1f} min)")
    print(f"Characters: {', '.join(result['metadata']['characters'])}")
    print(f"\nProcessing Pipeline:")
    for step in result['metadata']['processing_pipeline']:
        print(f"  ✓ {step}")

    print("\n" + "=" * 100)
    print("SAMPLE PROCESSED SCENES (First 3)")
    print("=" * 100)

    for shot in result['processed_shots'][:3]:
        print(f"\n--- Scene {shot['scene_number']} ({shot['duration']}s) ---")
        print(f"Original: {shot['original']}")
        print(f"\nEnhanced: {shot['enhanced']}")
        print(f"\nSummary:")
        print(f"  - Action: {shot['summary']['action_type']}")
        print(f"  - Characters: {', '.join(shot['summary']['characters'])}")
        print(f"  - Camera: {shot['summary']['camera_angle']}")
        print(f"  - Mood: {shot['summary']['mood']}")

    print("\n" + "=" * 100)
    print(f"Full processed data saved to: scenes_processed.json")
    print("=" * 100)

if __name__ == "__main__":
    main()

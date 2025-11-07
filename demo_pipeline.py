"""
Demo: Enhanced Video Generation Pipeline
Hiển thị chi tiết từng bước xử lý
"""
import json
from scene_processor import SceneProcessor

def print_separator(title="", width=100):
    """In dòng phân cách"""
    if title:
        print(f"\n{'='*width}")
        print(f"{title.center(width)}")
        print(f"{'='*width}\n")
    else:
        print(f"{'='*width}\n")

def demo_pipeline():
    """Demo toàn bộ pipeline"""

    # Load scenes
    print_separator("🎬 ENHANCED VIDEO GENERATION PIPELINE DEMO")

    print("📥 Loading original scenes...")
    with open("scenes_trex_vs_pteranodon.json", "r", encoding="utf-8") as f:
        scenes_data = json.load(f)

    print(f"✓ Loaded {len(scenes_data['shots'])} scenes")
    print(f"✓ Total duration: {scenes_data['total_duration']}s")

    # Initialize processor
    processor = SceneProcessor()

    # Demo từng bước cho 3 scenes đầu
    print_separator("🔍 CHI TIẾT XỬ LÝ TỪNG NODE (3 SCENES ĐẦU)")

    for idx in range(min(3, len(scenes_data['shots']))):
        shot = scenes_data['shots'][idx]
        scene_num = idx + 1

        print(f"\n{'─'*100}")
        print(f"SCENE {scene_num} / {len(scenes_data['shots'])}")
        print(f"{'─'*100}")

        original = shot['scene']
        print(f"\n📝 ORIGINAL:")
        print(f"   {original}")
        print(f"   Duration: {shot['duration']}s")

        # Step 1: Character Consistency
        print(f"\n🎭 [NODE 1] CHARACTER CONSISTENCY:")
        scene_with_char = processor.add_character_consistency(original, scene_num)
        if scene_with_char != original:
            # Extract added details
            char_details = scene_with_char.replace(original, "").strip()
            print(f"   ✓ Added: {char_details}")
        else:
            print(f"   ⊗ No characters detected in this scene")

        # Step 2: VFX Enhancement
        print(f"\n✨ [NODE 2] VFX ENHANCEMENT:")
        scene_with_vfx = processor.add_vfx_effects(scene_with_char, scene_num)
        if scene_with_vfx != scene_with_char:
            vfx_details = scene_with_vfx.replace(scene_with_char, "").strip()
            print(f"   ✓ Added: {vfx_details}")
        else:
            print(f"   ⊗ No VFX applicable")

        # Step 3: Smoke/Fire Effects
        print(f"\n🔥 [NODE 3] SMOKE/FIRE EFFECTS:")
        scene_enhanced = processor.add_smoke_fire(scene_with_vfx, scene_num)
        if scene_enhanced != scene_with_vfx:
            sfx_details = scene_enhanced.replace(scene_with_vfx, "").strip()
            print(f"   ✓ Added: {sfx_details}")
        else:
            print(f"   ⊗ No smoke/fire effects applicable")

        # Step 4: Summarize
        print(f"\n📊 [NODE 4] SCENE SUMMARY & ANALYSIS:")
        summary = processor.summarize_scene(original, scene_num, shot['duration'])
        print(f"   Characters: {', '.join(summary['characters']) if summary['characters'] else 'None'}")
        print(f"   Action Type: {summary['action_type']}")
        print(f"   Camera Angle: {summary['camera_angle']}")
        print(f"   Mood: {summary['mood']}")

        # Final Enhanced Scene
        print(f"\n🎯 FINAL ENHANCED SCENE:")
        print(f"   {scene_enhanced}")

        # Length comparison
        print(f"\n📏 ENHANCEMENT STATS:")
        original_len = len(original)
        enhanced_len = len(scene_enhanced)
        added = enhanced_len - original_len
        print(f"   Original length: {original_len} chars")
        print(f"   Enhanced length: {enhanced_len} chars")
        print(f"   Added: +{added} chars ({(added/original_len*100):.1f}% increase)")

    # Full processing
    print_separator("⚙️ PROCESSING ALL SCENES")
    print("Running full pipeline on all scenes...")
    result = processor.process_scenes(scenes_data)

    print(f"✓ Processing complete!")
    print(f"  Total scenes processed: {result['metadata']['total_scenes']}")
    print(f"  Total duration: {result['metadata']['total_duration']}s")
    print(f"  Pipeline steps: {', '.join(result['metadata']['processing_pipeline'])}")

    # Save results
    print("\n💾 Saving processed data...")
    with open("scenes_processed_demo.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("✓ Saved to: scenes_processed_demo.json")

    # Statistics
    print_separator("📊 PIPELINE STATISTICS")

    total_char_added = 0
    total_vfx_added = 0
    total_sfx_added = 0

    for shot in result['processed_shots']:
        enhanced = shot['enhanced']
        if '[VFX:' in enhanced:
            total_vfx_added += 1
        if '[SFX:' in enhanced:
            total_sfx_added += 1
        if '[' in shot['enhanced'] and ']' in shot['enhanced']:
            # Count character details
            if not ('[VFX:' in enhanced or '[SFX:' in enhanced):
                total_char_added += 1

    print(f"Character Details Added: {total_char_added}/{result['metadata']['total_scenes']} scenes")
    print(f"VFX Effects Added: {total_vfx_added}/{result['metadata']['total_scenes']} scenes")
    print(f"Smoke/Fire Effects Added: {total_sfx_added}/{result['metadata']['total_scenes']} scenes")

    coverage = ((total_char_added + total_vfx_added + total_sfx_added) /
                (result['metadata']['total_scenes'] * 3) * 100)
    print(f"\nOverall Enhancement Coverage: {coverage:.1f}%")

    # Action type distribution
    print_separator("🎬 SCENE ANALYSIS")

    action_types = {}
    moods = {}
    camera_angles = {}

    for shot in result['processed_shots']:
        summary = shot['summary']
        action = summary['action_type']
        mood = summary['mood']
        camera = summary['camera_angle']

        action_types[action] = action_types.get(action, 0) + 1
        moods[mood] = moods.get(mood, 0) + 1
        camera_angles[camera] = camera_angles.get(camera, 0) + 1

    print("Action Types Distribution:")
    for action, count in sorted(action_types.items(), key=lambda x: x[1], reverse=True):
        bar = "█" * int(count / max(action_types.values()) * 30)
        print(f"  {action:15s} | {bar} {count}")

    print("\nMood Distribution:")
    for mood, count in sorted(moods.items(), key=lambda x: x[1], reverse=True):
        bar = "█" * int(count / max(moods.values()) * 30)
        print(f"  {mood:15s} | {bar} {count}")

    print("\nCamera Angle Distribution:")
    for camera, count in sorted(camera_angles.items(), key=lambda x: x[1], reverse=True):
        bar = "█" * int(count / max(camera_angles.values()) * 30)
        print(f"  {camera:15s} | {bar} {count}")

    # Ready for video generation
    print_separator("🚀 READY FOR VIDEO GENERATION")

    print("✓ All scenes enhanced and analyzed")
    print("✓ Character consistency applied")
    print("✓ VFX and effects added")
    print("✓ Scene summaries generated")
    print("\n📤 Next steps:")
    print("  1. Import workflow: workflow_enhanced_video_generation.json")
    print("  2. Upload to Google Sheets with status='Ready'")
    print("  3. Workflow will auto-trigger and process")
    print("  4. Scenes sent to Video Generation API (Sora 2 / Veo 3)")
    print("  5. Status updated to 'Complete' with video links")

    print_separator("✅ DEMO COMPLETE")

if __name__ == "__main__":
    demo_pipeline()

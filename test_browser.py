"""
Test zendriver browser initialization
Run this to debug browser issues
"""
import asyncio
import zendriver as zd


async def test_browser():
    """Test basic browser initialization"""
    print("Testing Zendriver browser initialization...")
    print("-" * 50)

    try:
        print("1. Creating browser config...")
        config = zd.Config()
        config.add_argument("--no-first-run")
        config.add_argument("--no-default-browser-check")
        print("   ✅ Config created")

        print("\n2. Starting browser...")
        browser = await zd.start(config)
        print("   ✅ Browser started successfully")

        print("\n3. Opening test page...")
        page = await browser.get("https://www.google.com")
        print("   ✅ Page loaded")

        print("\n4. Waiting 5 seconds...")
        await asyncio.sleep(5)

        print("\n5. Closing browser...")
        await browser.stop()
        print("   ✅ Browser closed")

        print("\n" + "=" * 50)
        print("✅ SUCCESS! Zendriver is working correctly!")
        print("=" * 50)

        return True

    except Exception as e:
        print("\n" + "=" * 50)
        print("❌ ERROR! Browser initialization failed")
        print("=" * 50)
        print(f"\nError: {e}")
        print("\nPossible solutions:")
        print("1. Make sure zendriver is installed:")
        print("   pip install zendriver==0.14.2")
        print("\n2. Check Python version (requires 3.8+):")
        print("   python --version")
        print("\n3. Try running as Administrator")
        print("\n4. Check antivirus/firewall settings")
        print("\n5. Install/update Chrome browser")

        import traceback
        print("\nFull traceback:")
        traceback.print_exc()

        return False


if __name__ == "__main__":
    print("Zendriver Browser Test")
    print("=" * 50)

    # Run async test
    success = asyncio.run(test_browser())

    if success:
        print("\n✅ You can now run the main application!")
        print("   Run: python main.py")
    else:
        print("\n❌ Please fix the errors above before running main app")

    input("\nPress Enter to exit...")

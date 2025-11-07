"""
Simple manual login version
Just opens browser, you login manually, then you can generate videos
"""
import asyncio
import sys
import zendriver as zd


async def main():
    """Main function"""
    print("=" * 60)
    print("Sora Manual Login Tool")
    print("=" * 60)
    print()

    # Get user input
    print("This tool will:")
    print("1. Open Chrome browser")
    print("2. Navigate to sora.chatgpt.com")
    print("3. Wait for you to login manually")
    print("4. Then you can use the GUI to generate videos")
    print()

    headless = input("Run in headless mode? (y/N): ").lower().strip() == 'y'

    print("\nStarting browser...")

    try:
        # Create config
        config = zd.Config()
        if headless:
            config.add_argument("--headless=new")
        config.add_argument("--no-first-run")
        config.add_argument("--no-default-browser-check")

        # Start browser
        browser = await zd.start(config)
        print("✅ Browser started")

        # Open Sora
        print("\nOpening sora.chatgpt.com...")
        page = await browser.get("https://sora.chatgpt.com/explore")
        print("✅ Page loaded")

        print()
        print("=" * 60)
        print("👉 Please LOGIN in the browser window that just opened")
        print("=" * 60)
        print()
        print("Waiting for you to login...")
        print("(This script will wait for 5 minutes)")
        print()

        # Wait for login
        timeout = 300  # 5 minutes
        start_time = asyncio.get_event_loop().time()

        while asyncio.get_event_loop().time() - start_time < timeout:
            try:
                current_url = await page.url

                # Check if logged in (not on auth page)
                if "sora.chatgpt.com" in current_url and "auth" not in current_url.lower() and "login" not in current_url.lower():
                    await asyncio.sleep(3)  # Wait a bit more to be sure

                    # Check again
                    current_url = await page.url
                    if "sora.chatgpt.com" in current_url and "auth" not in current_url.lower():
                        print("\n✅ Login detected!")
                        print()
                        print("=" * 60)
                        print("SUCCESS! You are now logged in")
                        print("=" * 60)
                        print()
                        print("You can now:")
                        print("1. Keep this browser open")
                        print("2. Run the main app: python main.py")
                        print("3. Use the GUI to generate videos")
                        print()
                        print("Press Ctrl+C to close browser and exit")
                        print()

                        # Keep browser open
                        try:
                            while True:
                                await asyncio.sleep(1)
                        except KeyboardInterrupt:
                            print("\nClosing browser...")
                            await browser.stop()
                            print("Goodbye!")
                            return

                elapsed = int(asyncio.get_event_loop().time() - start_time)
                if elapsed % 15 == 0 and elapsed > 0:
                    remaining = timeout - elapsed
                    print(f"Still waiting... ({remaining}s remaining)")

                await asyncio.sleep(3)

            except Exception as e:
                print(f"Error: {e}")
                await asyncio.sleep(3)

        print("\n⏱️ Timeout - you took too long to login")
        print("Closing browser...")
        await browser.stop()

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"Error: {e}")

    input("\nPress Enter to exit...")

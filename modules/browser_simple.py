"""
Simplified browser automation - manual login
Opens browser and waits for user to login manually
"""
import asyncio
import time
from pathlib import Path
from typing import Optional, Callable
import zendriver as zd


class SoraBrowserSimple:
    """Simple browser automation with manual login"""

    def __init__(self):
        self.browser = None
        self.page = None
        self.is_logged_in = False

    async def init_and_open_sora(self, headless: bool = False):
        """
        Initialize browser and open sora.chatgpt.com
        User will login manually
        """
        try:
            # Create config
            config = zd.Config()
            if headless:
                config.add_argument("--headless=new")
            config.add_argument("--no-first-run")
            config.add_argument("--no-default-browser-check")

            # Start browser
            self.browser = await zd.start(config)

            # Open Sora
            self.page = await self.browser.get("https://sora.chatgpt.com/explore")

            return True

        except Exception as e:
            print(f"Failed to open browser: {e}")
            import traceback
            traceback.print_exc()
            return False

    async def wait_for_login(self, callback: Optional[Callable] = None, timeout: int = 300):
        """
        Wait for user to login manually
        Checks every 5 seconds if logged in
        """
        if callback:
            callback("Browser opened - Please login manually in the browser window")
            callback("Waiting for you to complete login...")

        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                # Check if on explore page (means logged in)
                current_url = await self.page.url

                if "sora.chatgpt.com" in current_url and "login" not in current_url.lower():
                    # Check for elements that only appear when logged in
                    try:
                        # Try to find something that indicates logged in state
                        # This might be a user icon, or just being on the main page
                        await asyncio.sleep(2)

                        # If we're still on sora.chatgpt.com after 2 seconds, assume logged in
                        current_url = await self.page.url
                        if "sora.chatgpt.com" in current_url and "auth" not in current_url.lower():
                            self.is_logged_in = True
                            if callback:
                                callback("✅ Login detected!")
                            return True
                    except:
                        pass

                # Not logged in yet, wait and check again
                elapsed = int(time.time() - start_time)
                if callback and elapsed % 10 == 0:
                    remaining = timeout - elapsed
                    callback(f"Still waiting for login... ({remaining}s remaining)")

                await asyncio.sleep(5)

            except Exception as e:
                print(f"Error checking login status: {e}")
                await asyncio.sleep(5)

        if callback:
            callback("⏱️ Timeout waiting for login")
        return False

    async def generate_video(
        self,
        prompt: str,
        callback: Optional[Callable] = None
    ) -> Optional[str]:
        """Generate video with given prompt"""
        try:
            if not self.is_logged_in:
                if callback:
                    callback("Not logged in!")
                return None

            if callback:
                callback("Looking for prompt input...")

            # Find text input
            text_selectors = [
                'textarea',
                'input[type="text"]',
                '[contenteditable="true"]'
            ]

            input_elem = None
            for selector in text_selectors:
                try:
                    input_elem = await self.page.find(selector, timeout=3)
                    if input_elem:
                        if callback:
                            callback(f"Found input with selector: {selector}")
                        break
                except:
                    continue

            if not input_elem:
                if callback:
                    callback("Could not find prompt input. Please enter prompt manually in browser.")
                # Give user time to enter manually
                await asyncio.sleep(5)
                return "manual"

            if callback:
                callback("Entering prompt...")

            # Enter prompt
            await input_elem.click()
            await asyncio.sleep(1)
            await input_elem.send_keys(prompt)
            await asyncio.sleep(1)

            if callback:
                callback("Looking for submit button...")

            # Try to find submit button
            submit_selectors = [
                'button[type="submit"]',
                'button:has-text("Generate")',
                'button:has-text("Create")',
                'button[aria-label*="submit"]'
            ]

            for selector in submit_selectors:
                try:
                    btn = await self.page.find(selector, timeout=2)
                    if btn:
                        await btn.click()
                        if callback:
                            callback("Submitted! Video generation started...")
                        break
                except:
                    continue
            else:
                # No button found, try Enter key
                await input_elem.send_keys("\n")
                if callback:
                    callback("Pressed Enter to submit...")

            if callback:
                callback("⏳ Video is generating... Please wait in the browser")
                callback("This can take 2-5 minutes")

            # Wait for video generation (simplified - just wait)
            await asyncio.sleep(10)

            if callback:
                callback("Generation in progress - check the browser window")

            return "generating"

        except Exception as e:
            if callback:
                callback(f"Error: {str(e)}")
            print(f"Generation error: {e}")
            import traceback
            traceback.print_exc()
            return None

    async def stop(self):
        """Stop browser"""
        if self.browser:
            try:
                await self.browser.stop()
            except Exception as e:
                print(f"Error stopping browser: {e}")
            finally:
                self.browser = None
                self.page = None
                self.is_logged_in = False


# Global instance
sora_browser_simple = SoraBrowserSimple()

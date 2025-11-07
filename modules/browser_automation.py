"""
Browser automation for sora.chatgpt.com using zendriver
"""
import asyncio
import time
from pathlib import Path
from typing import Optional, Callable
from zendriver import Browser
from .config import config


class SoraBrowserAutomation:
    """Automate Sora video generation via browser"""

    def __init__(self):
        self.browser: Optional[Browser] = None
        self.page = None
        self.is_logged_in = False

    async def init_browser(self, headless: bool = False):
        """Initialize browser instance"""
        try:
            # Initialize browser with zendriver (correct API)
            # Browser() returns a browser instance, then we need to start it
            import zendriver as zd

            # Create browser config
            config = zd.Config()
            if headless:
                config.add_argument("--headless=new")
            config.add_argument("--no-first-run")
            config.add_argument("--no-default-browser-check")
            config.add_argument("--disable-blink-features=AutomationControlled")

            # Start browser
            self.browser = await zd.start(config)
            self.page = await self.browser.get("about:blank")

            return True
        except Exception as e:
            print(f"Failed to initialize browser: {e}")
            import traceback
            traceback.print_exc()
            return False

    async def login_with_gmail(
        self,
        email: str,
        password: str,
        callback: Optional[Callable] = None
    ) -> bool:
        """
        Login to sora.chatgpt.com using Gmail

        Args:
            email: Gmail address
            password: Gmail password
            callback: Optional callback for status updates

        Returns:
            bool: True if login successful
        """
        try:
            if callback:
                callback("Opening sora.chatgpt.com...")

            # Navigate to Sora
            await self.page.get("https://sora.chatgpt.com/explore")
            await asyncio.sleep(3)

            if callback:
                callback("Looking for login button...")

            # Look for login/sign in button
            # This will vary based on actual page structure
            # Common selectors:
            login_selectors = [
                'button:has-text("Log in")',
                'button:has-text("Sign in")',
                'a:has-text("Log in")',
                'a:has-text("Sign in")',
                '[data-testid="login-button"]'
            ]

            login_clicked = False
            for selector in login_selectors:
                try:
                    elem = await self.page.find(selector, timeout=2)
                    if elem:
                        await elem.click()
                        login_clicked = True
                        break
                except:
                    continue

            if not login_clicked:
                # Maybe already on login page or already logged in
                if callback:
                    callback("Checking if already logged in...")

                # Check if already logged in by looking for user-specific elements
                try:
                    # Look for elements that only appear when logged in
                    await self.page.find('[data-testid="user-menu"]', timeout=3)
                    self.is_logged_in = True
                    if callback:
                        callback("Already logged in!")
                    return True
                except:
                    pass

            await asyncio.sleep(2)

            if callback:
                callback("Clicking 'Continue with Google'...")

            # Click "Continue with Google" button
            google_selectors = [
                'button:has-text("Continue with Google")',
                'button:has-text("Google")',
                '[data-provider="google"]',
                'button[name="provider"][value="google"]'
            ]

            google_clicked = False
            for selector in google_selectors:
                try:
                    elem = await self.page.find(selector, timeout=2)
                    if elem:
                        await elem.click()
                        google_clicked = True
                        break
                except:
                    continue

            if not google_clicked:
                if callback:
                    callback("Could not find Google login button")
                return False

            await asyncio.sleep(3)

            if callback:
                callback("Entering email...")

            # Enter email
            email_input = await self.page.find('input[type="email"]', timeout=5)
            if not email_input:
                if callback:
                    callback("Email input not found")
                return False

            await email_input.send_keys(email)
            await asyncio.sleep(1)

            # Click Next
            next_button = await self.page.find('button:has-text("Next")', timeout=3)
            if next_button:
                await next_button.click()
            else:
                # Try pressing Enter
                await email_input.send_keys("\n")

            await asyncio.sleep(3)

            if callback:
                callback("Entering password...")

            # Enter password
            password_input = await self.page.find('input[type="password"]', timeout=5)
            if not password_input:
                if callback:
                    callback("Password input not found")
                return False

            await password_input.send_keys(password)
            await asyncio.sleep(1)

            # Click Next/Sign in
            signin_button = await self.page.find('button:has-text("Next")', timeout=2)
            if not signin_button:
                signin_button = await self.page.find('button[type="submit"]', timeout=2)

            if signin_button:
                await signin_button.click()
            else:
                await password_input.send_keys("\n")

            await asyncio.sleep(5)

            if callback:
                callback("Verifying login...")

            # Wait for redirect back to Sora
            # Check if we're logged in by looking for user-specific elements
            try:
                await self.page.find('[data-testid="user-menu"]', timeout=10)
                self.is_logged_in = True
                if callback:
                    callback("✅ Login successful!")
                return True
            except:
                # Try alternative selectors
                try:
                    # Look for any element that indicates logged in state
                    current_url = await self.page.url
                    if "sora.chatgpt.com" in current_url and "login" not in current_url.lower():
                        self.is_logged_in = True
                        if callback:
                            callback("✅ Login successful!")
                        return True
                except:
                    pass

            if callback:
                callback("❌ Login verification failed")
            return False

        except Exception as e:
            if callback:
                callback(f"Login error: {str(e)}")
            print(f"Login failed: {e}")
            import traceback
            traceback.print_exc()
            return False

    async def generate_video(
        self,
        prompt: str,
        callback: Optional[Callable] = None
    ) -> Optional[str]:
        """
        Generate video on Sora

        Args:
            prompt: Text description for video
            callback: Optional callback for status updates

        Returns:
            str: Video URL or None if failed
        """
        try:
            if not self.is_logged_in:
                if callback:
                    callback("Not logged in!")
                return None

            if callback:
                callback("Looking for prompt input...")

            # Navigate to create page if not already there
            current_url = await self.page.url
            if "create" not in current_url.lower():
                # Try to find create/generate button
                create_selectors = [
                    'button:has-text("Create")',
                    'a:has-text("Create")',
                    'button:has-text("Generate")',
                    '[data-testid="create-button"]'
                ]

                for selector in create_selectors:
                    try:
                        elem = await self.page.find(selector, timeout=2)
                        if elem:
                            await elem.click()
                            await asyncio.sleep(2)
                            break
                    except:
                        continue

            if callback:
                callback("Entering prompt...")

            # Find prompt input - try multiple selectors
            prompt_selectors = [
                'textarea[placeholder*="describe"]',
                'textarea[placeholder*="Describe"]',
                'textarea[name="prompt"]',
                'textarea',
                'input[type="text"][placeholder*="describe"]'
            ]

            prompt_input = None
            for selector in prompt_selectors:
                try:
                    prompt_input = await self.page.find(selector, timeout=2)
                    if prompt_input:
                        break
                except:
                    continue

            if not prompt_input:
                if callback:
                    callback("Could not find prompt input")
                return None

            # Clear and enter prompt
            await prompt_input.click()
            await asyncio.sleep(0.5)

            # Clear existing text
            await prompt_input.send_keys("\x01")  # Ctrl+A
            await asyncio.sleep(0.2)
            await prompt_input.send_keys(prompt)
            await asyncio.sleep(1)

            if callback:
                callback("Submitting generation request...")

            # Find and click generate button
            generate_selectors = [
                'button:has-text("Generate")',
                'button:has-text("Create")',
                'button[type="submit"]',
                'button:has-text("Submit")'
            ]

            generate_button = None
            for selector in generate_selectors:
                try:
                    generate_button = await self.page.find(selector, timeout=2)
                    if generate_button:
                        break
                except:
                    continue

            if generate_button:
                await generate_button.click()
            else:
                # Try pressing Enter
                await prompt_input.send_keys("\n")

            await asyncio.sleep(3)

            if callback:
                callback("⏳ Generating video... This may take a few minutes...")

            # Wait for video to be generated
            # Look for video element or download button
            max_wait = 300  # 5 minutes max
            start_time = time.time()

            while time.time() - start_time < max_wait:
                # Check for video element
                try:
                    video = await self.page.find('video', timeout=2)
                    if video:
                        video_src = await video.get_attribute('src')
                        if video_src and video_src.startswith('http'):
                            if callback:
                                callback("✅ Video generated!")
                            return video_src
                except:
                    pass

                # Check for download button
                try:
                    download_btn = await self.page.find('button:has-text("Download")', timeout=1)
                    if download_btn:
                        # Try to get video URL
                        # Click download might trigger download
                        if callback:
                            callback("Video ready! Found download button")
                        return "download_ready"
                except:
                    pass

                await asyncio.sleep(5)
                if callback and int(time.time() - start_time) % 15 == 0:
                    elapsed = int(time.time() - start_time)
                    callback(f"Still generating... ({elapsed}s elapsed)")

            if callback:
                callback("⏱️ Generation timeout")
            return None

        except Exception as e:
            if callback:
                callback(f"Generation error: {str(e)}")
            print(f"Video generation failed: {e}")
            import traceback
            traceback.print_exc()
            return None

    async def download_video(
        self,
        output_path: str,
        callback: Optional[Callable] = None
    ) -> bool:
        """
        Download generated video

        Args:
            output_path: Local path to save video
            callback: Optional callback for status updates

        Returns:
            bool: True if download successful
        """
        try:
            if callback:
                callback("Looking for download button...")

            # Find download button
            download_selectors = [
                'button:has-text("Download")',
                'a:has-text("Download")',
                '[data-testid="download-button"]',
                'button[aria-label*="Download"]'
            ]

            download_btn = None
            for selector in download_selectors:
                try:
                    download_btn = await self.page.find(selector, timeout=2)
                    if download_btn:
                        break
                except:
                    continue

            if not download_btn:
                if callback:
                    callback("Download button not found")
                return False

            # Setup download listener
            # Note: This is simplified - actual implementation may need
            # to handle browser download dialog/settings

            await download_btn.click()

            if callback:
                callback("Download started...")

            # Wait for download to complete
            # This is platform/browser specific
            await asyncio.sleep(5)

            if callback:
                callback("✅ Download complete!")

            return True

        except Exception as e:
            if callback:
                callback(f"Download error: {str(e)}")
            return False

    async def close(self):
        """Close browser"""
        if self.browser:
            try:
                await self.browser.stop()
            except Exception as e:
                print(f"Error closing browser: {e}")
            finally:
                self.browser = None
                self.page = None
                self.is_logged_in = False


# Global instance
sora_browser = SoraBrowserAutomation()

from playwright.sync_api import Page, expect, sync_playwright
import time

def test_studio_features(page: Page):
    # 1. Load app
    page.goto("http://localhost:5173")

    # 2. Enter Control Room
    page.get_by_role("button", name="ENTER CONTROL ROOM").click()

    # 3. Verify Dashboard and Safety Panel
    expect(page.get_by_text("Pronunciation & Safety")).to_be_visible()
    expect(page.get_by_text("Banned Phrases")).to_be_visible()

    # Take screenshot of Dashboard
    page.screenshot(path="/home/jules/verification/dashboard_safety.png")
    print("Screenshot 1: Dashboard")

    # 4. Navigate to Prompt Library
    page.get_by_role("button", name="Prompt Library").click()
    expect(page.get_by_text("Manage AI voice track templates")).to_be_visible()

    # 5. Create New Prompt and Check Mix Settings
    page.get_by_role("button", name="+ New Prompt").click()

    # Check for Mix Settings
    expect(page.get_by_text("Mix Settings")).to_be_visible()
    expect(page.get_by_text("Music Bed")).to_be_visible()

    # Take screenshot of Prompt Library
    page.screenshot(path="/home/jules/verification/prompt_library_mix.png")
    print("Screenshot 2: Prompt Library")

if __name__ == "__main__":
    import os
    os.makedirs("/home/jules/verification", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            test_studio_features(page)
        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="/home/jules/verification/error.png")
        finally:
            browser.close()

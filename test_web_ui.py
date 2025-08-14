import asyncio
from playwright.async_api import async_playwright
import os
import time

async def test_performance_review_ui():
    """Test the Performance Review Tracker web UI to identify where analysis gets stuck."""
    
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(
            headless=False,  # Show browser
            slow_mo=500      # Slow down for visibility
        )
        
        page = await browser.new_page()
        
        # Track console and network
        console_logs = []
        network_logs = []
        
        page.on('console', lambda msg: console_logs.append(f'[{msg.type}] {msg.text}'))
        page.on('pageerror', lambda error: console_logs.append(f'[ERROR] {error}'))
        
        page.on('request', lambda req: network_logs.append(f'→ {req.method} {req.url}'))
        page.on('response', lambda resp: network_logs.append(f'← {resp.status} {resp.url}'))
        
        try:
            print("🌐 Step 1: Loading homepage...")
            await page.goto('http://localhost:8888', wait_until='networkidle')
            await page.screenshot(path='screenshots/01_homepage.png')
            print("✅ Homepage loaded")
            
            # Check page structure
            title = await page.title()
            print(f"📄 Title: {title}")
            
            print("\n🔍 Step 2: Analyzing page structure...")
            
            # Look for key sections
            sections = {
                'criteria_section': await page.query_selector('#criteria-section, .criteria-section'),
                'csv_section': await page.query_selector('#csv-section, .csv-section, #data-section'),
                'ai_section': await page.query_selector('#ai-section, .ai-section, #llm-section'),
                'generate_form': await page.query_selector('form, #generate-form')
            }
            
            for name, element in sections.items():
                if element:
                    print(f"✅ Found {name}")
                else:
                    print(f"❌ Missing {name}")
            
            print("\n⚙️ Step 3: Configuring options...")
            
            # Try to set AI to "none" - look for different possible selectors
            ai_none_selectors = [
                'input[value="none"]',
                'select option[value="none"]',
                'input[name*="ai"][value="none"]',
                'input[name*="llm"][value="none"]'
            ]
            
            ai_set = False
            for selector in ai_none_selectors:
                try:
                    element = await page.query_selector(selector)
                    if element:
                        await element.click()
                        print(f"✅ Set AI to 'none' using {selector}")
                        ai_set = True
                        break
                except:
                    continue
            
            if not ai_set:
                print("⚠️ Could not find AI 'none' option - proceeding anyway")
            
            await page.screenshot(path='screenshots/02_configured.png')
            
            print("\n🚀 Step 4: Starting analysis...")
            
            # Look for generate button with multiple selectors
            generate_selectors = [
                'button:has-text("Generate")',
                'input[type="submit"]',
                'button[type="submit"]',
                '#generate-btn',
                '.generate-btn',
                'button:has-text("Start")',
                'button:has-text("Run")'
            ]
            
            generate_button = None
            for selector in generate_selectors:
                try:
                    generate_button = await page.query_selector(selector)
                    if generate_button:
                        button_text = await generate_button.inner_text()
                        print(f"🔘 Found button: '{button_text}' using {selector}")
                        break
                except:
                    continue
            
            if not generate_button:
                print("❌ No generate button found\!")
                # Show all buttons for debugging
                all_buttons = await page.query_selector_all('button, input[type="submit"]')
                print(f"🔍 Available buttons ({len(all_buttons)}):")
                for i, btn in enumerate(all_buttons):
                    try:
                        text = await btn.inner_text()
                        print(f"  {i+1}. {text}")
                    except:
                        print(f"  {i+1}. [no text]")
                return
            
            # Click generate button
            print("🔄 Clicking generate button...")
            await generate_button.click()
            
            await page.screenshot(path='screenshots/03_after_click.png')
            
            print("\n⏳ Step 5: Monitoring analysis progress...")
            
            # Monitor for up to 60 seconds
            for seconds in range(60):
                # Look for progress indicators
                progress_indicators = [
                    '*:has-text("Initializing")',
                    '*:has-text("Loading")', 
                    '*:has-text("Generating")',
                    '*:has-text("Processing")',
                    '.progress',
                    '#timer',
                    '.timer',
                    '[id*="progress"]'
                ]
                
                current_state = []
                for selector in progress_indicators:
                    try:
                        elements = await page.query_selector_all(selector)
                        for elem in elements:
                            text = await elem.inner_text()
                            if text.strip():
                                current_state.append(text.strip())
                    except:
                        continue
                
                if current_state:
                    print(f"⏲️  {seconds}s: {', '.join(set(current_state))}")
                
                # Check for error messages
                error_selectors = [
                    '.alert-danger',
                    '.error',
                    '[class*="error"]',
                    '*:has-text("Error")',
                    '*:has-text("Failed")'
                ]
                
                errors = []
                for selector in error_selectors:
                    try:
                        elements = await page.query_selector_all(selector)
                        for elem in elements:
                            text = await elem.inner_text()
                            if text.strip() and 'error' in text.lower():
                                errors.append(text.strip())
                    except:
                        continue
                
                if errors:
                    print(f"❌ Errors found: {', '.join(set(errors))}")
                
                # Take periodic screenshots
                if seconds % 10 == 0:
                    await page.screenshot(path=f'screenshots/04_progress_{seconds}s.png')
                
                # Check if analysis completed
                completion_indicators = [
                    '*:has-text("Complete")',
                    '*:has-text("Finished")',
                    '*:has-text("Success")',
                    'a[href*="download"]',
                    'button:has-text("Download")'
                ]
                
                completed = False
                for selector in completion_indicators:
                    try:
                        element = await page.query_selector(selector)
                        if element:
                            text = await element.inner_text()
                            print(f"✅ Analysis completed: {text}")
                            completed = True
                            break
                    except:
                        continue
                
                if completed:
                    break
                
                await page.wait_for_timeout(1000)  # Wait 1 second
            
            await page.screenshot(path='screenshots/05_final.png')
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            await page.screenshot(path='screenshots/error.png')
        
        finally:
            print(f"\n📊 Console logs ({len(console_logs)}):")
            for log in console_logs[-20:]:  # Last 20 logs
                print(f"  {log}")
            
            print(f"\n🌐 Network logs ({len(network_logs)}):")
            for log in network_logs[-20:]:  # Last 20 requests
                print(f"  {log}")
            
            # Check for specific API calls
            analysis_requests = [log for log in network_logs if '/api/' in log and 'analysis' in log]
            if analysis_requests:
                print("\n🔍 Analysis API calls:")
                for req in analysis_requests:
                    print(f"  {req}")
            
            print("\n🔍 Browser will stay open for 10 seconds for manual inspection...")
            await page.wait_for_timeout(10000)
            await browser.close()

# Run the test
if __name__ == "__main__":
    print("🧪 Starting Performance Review Tracker UI Test\n")
    asyncio.run(test_performance_review_ui())
    print("\n✅ Test completed. Check screenshots/ directory for captured images.")

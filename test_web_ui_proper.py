import asyncio
from playwright.async_api import async_playwright
import time

async def test_complete_workflow():
    """Test the complete Performance Review Tracker workflow step by step."""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,  # Keep visible for debugging
            slow_mo=1000
        )
        
        page = await browser.new_page()
        
        # Track logs
        console_logs = []
        network_logs = []
        
        page.on('console', lambda msg: console_logs.append(f'[{msg.type.upper()}] {msg.text}'))
        page.on('pageerror', lambda error: console_logs.append(f'[ERROR] {error}'))
        page.on('request', lambda req: network_logs.append(f'→ {req.method} {req.url}'))
        page.on('response', lambda resp: network_logs.append(f'← {resp.status} {resp.url}'))
        
        try:
            print("🌐 Step 1: Loading homepage...")
            await page.goto('http://localhost:8888', wait_until='networkidle')
            await page.screenshot(path='screenshots/01_homepage.png')
            print("✅ Homepage loaded")
            
            print("\n🎯 Step 2: Selecting workflow type...")
            
            # Check if workflow selection is visible
            workflow_selection = await page.query_selector('#workflow-selection')
            if workflow_selection:
                is_visible = await workflow_selection.is_visible()
                print(f"✅ Workflow selection visible: {is_visible}")
                
                # Click on Competency Assessment
                competency_card = await page.query_selector('[data-workflow="competency"]')
                if competency_card:
                    print("🎯 Found competency card, clicking...")
                    # Wait for and click the competency assessment button
                    competency_btn = await page.query_selector('button:has-text("Start Competency Assessment")')
                    if competency_btn:
                        await competency_btn.click()
                        print("✅ Clicked 'Start Competency Assessment'")
                        await page.wait_for_timeout(2000)
                        await page.screenshot(path='screenshots/02_workflow_selected.png')
                    else:
                        print("❌ Competency button not found")
                        return
                else:
                    print("❌ Competency card not found")
                    return
            else:
                print("❌ Workflow selection not found")
                return
            
            print("\n📋 Step 3: Navigating workflow steps...")
            
            # Check if main workflow is now visible
            main_workflow = await page.query_selector('#main-workflow')
            if main_workflow:
                is_visible = await main_workflow.is_visible()
                print(f"✅ Main workflow visible: {is_visible}")
            
            # Step 3a: Skip criteria step (use defaults)
            print("📝 Step 3a: Handling criteria step...")
            criteria_next_btn = await page.query_selector('#criteria-next-btn')
            if criteria_next_btn:
                # Check if button is enabled
                is_disabled = await criteria_next_btn.is_disabled()
                print(f"📝 Criteria next button disabled: {is_disabled}")
                
                # If disabled, we might need to interact with criteria form
                if is_disabled:
                    # Try to enable it by using default criteria or skipping
                    print("📝 Trying to enable criteria next button...")
                    # Look for any form elements that might need interaction
                    upload_tab = await page.query_selector('[data-bs-target="#upload-tab"]')
                    if upload_tab and await upload_tab.is_visible():
                        await upload_tab.click()
                        await page.wait_for_timeout(1000)
                        print("📝 Clicked upload tab")
                
                # Try clicking next button
                try:
                    await criteria_next_btn.click()
                    print("✅ Clicked criteria next button")
                    await page.wait_for_timeout(2000)
                    await page.screenshot(path='screenshots/03_criteria_done.png')
                except Exception as e:
                    print(f"⚠️ Could not click criteria next: {e}")
                    # Try to force enable and click
                    await page.evaluate("document.getElementById('criteria-next-btn').disabled = false")
                    await criteria_next_btn.click()
                    print("✅ Force-enabled and clicked criteria next button")
            
            # Step 3b: Handle data step
            print("📊 Step 3b: Handling data step...")
            data_next_btn = await page.query_selector('#data-next-btn')
            if data_next_btn:
                is_disabled = await data_next_btn.is_disabled()
                print(f"📊 Data next button disabled: {is_disabled}")
                
                # Try to select CSV data source
                csv_radio = await page.query_selector('input[value="csv"]')
                if csv_radio:
                    await csv_radio.click()
                    print("📊 Selected CSV data source")
                    await page.wait_for_timeout(1000)
                
                try:
                    await data_next_btn.click()
                    print("✅ Clicked data next button")
                    await page.wait_for_timeout(2000)
                    await page.screenshot(path='screenshots/04_data_done.png')
                except Exception as e:
                    print(f"⚠️ Could not click data next: {e}")
                    # Force enable
                    await page.evaluate("document.getElementById('data-next-btn').disabled = false")
                    await data_next_btn.click()
                    print("✅ Force-enabled and clicked data next button")
            
            # Step 3c: Handle AI step
            print("🤖 Step 3c: Handling AI step...")
            
            # Look for "none" option for AI
            none_option = await page.query_selector('input[value="none"]')
            if none_option:
                await none_option.click()
                print("🤖 Selected 'none' for AI provider")
                await page.wait_for_timeout(1000)
            
            ai_next_btn = await page.query_selector('#ai-next-btn')
            if ai_next_btn:
                await ai_next_btn.click()
                print("✅ Clicked AI next button")
                await page.wait_for_timeout(2000)
                await page.screenshot(path='screenshots/05_ai_done.png')
            
            print("\n🚀 Step 4: Final generate step...")
            
            # Now we should be on the generate step
            generate_btn = await page.query_selector('#generate-btn')
            if generate_btn:
                is_visible = await generate_btn.is_visible()
                is_disabled = await generate_btn.is_disabled()
                print(f"🚀 Generate button - visible: {is_visible}, disabled: {is_disabled}")
                
                if is_visible and not is_disabled:
                    await page.screenshot(path='screenshots/06_ready_to_generate.png')
                    print("🔥 Clicking GENERATE PERFORMANCE REVIEW button...")
                    await generate_btn.click()
                    print("✅ Generate button clicked\!")
                    
                    # Now monitor the progress
                    await page.screenshot(path='screenshots/07_generate_clicked.png')
                    
                    print("\n⏳ Step 5: Monitoring analysis progress...")
                    
                    # Monitor for progress indicators and errors
                    for seconds in range(120):  # Monitor for 2 minutes
                        # Look for progress elements
                        progress_elements = await page.query_selector_all('.progress-bar, #progress-message, #progress-details, .progress')
                        
                        current_progress = []
                        for elem in progress_elements:
                            try:
                                text = await elem.inner_text()
                                if text.strip():
                                    current_progress.append(text.strip())
                            except:
                                continue
                        
                        if current_progress:
                            print(f"⏲️  {seconds}s: Progress - {', '.join(set(current_progress))}")
                        
                        # Check for "Initializing" or timer specifically
                        initializing_elem = await page.query_selector('text="Initializing"')
                        if initializing_elem:
                            print(f"⏳ {seconds}s: Found 'Initializing' element")
                        
                        # Check for timer display
                        timer_elem = await page.query_selector('[id*="timer"], .timer')
                        if timer_elem:
                            try:
                                timer_text = await timer_elem.inner_text()
                                if timer_text.strip():
                                    print(f"⏲️  {seconds}s: Timer shows: {timer_text}")
                            except:
                                pass
                        
                        # Check for errors
                        error_elements = await page.query_selector_all('.alert-danger, .error, [class*="error"]')
                        errors = []
                        for elem in error_elements:
                            try:
                                text = await elem.inner_text()
                                if text.strip() and ('error' in text.lower() or 'failed' in text.lower()):
                                    errors.append(text.strip())
                            except:
                                continue
                        
                        if errors:
                            print(f"❌ {seconds}s: Errors found - {', '.join(set(errors))}")
                        
                        # Take screenshot every 15 seconds
                        if seconds % 15 == 0:
                            await page.screenshot(path=f'screenshots/08_progress_{seconds}s.png')
                        
                        # Check if completed
                        completed = await page.query_selector('.alert-success, .complete, .finished, .download')
                        if completed:
                            print(f"✅ {seconds}s: Analysis appears to be completed\!")
                            break
                        
                        # Check if the generate button is re-enabled (could indicate completion or error)
                        btn_disabled = await generate_btn.is_disabled()
                        if not btn_disabled and seconds > 10:  # Give it at least 10 seconds
                            print(f"⚠️ {seconds}s: Generate button re-enabled - might indicate completion or error")
                        
                        await page.wait_for_timeout(1000)  # Wait 1 second
                    
                    await page.screenshot(path='screenshots/09_final_result.png')
                    
                else:
                    print("❌ Generate button not ready for clicking")
            else:
                print("❌ Generate button not found")
                # Debug: show current step
                current_step = await page.query_selector('.workflow-step[style*="block"], .workflow-step:not([style*="none"])')
                if current_step:
                    step_id = await current_step.get_attribute('id')
                    print(f"🔍 Current step seems to be: {step_id}")
        
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            await page.screenshot(path='screenshots/error_final.png')
        
        finally:
            print(f"\n📊 Console logs ({len(console_logs)}):")
            for log in console_logs[-10:]:  # Last 10 logs
                print(f"  {log}")
            
            print(f"\n🌐 Network logs ({len(network_logs)}):")
            api_requests = [log for log in network_logs if '/api/' in log]
            if api_requests:
                print("🔍 API requests:")
                for req in api_requests:
                    print(f"  {req}")
            else:
                print("⚠️ No API requests found")
            
            print("\n🔍 Keeping browser open for 15 seconds for manual inspection...")
            await page.wait_for_timeout(15000)
            await browser.close()

# Run the test
if __name__ == "__main__":
    print("🧪 Starting Complete Workflow Test\n")
    asyncio.run(test_complete_workflow())
    print("\n✅ Test completed. Check screenshots/ directory for the journey.")

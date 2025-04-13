from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Step 1: Connect to the already open Microsoft Edge browser
def connect_to_edge():
    try:
        options = webdriver.EdgeOptions()
        options.use_chromium = True
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # Default port for Edge debugging
        driver = webdriver.Edge(options=options)
        print("Connected to the open Microsoft Edge browser.")
        return driver
    except Exception as e:
        print(f"Failed to connect to Edge browser: {e}")
        return None

# Step 2: Scrape the schedule data
def scrape_schedule(driver):
    schedule_data = []
    rows = driver.find_elements(By.CSS_SELECTOR, "table tr")  # Adjust selector based on the website's structure

    for row in rows[1:]:  # Skip header row
        try:
            # Extract classroom name
            classroom = row.find_element(By.CSS_SELECTOR, "td.classroom").text.strip()  # Adjust selector
            if classroom not in ["edfe", "edkb", "edga"]:
                continue  # Skip classrooms not in the specified list

            # Extract date and instructor name
            date = row.find_element(By.CSS_SELECTOR, "td.date").text.strip()  # Adjust selector
            instructor = row.find_element(By.CSS_SELECTOR, "td.instructor").text.strip()  # Adjust selector

            # Check if "In-termine" is in the comments section
            comments = row.find_element(By.CSS_SELECTOR, "td.comments").text.strip()  # Adjust selector
            if "In-termine" not in comments:
                continue  # Skip rows without "In-termine"

            # Extract the registration link below "In-termine"
            registration_link = row.find_element(By.CSS_SELECTOR, "td.comments a").get_attribute("href")  # Adjust selector

            # Append the data to the schedule list
            schedule_data.append({
                "classroom": classroom,
                "date": date,
                "instructor": instructor,
                "registration_link": registration_link
            })
        except Exception as e:
            print(f"Error processing row: {e}")

    return schedule_data

# Step 3: Main function
def main():
    # Connect to Edge browser
    driver = connect_to_edge()
    if not driver:
        return

    # Scrape the schedule data
    print("Scraping schedule data...")
    schedule_data = scrape_schedule(driver)
    print("Scraped Schedule Data:", schedule_data)

    # Close the browser (optional, since the browser is already open manually)
    # driver.quit()

if _name_ == "_main_":
    main()
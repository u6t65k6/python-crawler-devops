from selenium.webdriver.common.by import By

# Save screenshot of the page
def snapshot(driver, path):
    driver.save_screenshot("./" + str(path) +".png")
    return str(path) + ".png"

    # filename = f"{path}.png"
    # driver.save_screenshot(filename)
    # return filename
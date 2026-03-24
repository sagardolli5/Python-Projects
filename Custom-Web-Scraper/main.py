from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

all_data = []

# to keep the browser running
chrome_option = webdriver.ChromeOptions()
chrome_option.add_experimental_option("detach", True)

URL = "https://www.nba.com/stats"

driver = webdriver.Chrome(options=chrome_option)
driver.get(URL)

wait = WebDriverWait(driver, 20)

# Accept cookies
wait.until(
    EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
).click()


parent = wait.until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "[class*='Layout_base']"))
)

cards = parent.find_elements(
    By.CSS_SELECTOR,
    "div[class*='LeaderBoardCard_lbcWrapper']"
)

for card in cards:
    # Category inside each card
    category = card.find_element(By.CSS_SELECTOR, "h2[class*='LeaderBoardCard_lbcTitle']").text.strip()

    # Find all player names
    names = card.find_elements(By.CSS_SELECTOR, "a[class*='LeaderBoardPlayerCard_lbpcTableLink']")

    # Find all corresponding scores
    scores = card.find_elements(By.CSS_SELECTOR,
            "td[class*='LeaderBoardWithButtons_lbwbCardValue'] a[class*='LeaderBoardPlayerCard_lbpcTableLink']")

    # Loop through names and scores
    for player_name, player_score in zip(names, scores):
        name = player_name.text.strip()
        score = player_score.text.strip()
        all_data.append({
            "Category": category,
            "Name": name,
            "Score": score
        })

driver.quit()

#all_data - list of dictionaries
df = pd.DataFrame(all_data)

# Reset index starting at 1
df.index = range(1, len(df) + 1)

# Convert 'Score' to integer
df['Score'] = df['Score'].astype(float)

# Display the table
print(df)
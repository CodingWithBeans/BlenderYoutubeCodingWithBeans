import time
import pyautogui

# List of actions to replay
actions = [
    ("click", 1354, 48, "left"),
    ("click", 1842, 796, "left"),
    ("click", 997, 1181, "left"),
    ("key", "0"),
    ("key", "enter"),
    ("click", 997, 1181, "right"),
    ("click", 979, 1135, "left"),
    ("click", 1903, 795, "left"),
    ("key", "1"),
    ("key", "enter"),
    ("click", 1002, 1183, "right"),
    ("click", 973, 1140, "left"),
    ("click", 1900, 802, "left"),
    # Repeated clicks at (1900, 802)
] + [("click", 1900, 802, "left")] * 10 + [  # Adding repeated clicks as a list
    ("click", 994, 1173, "right"),
    ("click", 960, 1143, "left"),
    ("click", 1896, 799, "left"),
] + [("click", 1896, 799, "left")] * 20 + [
    ("click", 983, 1183, "right"),
    ("click", 1055, 1072, "left"),
    ("click", 993, 1184, "left"),
    ("key", "0"),
    ("key", "enter"),
    ("click", 993, 1183, "right"),
    ("click", 947, 1147, "left"),
]

# Replay function
def replay_actions():
    print("Starting in 10 seconds...")
    time.sleep(3)  # 10-second delay before executing actions
    print("Replaying actions...")

    for action in actions:
        if action[0] == "key":
            key = action[1]
            if key == "enter":
                pyautogui.press("enter")  # Handle special keys
            else:
                pyautogui.press(key)  # Handle regular characters

        elif action[0] == "click":
            x, y, button = action[1], action[2], action[3]
            pyautogui.click(x=x, y=y, button=button)
        
        time.sleep(0.1)  # Add delay between actions

# Execute the replay
replay_actions()

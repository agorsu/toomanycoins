from nicegui import ui
from collections import Counter

# Coin calculator JPY - NiceGUI

# variables
total_balance = 0
wallet = { # Updated
    1: 0,
    5: 0,
    10: 0,
    50: 0,
    100: 0,
    500: 0
}

def roundup(target):
    coin_counts = [int(wallet[c].value or 0) for c in wallet]
    coins = list(wallet.keys())
    check = [coins[i] for i, n in enumerate(coin_counts) if n > 0]

    if not check:
        return target

    # Exact
    if any(target % c == 0 for c in check):
        return target
    
    remain = target % min(check)
    rounded = target + (min(check) - remain)
    rounding_label.set_text(f"Rounded up value: {rounded}") # updated
    return rounded

def find_combinations(nums, target):
    results = []
    current_combination = []

    def backtrack(start, target):
        if target == 0 and len(list(current_combination)) <= coin_limit.value:
            results.append(list(current_combination))
            return
        
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i-1]:
                continue  # skip duplicates to avoid redundant combinations
            current_combination.append(nums[i])
            backtrack(i + 1, target - nums[i])
            current_combination.pop()

    nums.sort()  # Sort the list to handle duplicates and for early pruning
    backtrack(0, target)
    if results:
        return max(results, key=len)
    return

def reset_inputs():
    for count in wallet.values():
        count.set_value(None)
    total_label.set_text("Total Balance: ¥0") # Updated
    rounding_label.set_text("")
    result_label.set_text("")
    target_value.value = None
    if 'error' in target_value._props:
        target_value.props(remove='error error-message')
    return

def calculate_total():
    global total_balance
    total_balance = sum(int(count.value or 0) * coin for coin, count in wallet.items()) #updated
    total_label.set_text(f"Total Balance: ¥{total_balance}") #updated
    return

def process_action():
    rounding_label.set_text("")
    if target_value.value is None or target_value.value <= 0:
        target_value.props('error error-message="Please enter a valid amount"')
        return

    holdings = total_balance # updated
    cost = int(target_value.value) # updated

    if holdings >= cost and holdings != 0: # updated
        coin_list = []
        for coin, count in wallet.items():
            coin_list.extend([coin] * int(count.value or 0))

        rounded_target = roundup(cost) # updated
        result = find_combinations(coin_list, rounded_target)

        if result:
            counts = Counter(result)
            #counted_result = [f"🪙{coin}c x {count}" if coin < 100 else f"🪙${str(round(coin * 0.01))} x {count}" for coin, count in counts.items()]
            counted_result = [f"🪙¥{coin} x {count}" for coin, count in counts.items()] # updated
            result_label.set_text(f"Result using {len(result)} coins: \n{'\n'.join(counted_result)}")
        else:
            result_label.set_text("No combinations found within limit")
    else:
        result_label.set_text("Insufficient balance")

# UI
with ui.card().classes('rounded-2xl shadow-xl'):
    ui.label('💰 Too Many Coins').classes('text-2xl font-bold mb-4')
    with ui.row():
        for coin in wallet.keys():
            label = f"¥{coin}" # Updated
            number_input = ui.number(label=label, min=0, on_change=calculate_total).classes('w-20')
            wallet[coin] = number_input

    total_label = ui.label('Total Balance: ¥0').classes('text-lg mt-4') # Updated
    
    with ui.row():
        target_value = ui.number(label='Target cost: ¥', min=0) # Updated
        coin_limit = ui.select([10, 20, 30, 50, 100], value=20, label='Coin Limit').classes('w-32 ml-2')
    
    with ui.row():
        ui.button('Calculate', on_click=process_action)
        ui.button('Reset', on_click=reset_inputs)
    
    rounding_label = ui.label('')
    result_label = ui.label('').classes('text-lg').style('white-space: pre-wrap')

# Page setup
ui.page_title('Too Many Coins')
ui.query('body').classes('bg-gray-500')
ui.run(favicon='💰')
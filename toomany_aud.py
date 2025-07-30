from nicegui import ui

# Coin calculator AUD - NiceGUI

# variables
coin_limit = 20
total_balance = 0
wallet = {
    5: 0,
    10: 0,
    20: 0,
    50: 0,
    100: 0,
    200: 0
}

def calculate_total():
    global total_balance
    total_balance = sum(int(count.value) * coin for coin, count in wallet.items()) / 100
    total_label.set_text(f"Total Balance: ${total_balance:.2f}")
    return

def reset_inputs():
    for count in wallet.values():
        count.set_value(0)
    total_label.set_text("Total Balance: $0.00")
    target_value.set_value(0)
    rounding_label.set_text("")
    result_label.set_text("")
    return

def process_action():
    coin_list = []

    def roundup(target_cents):
        exact = True
        check = [coin for coin, count in wallet.items() if int(count.value) > 0]
        exact = any(target_cents % c == 0 for c in check)
        if exact == False:
            remain = target_cents % min(check)
            target_cents = target_cents + (min(check) - remain)
            target_dollars = target_cents / 100
            rounding_label.set_text(f"Rounded up value: {target_dollars:.2f}")
        else:
            target_dollars = target_cents / 100
        return target_dollars
    
    def find_combinations(nums, target):
        results = []
        current_combination = []

        def backtrack(start, target):
            if target == 0:
                if len(list(current_combination)) <= coin_limit:
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
    
    if total_balance >= target_value.value and total_balance != 0:
        rounding_label.set_text("")
        target = roundup(target_value.value * 100)
        for coin, count in wallet.items():
            coin_list.extend([coin] * int(count.value))
        result = find_combinations(coin_list, target * 100)
        if result:
            result_label.set_text(f"Result: {result}")
        else:
            result_label.set_text("No combinations found within limit")
    else:
        rounding_label.set_text("")
        result_label.set_text("Insufficient balance")
    return

with ui.card():
    ui.label('Too Many Coins').classes('text-2xl font-bold mb-4')
    with ui.row():
        for coin in wallet.keys():
            label = f"{coin}c" if coin < 100 else f"${round(coin * 0.01)}"
            number_input = ui.number(label=label, value=0, min=0, on_change=calculate_total).classes('w-20')
            wallet[coin] = number_input

    total_label = ui.label('Total Balance: $0.00').classes('text-lg mt-4')
    target_value = ui.number(label='Target cost: $', precision=2)#.classes('mt-4 w-full')
    
    with ui.row():
        ui.button('Calculate', on_click=process_action)
        ui.button('Reset', on_click=reset_inputs)
    
    rounding_label = ui.label('')
    result_label = ui.label('').classes('text-lg')

ui.run()
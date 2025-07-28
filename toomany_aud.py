from nicegui import ui

# Coin calculator AU - NiceGUI

# variables
coins = [5, 10, 20, 50, 100, 200]
coin_counts = []
coin_limit = 20
total_dollars = 0

def calculate_total():
    global total_dollars
    wallet = [int(input.value) for input in coin_counts]
    total_cents = sum(count * coin for count, coin in zip(wallet, coins))
    total_dollars = total_cents / 100
    total_label.set_text(f"Total Value: ${total_dollars:.2f}")

def process_action():
    # Insert Logic to validate and find_combinations
    print(f"Total value: ${total_dollars:.2f}")
    print(f"Target cost: ${target_value.value:.2f}")
    print(f"Coin counts: {[int(input.value) for input in coin_counts]}")
    return

with ui.card():
    ui.label('Too Many Coins').classes('text-2xl font-bold mb-4')

    with ui.row():
        for coin in coins:
            label = f"{coin}c" if coin < 100 else f"${round(coin * 0.01)}"
            number_input = ui.number(label=label, value=0, min=0, on_change=calculate_total).classes('w-20')
            coin_counts.append(number_input)

    total_label = ui.label('').classes('text-lg mt-4')
    target_value = ui.number(label='Target cost: $', precision=2).classes('mt-4 w-full')
    ui.button('Calculate', on_click=process_action).classes('mt-4 w-full')

ui.run()

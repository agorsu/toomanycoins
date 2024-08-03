# Australian change calc
coins = [5, 10, 20, 50, 100, 200]
coin_counts = []
holdings = 0

#set max number of coins
coin_limit = 20 

# Input the number of each coin
for coin in coins:
    if coin < 100:
        count = int(input(f"How many {coin}c: "))
    else:
        count = int(input(f"How many ${round(coin*0.01)}: "))
    coin_counts.append(count)
    holdings += count * coin

print(f"\nTotal value: ${holdings/100:.2f}")
target_value = float(input("\nEnter the target cost: $"))
target_value = round(target_value*100)
coin_list = []

def roundup(target):
    exact = True
    check = [coins[i] for i, n in enumerate(coin_counts) if n > 0]
    exact = any(target % c == 0 for c in check)
    if exact == False:
        remain = target % min(check)
        target = target + (min(check) - remain)
        print(f"Rounded up value: {target/100:.2f}")
    return target

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

# validation logic
if holdings >= target_value and holdings != 0:
    target_value = roundup(target_value)
    for i, coin in enumerate(coins):
        coin_list.extend([coin] * coin_counts[i])
        coin_counts[i] = 0     
    result = find_combinations(coin_list, target_value)
    if result:
        print(result)
    else:
        print("No combinations found within limit")
else:
    print("Insufficient balance")



def countSubMultisets(nums, l, r):
    MOD = 10**9 + 7
    count = {}
    for num in nums:
        if num in count:
            count[num] += 1
        else: count[num] = 1
    
    zeroFreq = count[0] if 0 in count else 0
    if 0 in count:
        del count[0]
    if not count:
        return (zeroFreq + 1) % MOD
    
    prev = [0] * (r + 1)
    
    num, freq = next(iter(count.items()))
    for i in range(0, r + 1, num):
        if i // num <= freq:
            prev[i] = 1
            
    for num, freq in list(count.items())[1:]:
        cur = [0] * (r + 1)
        for j in range(r + 1):
            if (freq + 1) * num <= j:
                cur[j] = (prev[j] + cur[j-num] - prev[j-(freq+1)*num] + MOD) % MOD
            elif num <= j:
                cur[j] = (prev[j] + cur[j-num]) % MOD
            else:
                for k in range(freq + 1):
                    if j >= k * num:
                        cur[j] = (cur[j] + prev[j-k*num]) % MOD
        prev = cur
    
    ans = sum(prev[i] for i in range(l, r + 1)) % MOD
    
    return (ans * (zeroFreq + 1)) % MOD

nums = [1, 2, 2, 3]
l, r = 6, 6
print(countSubMultisets(nums, l, r))

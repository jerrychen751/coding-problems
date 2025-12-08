sum = 0
i = 1
j = 1
k = 1
while i * 3 < 1000:
    sum += i * 3
    i += 1

while j * 5 < 1000:
    sum += j * 5
    j += 1

while k < 1000:
    if k * 3 * 5 < 1000:
        sum -= k * 3 * 5
        k += 1
    else:
        break

print(sum)
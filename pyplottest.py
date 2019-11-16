import matplotlib.pyplot as plt
plt.plot([1, 2, 3, 4])
plt.ylabel('some numbers')
ax = plt.gca()
line = ax.lines[0]
x, y = line.get_xdata(), line.get_ydata()

print(x)
print(y)
plt.show()

import matplotlib.pyplot as plt

'''
# Data from the table
queue_size = [9, 10, 15, 20, 25, 30, 51]
cubic_foreground_cubic_background = [559.5099109, 541.7403159, 540.222469, 528.1685298, 536.9735758, 545.0030641, 536.2077304]
bbr_foreground_cubic_background = [309.8432251, 320.5457065, 372.5203479, 426.4771655, 544.4934559, 576.1290583, 581.3673974]
cubic_foreground_bbr_background = [2162.988263, 1711.150675, 957.0517333, 715.3228431, 518.3625369, 492.1930896, 492.1769663]
bbr_foreground_bbr_background = [559.8454441, 559.4517423, 567.8361899, 563.7910829, 546.6452424, 547.094318, 536.3822094]
'''
queue_size = [9, 10, 15, 20, 25, 30, 51]
cubic_foreground_cubic_background = [214.4734127, 221.5083435, 222.1307089, 227.2002083, 223.4746837, 220.1822483, 223.7938642]
bbr_foreground_cubic_background = [387.2926379, 374.3615889, 322.1300546, 281.3749708, 220.3883237, 208.2866647, 206.4099235]
cubic_foreground_bbr_background = [55.47880313, 70.12824863, 125.3850715, 167.756421, 231.4982111, 243.806755, 243.8147419]
bbr_foreground_bbr_background = [214.3448719, 214.4957124, 211.3285524, 212.8447995, 219.5207983, 219.3406073, 223.7210666]

# Plotting the data
plt.figure(figsize=(10, 6))

plt.plot(queue_size, cubic_foreground_cubic_background, label="CUBIC_foreground (CUBIC background)", marker='o')
plt.plot(queue_size, bbr_foreground_cubic_background, label="BBR_foreground (CUBIC background)", marker='o')
plt.plot(queue_size, cubic_foreground_bbr_background, label="CUBIC_foreground (BBR background)", marker='o')
plt.plot(queue_size, bbr_foreground_bbr_background, label="BBR_foreground (BBR background)", marker='o')

# Adding titles and labels
plt.title("Queue Size vs Affective bandwidth")
plt.xlabel("Queue Size (Mb)")
plt.ylabel("Affective bandwidth (Mbps)")
plt.legend()
plt.grid(True)
plt.show()


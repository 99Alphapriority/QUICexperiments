import matplotlib.pyplot as plt
import numpy as np

queue_size = [0.1, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 7, 7.5, 8.5, 10, 11, 12.5, 15, 17.5, 20, 50]
bbr_stddev = [6.456321355, 4.353455952, 6.275740919, 6.209071385, 5.137759249, 4.251322661, 4.272287863, 2.244592702, 5.265781273, 3.242738216, 4.556965397, 4.352478635, 3.595827959, 5.041797729, 4.298905624, 5.740436866, 4.160343231, 4.011161483, 4.563776688, 2.629211848, 4.079434, 3.54080878, 5.465449524]
cubic_stddev = [2.596971183, 4.071345222, 6.509335382, 6.375678734, 5.217757832, 4.325407828, 4.370844994, 2.413998348, 5.46990728, 3.682981395, 4.536024276, 4.721216748, 3.281413236, 5.430678181, 4.138263353, 5.75305327, 4.478938953, 4.407544555, 4.707815156, 2.745693407, 3.794859225, 3.383590643, 5.412415719]
# Plotting the data

custom_label_x = ['0.04*BDP(0.1)','0.2*DBP(0.5)','0.4*BDP(1)','0.6*BDP(1.5)','0.8*BDP(2)','1*BDP(2.5)', '1.2*BDP(3)','1.4*BDP(3.5)','1.6*BDP(4)','1.8*BDP(4.5)','2*BDP(5)','2.2*BDP(5.5)','2.4*BDP(6)','2.8*BDP(7)','3*BDP(7.5)','3.4*BDP(8.5)','4*BDP(10)','4.4*BDP(11)','5*DBP(12.5)','6*BDP(15)','7*BDP(17.5)','8*BDP(20)','20*BDP(50)']

x = np.arange(len(queue_size))  # Label locations
width = 0.35  # Width of the bars

fig, ax = plt.subplots(figsize=(12,6))
bars1 = ax.bar(x - width/2, bbr_stddev, width, label='BBR_foreground (CUBIC Background) stddev')
bars2 = ax.bar(x + width/2, cubic_stddev, width, label='CUBIC_foreground (bbr Background) stddev')

ax.set_xlabel('Queue Size')
ax.set_ylabel('Standard Deviation')
ax.set_title('Standard Deviation [mininet][10 runs x 10 mins][Average of last 8 runs]')
ax.set_xticks(x)
ax.set_xticklabels(custom_label_x, rotation=90)
ax.legend()
plt.grid(True)
plt.tight_layout()
plt.show()



'''
plt.xscale('log')
plt.xticks(ticks=queue_size, labels=custom_label_x, rotation=90)
plt.yticks(ticks=custom_label_y)

# Adding titles and labels
plt.title("Queue Size vs bandwidth [mininet][10 runs X 10 mins][Average of last 8 runs] (BDP=2.5MB/Bandwidth=1000Mbps/RTT=20ms)")
plt.xlabel("Queue Size (MB)")
plt.ylabel("Bandwidth (Mbps)")
plt.legend()
plt.grid(True)
plt.tight_layout()
#plt.xlim([queue_size[0], queue_size[-1]])
plt.show()
'''

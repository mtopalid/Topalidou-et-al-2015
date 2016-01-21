import numpy as np
from matplotlib import lines
import matplotlib.pyplot as plt


dpi = 50
# Model
D1_mean, D1_std = (0.4828, 0.4996), (0.06135, 0.05227)
D2_mean, D2_std = (0.9792, 1.0000), (0.01695, 0.00001)
D3_mean, D3_std = (0.8844, 0.8892), (0.02624, 0.03110)
# Monkeys
#D1_mean, D1_std = (0.36, 0.41), (0.05, 0.05)
#D2_mean, D2_std = (0.97, 0.97), (0.01, 0.01)
fig = plt.figure(figsize=(6,5), facecolor="w", dpi=dpi)
ax = plt.subplot(111)

ax.tick_params(axis='both', which='major', labelsize=8)

ax.xaxis.set_tick_params(size=0)
ax.yaxis.set_tick_params(width=1)

index = np.array([0,1])
width = 1
color = 'r'

# Pull the formatting out here
bar_kw = {'width': 0.95, 'linewidth':0, 'zorder':5}
err_kw = {'zorder': 10, 'fmt':'none', 'linewidth':0, 'elinewidth':1, 'ecolor':'k'}

def plot(X, mean, sigma, color, alpha):
    plt.bar(X, mean, alpha=alpha, color=color, **bar_kw)
    _,caps,_ = plt.errorbar(X+width/2.0, mean, sigma, **err_kw)
    for cap in caps: cap.set_markeredgewidth(1)

plot(index-width+0.0, D1_mean, D1_std, 'r', 0.45)
plot(index-width+2.5, D2_mean, D2_std, 'b', 0.45)
plot(index-width+5.0, D3_mean, D3_std, 'r', 0.45)

plt.xlim(-1.5,+6.5)
plt.xticks([-0.5,0.0,0.5, 2.0, 2.5, 3.0, 4.5, 5.0, 5.5],
           ["25 first\ntrials","\n\n\nDay 1 (GPi OFF)\n","25 last\ntrials",
            "25 first\ntrials","\n\n\nDay 2 (GPi ON)\n","25 last\ntrials",
            "25 first\ntrials","\n\n\nDay 3 (GPi OFF)\n","25 last\ntrials"])
# plt.xticks([-0.5,0.0,0.5, 2.0, 2.5, 3.0, 4.5, 5.0, 5.5],
#            ["25 first\ntrials","\n\n\nDay 1 (Muscimol)\n","25 last\ntrials",
#             "25 first\ntrials","\n\n\nDay 2 (Saline)\n","25 last\ntrials",
#             "25 first\ntrials","\n\n\nDay 3 (GPi OFF)\n","25 last\ntrials"])
plt.ylim(0.0,1.2)
plt.ylabel("Ratio of optimum trials")
plt.yticks([0,.25,.5,.75,1.0])

ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data',0))
ax.yaxis.set_ticks_position('left')

x,y = np.array([[-1.05, 1.0], [-0.1, -0.1]])

ax.add_line(lines.Line2D(x+0.0, y, lw=.5, color='k', clip_on=False))
ax.add_line(lines.Line2D(x+2.5, y, lw=.5, color='k', clip_on=False))
ax.add_line(lines.Line2D(x+5.0, y, lw=.5, color='k', clip_on=False))

x,y = np.array([[-1.05, 1.0], [1.05, 1.05]])
ax.add_line(lines.Line2D(x+0.0, y, lw=.5, color='k', clip_on=False))
ax.add_line(lines.Line2D(x+2.5, y, lw=.5, color='k', clip_on=False))
ax.add_line(lines.Line2D(x+5.0, y, lw=.5, color='k', clip_on=False))

ax.text(0.0, 1.065, "Value acquisition", ha="center", va="bottom", fontsize=8)
ax.text(2.5, 1.065, "Habit acquisition", ha="center", va="bottom", fontsize=8)
ax.text(5.0, 1.065, "Habit expression",  ha="center", va="bottom", fontsize=8)

plt.title("Theoretical results (model)")
#plt.title("Experimental results (monkey)")

# Custom function to draw the diff bars
# http://stackoverflow.com/questions/11517986/...
# ...indicating-the-statistically-significant-difference-in-bar-graph
# def label_diff(X1, X2, Y, text):
#     x = (X1+X2)/2.0
#     y = 1.15*Y
#     props = {'connectionstyle':'bar','arrowstyle':'-',\
#              'shrinkA':10,'shrinkB':10,'lw':1}
#     ax.annotate(text, xy=((X2+X1)/2., y+0.1), zorder=10, ha='center')
#     ax.annotate('', xy=(X1,y), xytext=(X2,y), arrowprops=props)
# label_diff(-0.5,0.5, 0.85, '***')
# label_diff( 2.0,3.0, 0.85, '***')

plt.tight_layout(pad=0)
plt.savefig("habits-mode.pdf", dpi=dpi)
#plt.show()

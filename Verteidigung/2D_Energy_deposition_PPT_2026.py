import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import cm
import matplotlib.cbook as cbook
import matplotlib.colors as colors

sns.set_style("white")
fig, ax = plt.subplots(figsize=(8, 6))
# Dataset
df = pd.read_csv('Scorer_1.csv')
x = df['X']
y = df['Y']

#x = np.arange(0,30,1)
#y = np.arange(0,30,1)
#X,Y = np.meshgrid(x, y)
Z = df['Edep']
# create figure
cw=ax.scatter(x,y, c=Z+0.0001, s= 200,marker='s', norm=colors.LogNorm(), cmap='viridis', edgecolors='none')
#cw=ax.scatter(x,y, c=Z, s= 200,marker='s',norm=divnorm, cmap='plasma', edgecolors='none')
#cw=ax.scatter(x,y, c=Z, s= 200,marker='s', norm=colors.CenteredNorm(),cmap='coolwarm', edgecolors='none')
ax.set_xlabel("X / µm",fontsize=12)
ax.set_ylabel("Y / µm",fontsize=12)
ax.set_xticks([-4.5,25,50,75,100,125,150,175,200])
ax.set_xticklabels([0,0.125,0.25,0.375,0.5,0.625,0.75,0.875,1.0],fontsize=12)
ax.set_yticks([0,25,50,75,100,125,150,175,200])
ax.set_yticklabels([-0.5,-0.375,-0.25,-0.125,0.0,0.125,0.25,0.375,0.5],fontsize=12)

ax.set_xlim(-4.5, 200)
ax.set_ylim(0, 200)
cbar=plt.colorbar(cw)
cbar.set_label('Edep / MeV',fontsize=12)
#cbar.set_ticks([0, 0.25, 2])
#plt.show()
plt.savefig("2D_Energy_deposition_ppt.png", dpi=300,bbox_inches='tight')
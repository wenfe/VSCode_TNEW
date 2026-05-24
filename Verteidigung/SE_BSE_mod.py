import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy.constants as sc
import math
import seaborn as sns
import pandas as pd
import seaborn.objects as so
sns.set_theme(style='ticks')


#df = pd.read_csv("SE_20241019.csv")
df = pd.read_csv("SE_20240807.csv")
df.columns = df.columns.str.strip()
for count_column in ["SE/counts", "Primary/counts"]:
	max_count = df[count_column].max()
	if max_count != 0:
		df[count_column] = df[count_column] / max_count
#sns.scatterplot('energy','depth',data=df)

fig, ax1 = plt.subplots()
#ax1 = sns.lineplot(x='Energy/keV',y='SE/counts',data=df[(df['Energy/keV']<41)],color='salmon',linewidth=1,label='Secondary Electrons')
ax1 = sns.lineplot(x='Energy/keV',y='SE/counts',data=df[(df['Energy/keV']<151)],color='salmon',linewidth=1,label='Secondary Electrons')
ax1.stackplot(df["Energy/keV"], df["SE/counts"], alpha=0.2,color="salmon") 


ax1.set_xlabel('Electron Energy / keV')
ax1.set_ylabel('Normalized counts / a.u.')
ax1.tick_params(axis="y", labelcolor="salmon")


ax1.set_ylabel("Normalized counts / a.u.", color="salmon")  
ax1.grid(axis = "x")

ax2 = ax1.twinx() 

ax2 = sns.lineplot(x='Energy_BSE/keV',y='Primary/counts',data=df[(df['Energy/keV']>149)],color='royalblue',linewidth=1,label='Deflected Primary Electrons')
ax2.stackplot(df["Energy_BSE/keV"], df["Primary/counts"], alpha=0.2,color="royalblue") 
 
ax2.set_xlim(-1,301)
ax2.set_ylim(0,1.05)
ax2.set_ylabel("Normalized counts / a.u.", color="royalblue")  
ax2.tick_params(axis="y", labelcolor="royalblue")

handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(
	handles1,
	labels1,
	loc='upper left',
	frameon=True,
	framealpha=0.85,
)
ax2.legend(
	handles2,
	labels2,
	loc='upper right',
	frameon=True,
	framealpha=0.85,
)
fig.tight_layout()

#plt.show()
plt.savefig("SE_BSE_20260427.png", dpi=300,bbox_inches='tight')
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 18:25:40 2021

@author: Matt
"""

from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.projections import get_projection_class
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch
import matplotlib

#All League Matches
df1 = pd.read_csv("EVE_GW1.csv")
df2 = pd.read_csv("SOU_GW2.csv")
df3 = pd.read_csv("NEW_GW3.csv")
df4 = pd.read_csv("UTD_GW4.csv")
df5 = pd.read_csv("WHU_GW5.csv")
df6 = pd.read_csv("BUR_GW6.csv")
df7 = pd.read_csv("BHA_GW7.csv")
df8 = pd.read_csv("WBA_GW8.csv")
df9 = pd.read_csv("MCI_GW9.csv")
df10 = pd.read_csv("CHE_GW10.csv")
df11 = pd.read_csv("ARS_GW11.csv")
df12 = pd.read_csv("CRY_GW12.csv")
df13 = pd.read_csv("LIV_GW13.csv")
df14 = pd.read_csv("LEI_GW14.csv")
df15 = pd.read_csv("WOL_GW15.csv")
df16 = pd.read_csv("LEE_GW16.csv")
df17 = pd.read_csv("FUL_GW17.csv")
df18 = pd.read_csv("SHU_GW18.csv")
df19 = pd.read_csv("LIV_GW19.csv")
df20 = pd.read_csv("BHA_GW20.csv")
df21 = pd.read_csv("CHE_GW21.csv")
df22 = pd.read_csv("WBA_GW22.csv")

#Combining Dataframes
all_gw = [df1,df2,df3,df4,df5,df6,df7,df8,df9,df10,df11,df12,df13,df14,df15,
          df16,df17,df18,df19,df20,df21,df22]
df = pd.concat(all_gw)

#Filter Pass
df=df[((df['type/value']==1) & (df['outcomeType/value']==1))]

#Set cmap
cmap = plt.cm.get_cmap('cool')

#Angle Multiplier
multiplier = 2*np.pi/24

def get_angle(val):
    x1, y1, x2, y2 = val
    dx = x2 - x1
    dy = y2 - y1
    result = np.arctan2(dy, dx)
    return result if result>=0 else result + 2*np.pi

df['length'] = np.sqrt(np.square(df["x"] - df["endX"]) + np.square(df["y"] - df["endY"]))
df['angle'] = df[['x', 'y', 'endX', 'endY']].apply(get_angle, axis=1)
df['angle_bin'] = pd.cut(df['angle'], bins=np.linspace(0, 2*np.pi, 25), right=True, labels=False)
pdf = df.groupby(['playerId', 'angle_bin']).agg(count = ('angle_bin', 'count'), avg_length = ('length', 'mean')).reset_index()

#Locations of Players
player_loc_dict = { 83532: (90, 50), ##KANE
                    321389 : (75, 50), ##NDOMBELE
                    91909 : (75, 80), ##SON
                    279425 : (75, 20), ##BERGWIJN
                    29595 : (55, 35), ##SISSOKO
                    101859 : (55, 65), ##HOJBJERG
                    362275 : (40, 85), ##REGUILON
                    117973 : (30, 65), ##DIER
                    69933 : (30, 35), ##ALDERWEIRELD
                    83683 : (40, 15), ##AURIER
                    25604 : (10, 50) ##LLORIS
                  }

def plot_inset(width, ax, pdf, x, y):
    ax_sub = inset_axes(ax, width=width, height=width, loc=10,
                       bbox_to_anchor=(x,y), bbox_transform=ax.transData, 
                       borderpad=0.0, axes_class=get_projection_class("polar"))
    colors = cmap(pdf['count']/pdf['count'].max())
    bars = ax_sub.bar(pdf['angle_bin']*multiplier, pdf['avg_length'], width=0.2, bottom=0, 
                      alpha=0.9, 
                      color=colors, zorder=3)
    ax_sub.set_xticklabels([])
    ax_sub.set_yticks([])
    ax_sub.grid(False)
    ax_sub.spines['polar'].set_visible(False)
    ax_sub.patch.set_alpha(0)
    return ax

#Font
matplotlib.font_manager._rebuild()
plt.rcParams['font.family'] = 'Myriad Pro'
colour = '#132257'
plt.rcParams['text.color'] = colour

fig, ax = plt.subplots()
fig.set_facecolor('#F8F8FF')
fig.patch.set_facecolor('#F8F8FF')
pitch = Pitch(pitch_type='opta', orientation='horizontal',
              pitch_color='#F8F8FF', line_color='#C0CEFF',
              constrained_layout=True, tight_layout=False,
              line_zorder=1, linewidth=0.5)
pitch.draw(ax=ax)
plt.text(0,108,"Tottenham Hotspur Pass Sonars", 
             fontsize=14, fontweight = 'bold')
plt.text(0,102,"Premier League 2020-21 | @trevillion_", 
             fontsize=10)
plt.text(1,2,"Colour = Frequency (Pink = More; Blue = Less)\nLength = Average Length of Pass\nDirection = Pass Direction",
               fontsize=5, alpha=0.5, zorder=1)
plt.text(1,97,"Players With Most Minutes In Each Position",
               fontsize=5, alpha=0.5, zorder=1)
plt.text(72,2,"Inspired by Eliot McKinley (@etmckinley)\n     & Abhishek Sharma (@abhisheksh_98)",
               fontsize=5, alpha=0.5, zorder=1)
plt.text(9,57,"LLORIS", fontsize=6)
plt.text(37,26,"AURIER", fontsize=6)
plt.text(24,46,"ALDERWEIRELD", fontsize=6)
plt.text(28,75,"DIER", fontsize=6)
plt.text(36,95,"REGUILÓN", fontsize=6)
plt.text(51,77,"HØJBJERG", fontsize=6)
plt.text(52,47,"SISSOKO", fontsize=6)
plt.text(73,91,"SON", fontsize=6)
plt.text(71,61,"NDOMBELE", fontsize=6)
plt.text(71,30,"BERGWIJN", fontsize=6)
plt.text(89,60,"KANE", fontsize=6)
for player_id, (x,y) in player_loc_dict.items():
    player_df = pdf.query("playerId == @player_id")
    plot_inset(0.6, ax, player_df, x, y)
plt.savefig('C:/Users/Matt/Documents/Football Data/matplotlib/Tottenham/Sissoko/Premier League Matches/PassSonars.png', 
            dpi=500, bbox_inches="tight",facecolor='#F8F8FF')
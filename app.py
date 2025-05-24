import streamlit as st
import pandas as pd
from mplsoccer import VerticalPitch
import matplotlib.pyplot as plt

st.title("La Liga 24-25")
st.subheader("Filter to any team/player to see all of their shots taken")

liga25 = pd.read_csv("LaLiga2024.csv")
liga25["X"] = liga25["X"] * 100
liga25["Y"] = liga25["Y"] * 100

print(liga25)


team = st.selectbox('Select a Team', liga25["team"].sort_values().unique(), index = None)
player = st.selectbox('Select a Player', liga25[liga25["team"] == team]["player"].sort_values().unique(), index = None)

def filter_data(df, team, player):
    if team:
        df = df[df["team"] == team]

    if player:
        df = df[df["player"] == player]
        
    return df

filtered_df = filter_data(liga25, team, player)

def shotmap(df):

    if df["player"].nunique() > 1:
        name = df["team"].unique()
    else:
        name = df["player"].unique()
        # team = df["team"].unique()
    
    total_shots = df.shape[0]
    total_goals = df[df['result'] == "Goal"].shape[0]
    total_xg = round(df["xG"].sum(),1)
    xg_pershot = round(total_xg / total_shots, 3)
    avg_goal_dist = f"{round(120 - (df[df["result"] == "Goal"]["X"].mean() * 1.2),2)} yards"
    dist_plot = df["X"].mean()
    avg_distance_yards = 120 - (df["X"] * 1.20).mean()
    max_shot_assists_player = df["player_assisted"].value_counts().idxmax()
    max_shot_assists_value = df["player_assisted"].value_counts().max()

    bg_color =  '#00477a'
    text_color = "#ffd7b9"
    goal_fill = "#d3af37"



    #figure
    fig = plt.figure(figsize=(8,12))
    fig.patch.set_facecolor(bg_color)

    #axes
    ax1 = fig.add_axes([0, .7, 1, .2])
    ax1.set_facecolor(bg_color)
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.axis("off")

    ax1.text(
        x = 0.5, y = 0.85,
        s=name[0],
        fontsize = 20,
        fontweight = "bold",
        color = text_color,
        ha = "center"
    )

    ax1.text(
        x = 0.5, y = 0.70,
        s="All shots in the La Liga 2024-25",
        fontsize = 14,
        fontweight = "bold",
        color = text_color,
        ha = "center"
    )

    ax1.text(
        x = 0.25, y = 0.5,
        s="Low Quality Chance",
        fontsize = 12,
        fontweight = "bold",
        color = text_color,
        ha = "center"
    )
    
    ax1.scatter(
    x = 0.39, 
    y = .53,
    s = 100,
    color = bg_color,
    edgecolor = text_color,
    linewidth = 0.8
    )

    ax1.scatter(
    x = 0.44, 
    y = .53,
    s = 200,
    color = bg_color,
    edgecolor = text_color,
    linewidth = 0.8
    )

    ax1.scatter(
    x = 0.49, 
    y = .53,
    s = 300,
    color = bg_color,
    edgecolor = text_color,
    linewidth = 0.8
    )

    ax1.scatter(
    x = 0.54, 
    y = .53,
    s = 400,
    color = bg_color,
    edgecolor = text_color,
    linewidth = 0.8
    )

    ax1.scatter(
    x = 0.59, 
    y = .53,
    s = 500,
    color = bg_color,
    edgecolor = text_color,
    linewidth = 0.8
    )
    

    ax1.text(
        x = 0.75, y = 0.5,
        s="High Quality Chance",
        fontsize = 12,
        fontweight = "bold",
        color = text_color,
        ha = "center"
    )




    ax1.text(
        x = 0.40, y = 0.3,
        s="Goal",
        fontsize = 12,
        fontweight = "bold",
        color = text_color,
        ha = "center"
    )

    ax1.scatter(
        x = 0.35, 
        y = 0.32,
        s = 200,
        color = goal_fill,
        alpha = 0.9,
        edgecolor = text_color,
        linewidth = 0.8
        )



    ax1.text(
        x = 0.57, y = 0.3,
        s="No Goal",
        fontsize = 12,
        fontweight = "bold",
        color = text_color,
        ha = "center"
    )

    ax1.scatter(
        x = 0.5, 
        y = 0.32,
        s = 200,
        color = bg_color,
        edgecolor = text_color,
        linewidth = 0.8
        )



    #Section 2

    ax2 = fig.add_axes([0.05, 0.3, 0.8, 0.4])
    ax2.set_facecolor(bg_color)
    ax2.axis("off")

    pitch = VerticalPitch(
        pitch_type = "opta",
        half = True,
        pitch_color = bg_color,
        pad_bottom = .2,
        line_color = text_color,
        linewidth = 0.75,
        goal_type = "box"
    )
    
    
    ax4 = fig.add_axes([0.9, 0.3, 0.2, 0.4])
    ax4.set_facecolor(bg_color)

    
    ax4.text(x=0.3, y=0.9, s="Shots", fontsize=15, fontweight="bold", color=text_color, ha="center")
    ax4.text(x=0.3, y=0.85, s=f"{total_shots}", fontsize=12, fontweight="bold", color=goal_fill, ha="center", alpha=1)

    
    ax4.text(x=0.3, y=0.7, s="xG per shot", fontsize=15, fontweight="bold", color=text_color, ha="center")
    ax4.text(x=0.3, y=0.65, s=f"{xg_pershot}", fontsize=12, fontweight="bold", color=goal_fill, ha="center", alpha=1)
    ax4.axis("off")

    
    ax4.text(x=0.3, y=0.45, s="Average\nGoal Distance", fontsize=15, fontweight="bold", color=text_color, ha="center")
    ax4.text(x=0.3, y=0.4, s=f"{avg_goal_dist}", fontsize=12, fontweight="bold", color=goal_fill, ha="center", alpha=1)
    ax4.axis("off")

    
    ax4.text(x=0.3, y=0.2, s="Maximum\nShot Assists", fontsize=15, fontweight="bold", color=text_color, ha="center")
    ax4.text(x=0.3, y=0.15, s=f"{max_shot_assists_player} : {max_shot_assists_value}", fontsize=12, fontweight="bold", color=goal_fill, ha="center", alpha=1)
    ax4.axis("off")



    pitch.draw(ax=ax2)

    ax2.scatter(x=90, y= dist_plot,
                s = 100, color = text_color, linewidth = 0.8)

    ax2.plot([90, 90], [100, dist_plot], color = text_color, linewidth = 2)
    ax2.text(x = 90, y = dist_plot - 5.5, ha = "center",
            s = f"Average\ndistance: \n{round(avg_distance_yards, 1)} yards",
            size=10, color = text_color, fontweight = "bold")


    for x in df.to_dict(orient = "records"):
        pitch.scatter(
            x['X'],
            x['Y'],
            s = 300 * x['xG'],
            color= goal_fill if x["result"] == "Goal" else bg_color,
            ax=ax2, alpha = 0.9, linewidth = 0.8,
            edgecolor = text_color
        )


    ax3 = fig.add_axes([0, 0.2, 1, 0.05])
    ax3.axis("off")
    ax3.set_facecolor(bg_color)


    ax3.text(x=0.25, y=0.85, s="Goals", fontsize=15, fontweight="bold", color=text_color, ha="center")
    ax3.text(x=0.25, y=0.5, s=f"{total_goals}", fontsize=12, fontweight="bold", color=goal_fill, ha="center", alpha=1)

    ax3.text(x=0.5, y=0.85, s="xG", fontsize=15, fontweight="bold", color=text_color, ha="center")
    ax3.text(x=0.5, y=0.5, s=f"{total_xg}", fontsize=12, fontweight="bold", color=goal_fill, ha="center", alpha=1)

    ax3.text(x=0.75, y=0.85, s="Scoring efficiency", fontsize=15, fontweight="bold", color=text_color, ha="center")
    ax3.text(x=0.75, y=0.5, s=f"{round(total_goals / total_xg * 100, 2)} %", fontsize=12, fontweight="bold", color=goal_fill, ha="center", alpha=1)



    st.pyplot(fig)


shotmap(filtered_df)






import streamlit as st
import pandas as pd
from mplsoccer import VerticalPitch
import matplotlib.pyplot as plt

st.title("La Liga 24-25")
st.subheader("Filter to any team/player to see all of their shots taken")

liga25 = pd.read_csv("LaLiga2024_25.csv")
liga25["X"] = liga25["X"] * 100
liga25["Y"] = liga25["Y"] * 100

print(liga25)

player = st.selectbox('Select a Player', liga25["player"].sort_values().unique(), index = None)

def filter_data(df, player):
    if player:
        df = df[df["player"] == player]
    
    return df

filtered_df = filter_data(liga25, player)

def shotmap(df):
    name = df["player"].unique()
    total_shots = df.shape[0]
    total_goals = df[df['result'] == "Goal"].shape[0]
    total_xg = round(df["xG"].sum(),1)
    xg_per_shot = total_xg / total_shots
    dist_plot = df["X"].mean()
    avg_distance_yards = 120 - (df["X"] * 1.20).mean()

    bg_color =  '#0C0D0E'

    #figure
    fig = plt.figure(figsize=(8,12))
    fig.patch.set_facecolor(bg_color)

    #axes
    ax1 = fig.add_axes([0, .7, 1, .2])
    ax1.set_facecolor(bg_color)
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)

    ax1.text(
        x = 0.5, y = 0.85,
        s=name[0],
        fontsize = 20,
        fontweight = "bold",
        color = "white",
        ha = "center"
    )

    ax1.text(
        x = 0.5, y = 0.70,
        s="All shots in the La Liga 2024-25",
        fontsize = 14,
        fontweight = "bold",
        color = "white",
        ha = "center"
    )

    ax1.text(
        x = 0.25, y = 0.5,
        s="Low Quality Chance",
        fontsize = 12,
        fontweight = "bold",
        color = "white",
        ha = "center"
    )

    points = [0.39, 0.44, 0.49, 0.54, 0.59]
    s = 0

    for x in points:
        ax1.scatter(
        x = x, 
        y = .53,
        s = s + 100,
        color = bg_color,
        edgecolor = "white",
        linewidth = 0.8
        )

    ax1.text(
        x = 0.75, y = 0.5,
        s="High Quality Chance",
        fontsize = 12,
        fontweight = "bold",
        color = "white",
        ha = "center"
    )




    ax1.text(
        x = 0.40, y = 0.3,
        s="Goal",
        fontsize = 12,
        fontweight = "bold",
        color = "white",
        ha = "center"
    )

    ax1.scatter(
        x = 0.35, 
        y = 0.32,
        s = 200,
        color = "red",
        alpha = 0.7,
        edgecolor = "white",
        linewidth = 0.8
        )



    ax1.text(
        x = 0.57, y = 0.3,
        s="No Goal",
        fontsize = 12,
        fontweight = "bold",
        color = "white",
        ha = "center"
    )

    ax1.scatter(
        x = 0.5, 
        y = 0.32,
        s = 200,
        color = bg_color,
        edgecolor = "white",
        linewidth = 0.8
        )



    #Section 2

    ax2 = fig.add_axes([0.05, 0.25, 0.9, 0.5])
    ax2.set_facecolor(bg_color)

    pitch = VerticalPitch(
        pitch_type = "opta",
        half = True,
        pitch_color = bg_color,
        pad_bottom = .2,
        line_color = "white",
        linewidth = 0.75,
        axis = True,
        label = True,
        goal_type = "box"
    )


    pitch.draw(ax=ax2)

    ax2.scatter(x=90, y= dist_plot,
                s = 100, color = "white", linewidth = 0.8)

    ax2.plot([90, 90], [100, dist_plot], color = "white", linewidth = 2)
    ax2.text(x = 90, y = dist_plot - 5.5, ha = "center",
            s = f"Average\ndistance: \n{round(avg_distance_yards, 1)} yards",
            size=10, color = "white", fontweight = "bold")


    for x in df.to_dict(orient = "records"):
        pitch.scatter(
            x['X'],
            x['Y'],
            s = 300 * x['xG'],
            color= "red" if x["result"] == "Goal" else bg_color,
            ax=ax2, alpha = 0.7, linewidth = 0.8,
            edgecolor = "white"
        )


    ax3 = fig.add_axes([0, 0.2, 1, 0.05])
    ax3.set_facecolor(bg_color)

    ax3.text(x=0.25, y=0.5, s="Shots", fontsize=15, fontweight="bold", color="white", ha="center")
    ax3.text(x=0.25, y=0.2, s=f"{total_shots}", fontsize=12, fontweight="bold", color="red", ha="center", alpha=0.7)

    ax3.text(x=0.50, y=0.5, s="Goals", fontsize=15, fontweight="bold", color="white", ha="center")
    ax3.text(x=0.5, y=0.2, s=f"{total_goals}", fontsize=12, fontweight="bold", color="red", ha="center", alpha=0.7)

    ax3.text(x=0.75, y=0.5, s="xG", fontsize=15, fontweight="bold", color="white", ha="center")
    ax3.text(x=0.75, y=0.2, s=f"{total_xg}", fontsize=12, fontweight="bold", color="red", ha="center", alpha=0.7)

    st.pyplot(fig)


shotmap(filtered_df)






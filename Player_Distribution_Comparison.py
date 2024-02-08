# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 11:14:42 2024

@author: salvarezbarb
"""

import streamlit as st 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.patches as patches 
import seaborn as sns 

import pickle 
from pathlib import Path 

import streamlit_authenticator as stauth

st. set_page_config(layout="wide")

# -------------------

names = ["Chelsea FC"]
usernames = ["BlueStreamDataAnalytics"]

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)
    
credentials = {
    "usernames":{
        usernames[0]:{
            "name":names[0],
            "password":hashed_passwords[0]
            },           
        }
    }
    
authenticator = stauth.Authenticate(credentials, "Player_distributions", "}a=^N6kR8;18", cookie_expiry_days=30.0)
    
name, authentication_status, username = authenticator.login()

if authentication_status == False:
    st.error("Username/password is incorrect")
    
if authentication_status == None:
    st.warning("Please enter your username and password")
    
if authentication_status:
    
# ------------------------

    st.title("PLAYER COMPARISON")
    st.write("With this app you're able to compare **two players** on a set of **10 different variables**")
    
    st.sidebar.header("INPUT PARAMETERS")
    
    def user_input_features():
        p1 = st.sidebar.number_input("Player 1 ID", value = 465920, placeholder = "Insert ID number...")
        p2 = st.sidebar.number_input("Player 2 ID", value = 538980, placeholder = "Insert ID number...")
        return p1,p2
    
    p1,p2, = user_input_features()
    
    st.subheader("PLAYER IDS")
    st.write("Player 1 ID: ", p1, "Player 2 ID:", p2)
    
    df = pd.read_csv("CentreForward_AllMeasures_Random.csv")
    
    # Filtering out columns
    df = df.iloc[:,:23]
    
    # Filtering out columns again
    #df.drop(columns = ['Transfermarkt ID', 'playerId', 'SkillCornerID', 'Position',
    #       'Winger Player Score', 'GM', 'Min', 'Age'], axis = 1, inplace = True)
    
    # Renaming to get rid of the PC1
    df.rename(columns={'Speed PC1':"Speed", 'Dynamic Movement/Acceleration PC1':"Dynamic Movement/Acceleration", 'Attacking Runs PC1':"Attacking Runs",
           'Creation PC1':"Creation", 'Goals PC1':"Goals", 'Ball Carrying PC1':"Ball Carrying", 'BTL PC1':"BTL",
           'Pressing PC1':"Pressing", '1v1 Att PC1':"1v1 Att", 'Aerial Presence PC1':"Aerial Presence"}, inplace = True)
    
    df_filter = df[(df["optaPersonId"]==p1) | (df["optaPersonId"] == p2)]
    
    st.subheader("TABLE PREVIEW")
    st.table(df_filter)
    
    st.subheader("DISTRIBUTION PLOTS")
    
    
    player1_name = df[df["optaPersonId"] == p1]["firstName"].tolist()[0] + " " + df[df["optaPersonId"] == p1]["lastName"].tolist()[0] 
    player2_name = df[df["optaPersonId"] == p2]["firstName"].tolist()[0] + " " + df[df["optaPersonId"] == p2]["lastName"].tolist()[0]
    
    num_bins = 20
    
    # Creating a 2x2 subplot grid
    fig, axs = plt.subplots(2, 5, figsize=(16, 8))
    
    # fig.suptitle(str(player1_name) + " vs. " + str(player2_name), fontsize=30)
    
    fig.text(0.01,0.80,player1_name, fontsize=14)
    fig.text(0.01,0.65,player2_name, fontsize=14)
    
    fig.text(0.01,0.35,player1_name, fontsize=14)
    fig.text(0.01,0.20,player2_name, fontsize=14)
    
    # ------------------------------------------------------------------------------------------
    
    variable = df.columns[3]
    var = df[variable].tolist()
    
    player1_list = []
    val1 = df[df["optaPersonId"] == p1][variable].tolist()[0]
    for i in np.histogram(df[variable], bins = num_bins)[1]:
        if i < val1:
            player1_list.append(i)
        else:
            player1_list.append(i)
            break
    
    player2_list = []
    val2 = df[df["optaPersonId"] == p2][variable].tolist()[0]
    for i in np.histogram(df[variable], bins = num_bins)[1]:
        if i < val2:
            player2_list.append(i)
        else:
            player2_list.append(i)
            break
    
    ax = axs[0, 0]
    # Under - P2
    sns.histplot(var, bins = num_bins, color = "#FF8383", ax=ax, edgecolor="grey")
    sns.histplot(var, bins = player2_list, color = "red", ax=ax)
    
    for p in ax.patches:  # turn the histogram upside down
        p.set_height(-p.get_height())
    for l in ax.lines:  # turn the kde curve upside down
        l.set_ydata(-l.get_ydata())
    
    # Above - P1
    sns.histplot(var, bins = num_bins, color = "#A0D1FF", ax=ax, edgecolor="grey")
    sns.histplot(var, bins = player1_list, color = "#004080", ax=ax)
    
    pos_ticks = np.array([t for t in ax.get_yticks() if t > 0])
    ticks = np.concatenate([-pos_ticks[::-1], [0], pos_ticks])
    ax.set_yticks(ticks)
    ax.set_yticklabels([f'{abs(t):.2f}' for t in ticks])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    plt.xlabel(variable)
    plt.ylabel("")
    
    ax.axvline(x=val1, ymin=0.5, ymax=(1-0.01), color='#A0D1FF', linestyle='dashed')
    ax.axvline(x=val2, ymax=0.5, ymin=0.01, color='#FF8383', linestyle='dashed')
    
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_yticks([])
    
    ax.title.set_text(variable)
        
    # ------------------------------------------------------------------------------------------
    variable = df.columns[4]
    var = df[variable].tolist()
    
    
    player1_list = []
    val1 = df[df["optaPersonId"] == p1][variable].tolist()[0]
    for i in np.histogram(df[variable], bins = num_bins)[1]:
        if i < val1:
            player1_list.append(i)
        else:
            player1_list.append(i)
            break
    
    player2_list = []
    val2 = df[df["optaPersonId"] == p2][variable].tolist()[0]
    for i in np.histogram(df[variable], bins = num_bins)[1]:
        if i < val2:
            player2_list.append(i)
        else:
            player2_list.append(i)
            break
    
    ax = axs[0, 1]
    # Under - P2
    sns.histplot(var, bins = num_bins, color = "#FF8383", ax=ax, edgecolor="grey")
    sns.histplot(var, bins = player2_list, color = "red", ax=ax)
    
    for p in ax.patches:  # turn the histogram upside down
        p.set_height(-p.get_height())
    for l in ax.lines:  # turn the kde curve upside down
        l.set_ydata(-l.get_ydata())
    
    # Above - P1
    sns.histplot(var, bins = num_bins, color = "#A0D1FF", ax=ax, edgecolor="grey")
    sns.histplot(var, bins = player1_list, color = "#004080", ax=ax)
    
    pos_ticks = np.array([t for t in ax.get_yticks() if t > 0])
    ticks = np.concatenate([-pos_ticks[::-1], [0], pos_ticks])
    ax.set_yticks(ticks)
    ax.set_yticklabels([f'{abs(t):.2f}' for t in ticks])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    plt.xlabel(variable)
    plt.ylabel("")
    
    ax.axvline(x=val1, ymin=0.5, ymax=(1-0.01), color='#A0D1FF', linestyle='dashed')
    ax.axvline(x=val2, ymax=0.5, ymin=0.01, color='#FF8383', linestyle='dashed')
    
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_yticks([])
    
    ax.title.set_text(variable)
    # ------------------------------------------------------------------------------------------
    variable = df.columns[5]
    var = df[variable].tolist()
    
    player1_list = []
    val1 = df[df["optaPersonId"] == p1][variable].tolist()[0]
    for i in np.histogram(df[variable], bins = num_bins)[1]:
        if i < val1:
            player1_list.append(i)
        else:
            player1_list.append(i)
            break
    
    player2_list = []
    val2 = df[df["optaPersonId"] == p2][variable].tolist()[0]
    for i in np.histogram(df[variable], bins = num_bins)[1]:
        if i < val2:
            player2_list.append(i)
        else:
            player2_list.append(i)
            break
    
    ax = axs[0, 2]
    # Under - P2
    sns.histplot(var, bins = num_bins, color = "#FF8383", ax=ax, edgecolor="grey")
    sns.histplot(var, bins = player2_list, color = "red", ax=ax)
    
    for p in ax.patches:  # turn the histogram upside down
        p.set_height(-p.get_height())
    for l in ax.lines:  # turn the kde curve upside down
        l.set_ydata(-l.get_ydata())
    
    # Above - P1
    sns.histplot(var, bins = num_bins, color = "#A0D1FF", ax=ax, edgecolor="grey")
    sns.histplot(var, bins = player1_list, color = "#004080", ax=ax)
    
    pos_ticks = np.array([t for t in ax.get_yticks() if t > 0])
    ticks = np.concatenate([-pos_ticks[::-1], [0], pos_ticks])
    ax.set_yticks(ticks)
    ax.set_yticklabels([f'{abs(t):.2f}' for t in ticks])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    plt.xlabel(variable)
    plt.ylabel("")
    
    ax.axvline(x=val1, ymin=0.5, ymax=(1-0.01), color='#A0D1FF', linestyle='dashed')
    ax.axvline(x=val2, ymax=0.5, ymin=0.01, color='#FF8383', linestyle='dashed')
    
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_yticks([])
    
    ax.title.set_text(variable)
    
    # ------------------------------------------------------------------------------------------
    variable = df.columns[6]
    var = df[variable].tolist()
    
    player1_list = []
    val1 = df[df["optaPersonId"] == p1][variable].tolist()[0]
    for i in np.histogram(df[variable], bins = num_bins)[1]:
        if i < val1:
            player1_list.append(i)
        else:
            player1_list.append(i)
            break
    
    player2_list = []
    val2 = df[df["optaPersonId"] == p2][variable].tolist()[0]
    for i in np.histogram(df[variable], bins = num_bins)[1]:
        if i < val2:
            player2_list.append(i)
        else:
            player2_list.append(i)
            break
    
    ax = axs[0, 3]
    # Under - P2
    sns.histplot(var, bins = num_bins, color = "#FF8383", ax=ax, edgecolor="grey")
    sns.histplot(var, bins = player2_list, color = "red", ax=ax)
    
    for p in ax.patches:  # turn the histogram upside down
        p.set_height(-p.get_height())
    for l in ax.lines:  # turn the kde curve upside down
        l.set_ydata(-l.get_ydata())
    
    # Above - P1
    sns.histplot(var, bins = num_bins, color = "#A0D1FF", ax=ax, edgecolor="grey")
    sns.histplot(var, bins = player1_list, color = "#004080", ax=ax)
    
    pos_ticks = np.array([t for t in ax.get_yticks() if t > 0])
    ticks = np.concatenate([-pos_ticks[::-1], [0], pos_ticks])
    ax.set_yticks(ticks)
    ax.set_yticklabels([f'{abs(t):.2f}' for t in ticks])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    plt.xlabel(variable)
    plt.ylabel("")
    
    ax.axvline(x=val1, ymin=0.5, ymax=(1-0.01), color='#A0D1FF', linestyle='dashed')
    ax.axvline(x=val2, ymax=0.5, ymin=0.01, color='#FF8383', linestyle='dashed')
    
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_yticks([])
    
    ax.title.set_text(variable)
    
    # ------------------------------------------------------------------------------------------
    variable = df.columns[7]
    var = df[variable].tolist()
    
    player1_list = []
    val1 = df[df["optaPersonId"] == p1][variable].tolist()[0]
    for i in np.histogram(df[variable], bins = num_bins)[1]:
        if i < val1:
            player1_list.append(i)
        else:
            player1_list.append(i)
            break
    
    player2_list = []
    val2 = df[df["optaPersonId"] == p2][variable].tolist()[0]
    for i in np.histogram(df[variable], bins = num_bins)[1]:
        if i < val2:
            player2_list.append(i)
        else:
            player2_list.append(i)
            break
    
    ax = axs[0, 4]
    # Under - P2
    sns.histplot(var, bins = num_bins, color = "#FF8383", ax=ax, edgecolor="grey")
    sns.histplot(var, bins = player2_list, color = "red", ax=ax)
    
    for p in ax.patches:  # turn the histogram upside down
        p.set_height(-p.get_height())
    for l in ax.lines:  # turn the kde curve upside down
        l.set_ydata(-l.get_ydata())
    
    # Above - P1
    sns.histplot(var, bins = num_bins, color = "#A0D1FF", ax=ax, edgecolor="grey")
    sns.histplot(var, bins = player1_list, color = "#004080", ax=ax)
    
    pos_ticks = np.array([t for t in ax.get_yticks() if t > 0])
    ticks = np.concatenate([-pos_ticks[::-1], [0], pos_ticks])
    ax.set_yticks(ticks)
    ax.set_yticklabels([f'{abs(t):.2f}' for t in ticks])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    plt.xlabel(variable)
    plt.ylabel("")
    
    ax.axvline(x=val1, ymin=0.5, ymax=(1-0.01), color='#A0D1FF', linestyle='dashed')
    ax.axvline(x=val2, ymax=0.5, ymin=0.01, color='#FF8383', linestyle='dashed')
    
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_yticks([])
    
    ax.title.set_text(variable)
    
    # ------------------------------------------------------------------------------------------
    variable = df.columns[8]
    var = df[variable].tolist()
    
    player1_list = []
    val1 = df[df["optaPersonId"] == p1][variable].tolist()[0]
    for i in np.histogram(df[variable], bins = num_bins)[1]:
        if i < val1:
            player1_list.append(i)
        else:
            player1_list.append(i)
            break
    
    player2_list = []
    val2 = df[df["optaPersonId"] == p2][variable].tolist()[0]
    for i in np.histogram(df[variable], bins = num_bins)[1]:
        if i < val2:
            player2_list.append(i)
        else:
            player2_list.append(i)
            break
    
    
    ax = axs[1, 0]
    # Under - P2
    sns.histplot(var, bins = num_bins, color = "#FF8383", ax=ax, edgecolor="grey")
    sns.histplot(var, bins = player2_list, color = "red", ax=ax)
    
    for p in ax.patches:  # turn the histogram upside down
        p.set_height(-p.get_height())
    for l in ax.lines:  # turn the kde curve upside down
        l.set_ydata(-l.get_ydata())
    
    # Above - P1
    sns.histplot(var, bins = num_bins, color = "#A0D1FF", ax=ax, edgecolor="grey")
    sns.histplot(var, bins = player1_list, color = "#004080", ax=ax)
    
    pos_ticks = np.array([t for t in ax.get_yticks() if t > 0])
    ticks = np.concatenate([-pos_ticks[::-1], [0], pos_ticks])
    ax.set_yticks(ticks)
    ax.set_yticklabels([f'{abs(t):.2f}' for t in ticks])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    plt.xlabel(variable)
    plt.ylabel("")
    
    ax.axvline(x=val1, ymin=0.5, ymax=(1-0.01), color='#A0D1FF', linestyle='dashed')
    ax.axvline(x=val2, ymax=0.5, ymin=0.01, color='#FF8383', linestyle='dashed')
    
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_yticks([])
    
    ax.title.set_text(variable)
    
    # ------------------------------------------------------------------------------------------
    variable = df.columns[9]
    var = df[variable].tolist()
    
    player1_list = []
    val1 = df[df["optaPersonId"] == p1][variable].tolist()[0]
    for i in np.histogram(df[variable], bins = num_bins)[1]:
        if i < val1:
            player1_list.append(i)
        else:
            player1_list.append(i)
            break
    
    player2_list = []
    val2 = df[df["optaPersonId"] == p2][variable].tolist()[0]
    for i in np.histogram(df[variable], bins = num_bins)[1]:
        if i < val2:
            player2_list.append(i)
        else:
            player2_list.append(i)
            break
    
    ax = axs[1, 1]
    # Under - P2
    sns.histplot(var, bins = num_bins, color = "#FF8383", ax=ax, edgecolor="grey")
    sns.histplot(var, bins = player2_list, color = "red", ax=ax)
    
    for p in ax.patches:  # turn the histogram upside down
        p.set_height(-p.get_height())
    for l in ax.lines:  # turn the kde curve upside down
        l.set_ydata(-l.get_ydata())
    
    # Above - P1
    sns.histplot(var, bins = num_bins, color = "#A0D1FF", ax=ax, edgecolor="grey")
    sns.histplot(var, bins = player1_list, color = "#004080", ax=ax)
    
    pos_ticks = np.array([t for t in ax.get_yticks() if t > 0])
    ticks = np.concatenate([-pos_ticks[::-1], [0], pos_ticks])
    ax.set_yticks(ticks)
    ax.set_yticklabels([f'{abs(t):.2f}' for t in ticks])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    plt.xlabel(variable)
    plt.ylabel("")
    
    ax.axvline(x=val1, ymin=0.5, ymax=(1-0.01), color='#A0D1FF', linestyle='dashed')
    ax.axvline(x=val2, ymax=0.5, ymin=0.01, color='#FF8383', linestyle='dashed')
    
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_yticks([])
    
    ax.title.set_text(variable)
    # ------------------------------------------------------------------------------------------
    variable = df.columns[10]
    var = df[variable].tolist()
    
    player1_list = []
    val1 = df[df["optaPersonId"] == p1][variable].tolist()[0]
    for i in np.histogram(df[variable], bins = num_bins)[1]:
        if i < val1:
            player1_list.append(i)
        else:
            player1_list.append(i)
            break
    
    player2_list = []
    val2 = df[df["optaPersonId"] == p2][variable].tolist()[0]
    for i in np.histogram(df[variable], bins = num_bins)[1]:
        if i < val2:
            player2_list.append(i)
        else:
            player2_list.append(i)
            break
    
    ax = axs[1, 2]
    # Under - P2
    sns.histplot(var, bins = num_bins, color = "#FF8383", ax=ax, edgecolor="grey")
    sns.histplot(var, bins = player2_list, color = "red", ax=ax)
    
    for p in ax.patches:  # turn the histogram upside down
        p.set_height(-p.get_height())
    for l in ax.lines:  # turn the kde curve upside down
        l.set_ydata(-l.get_ydata())
    
    # Above - P1
    sns.histplot(var, bins = num_bins, color = "#A0D1FF", ax=ax, edgecolor="grey")
    sns.histplot(var, bins = player1_list, color = "#004080", ax=ax)
    
    pos_ticks = np.array([t for t in ax.get_yticks() if t > 0])
    ticks = np.concatenate([-pos_ticks[::-1], [0], pos_ticks])
    ax.set_yticks(ticks)
    ax.set_yticklabels([f'{abs(t):.2f}' for t in ticks])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    plt.xlabel(variable)
    plt.ylabel("")
    
    ax.axvline(x=val1, ymin=0.5, ymax=(1-0.01), color='#A0D1FF', linestyle='dashed')
    ax.axvline(x=val2, ymax=0.5, ymin=0.01, color='#FF8383', linestyle='dashed')
    
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_yticks([])
    
    ax.title.set_text(variable)
    
    # ------------------------------------------------------------------------------------------
    variable = df.columns[11]
    var = df[variable].tolist()
    
    player1_list = []
    val1 = df[df["optaPersonId"] == p1][variable].tolist()[0]
    for i in np.histogram(df[variable], bins = num_bins)[1]:
        if i < val1:
            player1_list.append(i)
        else:
            player1_list.append(i)
            break
    
    player2_list = []
    val2 = df[df["optaPersonId"] == p2][variable].tolist()[0]
    for i in np.histogram(df[variable], bins = num_bins)[1]:
        if i < val2:
            player2_list.append(i)
        else:
            player2_list.append(i)
            break
    
    ax = axs[1, 3]
    # Under - P2
    sns.histplot(var, bins = num_bins, color = "#FF8383", ax=ax, edgecolor="grey")
    sns.histplot(var, bins = player2_list, color = "red", ax=ax)
    
    for p in ax.patches:  # turn the histogram upside down
        p.set_height(-p.get_height())
    for l in ax.lines:  # turn the kde curve upside down
        l.set_ydata(-l.get_ydata())
    
    # Above - P1
    sns.histplot(var, bins = num_bins, color = "#A0D1FF", ax=ax, edgecolor="grey")
    sns.histplot(var, bins = player1_list, color = "#004080", ax=ax)
    
    pos_ticks = np.array([t for t in ax.get_yticks() if t > 0])
    ticks = np.concatenate([-pos_ticks[::-1], [0], pos_ticks])
    ax.set_yticks(ticks)
    ax.set_yticklabels([f'{abs(t):.2f}' for t in ticks])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    plt.xlabel(variable)
    plt.ylabel("")
    
    ax.axvline(x=val1, ymin=0.5, ymax=(1-0.01), color='#A0D1FF', linestyle='dashed')
    ax.axvline(x=val2, ymax=0.5, ymin=0.01, color='#FF8383', linestyle='dashed')
    
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_yticks([])
    
    ax.title.set_text(variable)
    
    # ------------------------------------------------------------------------------------------
    variable = df.columns[12]
    var = df[variable].tolist()
    
    player1_list = []
    val1 = df[df["optaPersonId"] == p1][variable].tolist()[0]
    for i in np.histogram(df[variable], bins = num_bins)[1]:
        if i < val1:
            player1_list.append(i)
        else:
            player1_list.append(i)
            break
    
    player2_list = []
    val2 = df[df["optaPersonId"] == p2][variable].tolist()[0]
    for i in np.histogram(df[variable], bins = num_bins)[1]:
        if i < val2:
            player2_list.append(i)
        else:
            player2_list.append(i)
            break
    
    ax = axs[1, 4]
    # Under - P2
    sns.histplot(var, bins = num_bins, color = "#FF8383", ax=ax, edgecolor="grey")
    sns.histplot(var, bins = player2_list, color = "red", ax=ax)
    
    for p in ax.patches:  # turn the histogram upside down
        p.set_height(-p.get_height())
    for l in ax.lines:  # turn the kde curve upside down
        l.set_ydata(-l.get_ydata())
    
    # Above - P1
    sns.histplot(var, bins = num_bins, color = "#A0D1FF", ax=ax, edgecolor="grey")
    sns.histplot(var, bins = player1_list, color = "#004080", ax=ax)
    
    pos_ticks = np.array([t for t in ax.get_yticks() if t > 0])
    ticks = np.concatenate([-pos_ticks[::-1], [0], pos_ticks])
    ax.set_yticks(ticks)
    ax.set_yticklabels([f'{abs(t):.2f}' for t in ticks])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    
    ax.axvline(x=val1, ymin=0.5, ymax=(1-0.01), color='#A0D1FF', linestyle='dashed')
    ax.axvline(x=val2, ymax=0.5, ymin=0.01, color='#FF8383', linestyle='dashed')
    
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_yticks([])
    
    ax.title.set_text(variable)
    
    plt.subplots_adjust(hspace=0.5)
    
    
    st.pyplot(fig)
    
    authenticator.logout("Logout", "sidebar")



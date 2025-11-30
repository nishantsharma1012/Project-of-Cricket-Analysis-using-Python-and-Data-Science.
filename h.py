import streamlit as st
from streamlit_option_menu import option_menu
import base64
from streamlit_lottie import st_lottie
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

plt.style.use('seaborn-v0_8-whitegrid')
st.set_page_config(layout="wide", page_title="CRICSTATS", page_icon="📊")
def encode_image_to_base64(file_path):
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

image_base64 = encode_image_to_base64(r"D:\python training\aa1.jpg")
if image_base64:
    st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpeg;base64,{image_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    [data-testid="stHeader"] {{ background: rgba(255, 255, 255, 0.7); }}
    [data-testid="stSidebar"] > div:first-child {{ background: rgba(255, 255, 255, 0.85); }}
    </style>
    """, unsafe_allow_html=True)

def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_json = load_lottie_url("https://lottie.host/afa68dc7-d014-475e-b397-31d6aec68d0d/6syEIOwq3Q.json")
with st.sidebar:
    if lottie_json:
        st_lottie(lottie_json, height=150)

with st.sidebar:
    selected_menu = option_menu(
        menu_title="Main Menu",
        options=["Home", "Player Analyse", "Player Graph", "Trophy Analyse", "live", "About Us"],
        icons=["house", "person-lines-fill", "bar-chart", "people", "trophy", "info-circle"],
        default_index=0
    )

st.title("🔷 CRICSTATS DASHBOARD")

@st.cache_data
def load_player_data():
    df = pd.read_excel(r"D:\python training\ICC Test Bat 3001.xlsx") 
    df.columns = df.columns.map(str)
    df['Player_clean'] = df['Player'].str.lower().str.replace(r'[\xa0*]', '', regex=True).str.strip()
    for col in ['Runs', '100', '50', 'Inn', 'Avg', 'Mat', 'NO', 'HS', '0']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce')
    if 'Span' in df.columns:
        df[['Start_Year', 'End_Year']] = df['Span'].str.split('-', expand=True)
        df['Start_Year'] = pd.to_numeric(df['Start_Year'], errors='coerce')
        df['End_Year'] = pd.to_numeric(df['End_Year'], errors='coerce')
        df['Career_Length'] = df['End_Year'] - df['Start_Year']
    return df

df_players = load_player_data()

@st.cache_data
def load_trophy_data():
    df = pd.read_csv(r"D:\python training\all_champions_trophy_matches_results.csv", dtype=str) 
    df.columns = df.columns.map(str)
    if 'Winner' in df.columns:
        df['Winner'] = df['Winner'].str.strip()
    if 'Player of the Match' in df.columns:
        df['Player of the Match'] = df['Player of the Match'].str.strip()
    return df

df_trophy = load_trophy_data()

if selected_menu == "Home":
    st.markdown("""
    <style>
    .welcome-title {
        font-size: 3rem;
        font-weight: bold;
        color: black;
        background: linear-gradient(90deg, #ff4500, #ff7300);
        padding: 18px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.3);
    }
    .welcome-subtitle {
        font-size: 1.2rem;
        color: #000000;
        text-align: center;
        margin-top: 8px;
    }
    </style>
    <div class="welcome-title">🏏 Welcome to CRICSTATS</div>
    <div class="welcome-subtitle">Your ultimate cricket analytics hub</div>
""", unsafe_allow_html=True)

    cricket_anim = load_lottie_url("https://lottie.host/7b27d1ae-bf2f-4c74-a888-f26b237a6f1a/nfRsbO65wN.json")
    if cricket_anim:
        st_lottie(cricket_anim, height=250, key="cricket")

    st.markdown("### 🌟 Key Features")
    col1, col2, col3 = st.columns(3)

    with col1:
         st.markdown(
        "<div style='background-color:#F0F8FF; padding:15px; border-radius:10px; text-align:center; color:black;'>"
        "📊 <b>Player Analysis</b><br>Get complete stats of your favorite players."
        "</div>", unsafe_allow_html=True
    )

    with col2:
         st.markdown(
        "<div style='background-color:#FFF5EE; padding:15px; border-radius:10px; text-align:center; color:black;'>"
        "📈 <b>Player Graphs</b><br>Visualize runs, averages, and more over the years."
        "</div>", unsafe_allow_html=True
    )

    with col3:
         st.markdown(
        "<div style='background-color:#F5FFFA; padding:15px; border-radius:10px; text-align:center; color:black;'>"
        "👤 <b>Player Comparison</b><br>Comparison between two players."
        "</div>", unsafe_allow_html=True
    )
    st.markdown("---")
    
    # Add some quick stats on the home page
    st.markdown("### 📊 Quick Stats")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_players = len(df_players)
        st.metric("Total Players", total_players)
    
    with col2:
        highest_run = df_players['Runs'].max()
        st.metric("Highest Runs", f"{highest_run:,}")
    
    with col3:
        best_avg = df_players[df_players['Inn'] > 20]['Avg'].max()
        st.metric("Best Average", f"{best_avg:.2f}")
    
    with col4:
        most_100s = df_players['100'].max()
        st.metric("Most Centuries", most_100s)

elif selected_menu == "Player Analyse":
    st.subheader("👤 Player Analysis")
    players = df_players["Player"].dropna().unique().tolist()
    choice = st.selectbox("Select a Player", players)
    if choice:
        player_data = df_players[df_players["Player"] == choice].iloc[0]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Runs", f"{player_data['Runs']:,}")
            st.metric("Highest Score", player_data['HS'])
            st.metric("Batting Average", f"{player_data['Avg']:.2f}")
            
        with col2:
            st.metric("Matches", player_data['Mat'])
            st.metric("Innings", player_data['Inn'])
            st.metric("Not Outs", player_data['NO'])
            
        with col3:
            st.metric("Centuries", player_data['100'])
            st.metric("Half Centuries", player_data['50'])
            st.metric("Ducks", player_data['0'])
        
        # Career timeline visualization
        if pd.notna(player_data['Start_Year']) and pd.notna(player_data['End_Year']):
            fig, ax = plt.subplots(figsize=(10, 2))
            ax.plot([player_data['Start_Year'], player_data['End_Year']], [1, 1], linewidth=10, color='blue')
            ax.set_xlim(player_data['Start_Year'] - 2, player_data['End_Year'] + 2)
            ax.set_yticks([])
            ax.set_title(f"Career Timeline: {player_data['Start_Year']} - {player_data['End_Year']}")
            ax.set_xlabel("Year")
            st.pyplot(fig)

elif selected_menu == "Player Graph":
    st.subheader("📊 Player Graphs")

    section = option_menu(
        None,
        ["Player Comparison", "Top 10 by Runs", "Top 10 by Average", "Year-wise Top Scorers", "Player Distribution", "Century Analysis"],
        icons=["people", "trophy", "bar-chart", "calendar", "pie-chart", "star"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#ffffff"},
            "icon": {"color": "black", "font-size": "18px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "center",
                "margin": "0px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {
                "background-color": "#e63946",
                "color": "white",
                "font-weight": "bold",
                "border-radius": "6px",
            },
        },
    )

    all_players = df_players['Player'].dropna().unique().tolist()

    if section == "Player Comparison":
        st.markdown("### Compare Two Players")
        col1, col2 = st.columns(2)
        player1 = col1.selectbox("Select Player 1", all_players, key="p1_horiz")
        player2 = col2.selectbox("Select Player 2", all_players, key="p2_horiz")

        if player1 and player2 and player1 != player2:
            d1 = df_players[df_players['Player'] == player1].iloc[0]
            d2 = df_players[df_players['Player'] == player2].iloc[0]

            compare_df = pd.DataFrame({
                "Metric": ['Runs', 'Innings', '100s', '50s', 'Average', 'Matches', 'Career Span'],
                player1: [d1['Runs'], d1['Inn'], d1['100'], d1['50'], d1['Avg'], d1['Mat'], 
                         f"{d1['Start_Year']}-{d1['End_Year']}" if pd.notna(d1['Start_Year']) and pd.notna(d1['End_Year']) else "N/A"],
                player2: [d2['Runs'], d2['Inn'], d2['100'], d2['50'], d2['Avg'], d2['Mat'],
                         f"{d2['Start_Year']}-{d2['End_Year']}" if pd.notna(d2['Start_Year']) and pd.notna(d2['End_Year']) else "N/A"]
            }).set_index("Metric")

            # Display comparison table
            st.dataframe(compare_df)
            
            # Radar chart for comparison
            metrics = ['Runs', '100s', '50s', 'Average']
            values1 = [d1['Runs']/10000, d1['100'], d1['50'], d1['Avg']/100]
            values2 = [d2['Runs']/10000, d2['100'], d2['50'], d2['Avg']/100]
            
            angles = np.linspace(0, 2*np.pi, len(metrics), endpoint=False).tolist()
            values1 += values1[:1]
            values2 += values2[:1]
            angles += angles[:1]
            
            fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
            ax.plot(angles, values1, 'o-', linewidth=2, label=player1)
            ax.fill(angles, values1, alpha=0.25)
            ax.plot(angles, values2, 'o-', linewidth=2, label=player2)
            ax.fill(angles, values2, alpha=0.25)
            ax.set_thetagrids(np.degrees(angles[:-1]), metrics)
            ax.set_title("Player Comparison Radar Chart")
            ax.legend(loc='upper right')
            st.pyplot(fig)

    elif section == "Top 10 by Runs":
        top_runs = df_players[df_players['Runs'].notna()].nlargest(10, 'Runs')
        fig, ax = plt.subplots(figsize=(10,6))
        bars = ax.barh(top_runs['Player'], top_runs['Runs'], color='gold')
        ax.bar_label(bars, fmt='%d', padding=3)
        ax.invert_yaxis()
        ax.set_title("Top 10 Players by Runs")
        ax.set_xlabel("Runs")
        st.pyplot(fig)
        
        # Add a pie chart showing distribution of runs among top 10
        fig, ax = plt.subplots(figsize=(8,8))
        ax.pie(top_runs['Runs'], labels=top_runs['Player'], autopct='%1.1f%%')
        ax.set_title("Percentage Distribution of Runs Among Top 10")
        st.pyplot(fig)

    elif section == "Top 10 by Average":
        # Filter players with minimum 20 innings
        top_avg = df_players[(df_players['Avg'].notna()) & (df_players['Inn'] > 20)].nlargest(10, 'Avg')
        fig, ax = plt.subplots(figsize=(10,6))
        bars = ax.barh(top_avg['Player'], top_avg['Avg'], color='green')
        ax.bar_label(bars, fmt='%.2f', padding=3)
        ax.invert_yaxis()
        ax.set_title("Top 10 Players by Batting Average (min 20 innings)")
        ax.set_xlabel("Average")
        st.pyplot(fig)

    elif section == "Year-wise Top Scorers":
        years = sorted(df_players['Start_Year'].dropna().unique())
        selected_year = st.selectbox("Select Start Year", years)
        if selected_year:
            year_df = df_players[(df_players['Start_Year'] <= selected_year) & 
                                 (df_players['End_Year'] >= selected_year)]
            if not year_df.empty:
                top_year = year_df.nlargest(10, 'Runs')
                fig, ax = plt.subplots(figsize=(10,6))
                bars = ax.barh(top_year['Player'], top_year['Runs'], color='purple')
                ax.bar_label(bars, fmt='%d', padding=3)
                ax.invert_yaxis()
                ax.set_title(f"Top 10 Run Scorers in {selected_year}")
                ax.set_xlabel("Runs")
                st.pyplot(fig)
            else:
                st.warning("No data available for this year.")
                
    elif section == "Player Distribution":
        st.markdown("### Player Distribution Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribution of batting averages
            fig, ax = plt.subplots(figsize=(8,6))
            filtered_avg = df_players[(df_players['Avg'].notna()) & (df_players['Inn'] > 20)]['Avg']
            ax.hist(filtered_avg, bins=20, color='skyblue', edgecolor='black')
            ax.set_title("Distribution of Batting Averages")
            ax.set_xlabel("Average")
            ax.set_ylabel("Number of Players")
            st.pyplot(fig)
        
        with col2:
            # Distribution of centuries
            fig, ax = plt.subplots(figsize=(8,6))
            centuries = df_players[df_players['100'].notna()]['100']
            ax.hist(centuries, bins=range(0, int(centuries.max())+10, 10), color='lightcoral', edgecolor='black')
            ax.set_title("Distribution of Centuries")
            ax.set_xlabel("Number of Centuries")
            ax.set_ylabel("Number of Players")
            st.pyplot(fig)
            
        # Scatter plot of runs vs average
        fig, ax = plt.subplots(figsize=(10,6))
        scatter = ax.scatter(df_players['Runs'], df_players['Avg'], alpha=0.6)
        ax.set_title("Runs vs Batting Average")
        ax.set_xlabel("Total Runs")
        ax.set_ylabel("Batting Average")
        st.pyplot(fig)
        
    elif section == "Century Analysis":
        st.markdown("### Century Analysis")
        
        # Top century makers
        top_century = df_players[df_players['100'].notna()].nlargest(10, '100')
        fig, ax = plt.subplots(figsize=(10,6))
        bars = ax.barh(top_century['Player'], top_century['100'], color='orange')
        ax.bar_label(bars, fmt='%d', padding=3)
        ax.invert_yaxis()
        ax.set_title("Top 10 Century Makers")
        ax.set_xlabel("Number of Centuries")
        st.pyplot(fig)
        
        # Century conversion rate (100s per innings)
        df_players['Century_Rate'] = df_players['100'] / df_players['Inn']
        top_rate = df_players[(df_players['Century_Rate'].notna()) & (df_players['Inn'] > 20)].nlargest(10, 'Century_Rate')
        
        fig, ax = plt.subplots(figsize=(10,6))
        bars = ax.barh(top_rate['Player'], top_rate['Century_Rate']*100, color='lightgreen')
        ax.bar_label(bars, fmt='%.2f%%', padding=3)
        ax.invert_yaxis()
        ax.set_title("Top 10 Century Conversion Rate (min 20 innings)")
        ax.set_xlabel("Centuries per 100 Innings (%)")
        st.pyplot(fig)

elif selected_menu == "Trophy Analyse":
    st.subheader("🏆 Champions Trophy Analysis")
    
    tab1, tab2, tab3 = st.tabs(["Team Performance", "Player Awards", "Match Analysis"])
    
    with tab1:
        wins = df_trophy['Winner'].value_counts()
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(wins.index, wins.values, color='skyblue')
        ax.bar_label(bars, fmt='%d', padding=3)
        ax.set_title("Total Wins by Team")
        ax.set_ylabel("Number of Wins")
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
        # Win percentage by team
        total_matches = len(df_trophy)
        win_percentage = (wins / total_matches * 100).sort_values(ascending=False)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(win_percentage.index, win_percentage.values, color='lightcoral')
        ax.bar_label(bars, fmt='%.1f%%', padding=3)
        ax.set_title("Win Percentage by Team")
        ax.set_ylabel("Win Percentage (%)")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    
    with tab2:
        pom = df_trophy['Player of the Match'].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(pom.index, pom.values, color='gold')
        ax.bar_label(bars, fmt='%d', padding=3)
        ax.invert_yaxis()
        ax.set_title("Top 10 Player of the Match Awards")
        ax.set_xlabel("Number of Awards")
        st.pyplot(fig)
    
    with tab3:
        if 'Toss' in df_trophy.columns:
            toss = df_trophy['Toss'].str.extract(r'elected to (.*) first')[0].value_counts()
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.pie(toss, labels=toss.index, autopct="%1.1f%%", startangle=90)
            ax.set_title("Toss Decisions")
            st.pyplot(fig)
        
        # Year-wise analysis if date column exists
        if 'Date' in df_trophy.columns:
            try:
                df_trophy['Year'] = pd.to_datetime(df_trophy['Date']).dt.year
                yearly_matches = df_trophy['Year'].value_counts().sort_index()
                
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(yearly_matches.index, yearly_matches.values, marker='o')
                ax.set_title("Number of Matches by Year")
                ax.set_xlabel("Year")
                ax.set_ylabel("Number of Matches")
                st.pyplot(fig)
            except:
                st.warning("Could not parse dates for year-wise analysis")

elif selected_menu == "live":
    st.subheader("🔴 Live Cricket Scores")

    API_KEY = "b75a8e99-0d88-47c9-b295-d6847fe7664b"
    url = f"https://api.cricapi.com/v1/currentMatches?apikey={API_KEY}&offset=0"

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        matches = data.get("data", [])

        if matches:
            for match in matches:
                team1 = match['teamInfo'][0]['name']
                team2 = match['teamInfo'][1]['name']
                match_type = match.get("matchType", "Unknown").upper()
                status = match.get("status", "N/A")

                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #1e3c72, #2a5298);
                    color: white;
                    padding: 18px;
                    border-radius: 15px;
                    margin-bottom: 20px;
                    box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
                ">
                    <h3 style="margin:0; text-align:center;">🏏 {team1} <span style="color:#FFD700;">vs</span> {team2}</h3>
                    <p style="margin:6px 0; text-align:center;"><b>Match Type:</b> {match_type} | <b>Status:</b> {status}</p>
                </div>
                """, unsafe_allow_html=True)

                if "score" in match and match["score"]:
                    for s in match["score"]:
                        st.markdown(f"""
                        <div style="
                            background: rgba(255,255,255,0.9);
                            padding: 12px;
                            border-radius: 10px;
                            margin-bottom: 10px;
                        ">
                            <b>{s.get("inning","")}</b> - {s.get("r",0)}/{s.get("w",0)} in {s.get("o",0)} overs
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No live score available yet.")
        else:
            st.info("No live matches right now.")
    except Exception as e:
        st.error(f"Error fetching live scores: {e}")

elif selected_menu == "About Us":
    st.subheader("ℹ️ About CRICSTATS")
    st.write("""
        CRICSTATS is a cricket analytics dashboard built with Streamlit.  
        - 📊 Analyze players' performance (Runs, 100s, 50s, Averages).  
        - 🏆 Explore Trophy history and match results.  
        - 📈 Visualize career comparisons and yearly breakdowns.  
        - 🔴 Follow Live Matches in real-time.  
    """)
    
    st.markdown("### 📈 Key Features")
    st.markdown("""
    - **Player Analysis**: Detailed statistics for individual players
    - **Player Comparison**: Side-by-side comparison of two players
    - **Top Performers**: Lists of top players by runs, average, centuries
    - **Year-wise Analysis**: Performance analysis by year
    - **Distribution Analysis**: Histograms and scatter plots of player statistics
    - **Trophy Analysis**: Team performance in tournaments
    - **Live Scores**: Real-time match updates
    """)
    
    st.markdown("### 🛠️ Built With")
    st.markdown("""
    - Python
    - Streamlit
    - Pandas
    - Matplotlib
    - Seaborn
    - CricAPI
    """)
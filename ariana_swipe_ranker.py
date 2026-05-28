
import streamlit as st
import pandas as pd
import random
from pathlib import Path

st.set_page_config(
    page_title="Ariana Grande Swipe Ranker",
    page_icon="💗",
    layout="wide"
)

SAVE_FILE = Path("ariana_swipe_rankings.csv")

ALBUMS = {
    "Yours Truly": [
        "Honeymoon Avenue", "Baby I", "Right There", "Tattooed Heart", "Lovin' It",
        "Piano", "Daydreamin'", "The Way", "You’ll Never Know", "Almost Is Never Enough",
        "Popular Song", "Better Left Unsaid"
    ],
    "My Everything": [
        "Intro", "Problem", "One Last Time", "Why Try", "Break Free", "Best Mistake",
        "Be My Baby", "Break Your Heart Right Back", "Love Me Harder",
        "Just a Little Bit of Your Heart", "Hands on Me", "My Everything",
        "Bang Bang", "Only 1", "You Don’t Know Me"
    ],
    "Dangerous Woman": [
        "Moonlight", "Dangerous Woman", "Be Alright", "Into You", "Side to Side",
        "Let Me Love You", "Greedy", "Leave Me Lonely", "Everyday", "Sometimes",
        "I Don’t Care", "Bad Decisions", "Touch It", "Knew Better / Forever Boy",
        "Thinking Bout You"
    ],
    "Sweetener": [
        "raindrops (an angel cried)", "blazed", "the light is coming", "R.E.M",
        "God is a woman", "sweetener", "successful", "everytime", "breathin",
        "no tears left to cry", "borderline", "better off", "goodnight n go",
        "pete davidson", "get well soon"
    ],
    "thank u, next": [
        "imagine", "needy", "NASA", "bloodline", "fake smile", "bad idea",
        "make up", "ghostin", "in my head", "7 rings", "thank u, next",
        "break up with your girlfriend, i’m bored"
    ],
    "Positions": [
        "shut up", "34+35", "motive", "just like magic", "off the table",
        "six thirty", "safety net", "my hair", "nasty", "west side",
        "love language", "positions", "obvious", "pov"
    ],
    "Eternal Sunshine": [
        "intro (end of the world)", "bye", "don’t wanna break up again",
        "Saturn Returns Interlude", "eternal sunshine", "supernatural",
        "true story", "the boy is mine", "yes, and?", "we can’t be friends",
        "i wish i hated you", "imperfect for you", "ordinary things"
    ]
}

PASTELS = {
    "Yours Truly": "#ffd6e8",
    "My Everything": "#d7e3ff",
    "Dangerous Woman": "#e6d5ff",
    "Sweetener": "#ffe0f0",
    "thank u, next": "#ffd1dc",
    "Positions": "#d9f5e8",
    "Eternal Sunshine": "#fff0c9",
}

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #ffe3f1 0%, #eee6ff 45%, #fff6d9 100%);
}
.block-container {
    padding-top: 2rem;
}
.big-title {
    font-size: 56px;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, #d14d8f, #8157c6, #ff8fab);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0;
}
.subtitle {
    text-align: center;
    color: #7e6a9e;
    font-size: 19px;
    margin-bottom: 25px;
}
.card {
    border-radius: 32px;
    padding: 35px;
    min-height: 300px;
    text-align: center;
    box-shadow: 0px 12px 35px rgba(126, 87, 194, 0.18);
    border: 3px solid rgba(255,255,255,0.9);
}
.left-card {
    background: linear-gradient(135deg, #dbe7ff, #f9ddff);
}
.right-card {
    background: linear-gradient(135deg, #ffd2e4, #fff1f7);
}
.song {
    font-size: 35px;
    font-weight: 850;
    color: #3b235f;
    margin-top: 50px;
}
.album {
    font-size: 18px;
    color: #7e6a9e;
    font-style: italic;
}
.vs {
    text-align: center;
    font-size: 48px;
    font-weight: 900;
    color: #9d62d9;
    padding-top: 120px;
}
.stat-box {
    background: rgba(255,255,255,0.65);
    border-radius: 22px;
    padding: 18px;
    border: 1px solid white;
}
</style>
""", unsafe_allow_html=True)

def all_songs(album):
    return ALBUMS[album]

def total_pairs(album):
    n = len(ALBUMS[album])
    return n * (n - 1) // 2

def make_pairs(album):
    songs = ALBUMS[album]
    pairs = []
    for i in range(len(songs)):
        for j in range(i + 1, len(songs)):
            pairs.append((songs[i], songs[j]))
    random.shuffle(pairs)
    return pairs

def load_results():
    if SAVE_FILE.exists():
        return pd.read_csv(SAVE_FILE)
    return pd.DataFrame(columns=["Album", "Winner", "Loser"])

def save_vote(album, winner, loser):
    results = load_results()
    new_row = pd.DataFrame([{"Album": album, "Winner": winner, "Loser": loser}])
    results = pd.concat([results, new_row], ignore_index=True)
    results.to_csv(SAVE_FILE, index=False)

def ranking_for_album(album):
    results = load_results()
    songs = ALBUMS[album]
    scores = {song: 0 for song in songs}
    losses = {song: 0 for song in songs}

    album_results = results[results["Album"] == album]
    for _, row in album_results.iterrows():
        scores[row["Winner"]] = scores.get(row["Winner"], 0) + 1
        losses[row["Loser"]] = losses.get(row["Loser"], 0) + 1

    rows = []
    for song in songs:
        wins = scores.get(song, 0)
        loses = losses.get(song, 0)
        played = wins + loses
        win_rate = wins / played if played else 0
        rows.append({
            "Song": song,
            "Wins": wins,
            "Losses": loses,
            "Score": wins,
            "Win Rate": round(win_rate * 100, 1)
        })

    return pd.DataFrame(rows).sort_values(["Score", "Win Rate"], ascending=False)

if "album" not in st.session_state:
    st.session_state.album = "Sweetener"

if "pairs" not in st.session_state:
    st.session_state.pairs = make_pairs(st.session_state.album)

if "current_pair" not in st.session_state:
    st.session_state.current_pair = st.session_state.pairs.pop() if st.session_state.pairs else None

st.markdown('<div class="big-title">♡ Ariana Grande Song Ranker ♡</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Choose between two songs. The app scores your taste by album 💿✨</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("💗 Menu")
    selected_album = st.selectbox("Choose album", list(ALBUMS.keys()), index=list(ALBUMS.keys()).index(st.session_state.album))

    if selected_album != st.session_state.album:
        st.session_state.album = selected_album
        st.session_state.pairs = make_pairs(selected_album)
        st.session_state.current_pair = st.session_state.pairs.pop() if st.session_state.pairs else None
        st.rerun()

    results = load_results()
    album_votes = len(results[results["Album"] == st.session_state.album])
    st.markdown("### Progress")
    st.progress(min(album_votes / total_pairs(st.session_state.album), 1.0))
    st.write(f"{album_votes} / {total_pairs(st.session_state.album)} comparisons")

    if st.button("🔄 New random pair"):
        if st.session_state.pairs:
            st.session_state.current_pair = st.session_state.pairs.pop()
            st.rerun()

    if st.button("🧹 Reset ALL rankings"):
        if SAVE_FILE.exists():
            SAVE_FILE.unlink()
        st.session_state.pairs = make_pairs(st.session_state.album)
        st.session_state.current_pair = st.session_state.pairs.pop()
        st.rerun()

    st.caption("Pastel ranking game made for comparing your Ariana favorites.")

album_color = PASTELS.get(st.session_state.album, "#ffe3f1")
st.markdown(
    f"""
    <div class="stat-box">
    <h3 style="color:#6d4c9f;">Current album: {st.session_state.album}</h3>
    <p style="color:#7e6a9e;">Pick the song you like more. Each win adds 1 point.</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

pair = st.session_state.current_pair

if pair is None:
    st.success("You finished all comparisons for this album! 🎉 Check your results below.")
else:
    left_song, right_song = pair

    col1, col2, col3 = st.columns([5, 1.3, 5])

    with col1:
        st.markdown(
            f"""
            <div class="card left-card">
                <div style="font-size:50px;">🎧</div>
                <div class="song">{left_song}</div>
                <div class="album">{st.session_state.album}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("⬅️ I prefer this one", use_container_width=True):
            save_vote(st.session_state.album, left_song, right_song)
            st.session_state.current_pair = st.session_state.pairs.pop() if st.session_state.pairs else None
            st.rerun()

    with col2:
        st.markdown('<div class="vs">VS</div>', unsafe_allow_html=True)

    with col3:
        st.markdown(
            f"""
            <div class="card right-card">
                <div style="font-size:50px;">💖</div>
                <div class="song">{right_song}</div>
                <div class="album">{st.session_state.album}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("I prefer this one ➡️", use_container_width=True):
            save_vote(st.session_state.album, right_song, left_song)
            st.session_state.current_pair = st.session_state.pairs.pop() if st.session_state.pairs else None
            st.rerun()

st.divider()

st.subheader(f"🏆 Ranking for {st.session_state.album}")
ranking = ranking_for_album(st.session_state.album)
st.dataframe(ranking, hide_index=True, use_container_width=True)

st.subheader("🌟 Overall ranking across all albums")
all_rankings = []
for album in ALBUMS:
    temp = ranking_for_album(album)
    temp.insert(0, "Album", album)
    all_rankings.append(temp)

overall = pd.concat(all_rankings, ignore_index=True)
overall = overall.sort_values(["Score", "Win Rate"], ascending=False)
st.dataframe(overall, hide_index=True, use_container_width=True)

st.download_button(
    "Download my rankings 💾",
    data=load_results().to_csv(index=False).encode("utf-8"),
    file_name="ariana_swipe_rankings.csv",
    mime="text/csv"
)

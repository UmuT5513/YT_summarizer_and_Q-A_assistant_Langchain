import streamlit as st
import requests
import os

# ── API Configuration ────────────────────────────────────────────────────────
API_BASE_URL = "http://127.0.0.1:8000"

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="YouTube Assistant",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    /* Title styling */
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(120deg, #e94560, #ff6b6b, #ffa502);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #8892b0;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Card styling */
    .info-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
    }
    .info-card h4 {
        color: #e94560;
        margin-bottom: 0.5rem;
    }
    .info-card p {
        color: #ccd6f6;
    }
    
    /* Metric cards */
    .metric-card {
        background: rgba(233, 69, 96, 0.1);
        border: 1px solid rgba(233, 69, 96, 0.3);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        text-align: center;
    }
    .metric-card .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #e94560;
    }
    .metric-card .metric-label {
        font-size: 0.85rem;
        color: #8892b0;
        margin-top: 0.25rem;
    }
    
    /* Summary box */
    .summary-box {
        background: rgba(255,255,255,0.03);
        border-left: 4px solid #e94560;
        border-radius: 0 12px 12px 0;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #ccd6f6;
        line-height: 1.7;
    }
    
    /* Chat messages */
    .user-msg {
        background: rgba(233, 69, 96, 0.15);
        border: 1px solid rgba(233, 69, 96, 0.3);
        border-radius: 16px 16px 4px 16px;
        padding: 1rem 1.25rem;
        margin: 0.5rem 0;
        color: #ccd6f6;
        max-width: 85%;
        margin-left: auto;
    }
    .bot-msg {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px 16px 16px 4px;
        padding: 1rem 1.25rem;
        margin: 0.5rem 0;
        color: #ccd6f6;
        max-width: 85%;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(15, 15, 26, 0.95);
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #e94560, #c23152);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #ff6b6b, #e94560);
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(233, 69, 96, 0.4);
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 10px;
        color: #ccd6f6;
    }
    .stTextInput > div > div > input:focus {
        border-color: #e94560;
        box-shadow: 0 0 0 1px #e94560;
    }
    
    /* Divider */
    .fancy-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #e94560, transparent);
        margin: 1.5rem 0;
        border: none;
    }
    
    /* Status badges */
    .status-fetched {
        display: inline-block;
        background: rgba(0, 200, 83, 0.15);
        color: #00c853;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .status-processing {
        display: inline-block;
        background: rgba(255, 165, 2, 0.15);
        color: #ffa502;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
        color: #8892b0;
        border: 1px solid rgba(255,255,255,0.1);
        padding: 0.5rem 1.5rem;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(233, 69, 96, 0.2) !important;
        color: #e94560 !important;
        border-color: #e94560 !important;
    }
</style>
""", unsafe_allow_html=True)


# ── API Helper Functions ─────────────────────────────────────────────────────
def api_get(endpoint):
    """GET request to FastAPI backend."""
    try:
        resp = requests.get(f"{API_BASE_URL}{endpoint}", timeout=30)
        resp.raise_for_status()
        return resp.json()
    except requests.ConnectionError:
        return None
    except requests.HTTPError:
        return None


def api_post(endpoint, params=None, json_data=None):
    """POST request to FastAPI backend."""
    try:
        resp = requests.post(f"{API_BASE_URL}{endpoint}", params=params, json=json_data, timeout=120)
        resp.raise_for_status()
        return resp.json()
    except requests.ConnectionError:
        st.error("❌ Cannot connect to API. Make sure the FastAPI server is running on http://127.0.0.1:8000")
        return None
    except requests.HTTPError as e:
        st.error(f"❌ API Error: {e}")
        return None


def format_duration(seconds):
    """Convert seconds to HH:MM:SS format."""
    if not seconds:
        return "N/A"
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    return f"{minutes}m {secs}s"


# ── Session State ────────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "video_metadata" not in st.session_state:
    st.session_state.video_metadata = None
if "summary_result" not in st.session_state:
    st.session_state.summary_result = None


# ── Fetch data from API ─────────────────────────────────────────────────────
all_videos = api_get("/videos") or []
all_channels = api_get("/channels") or []


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p style="font-size:1.5rem; font-weight:700; color:#e94560;">🎬 YouTube Assistant</p>', unsafe_allow_html=True)
    st.markdown('<p style="color:#8892b0; font-size:0.85rem;">AI-Powered Video Analysis</p>', unsafe_allow_html=True)
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    # Statistics
    st.markdown(f"""
    <div style="display:flex; gap:0.75rem; margin-bottom:1.5rem;">
        <div class="metric-card" style="flex:1;">
            <div class="metric-value">{len(all_videos)}</div>
            <div class="metric-label">Videos</div>
        </div>
        <div class="metric-card" style="flex:1;">
            <div class="metric-value">{len(all_channels)}</div>
            <div class="metric-label">Channels</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    # API Status
    api_status = api_get("/")
    if api_status:
        st.markdown('<p style="color:#00c853; font-size:0.8rem;">🟢 API Connected</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p style="color:#e94560; font-size:0.8rem;">🔴 API Disconnected</p>', unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    # Processed Videos List
    st.markdown('<p style="color:#e94560; font-weight:600; font-size:0.95rem;">📂 Processed Videos</p>', unsafe_allow_html=True)

    if all_videos:
        for v in all_videos:
            title = v.get("video_title", "Unknown")
            vid = v.get("video_id", "")
            duration = v.get("duration_seconds", 0)
            title_short = title[:35] + "..." if len(title) > 35 else title
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.03); border-radius:8px; padding:0.6rem 0.8rem; margin-bottom:0.4rem; border:1px solid rgba(255,255,255,0.06);">
                <p style="color:#ccd6f6; font-size:0.8rem; margin:0; font-weight:500;">🎥 {title_short}</p>
                <p style="color:#8892b0; font-size:0.7rem; margin:0;">{vid} • {format_duration(duration)}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<p style="color:#8892b0; font-size:0.8rem;">No videos processed yet.</p>', unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:#4a4a6a; font-size:0.7rem; text-align:center;">Powered by LangChain + OpenAI</p>', unsafe_allow_html=True)


# ── Main Content ─────────────────────────────────────────────────────────────
st.markdown('<h1 class="main-title">YouTube Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Summarize videos & ask questions with AI</p>', unsafe_allow_html=True)

# ── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["🔗  Add Video", "📝  Summarize", "💬  Q&A Chat", "📄  Transcript"])


# ── TAB 1: Add Video ────────────────────────────────────────────────────────
with tab1:
    st.markdown("")
    col_input, col_spacer = st.columns([3, 1])

    with col_input:
        video_url = st.text_input(
            "YouTube Video URL",
            placeholder="https://www.youtube.com/watch?v=...",
            label_visibility="collapsed",
        )

    process_btn = st.button("🚀  Process Video", use_container_width=False)

    if process_btn and video_url:
        with st.status("Processing video...", expanded=True) as status:
            try:
                st.write("📡 Sending video to API for processing...")
                result = api_post("/add_transcript_to_system", params={"video_url": video_url})

                if result:
                    st.session_state.video_metadata = result
                    st.write(f"✅ Video ID: `{result.get('video_id')}`")
                    st.write(f"✅ Channel ID: `{result.get('channel_id')}`")
                    st.write(f"✅ {result.get('message', 'Done!')}")
                    status.update(label="Video processed successfully!", state="complete")
                else:
                    status.update(label="Error occurred!", state="error")

            except Exception as e:
                status.update(label="Error occurred!", state="error")
                st.error(f"❌ {str(e)}")

    # Show result card if available
    if st.session_state.video_metadata:
        meta = st.session_state.video_metadata
        st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="font-size:1rem;">🎥</div>
                <div class="metric-label">Video ID: {meta.get('video_id', 'N/A')}</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="font-size:1rem;">📺</div>
                <div class="metric-label">Channel ID: {meta.get('channel_id', 'N/A')}</div>
            </div>""", unsafe_allow_html=True)


# ── TAB 2: Summarize ────────────────────────────────────────────────────────
with tab2:
    st.markdown("")

    if all_videos:
        video_options = {f"🎥 {v.get('video_title', 'Unknown')[:50]} ({v.get('video_id')})": v.get("video_id") for v in all_videos}
        selected_video = st.selectbox(
            "Select a video to summarize",
            options=list(video_options.keys()),
            label_visibility="collapsed",
            placeholder="Select a video to summarize...",
        )

        summarize_btn = st.button("✨  Generate Summary", use_container_width=False)

        if summarize_btn and selected_video:
            video_id = video_options[selected_video]
            with st.spinner("🤖 AI is generating summary..."):
                try:
                    result = api_post(f"/summarize/{video_id}")
                    if result:
                        st.session_state.summary_result = result.get("summary")
                except Exception as e:
                    st.error(f"❌ Error generating summary: {str(e)}")

        if st.session_state.summary_result:
            summary_data = st.session_state.summary_result
            st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

            # Handle both dict and structured output
            if isinstance(summary_data, dict):
                video_title = summary_data.get("video_title", "Video Summary")
                summary_text = summary_data.get("summary", "")
                key_takeaways = summary_data.get("key_takeaways", "")
            else:
                video_title = "Video Summary"
                summary_text = str(summary_data)
                key_takeaways = ""

            # Title
            st.markdown(f"""
            <div class="info-card">
                <h4>📌 {video_title}</h4>
            </div>
            """, unsafe_allow_html=True)

            # Summary
            st.markdown(f"""
            <div class="summary-box">
                <strong style="color:#e94560;">📝 Summary</strong><br><br>
                {summary_text}
            </div>
            """, unsafe_allow_html=True)

            # Key Takeaways
            if key_takeaways:
                st.markdown(f"""
                <div class="summary-box" style="border-left-color:#ffa502;">
                    <strong style="color:#ffa502;">🔑 Key Takeaways</strong><br><br>
                    {key_takeaways}
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="info-card" style="text-align:center;">
            <h4>No Videos Yet</h4>
            <p>Go to the <strong>Add Video</strong> tab to process your first YouTube video.</p>
        </div>
        """, unsafe_allow_html=True)


# ── TAB 3: Q&A Chat ─────────────────────────────────────────────────────────
with tab3:
    st.markdown("")

    # Scope selection
    col_scope, col_select = st.columns([1, 2])

    selected_id = None

    with col_scope:
        scope = st.radio(
            "Chat Scope",
            ["🎥 Single Video", "📺 Entire Channel"],
            label_visibility="collapsed",
            horizontal=True,
        )

    with col_select:
        if scope == "🎥 Single Video" and all_videos:
            video_opts = {f"{v.get('video_title', 'Unknown')[:45]} ({v.get('video_id')})": v.get("video_id") for v in all_videos}
            selected = st.selectbox("Select video", options=list(video_opts.keys()), label_visibility="collapsed", key="qa_video")
            selected_id = video_opts[selected] if selected else None
        elif scope == "📺 Entire Channel" and all_channels:
            chan_opts = {f"{c.get('channel_name', 'Unknown')} ({c.get('channel_id')})": c.get("channel_id") for c in all_channels}
            selected = st.selectbox("Select channel", options=list(chan_opts.keys()), label_visibility="collapsed", key="qa_channel")
            selected_id = chan_opts[selected] if selected else None
        else:
            st.markdown('<p style="color:#8892b0;">No data available. Process a video first.</p>', unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    # Chat history display
    chat_container = st.container()
    with chat_container:
        if st.session_state.chat_history:
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown(f'<div class="user-msg">🧑 {msg["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="bot-msg">🤖 {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align:center; padding:3rem; color:#4a4a6a;">
                <p style="font-size:2.5rem; margin-bottom:0.5rem;">💬</p>
                <p style="font-size:1rem;">Ask anything about your videos</p>
                <p style="font-size:0.8rem;">Select a video or channel and start chatting</p>
            </div>
            """, unsafe_allow_html=True)

    # Chat input
    question = st.chat_input("Ask a question about the video...")

    if question and selected_id:
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": question})

        # Call the correct API endpoint
        with st.spinner("🤖 Thinking..."):
            try:
                if scope == "🎥 Single Video":
                    result = api_post(
                        f"/chat_video/{selected_id}",
                        params={"question": question, "video_id": selected_id}
                    )
                else:
                    result = api_post(
                        f"/chat_channel/{selected_id}",
                        params={"question": question, "channel_id": selected_id}
                    )

                if result:
                    answer = result.get("answer", "No answer received.")
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
                else:
                    st.session_state.chat_history.append({"role": "assistant", "content": "❌ Failed to get answer from API."})

            except Exception as e:
                st.session_state.chat_history.append({"role": "assistant", "content": f"❌ Error: {str(e)}"})

        st.rerun()

    # Clear chat button
    if st.session_state.chat_history:
        st.markdown("")
        if st.button("🗑️  Clear Chat", use_container_width=False):
            st.session_state.chat_history = []
            st.rerun()


# ── TAB 4: Transcript ───────────────────────────────────────────────────────
with tab4:
    st.markdown("")

    if all_videos:
        video_options_t = {f"🎥 {v.get('video_title', 'Unknown')[:50]} ({v.get('video_id')})": v.get("video_id") for v in all_videos}
        selected_transcript = st.selectbox(
            "Select a video to view transcript",
            options=list(video_options_t.keys()),
            label_visibility="collapsed",
            placeholder="Select a video...",
            key="transcript_select",
        )

        view_btn = st.button("📄  View Transcript", use_container_width=False)

        if view_btn and selected_transcript:
            video_id = video_options_t[selected_transcript]
            with st.spinner("Loading transcript..."):
                result = api_get(f"/transcript/{video_id}")
                if result:
                    transcript_text = result.get("transcript", "No transcript found.")
                    st.markdown(f"""
                    <div class="summary-box">
                        <strong style="color:#e94560;">📄 Transcript — {video_id}</strong><br><br>
                        <div style="max-height:500px; overflow-y:auto; white-space:pre-wrap;">
{transcript_text}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="info-card" style="text-align:center;">
            <h4>No Videos Yet</h4>
            <p>Go to the <strong>Add Video</strong> tab to process your first YouTube video.</p>
        </div>
        """, unsafe_allow_html=True)

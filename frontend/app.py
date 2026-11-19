import time
from concurrent.futures import ThreadPoolExecutor

import streamlit as st

from frontend.api_client import create_website, ask_question


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="ChatAMU",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# Helpers
# --------------------------------------------------

def html(markup: str) -> str:
    """Strip indentation and blank lines so Streamlit's markdown
    parser never mistakes our HTML for a code block."""
    return "\n".join(
        line.strip() for line in markup.splitlines() if line.strip()
    )


def render(markup: str, target=None):
    (target or st).markdown(html(markup), unsafe_allow_html=True)


# One web graphic reused in the splash, hero, loader and sidebar.
WEB_SVG = """
<svg class="web" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <g class="links" stroke="currentColor" stroke-width="1.4" fill="none">
    <line x1="100" y1="100" x2="100" y2="28"/>
    <line x1="100" y1="100" x2="163" y2="64"/>
    <line x1="100" y1="100" x2="163" y2="136"/>
    <line x1="100" y1="100" x2="100" y2="172"/>
    <line x1="100" y1="100" x2="37" y2="136"/>
    <line x1="100" y1="100" x2="37" y2="64"/>
    <polygon points="100,28 163,64 163,136 100,172 37,136 37,64"/>
  </g>
  <g class="nodes">
    <circle class="n n1" cx="100" cy="28" r="6"/>
    <circle class="n n2" cx="163" cy="64" r="6"/>
    <circle class="n n3" cx="163" cy="136" r="6"/>
    <circle class="n n4" cx="100" cy="172" r="6"/>
    <circle class="n n5" cx="37" cy="136" r="6"/>
    <circle class="n n6" cx="37" cy="64" r="6"/>
    <circle class="core" cx="100" cy="100" r="11"/>
  </g>
</svg>
"""


# --------------------------------------------------
# Styling
# --------------------------------------------------

STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Figtree:wght@400;500;600&display=swap');

:root {
  --ink: #0e2a27;
  --ink-soft: #1c4742;
  --teal: #1f7a6d;
  --mist: #dce9e5;
  --paper: #f4f8f6;
  --brass: #c8963e;
  --brass-deep: #9b7020;
  --text: #12221f;
  --muted: #5b716c;
}

html, body, [class*="css"], .stApp, .stMarkdown, p, label, input, textarea {
  font-family: 'Figtree', sans-serif;
}
.stApp { background: var(--paper); color: var(--text); }
header[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 2.2rem; max-width: 1080px; }

h1, h2, h3, .display {
  font-family: 'Bricolage Grotesque', sans-serif !important;
  color: var(--ink);
  letter-spacing: -0.02em;
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
  background: var(--ink);
  border-right: 4px solid var(--brass);
}
section[data-testid="stSidebar"] * { color: #e6f1ee; }
section[data-testid="stSidebar"] .brand {
  display: flex; align-items: center; gap: .7rem; margin: .4rem 0 1.4rem;
}
section[data-testid="stSidebar"] .brand .web { width: 46px; height: 46px; color: var(--brass); }
section[data-testid="stSidebar"] .brand span {
  font-family: 'Bricolage Grotesque', sans-serif; font-weight: 800; font-size: 1.55rem;
}
.status-pill {
  display: inline-flex; align-items: center; gap: .5rem;
  padding: .35rem .8rem; border-radius: 999px; font-size: .85rem; font-weight: 500;
  background: rgba(255,255,255,.08);
}
.status-pill i { width: 9px; height: 9px; border-radius: 50%; background: #6b7f7b; display: inline-block; }
.status-pill.on i { background: #4fe0b0; box-shadow: 0 0 0 4px rgba(79,224,176,.18); }
.site-url { word-break: break-all; font-size: .9rem; opacity: .85; margin: .7rem 0 1.2rem; }
section[data-testid="stSidebar"] .stButton > button {
  width: 100%; background: transparent; color: #e6f1ee;
  border: 1px solid rgba(255,255,255,.25); border-radius: 10px;
}
section[data-testid="stSidebar"] .stButton > button:hover {
  border-color: var(--brass); color: var(--brass);
}

/* ---------- Hero ---------- */
.hero {
  display: grid; grid-template-columns: 1.4fr 1fr; align-items: center; gap: 2rem;
  background: var(--ink); color: #fff; border-radius: 22px;
  padding: 2.6rem 2.8rem; margin-bottom: 1.6rem; overflow: hidden; position: relative;
}
.hero h1 {
  color: #fff; font-size: clamp(2rem, 4.2vw, 3.2rem); line-height: 1.05; margin: 0 0 .9rem;
  font-weight: 800;
}
.hero p { color: #b9d2cc; font-size: 1.05rem; max-width: 32ch; margin: 0; }
.hero .web { width: 100%; max-width: 260px; justify-self: center; color: var(--ink-soft); }
.hero .web .n { fill: var(--brass); }
.hero .web .core { fill: #fff; }
.hero .web .links { stroke: #2f6a63; }

/* ---------- How it works ---------- */
.steps { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.8rem; }
.step { border-left: 3px solid var(--brass); padding: .2rem 0 .2rem 1rem; }
.step b { font-family: 'Bricolage Grotesque', sans-serif; font-size: 1.05rem; color: var(--ink); }
.step p { margin: .2rem 0 0; color: var(--muted); font-size: .93rem; }

/* ---------- Form ---------- */
div[data-testid="stForm"] {
  background: #fff; border: 1px solid var(--mist); border-radius: 18px;
  padding: 1.4rem 1.5rem; box-shadow: 0 10px 30px -18px rgba(14,42,39,.35);
}
div[data-testid="stTextInput"] input {
  border-radius: 12px; border: 1.5px solid var(--mist); padding: .75rem .9rem; font-size: 1rem;
}
div[data-testid="stTextInput"] input:focus { border-color: var(--teal); box-shadow: 0 0 0 3px rgba(31,122,109,.18); }
.stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] {
  background: var(--brass); border: none; color: #1b1405; font-weight: 700;
  border-radius: 12px; padding: .65rem 1.4rem;
}
.stButton > button[kind="primary"]:hover, .stFormSubmitButton > button[kind="primary"]:hover {
  background: var(--brass-deep); color: #fff;
}

/* ---------- Stats ---------- */
.stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin: 1rem 0 1.6rem; }
.stat { background: #fff; border: 1px solid var(--mist); border-radius: 16px; padding: 1rem 1.2rem; }
.stat .num { font-family: 'Bricolage Grotesque', sans-serif; font-size: 2.1rem; font-weight: 800; color: var(--ink); line-height: 1; }
.stat .lbl { color: var(--muted); font-size: .9rem; margin-top: .3rem; }

/* ---------- Connected banner ---------- */
.banner {
  display: flex; align-items: center; gap: 1rem; background: #fff;
  border: 1px solid var(--mist); border-left: 5px solid var(--teal);
  border-radius: 14px; padding: .9rem 1.2rem; margin-bottom: .6rem;
}
.banner .web { width: 38px; height: 38px; color: var(--teal); flex: none; }
.banner .web .n { fill: var(--brass); }
.banner .web .core { fill: var(--teal); }
.banner b { font-family: 'Bricolage Grotesque', sans-serif; color: var(--ink); }
.banner span { color: var(--muted); font-size: .92rem; word-break: break-all; }

/* ---------- Chat ---------- */
div[data-testid="stChatMessage"] {
  background: #fff; border: 1px solid var(--mist); border-radius: 16px; padding: 1rem 1.2rem;
}
div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
  background: var(--ink); border-color: var(--ink);
}
div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) * { color: #fff; }
div[data-testid="stChatInput"] { border-radius: 16px; }
.typing { display: flex; align-items: center; gap: .35rem; color: var(--muted); }
.typing span {
  width: 8px; height: 8px; border-radius: 50%; background: var(--brass);
  animation: bounce 1.1s infinite ease-in-out;
}
.typing span:nth-child(2) { animation-delay: .15s; }
.typing span:nth-child(3) { animation-delay: .3s; }
.typing em { margin-left: .5rem; font-style: normal; font-size: .92rem; }
@keyframes bounce { 0%, 80%, 100% { transform: translateY(0); opacity: .5; } 40% { transform: translateY(-6px); opacity: 1; } }

/* ---------- Web graphic animation ---------- */
.web .n { fill: var(--brass); transform-box: fill-box; transform-origin: center; animation: pulse 2.4s infinite ease-in-out; }
.web .n2 { animation-delay: .4s; } .web .n3 { animation-delay: .8s; }
.web .n4 { animation-delay: 1.2s; } .web .n5 { animation-delay: 1.6s; } .web .n6 { animation-delay: 2s; }
.web .core { fill: var(--ink); }
@keyframes pulse { 0%, 100% { transform: scale(1); opacity: .75; } 50% { transform: scale(1.5); opacity: 1; } }

/* ---------- Full-screen overlays (splash + crawl loader) ---------- */
.overlay {
  position: fixed; inset: 0; z-index: 999999; display: flex; align-items: center; justify-content: center;
  background: var(--ink); color: #fff; flex-direction: column; text-align: center; padding: 2rem;
}
.overlay .web { width: 150px; height: 150px; color: #2f6a63; }
.overlay .web .n { fill: var(--brass); }
.overlay .web .core { fill: #fff; }
.overlay .web .links { animation: spin 18s linear infinite; transform-origin: 100px 100px; }
@keyframes spin { to { transform: rotate(360deg); } }
.overlay h2 { color: #fff; font-size: 2.4rem; margin: 1rem 0 .2rem; font-weight: 800; }
.overlay p.sub { color: #9fbfb8; margin: 0; }
.splash { animation: splash-out .5s ease 1.4s forwards; }
@keyframes splash-out { to { opacity: 0; visibility: hidden; } }

.stage-list { list-style: none; padding: 0; margin: 1.6rem 0 0; text-align: left; min-width: 320px; }
.stage-list li { display: flex; align-items: center; gap: .8rem; padding: .45rem 0; color: #6f918a; font-size: 1rem; }
.stage-list li i { width: 12px; height: 12px; border-radius: 50%; border: 2px solid #3d6a62; flex: none; }
.stage-list li.done { color: #bfd8d2; }
.stage-list li.done i { background: #4fe0b0; border-color: #4fe0b0; }
.stage-list li.active { color: #fff; font-weight: 600; }
.stage-list li.active i { border-color: var(--brass); background: var(--brass); animation: pulse 1.2s infinite; }
.stage-list small { display: block; font-weight: 400; color: #9fbfb8; font-size: .82rem; }
.elapsed { margin-top: 1.4rem; color: #7ea39b; font-size: .88rem; }

@media (max-width: 760px) {
  .hero { grid-template-columns: 1fr; padding: 1.8rem; }
  .hero .web { display: none; }
  .steps, .stats { grid-template-columns: 1fr; }
}
@media (prefers-reduced-motion: reduce) {
  .web .n, .typing span, .overlay .web .links, .stage-list li.active i { animation: none; }
}
</style>
"""

render(STYLE)


# --------------------------------------------------
# Session state
# --------------------------------------------------

defaults = {
    "splash_done": False,
    "website_indexed": False,
    "website_url": "",
    "messages": [],
    "index_stats": {},
    "pending_question": None,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# --------------------------------------------------
# Splash screen (first load only)
# --------------------------------------------------

if not st.session_state.splash_done:
    splash = st.empty()
    render(
        f"""
        <div class="overlay splash">
          {WEB_SVG}
          <h2>ChatAMU</h2>
          <p class="sub">Warming up the crawler</p>
        </div>
        """,
        splash,
    )
    time.sleep(1.8)
    splash.empty()
    st.session_state.splash_done = True


# --------------------------------------------------
# Crawl loading screen
# --------------------------------------------------

# The backend call is a single blocking request, so these stages are
# time-based estimates of what is happening, not live progress.
CRAWL_STAGES = [
    ("Crawling pages", "Following links within the website"),
    ("Reading PDFs", "Extracting text from linked documents"),
    ("Cutting into chunks", "Splitting content into searchable passages"),
    ("Creating embeddings", "Storing the passages in the vector database"),
]
SECONDS_PER_STAGE = 7


def run_with_loader(url: str):
    """Run create_website in a worker thread while a full-screen
    loader animates in the main thread."""
    slot = st.empty()
    start = time.time()

    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(create_website, url)

        while not future.done():
            elapsed = time.time() - start
            active = min(int(elapsed // SECONDS_PER_STAGE), len(CRAWL_STAGES) - 1)

            items = []
            for i, (label, detail) in enumerate(CRAWL_STAGES):
                state = "done" if i < active else "active" if i == active else ""
                small = f"<small>{detail}</small>" if i == active else ""
                items.append(f'<li class="{state}"><i></i><div>{label}{small}</div></li>')

            render(
                f"""
                <div class="overlay">
                  {WEB_SVG}
                  <h2>Reading your website</h2>
                  <p class="sub">Larger sites can take a few minutes. Keep this tab open.</p>
                  <ul class="stage-list">{''.join(items)}</ul>
                  <div class="elapsed">{int(elapsed)}s elapsed</div>
                </div>
                """,
                slot,
            )
            time.sleep(0.5)

        try:
            return future.result()
        finally:
            slot.empty()


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:
    render(f'<div class="brand">{WEB_SVG}<span>ChatAMU</span></div>')

    if st.session_state.website_indexed:
        render('<div class="status-pill on"><i></i>Website connected</div>')
        render(f'<div class="site-url">{st.session_state.website_url}</div>')

        if st.button("Clear conversation"):
            st.session_state.messages = []
            st.rerun()

        if st.button("Connect a different website"):
            st.session_state.website_indexed = False
            st.session_state.website_url = ""
            st.session_state.messages = []
            st.session_state.index_stats = {}
            st.rerun()
    else:
        render('<div class="status-pill"><i></i>No website connected</div>')
        render(
            '<div class="site-url">Paste a URL on the main page to get started.</div>'
        )


# --------------------------------------------------
# Landing view: hero + website form
# --------------------------------------------------

if not st.session_state.website_indexed:

    render(
        f"""
        <div class="hero">
          <div>
            <h1>Give it a website. Ask it anything.</h1>
            <p>ChatAMU reads every page and PDF, then answers questions from what it finds.</p>
          </div>
          {WEB_SVG}
        </div>
        <div class="steps">
          <div class="step"><b>Crawl</b><p>Follows links across the site and its documents.</p></div>
          <div class="step"><b>Index</b><p>Turns the content into searchable passages.</p></div>
          <div class="step"><b>Chat</b><p>Ask in plain language and get answers from the site.</p></div>
        </div>
        """
    )

    with st.form("website_form"):
        website_url = st.text_input(
            "Website URL",
            placeholder="https://example.com",
        )
        submit_website = st.form_submit_button(
            "Crawl and index website",
            type="primary",
        )

    if submit_website:
        if not website_url.strip():
            st.warning("Enter a website URL to continue.")
        else:
            try:
                result = run_with_loader(website_url.strip())

                st.session_state.website_indexed = True
                st.session_state.website_url = result["website_url"]
                st.session_state.messages = []
                st.session_state.index_stats = {
                    "message": result["message"],
                    "Web pages": result["web_pages_processed"],
                    "PDFs": result["pdfs_processed"],
                    "Chunks": result["chunks_indexed"],
                }
                st.rerun()

            except Exception as exc:
                st.error(f"Indexing failed: {exc}. Check the URL and try again.")


# --------------------------------------------------
# Chat view
# --------------------------------------------------

else:

    render(
        f"""
        <div class="banner">
          {WEB_SVG}
          <div><b>Connected</b><br><span>{st.session_state.website_url}</span></div>
        </div>
        """
    )

    stats = st.session_state.index_stats
    if stats:
        render(
            f"""
            <div class="stats">
              <div class="stat"><div class="num">{stats['Web pages']}</div><div class="lbl">Web pages read</div></div>
              <div class="stat"><div class="num">{stats['PDFs']}</div><div class="lbl">PDFs read</div></div>
              <div class="stat"><div class="num">{stats['Chunks']}</div><div class="lbl">Passages indexed</div></div>
            </div>
            """
        )

    # Starter questions for an empty conversation
    if not st.session_state.messages:
        st.markdown("#### Try asking")
        starters = [
            "What is this website about?",
            "Summarize the main sections of the site.",
            "Which documents or PDFs are available?",
        ]
        cols = st.columns(len(starters))
        for col, text in zip(cols, starters):
            if col.button(text, use_container_width=True, key=f"starter_{text}"):
                st.session_state.pending_question = text
                st.rerun()

    # Previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("sources"):
                with st.expander("Sources"):
                    for source in message["sources"]:
                        st.markdown(f"- {source}")

    # Input (typed or from a starter button)
    question = st.chat_input("Ask something about this website...")
    if st.session_state.pending_question:
        question = st.session_state.pending_question
        st.session_state.pending_question = None

    if question:
        st.session_state.messages.append({"role": "user", "content": question})

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            slot = st.empty()
            render(
                """
                <div class="typing"><span></span><span></span><span></span><em>Searching the website</em></div>
                """,
                slot,
            )

            try:
                result = ask_question(question)
                answer = result["answer"]

                raw_sources = result.get("sources") or []
                sources = [
                    s.get("url", str(s)) if isinstance(s, dict) else str(s)
                    for s in raw_sources
                ]

                slot.markdown(answer)

                if sources:
                    with st.expander("Sources"):
                        for source in sources:
                            st.markdown(f"- {source}")

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer, "sources": sources}
                )

            except Exception as exc:
                slot.empty()
                st.error(f"The answer could not be generated: {exc}")
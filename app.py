import streamlit as st

from travel_ai import chat_with_concierge, generate_travel_plan

st.set_page_config(
    page_title="WANDERLUX — Bespoke Travel",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_plan" not in st.session_state:
    st.session_state.current_plan = None
if "concierge_open" not in st.session_state:
    st.session_state.concierge_open = False


def _on_concierge_dismiss() -> None:
    st.session_state.concierge_open = False


@st.dialog(
    "✦ Luxury Concierge",
    width="large",
    on_dismiss=_on_concierge_dismiss,
)
def concierge_dialog() -> None:
    st.caption("Ask about destinations, budgets, packing, or tweaks to your plan.")
    if st.button("Clear chat", key="clear_chat"):
        st.session_state.messages = []
        st.rerun()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask your concierge…", key="chat_input_concierge"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.spinner("Consulting…"):
            reply = chat_with_concierge(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()


# CSS — padded page, full-bleed hero, planner row top-aligned, scrollable plan
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;500&display=swap');
#MainMenu, footer {visibility:hidden !important;}
/* Remove reserved space from hidden chrome (black bar at top) */
[data-testid="stHeader"] {
  display: none !important;
  height: 0 !important;
  min-height: 0 !important;
  margin: 0 !important;
  padding: 0 !important;
  border: none !important;
  overflow: hidden !important;
}
[data-testid="stToolbar"] {display:none !important; height:0 !important; min-height:0 !important;}
[data-testid="stDecoration"] {display:none !important;}
[data-testid="stAppViewContainer"] {
  background:#030303 !important;
  padding-top: 0 !important;
}
.stApp > header + div,
.stApp [data-testid="stMain"] {
  padding-top: 0 !important;
}
[data-testid="stMain"] > div {
  padding-top: 0 !important;
  margin-top: 0 !important;
}
.block-container {
  padding-left: clamp(1rem, 4vw, 2.75rem) !important;
  padding-right: clamp(1rem, 4vw, 2.75rem) !important;
  padding-top: 0 !important;
  max-width: 1320px !important;
  margin: 0 auto !important;
}
.hero {
  position:relative; width:100vw; min-height:92vh; overflow:hidden;
  left:50%; transform:translateX(-50%); max-width:100vw;
  background:#000;
  box-shadow: inset 0 -1px 0 rgba(201,169,110,0.12);
}
.hero video {position:absolute; inset:0; width:100%; height:100%; object-fit:cover; z-index:0;}
.hero-overlay {position:absolute; inset:0; z-index:1; background:linear-gradient(180deg,rgba(0,0,0,0.2) 0%,rgba(0,0,0,0.88) 75%,#030303 100%);}
.hero-content {position:relative; z-index:2; text-align:center; max-width:900px; margin:0 auto; padding:16vh 1.5rem 7vh;}
.eyebrow {font-family:'Inter',sans-serif; font-size:0.82rem; letter-spacing:0.22em; color:rgba(201,169,110,0.95); text-transform:uppercase; margin-bottom:1.75rem;}
.hero-title {font-family:'Playfair Display',serif; font-size:clamp(3rem,10vw,7rem); font-weight:700; line-height:0.95; background:linear-gradient(120deg,#fff 0%,#f0e6d8 40%,#C9A96E 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin:0 0 1.5rem 0; filter:drop-shadow(0 4px 24px rgba(0,0,0,0.5));}
.hero-subtitle {font-family:'Inter',sans-serif; font-size:1.2rem; color:rgba(255,255,255,0.86); margin:0; font-weight:300; letter-spacing:0.02em;}
.main {background:linear-gradient(180deg,#030303 0%,#060606 40%,#050505 100%); padding:72px 0 96px;}
.section-title-wrap {text-align:center; margin-bottom:2.75rem;}
.section-title {font-family:'Playfair Display',serif; font-size:clamp(1.85rem,4vw,2.6rem); color:#d4b87a; margin:0; letter-spacing:0.02em;}
.section-rule {width:120px; height:1px; margin:1.25rem auto 0; background:linear-gradient(90deg,transparent,rgba(201,169,110,0.55),transparent);}
/*
  Planner row: right column is position:absolute with top/bottom aligned to this row.
  Row height = left column only (trip details + buttons), so long plans do NOT grow the page.
  Plan scrolls only inside the right box.
*/
[data-testid="stHorizontalBlock"]:has(.panel) {
  position: relative !important;
  align-items: flex-start !important;
  overflow: visible !important;
  /* room for absolute right column (matches ~1 : 1.45 column ratio + gap) */
  padding-right: 0 !important;
  min-height: 12rem;
}
[data-testid="stHorizontalBlock"]:has(.panel) > div[data-testid="column"]:first-child {
  flex: 0 0 40% !important;
  max-width: 41% !important;
  width: 41% !important;
  position: relative !important;
  z-index: 2 !important;
}
[data-testid="stHorizontalBlock"]:has(.panel) > div[data-testid="column"]:last-child {
  position: absolute !important;
  top: 0 !important;
  bottom: 0 !important;
  right: 0 !important;
  left: calc(41% + 1.75rem) !important;
  width: auto !important;
  flex: none !important;
  max-width: none !important;
  display: flex !important;
  flex-direction: column !important;
  min-height: 0 !important;
  z-index: 1 !important;
}
.panel {
  background:linear-gradient(165deg,rgba(255,255,255,0.04) 0%,rgba(255,255,255,0.01) 100%);
  border:1px solid rgba(201,169,110,0.22);
  border-radius:22px;
  padding:2rem 2.25rem 2.25rem;
  backdrop-filter:blur(24px);
  box-shadow:0 24px 64px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.06);
}
[data-testid="stHorizontalBlock"]:has(.panel) > div[data-testid="column"]:last-child [data-testid="stVerticalBlock"] {
  flex: 1 1 auto !important;
  min-height: 0 !important;
  height: 100% !important;
  max-height: none !important;
  background:linear-gradient(180deg,rgba(18,18,18,0.98) 0%,rgba(8,8,8,0.99) 100%);
  border:1px solid rgba(201,169,110,0.18);
  border-radius:22px;
  padding:2rem 2.25rem;
  box-shadow:0 24px 64px rgba(0,0,0,0.5), inset 0 1px 0 rgba(201,169,110,0.06);
  overflow-y: auto !important;
  overflow-x: hidden !important;
  scrollbar-width: thin;
  scrollbar-color:rgba(201,169,110,0.35) rgba(255,255,255,0.04);
}
[data-testid="stHorizontalBlock"]:has(.panel) > div[data-testid="column"]:last-child [data-testid="stVerticalBlock"]::-webkit-scrollbar {width:8px;}
[data-testid="stHorizontalBlock"]:has(.panel) > div[data-testid="column"]:last-child [data-testid="stVerticalBlock"]::-webkit-scrollbar-track {background:rgba(255,255,255,0.03); border-radius:8px;}
[data-testid="stHorizontalBlock"]:has(.panel) > div[data-testid="column"]:last-child [data-testid="stVerticalBlock"]::-webkit-scrollbar-thumb {background:rgba(201,169,110,0.35); border-radius:8px;}
[data-testid="stHorizontalBlock"]:has(.panel) > div[data-testid="column"]:last-child [data-testid="stVerticalBlock"]::-webkit-scrollbar-thumb:hover {background:rgba(201,169,110,0.5);}
@media (max-width: 900px) {
  [data-testid="stHorizontalBlock"]:has(.panel) > div[data-testid="column"]:first-child {
    flex: 1 1 auto !important;
    max-width: 100% !important;
    width: 100% !important;
  }
  [data-testid="stHorizontalBlock"]:has(.panel) > div[data-testid="column"]:last-child {
    position: relative !important;
    left: auto !important;
    right: auto !important;
    top: auto !important;
    bottom: auto !important;
    width: 100% !important;
    margin-top: 1.25rem !important;
    min-height: min(60vh, 420px) !important;
  }
  [data-testid="stHorizontalBlock"]:has(.panel) > div[data-testid="column"]:last-child [data-testid="stVerticalBlock"] {
    max-height: min(60vh, 480px) !important;
  }
}
.label {font-family:'Inter',sans-serif !important; font-size:0.8rem !important; color:#c9a96e !important; text-transform:uppercase !important; letter-spacing:0.12em !important;}
.footer-bar {margin-top:2.5rem; padding-top:1.5rem; border-top:1px solid rgba(201,169,110,0.1);}
</style>
""",
    unsafe_allow_html=True,
)

# HERO
st.markdown(
    """
<div class="hero">
    <video autoplay loop muted playsinline preload="auto">
        <source src="https://res.cloudinary.com/dobretz2v/video/upload/v1776785425/travel_xgn6gi.mp4" type="video/mp4">
    </video>
    <div class="hero-overlay"></div>
    <div class="hero-content">
        <div class="eyebrow">✦ WANDERLUX ✦ BESPOKE TRAVEL</div>
        <h1 class="hero-title">Discover<br><span style="font-style:italic; font-weight:400;">Your</span><br>Journey</h1>
        <p class="hero-subtitle">Extraordinary trips shaped around your days and your budget</p>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="main">', unsafe_allow_html=True)
st.markdown(
    """
<div class="section-title-wrap">
  <h2 class="section-title">✦ Plan Your Trip ✦</h2>
  <div class="section-rule"></div>
</div>
""",
    unsafe_allow_html=True,
)

left, right = st.columns([1, 1.45], gap="large")

with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(
        '<div class="eyebrow" style="margin-bottom:1.1rem;">Trip details</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h3 style=\"font-family:'Playfair Display',serif; font-size:1.55rem; color:#F5F0E8; margin:0 0 1.1rem 0;\">Where are you going?</h3>",
        unsafe_allow_html=True,
    )

    destination = st.text_input(
        "Destination",
        placeholder="Paris • Bali • Tokyo • Rome",
        label_visibility="collapsed",
        key="dest",
    )

    st.markdown('<div class="label">Trip length</div>', unsafe_allow_html=True)
    days = st.slider(
        "Days",
        1,
        21,
        7,
        format="%d days",
        label_visibility="collapsed",
        key="days_sl",
    )

    st.markdown('<div class="label" style="margin-top:0.85rem;">Budget</div>', unsafe_allow_html=True)
    budget = st.selectbox(
        "Budget",
        [
            "Budget — hostels, transit, street food",
            "Moderate — mid hotels & mix of dining",
            "Comfort — nicer stays & sit-down meals",
            "Luxury — high-end hotels & experiences",
            "Ultra — best-in-class, private where it fits",
        ],
        index=2,
        label_visibility="collapsed",
        key="budget_sel",
    )

    st.markdown('<div style="height:1.35rem;"></div>', unsafe_allow_html=True)

    gen = st.button("✦ Generate travel plan", use_container_width=True, key="gen")
    con = st.button("✦ Open concierge chat", use_container_width=True, key="con")

    if gen:
        if destination.strip():
            with st.spinner("Crafting your itinerary…"):
                st.session_state.current_plan = generate_travel_plan(
                    destination.strip(), days, budget
                )
            st.rerun()
        else:
            st.error("Enter a destination first.")

    if con:
        st.session_state.concierge_open = True

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    # Scroll + border are applied via CSS on this column's stVerticalBlock (wrapping all blocks below).
    if st.session_state.current_plan:
        st.markdown(
            '<div class="eyebrow" style="margin-bottom:0.85rem;">Your itinerary</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<h2 style="font-family:\'Playfair Display\',serif; font-size:1.65rem; color:#C9A96E; margin-bottom:1.1rem;">✦ Travel plan ✦</h2>',
            unsafe_allow_html=True,
        )
        st.markdown(st.session_state.current_plan)
    else:
        st.markdown(
            """
<div style="text-align:center; padding:3rem 1rem 2.5rem; color:rgba(201,169,110,0.35);">
  <div style="font-size:4.5rem; margin-bottom:0.75rem; opacity:0.85;">✦</div>
  <h3 style="font-family:'Playfair Display',serif; font-size:1.55rem; color:rgba(245,240,232,0.5); margin:0 0 0.6rem 0;">Your plan appears here</h3>
  <p style="font-size:1rem; color:rgba(255,255,255,0.35);">Enter a destination and tap <strong style="color:rgba(201,169,110,0.65);">Generate travel plan</strong></p>
</div>
""",
            unsafe_allow_html=True,
        )

st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="footer-bar"></div>', unsafe_allow_html=True)
_, fab = st.columns([3, 1])
with fab:
    if st.button("Concierge ✦", use_container_width=True, key="con_footer"):
        st.session_state.concierge_open = True

if st.session_state.concierge_open:
    concierge_dialog()

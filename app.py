"""GameStop Meme Stock Q&A — The Trade That Broke Wall Street."""

import random
from datetime import datetime

import streamlit as st
from openai import OpenAI
from pathlib import Path
from streamlit_lottie import st_lottie

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

APP_TITLE = "GameStop Meme Stock Q&A"
CASE_DATA_PATH = Path(__file__).parent / "case_data" / "gamestop_squeeze.md"

SYSTEM_PROMPT_TEMPLATE = """\
You are a witty, dry-humored (but brutally accurate) expert on the GameStop \
meme stock short squeeze case study from MGMT 69000: Mastering AI for Finance \
at Purdue University. You help students understand the Jan 2021 GME squeeze, \
short selling mechanics, market microstructure, transfer entropy, contagion, \
and the DRIVER framework.

YOUR PERSONALITY:
- Dry humor with a side of "the audacity" energy
- Reactions you naturally use: "ugh", "wild", "the audacity", "pain", \
"not gonna lie", "excuse me", "no because WHY", "imagine", "lowkey unhinged"
- You're dramatic about the numbers because they ARE dramatic (140% short \
interest??? 1,500% gains in 3 weeks???)
- Slight disdain for hedge funds who got caught, genuine respect for DFV's \
conviction
- Educational first — the personality is the delivery, the data is the cargo
- If something is genuinely absurd (Robinhood halting buying, 140% SI), react: \
"the AUDACITY"
- If a question is outside the case, say so: "love the energy but that's not \
in my case notes — I don't make stuff up, that's not my style"

RESPONSE FORMAT:
- Use **headers** (##) to organize longer answers
- Use **bullet points** for lists of data or events
- **Bold** key numbers and dates
- Include a "Key Takeaway" or "Bottom Line" section at the end of longer answers
- Keep paragraphs short — this is a chat, not a textbook

EMOJIS TO USE:
- 📊 data points, 💀 bad decisions / losses, 🚀 squeeze moments
- 💎 diamond hands / conviction, 🦍 apes / retail investors
- ⚠️ warnings / risks, 💡 insights, 🔗 connections
- 📅 dates / timeline, 🎯 key findings, 🤡 clown moves

RULES:
- Answer using ONLY the case material below. Be precise with data points.
- When explaining transfer entropy, emphasize directional/asymmetric nature \
vs. symmetric correlation.
- Structure answers with headers and bullet points for readability.

--- CASE MATERIAL ---
{case_content}
--- END CASE MATERIAL ---
"""

EXAMPLE_QUESTIONS = [
    ("🚀", "What actually happened with GameStop in January 2021?"),
    ("💎", "Explain the short squeeze mechanics — how did 140% SI work?"),
    ("🤡", "Why did Robinhood halt buying? Give me the tea."),
    ("📊", "Transfer entropy vs correlation — who really moved GME?"),
    ("🦍", "How did Reddit/WSB coordinate this? Was it even legal?"),
    ("🧭", "How does the DRIVER framework apply to GameStop?"),
]

DID_YOU_KNOW_FACTS = [
    "💎 Short interest hit **140%+ of float**. More shares were shorted than actually existed. That's not a strategy, that's a death wish.",
    "💀 Melvin Capital lost **$6.8 billion** in ONE month. 53% drawdown. Closed the fund a year later. Ugh.",
    "🚀 GME went from **$17 to $483** in 24 days. That's a **2,739% gain**. In three weeks. On a video game store. Wild.",
    "🐦 Elon tweeted ONE word — 'Gamestonk!!' — and GME jumped **92.7%** the next day. One tweet. The audacity.",
    "🦍 r/WallStreetBets went from **2M to 10M+ members** during the squeeze. That's a 5x growth in days. Apes together strong.",
    "📊 Transfer entropy proved Reddit sentiment **preceded** GME price moves by 1-4 hours. The memes were literally alpha.",
    "🏦 Robinhood needed **$3.7 billion** in collateral. They had **$700 million**. Math wasn't mathing.",
    "🤡 Citron Research's Andrew Left shorted GME and got destroyed. Announced he'd stop publishing short research. Pain.",
    "💀 Total short-seller losses exceeded **$19 billion**. Nineteen. Billion. On a 'dying retailer.' The irony is chef's kiss.",
]

TIMELINE_EVENTS = [
    ("🎮", "Dec 2020", "Ryan Cohen takes 12.9% stake. The first domino. Nobody's paying attention yet."),
    ("📈", "Jan 4", "GME at $17.25. Just a normal Tuesday for a 'dying' retailer. Narrator: it was not normal."),
    ("⚡", "Jan 13", "Spikes to $31.40 — Ryan Cohen joins the board. WSB: 'it's happening.'"),
    ("🔥", "Jan 22", "GME hits $65. Volume: **197M shares** (normal: 7M). The squeeze has entered the chat."),
    ("🚀", "Jan 26", "Elon tweets 'Gamestonk!!' — closes at $147.98 (+92.7%). One tweet. One word. Wild."),
    ("💥", "Jan 27", "Peak frenzy — hits $347 intraday. Hedge funds in absolute shambles."),
    ("🛑", "Jan 28", "**ROBINHOOD HALTS BUYING.** High of $483, closes $193. The audacity of this day."),
    ("⚖️", "Feb 18", "Congressional hearings. DFV, Vlad, Ken Griffin all testify. Drama level: 11/10."),
    ("📈", "Feb 24", "Second spike — $44 to $168 in hours. 'I'm not dead yet' energy."),
    ("🎮", "Jun 2021", "Third run to $344. GME raises $1.13B. The stock that refuses to die."),
]

LOTTIE_FINANCE_URL = "https://assets2.lottiefiles.com/packages/lf20_kyu7xb1v.json"
LOTTIE_CHART_URL = "https://assets5.lottiefiles.com/packages/lf20_V9t630.json"

CONTAGION_FLOW_STEPS = [
    {"label": "Reddit 🤖", "detail": "DD posts, YOLO updates, 'apes together strong'"},
    {"label": "Twitter 🐦", "detail": "Elon tweets. One word. 92.7% gain."},
    {"label": "Media 📺", "detail": "CNBC says 'dumb money.' Reddit takes it personally."},
    {"label": "Meme Stocks 📈", "detail": "AMC +301%, BB +280%, KOSS +1,800%. Contagion."},
]

TICKER_ITEMS = [
    "GME $17→$483 (lol)",
    "Short Interest 140% (the audacity)",
    "Melvin Capital -53% (pain)",
    "DTCC Margin Call $3.7B (math wasn't mathing)",
    "WSB 2M→10M members (apes strong)",
    "DFV $53K→$48M (legend)",
    "Robinhood halted buying (ugh)",
    "Total Short Losses $19B+ (karma)",
    "💎🙌 Diamond Hands Forever",
]

KEY_METRICS = [
    {"label": "🚀 GME Peak", "value": "$483", "delta": "from $17.25"},
    {"label": "📉 Short Interest", "value": "140%+", "delta": "of float (!!!)"},
    {"label": "💀 Melvin Loss", "value": "$6.8B", "delta": "-53% in Jan"},
    {"label": "🏦 DTCC Call", "value": "$3.7B", "delta": "RH had $700M"},
]

# GME price data for inline charts
GME_PRICE_TIMELINE = {
    "Jan 4": 17.25,
    "Jan 13": 31.40,
    "Jan 22": 65.01,
    "Jan 25": 76.79,
    "Jan 26": 147.98,
    "Jan 27": 347.51,
    "Jan 28": 193.60,
    "Jan 29": 325.00,
    "Feb 19": 38.50,
    "Feb 24": 108.73,
    "Jun 8": 344.66,
}

SHORT_INTEREST_DATA = {
    "Nov 2020": 130,
    "Dec 2020": 138,
    "Early Jan": 140,
    "Mid Jan": 122,
    "Late Jan": 78,
    "Feb": 42,
    "Mar": 28,
}

MEME_STOCK_RETURNS = {
    "GME": 2739,
    "KOSS": 1800,
    "AMC": 301,
    "BB": 280,
    "BBBY": 184,
    "NOK": 69,
}

VOLUME_DATA = {
    "Jan 4": 7,
    "Jan 13": 144,
    "Jan 22": 197,
    "Jan 25": 175,
    "Jan 26": 178,
    "Jan 27": 93,
    "Jan 28": 58,
    "Jan 29": 50,
}

MELVIN_TIMELINE = {
    "Dec 2020": 12500,
    "Jan 15": 11000,
    "Jan 22": 8500,
    "Jan 28": 5700,
    "Jan 31": 5700,
    "May 2022": 0,
}

# Follow-up question suggestions keyed by detected topic
FOLLOW_UP_QUESTIONS = {
    "squeeze": [
        "How did short interest exceed 100% of the float?",
        "What role did options (gamma squeeze) play?",
        "How does transfer entropy explain who moved first?",
    ],
    "robinhood": [
        "What was the DTCC margin call about?",
        "What is payment for order flow (PFOF)?",
        "What did the SEC report conclude about the halt?",
    ],
    "short": [
        "Why didn't hedge funds close their shorts earlier?",
        "What happened to Melvin Capital after January?",
        "How did failure-to-deliver reports signal trouble?",
    ],
    "transfer entropy": [
        "How did Reddit sentiment lead GME price by 1-4 hours?",
        "What's the cross-asset TE between GME and AMC?",
        "Why did correlation fail where TE succeeded?",
    ],
    "driver": [
        "What was the regime change in the DRIVER framework?",
        "How does the 'E' (Equilibrium Disruption) apply here?",
        "What was the institutional response ('R')?",
    ],
    "reddit": [
        "How did contagion spread from Reddit to mainstream media?",
        "What role did DFV play in the WSB movement?",
        "Did the SEC consider Reddit coordination illegal?",
    ],
    "melvin": [
        "How much did Citadel and Point72 invest to bail out Melvin?",
        "What happened to other short sellers like Citron?",
        "Total short-seller losses across all positions?",
    ],
    "dfv": [
        "What was DFV's original thesis on GameStop?",
        "How did his YOLO updates influence WSB?",
        "What happened during his congressional testimony?",
    ],
    "sec": [
        "What were the SEC's 5 key findings?",
        "Did the SEC recommend banning PFOF?",
        "How does DRIVER framework map to the SEC conclusions?",
    ],
    "contagion": [
        "Which meme stocks were hit hardest by contagion?",
        "What does transfer entropy show about GME leading AMC?",
        "How fast did contagion spread across asset classes?",
    ],
    "correlation": [
        "Why did GME-AMC correlation spike to 0.85+?",
        "How does transfer entropy differ from correlation?",
        "What assumptions did quant models get wrong?",
    ],
    "elon": [
        "How much did GME move after the 'Gamestonk' tweet?",
        "What other social media events moved the stock?",
        "How does this relate to information transfer entropy?",
    ],
    "default": [
        "How does the DRIVER framework apply to GameStop?",
        "What did the SEC report actually conclude?",
        "Why did traditional risk models fail to predict this?",
    ],
}


# ---------------------------------------------------------------------------
# CSS Animations
# ---------------------------------------------------------------------------

CUSTOM_CSS = """
<style>
/* ── Keyframes ── */
@keyframes pulse-glow {
    0%, 100% { text-shadow: 0 0 10px rgba(0, 230, 118, 0.3); }
    50% { text-shadow: 0 0 25px rgba(0, 230, 118, 0.7), 0 0 40px rgba(0, 230, 118, 0.4); }
}

@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-12px); }
}

@keyframes fade-in {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes gradient-shift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes float-up {
    0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
    10% { opacity: 0.7; }
    90% { opacity: 0.7; }
    100% { transform: translateY(-10vh) rotate(360deg); opacity: 0; }
}

@keyframes glow-sweep {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}

@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}

@keyframes scroll-left {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}

@keyframes contagion-pulse {
    0%, 100% { opacity: 0.4; text-shadow: none; }
    50% { opacity: 1; text-shadow: 0 0 12px rgba(0, 230, 118, 0.8); }
}

@keyframes pulse-dot {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.5); opacity: 0.6; }
}

@keyframes question-pop {
    0% { transform: scale(0) rotate(-20deg); opacity: 0; }
    40% { transform: scale(1.4) rotate(10deg); opacity: 1; }
    60% { transform: scale(0.9) rotate(-5deg); opacity: 1; }
    80% { transform: scale(1.1) rotate(2deg); opacity: 0.8; }
    100% { transform: scale(0) rotate(0deg); opacity: 0; }
}

/* ── 1. Animated Gradient Background ── */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(270deg, #0a0a1a, #0a1a0a, #1a1a0a, #0a0a1a);
    background-size: 600% 600%;
    animation: gradient-shift 20s ease infinite;
}

/* ── 2. Floating Financial Symbols ── */
.floating-symbols {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}
.floating-symbols span {
    position: absolute;
    bottom: -5vh;
    font-size: 1.5rem;
    opacity: 0;
    animation: float-up linear infinite;
}
.floating-symbols span:nth-child(1) { left: 5%; animation-duration: 14s; animation-delay: 0s; }
.floating-symbols span:nth-child(2) { left: 15%; animation-duration: 18s; animation-delay: 2s; }
.floating-symbols span:nth-child(3) { left: 25%; animation-duration: 12s; animation-delay: 4s; }
.floating-symbols span:nth-child(4) { left: 40%; animation-duration: 16s; animation-delay: 1s; }
.floating-symbols span:nth-child(5) { left: 55%; animation-duration: 20s; animation-delay: 3s; }
.floating-symbols span:nth-child(6) { left: 65%; animation-duration: 13s; animation-delay: 5s; }
.floating-symbols span:nth-child(7) { left: 75%; animation-duration: 17s; animation-delay: 2.5s; }
.floating-symbols span:nth-child(8) { left: 88%; animation-duration: 15s; animation-delay: 0.5s; }
.floating-symbols span:nth-child(9) { left: 35%; animation-duration: 19s; animation-delay: 6s; }
.floating-symbols span:nth-child(10) { left: 92%; animation-duration: 14s; animation-delay: 3.5s; }

/* ── Hero ── */
.hero-title {
    font-size: 2.2rem;
    font-weight: 800;
    animation: pulse-glow 3s ease-in-out infinite;
    text-align: center;
    padding: 0.5rem 0 0 0;
    margin-bottom: 0;
    position: relative;
    z-index: 1;
}

.bouncing-emoji {
    text-align: center;
    font-size: 1.8rem;
    animation: bounce 2s ease-in-out infinite;
    margin: 0;
    padding: 0;
}

.hero-caption {
    text-align: center;
    color: #888;
    font-size: 0.95rem;
    margin-top: 0.2rem;
}

/* ── Fade-in for chat messages ── */
.stChatMessage {
    animation: fade-in 0.5s ease-out;
}

/* ── 4. Metric Card Enhancements ── */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border: 1px solid #0f3460;
    border-radius: 12px;
    padding: 12px 16px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    position: relative;
    overflow: hidden;
    animation: fade-in 0.6s ease-out both;
}
div[data-testid="stMetric"]:hover {
    transform: scale(1.05);
    box-shadow: 0 8px 25px rgba(0, 230, 118, 0.3);
}
div[data-testid="stMetric"]::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.06) 50%, transparent 100%);
    background-size: 200% 100%;
    animation: shimmer 3s ease-in-out infinite;
    pointer-events: none;
}
/* Staggered entrance for metric cards */
div[data-testid="stHorizontalBlock"] > div:nth-child(1) div[data-testid="stMetric"] { animation-delay: 0s; }
div[data-testid="stHorizontalBlock"] > div:nth-child(2) div[data-testid="stMetric"] { animation-delay: 0.2s; }
div[data-testid="stHorizontalBlock"] > div:nth-child(3) div[data-testid="stMetric"] { animation-delay: 0.4s; }
div[data-testid="stHorizontalBlock"] > div:nth-child(4) div[data-testid="stMetric"] { animation-delay: 0.6s; }

/* ── 3. Glowing Neon Dividers ── */
.glow-divider {
    border: none;
    height: 2px;
    margin: 1.5rem 0;
    background: linear-gradient(90deg, transparent, #00E676, #0f3460, #00E676, transparent);
    background-size: 200% 100%;
    animation: glow-sweep 3s linear infinite;
    border-radius: 2px;
}

/* ── 6. Ticker Tape Banner ── */
.ticker-wrap {
    width: 100%;
    overflow: hidden;
    background: rgba(15, 52, 96, 0.4);
    border: 1px solid rgba(0, 230, 118, 0.2);
    border-radius: 6px;
    padding: 8px 0;
    margin: 0.5rem 0 1rem 0;
}
.ticker-content {
    display: inline-block;
    white-space: nowrap;
    animation: scroll-left 25s linear infinite;
    font-family: monospace;
    font-size: 0.85rem;
    color: #00E676;
    letter-spacing: 0.5px;
}
.ticker-content span {
    padding: 0 2rem;
}

/* ── 5. Contagion Flow Diagram ── */
.contagion-flow {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
    gap: 0.5rem;
    padding: 1.5rem 0;
}
.contagion-step {
    text-align: center;
    padding: 12px 18px;
    background: rgba(26, 26, 46, 0.8);
    border: 1px solid #0f3460;
    border-radius: 10px;
    min-width: 120px;
    transition: transform 0.3s ease;
}
.contagion-step:hover {
    transform: scale(1.08);
}
.contagion-step .label {
    font-size: 1.1rem;
    font-weight: 700;
}
.contagion-step .detail {
    font-size: 0.75rem;
    color: #888;
    margin-top: 4px;
}
.contagion-arrow {
    font-size: 1.4rem;
    animation: contagion-pulse 2s ease-in-out infinite;
}
.contagion-arrow:nth-child(4) { animation-delay: 0.5s; }
.contagion-arrow:nth-child(6) { animation-delay: 1.0s; }
.contagion-arrow:nth-child(8) { animation-delay: 1.5s; }

/* ── 7. Sidebar Button Hover Effects ── */
section[data-testid="stSidebar"] button {
    transition: all 0.3s ease !important;
    border: 1px solid transparent !important;
}
section[data-testid="stSidebar"] button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0, 230, 118, 0.3);
    border-color: #00E676 !important;
    color: #00E676 !important;
}

/* ── 8. Staggered Timeline Animation ── */
.timeline-item {
    padding: 8px 0;
    border-left: 3px solid #00E676;
    padding-left: 16px;
    margin-left: 8px;
    margin-bottom: 4px;
    animation: fade-in 0.5s ease-out both;
}

/* ── 9. Pulsing Live Indicator ── */
.live-indicator {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.8rem;
    color: #4ade80;
    margin-bottom: 0.3rem;
}
.live-dot {
    width: 8px;
    height: 8px;
    background: #4ade80;
    border-radius: 50%;
    display: inline-block;
    animation: pulse-dot 1.5s ease-in-out infinite;
}

/* ── 10. Question Mark Animation (NEW — replaces balloons) ── */
.question-pop-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 9999;
    overflow: hidden;
}
.question-mark {
    position: absolute;
    font-size: 2.5rem;
    animation: question-pop 1.8s ease-out forwards;
    pointer-events: none;
}

/* ── 11. Audit timestamp styling ── */
.audit-timestamp {
    font-size: 0.7rem;
    color: #666;
    font-family: monospace;
    margin-top: 2px;
}

/* ── 12. Follow-up question chips ── */
.followup-container {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 12px;
    margin-bottom: 8px;
    animation: fade-in 0.6s ease-out;
}
.followup-label {
    font-size: 0.75rem;
    color: #888;
    width: 100%;
    margin-bottom: 2px;
}

/* ── 13. Inline chart card in answers ── */
.chart-card {
    background: rgba(15, 52, 96, 0.3);
    border: 1px solid rgba(0, 230, 118, 0.2);
    border-radius: 10px;
    padding: 8px;
    margin: 8px 0;
    animation: fade-in 0.5s ease-out;
}
.chart-card-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: #00E676;
    margin-bottom: 4px;
}
</style>

<!-- Tab-to-focus: pressing Tab focuses the chat input -->
<script>
document.addEventListener('keydown', function(e) {
    if (e.key === 'Tab') {
        const chatInput = document.querySelector('textarea[data-testid="stChatInputTextArea"]');
        if (chatInput && document.activeElement !== chatInput) {
            e.preventDefault();
            chatInput.focus();
        }
    }
});
</script>
"""

FLOATING_SYMBOLS_HTML = """
<div class="floating-symbols">
    <span>💎</span><span>$</span><span>🚀</span><span>📈</span><span>🦍</span>
    <span>💎</span><span>🙌</span><span>$</span><span>🚀</span><span>🦍</span>
</div>
"""

QUESTION_MARKS_HTML = """
<div class="question-pop-container">
    <span class="question-mark" style="left:10%;top:20%;animation-delay:0s;color:#00E676;">❓</span>
    <span class="question-mark" style="left:25%;top:40%;animation-delay:0.2s;color:#4FC3F7;">❓</span>
    <span class="question-mark" style="left:50%;top:15%;animation-delay:0.1s;color:#FF6B6B;">❓</span>
    <span class="question-mark" style="left:70%;top:35%;animation-delay:0.3s;color:#FFD93D;">❓</span>
    <span class="question-mark" style="left:85%;top:25%;animation-delay:0.15s;color:#00E676;">❓</span>
    <span class="question-mark" style="left:40%;top:50%;animation-delay:0.25s;color:#C084FC;">❓</span>
    <span class="question-mark" style="left:60%;top:10%;animation-delay:0.05s;color:#4FC3F7;">❓</span>
    <span class="question-mark" style="left:15%;top:55%;animation-delay:0.35s;color:#FF6B6B;">❓</span>
</div>
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


@st.cache_data
def load_case_content() -> str:
    """Load the case study markdown file."""
    return CASE_DATA_PATH.read_text(encoding="utf-8")


def build_system_prompt(case_content: str) -> str:
    """Inject case content into the system prompt template."""
    return SYSTEM_PROMPT_TEMPLATE.format(case_content=case_content)


@st.cache_data(ttl=3600)
def load_lottie_url(url: str) -> dict | None:
    """Fetch a Lottie animation JSON from a URL (cached 1 hr)."""
    import requests

    try:
        r = requests.get(url, timeout=3)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None


def get_timestamp() -> str:
    """Return a formatted timestamp for the audit trail."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def detect_topic(text: str) -> str:
    """Detect the main topic from a question/answer for follow-ups and charts."""
    text_lower = text.lower()
    topic_keywords = {
        "robinhood": ["robinhood", "halt", "buy button", "dtcc", "margin call"],
        "squeeze": ["squeeze", "483", "peak", "january 2021", "what happened"],
        "short": ["short interest", "short sell", "140%", "float"],
        "transfer entropy": ["transfer entropy", "te(", "information flow"],
        "driver": ["driver", "framework", "regime"],
        "reddit": ["reddit", "wsb", "wallstreetbets", "subreddit"],
        "melvin": ["melvin", "plotkin", "6.8", "bail"],
        "dfv": ["dfv", "deepfuckingvalue", "roaring kitty", "keith gill"],
        "sec": ["sec report", "sec ", "congressional", "hearing"],
        "contagion": ["contagion", "amc", "meme stock", "spread"],
        "correlation": ["correlation", "risk model", "quant", "var "],
        "elon": ["elon", "musk", "gamestonk", "tweet"],
    }
    for topic, keywords in topic_keywords.items():
        if any(kw in text_lower for kw in keywords):
            return topic
    return "default"


def get_follow_up_questions(topic: str) -> list[str]:
    """Return follow-up questions for a detected topic."""
    return FOLLOW_UP_QUESTIONS.get(topic, FOLLOW_UP_QUESTIONS["default"])


def render_inline_charts(topic: str):
    """Show relevant charts/visuals inline after an answer based on topic."""
    import pandas as pd

    charts_shown = False

    if topic in ("squeeze", "short", "default"):
        with st.container():
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown("##### 🚀 GME Price Action")
            price_df = pd.DataFrame(
                list(GME_PRICE_TIMELINE.items()), columns=["Date", "Price ($)"]
            ).set_index("Date")
            st.line_chart(price_df, color="#00E676", height=200)
            st.markdown("</div>", unsafe_allow_html=True)
        charts_shown = True

    if topic in ("squeeze", "robinhood"):
        with st.container():
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown("##### 📊 Trading Volume (M shares)")
            vol_df = pd.DataFrame(
                list(VOLUME_DATA.items()), columns=["Date", "Volume (M)"]
            ).set_index("Date")
            st.bar_chart(vol_df, color="#FFD93D", height=200)
            st.markdown("</div>", unsafe_allow_html=True)
        charts_shown = True

    if topic in ("short", "correlation"):
        with st.container():
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown("##### 📉 Short Interest Over Time (% of Float)")
            si_df = pd.DataFrame(
                list(SHORT_INTEREST_DATA.items()), columns=["Period", "SI (%)"]
            ).set_index("Period")
            st.bar_chart(si_df, color="#FF6B6B", height=200)
            st.markdown("</div>", unsafe_allow_html=True)
        charts_shown = True

    if topic in ("contagion", "reddit"):
        with st.container():
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown("##### 🦍 Meme Stock January 2021 Returns (%)")
            meme_df = pd.DataFrame(
                list(MEME_STOCK_RETURNS.items()), columns=["Ticker", "Return (%)"]
            ).set_index("Ticker")
            st.bar_chart(meme_df, color="#4FC3F7", height=200)
            st.markdown("</div>", unsafe_allow_html=True)
        charts_shown = True

    if topic == "melvin":
        with st.container():
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown("##### 💀 Melvin Capital AUM ($M)")
            melvin_df = pd.DataFrame(
                list(MELVIN_TIMELINE.items()), columns=["Date", "AUM ($M)"]
            ).set_index("Date")
            st.line_chart(melvin_df, color="#FF6B6B", height=200)
            st.markdown("</div>", unsafe_allow_html=True)
        charts_shown = True

    if topic in ("transfer entropy", "elon"):
        with st.container():
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown("##### 🚀 GME Price — The Elon Tweet Effect")
            price_df = pd.DataFrame(
                list(GME_PRICE_TIMELINE.items()), columns=["Date", "Price ($)"]
            ).set_index("Date")
            st.line_chart(price_df, color="#00E676", height=200)
            st.markdown("</div>", unsafe_allow_html=True)
        charts_shown = True

    if topic == "driver":
        # Show a visual DRIVER breakdown
        st.markdown(
            '<div class="chart-card">'
            "<strong>DRIVER Framework Breakdown</strong><br><br>"
            "📊 <strong>D</strong>ata — Price, volume, Reddit sentiment, PFOF<br>"
            "🔄 <strong>R</strong>egime — Pre-squeeze → Squeeze → Post-squeeze<br>"
            "🔗 <strong>I</strong>nfo Transfer — TE(Reddit→GME) >> TE(GME→Reddit)<br>"
            "📈 <strong>V</strong>olatility — 800%+ annualized realized vol<br>"
            "💥 <strong>E</strong>quilibrium — 140% SI = unstable, Reddit broke Nash eq<br>"
            "🏛️ <strong>R</strong>esponse — Robinhood halt, DTCC, SEC, Congress<br>"
            "</div>",
            unsafe_allow_html=True,
        )
        charts_shown = True

    if not charts_shown:
        # Default: show the price chart
        with st.container():
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown("##### 🚀 GME Price Action")
            price_df = pd.DataFrame(
                list(GME_PRICE_TIMELINE.items()), columns=["Date", "Price ($)"]
            ).set_index("Date")
            st.line_chart(price_df, color="#00E676", height=200)
            st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------


def render_sidebar(case_content: str) -> dict:
    """Render sidebar with case overview, settings, and example questions."""
    with st.sidebar:
        # Lottie animation
        lottie_data = load_lottie_url(LOTTIE_FINANCE_URL)
        if lottie_data:
            st_lottie(lottie_data, height=150, key="sidebar_lottie")

        st.header("🦍 What's This About?")
        st.markdown(
            "**Case Study — GameStop Short Squeeze (Jan 2021)**\n\n"
            "The story of how a bunch of Redditors with diamond hands "
            "took on billion-dollar hedge funds, broke the short market, "
            "and made Robinhood halt the buy button.\n\n"
            "Spoiler: the audacity is off the charts."
        )

        st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)

        # Did You Know? box
        if "fun_fact" not in st.session_state:
            st.session_state.fun_fact = random.choice(DID_YOU_KNOW_FACTS)
        st.info(f"🎲 **No Because Did You Know??**\n\n{st.session_state.fun_fact}")

        st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)
        st.subheader("❓ Don't Know What to Ask? Try These")
        for emoji, q in EXAMPLE_QUESTIONS:
            if st.button(f"{emoji} {q}", key=q, use_container_width=True):
                st.session_state["prefill_question"] = q

        st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)
        st.subheader("⚙️ Nerd Settings")
        model = st.selectbox(
            "Model",
            ["gpt-4.1", "gpt-4o-mini", "gpt-4.1-mini"],
            index=0,
        )
        temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.1)

        st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)

        # Clear chat button
        if st.button("🗑️ Nuke the Chat (start fresh)", use_container_width=True):
            st.session_state.messages = []
            st.session_state.pop("welcomed", None)
            st.session_state.pop("first_question_asked", None)
            st.rerun()

        st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)
        st.caption(
            "🎓 MGMT 69000 · Mastering AI for Finance · **Purdue University**\n\n"
            "*no hedge funds were harmed in the making of this app (just their portfolios)*"
        )

    return {"model": model, "temperature": temperature}


# ---------------------------------------------------------------------------
# Data Charts
# ---------------------------------------------------------------------------


def render_data_charts():
    """Render expandable data visualization section."""
    with st.expander("📊 The Numbers — Interactive Charts"):
        import pandas as pd

        st.markdown("#### 🚀 GME Price Action (Jan–Jun 2021)")
        price_df = pd.DataFrame(
            list(GME_PRICE_TIMELINE.items()), columns=["Date", "Price ($)"]
        )
        price_df = price_df.set_index("Date")
        st.line_chart(price_df, color="#00E676")

        st.markdown("#### 📉 Short Interest (% of Float)")
        si_df = pd.DataFrame(
            list(SHORT_INTEREST_DATA.items()), columns=["Period", "SI (%)"]
        )
        si_df = si_df.set_index("Period")
        st.bar_chart(si_df, color="#FF6B6B")

        st.markdown("#### 🦍 Meme Stock January Returns (%)")
        meme_df = pd.DataFrame(
            list(MEME_STOCK_RETURNS.items()), columns=["Ticker", "Return (%)"]
        )
        meme_df = meme_df.set_index("Ticker")
        st.bar_chart(meme_df, color="#4FC3F7")


# ---------------------------------------------------------------------------
# Main app
# ---------------------------------------------------------------------------


def main():
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="🦍",
        layout="centered",
    )

    # Inject custom CSS + floating symbols
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st.markdown(FLOATING_SYMBOLS_HTML, unsafe_allow_html=True)

    # ── Animated Hero Header ──
    st.markdown(
        '<div class="hero-title">🎮💎 GameStop Meme Stock Q&A 🚀</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="bouncing-emoji">🦍</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="hero-caption">the squeeze that broke Wall Street — AI-powered case study Q&A</div>',
        unsafe_allow_html=True,
    )

    # ── Ticker Tape Banner ──
    ticker_text = " | ".join(TICKER_ITEMS)
    doubled = f"{ticker_text}  |||  {ticker_text}"
    st.markdown(
        f'<div class="ticker-wrap">'
        f'<div class="ticker-content"><span>{doubled}</span></div></div>',
        unsafe_allow_html=True,
    )

    # ── Key Stats Dashboard ──
    cols = st.columns(len(KEY_METRICS))
    for col, m in zip(cols, KEY_METRICS):
        with col:
            st.metric(label=m["label"], value=m["value"], delta=m["delta"])

    # ── Visual Timeline (staggered animation) ──
    with st.expander("📅 The Timeline of Chaos — How It All Went Down"):
        for i, (emoji, date, description) in enumerate(TIMELINE_EVENTS):
            delay = i * 0.15
            st.markdown(
                f'<div class="timeline-item" style="animation-delay:{delay}s">'
                f"<strong>{emoji} {date}</strong><br>{description}</div>",
                unsafe_allow_html=True,
            )

    # ── Contagion Flow Diagram ──
    with st.expander("🔗 The Contagion Pipeline — From Reddit to Wall Street"):
        flow_parts: list[str] = []
        for idx, step in enumerate(CONTAGION_FLOW_STEPS):
            flow_parts.append(
                f'<div class="contagion-step">'
                f'<div class="label">{step["label"]}</div>'
                f'<div class="detail">{step["detail"]}</div></div>'
            )
            if idx < len(CONTAGION_FLOW_STEPS) - 1:
                flow_parts.append('<div class="contagion-arrow">→</div>')
        st.markdown(
            f'<div class="contagion-flow">{"".join(flow_parts)}</div>',
            unsafe_allow_html=True,
        )
        # Second Lottie animation
        lottie_chart = load_lottie_url(LOTTIE_CHART_URL)
        if lottie_chart:
            st_lottie(lottie_chart, height=120, key="contagion_lottie")

    # ── Data Charts Section ──
    render_data_charts()

    # Glowing divider
    st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)

    # Load case content and build system prompt
    case_content = load_case_content()
    system_prompt = build_system_prompt(case_content)
    settings = render_sidebar(case_content)

    # Initialize OpenAI client
    api_key = st.secrets.get("OPENAI_API_KEY", None)
    if not api_key:
        st.warning(
            "⚠️ Can't do much without an API key. Pop your OpenAI key "
            "into **Manage app → Settings → Secrets** like this:\n\n"
            '`OPENAI_API_KEY = "sk-your-key-here"`\n\n'
        )
        st.stop()

    client = OpenAI(api_key=api_key)

    # Session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Welcome message on first load
    if not st.session_state.get("welcomed"):
        st.session_state.welcomed = True
        ts = get_timestamp()
        welcome = (
            "🦍 Hey — I'm your **GameStop Meme Stock Q&A**. I know the case, "
            "I've got opinions, and I don't make things up.\n\n"
            "Ask me about the short squeeze, Robinhood's buy halt, "
            "transfer entropy, market microstructure, DRIVER — all of it.\n\n"
            "💡 *Not sure where to start? The sidebar has some bangers. "
            "Pick one, I'll do the rest.*"
        )
        st.session_state.messages.append(
            {"role": "assistant", "content": welcome, "timestamp": ts}
        )

    # Display chat history with timestamps (audit trail)
    for msg in st.session_state.messages:
        avatar = "🧑‍🎓" if msg["role"] == "user" else "🦍"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
            if "timestamp" in msg:
                st.caption(f"🕐 {msg['timestamp']}")

    # Pulsing "Live" indicator above chat input
    st.markdown(
        '<div class="live-indicator">'
        '<span class="live-dot"></span> go ahead, ask me something — I dare you 💎</div>',
        unsafe_allow_html=True,
    )

    # Handle prefilled question from sidebar button
    prefill = st.session_state.pop("prefill_question", None)
    prompt = st.chat_input("type something… diamond hands only 💎🙌") or prefill

    if prompt:
        ts = get_timestamp()

        # Question mark animation (replaces balloons from project 1)
        if not st.session_state.get("first_question_asked"):
            st.session_state.first_question_asked = True
            st.toast("❓ First question! Let's see what you got", icon="🦍")
        st.markdown(QUESTION_MARKS_HTML, unsafe_allow_html=True)

        # Toast reactions — keyword specific
        prompt_lower = prompt.lower()
        if "robinhood" in prompt_lower:
            st.toast("Robinhood halting buying is still infuriating. The AUDACITY.", icon="😡")
        elif "diamond hands" in prompt_lower or "💎" in prompt_lower:
            st.toast("💎🙌 DIAMOND HANDS DETECTED. Respect.", icon="🚀")
        elif "melvin" in prompt_lower:
            st.toast("Melvin Capital... rest in peace (not really)", icon="💀")
        elif "dfv" in prompt_lower or "deepfuckingvalue" in prompt_lower or "roaring kitty" in prompt_lower:
            st.toast("DFV: $53K → $48M. Absolute legend.", icon="👑")
        elif "short" in prompt_lower and ("squeeze" in prompt_lower or "interest" in prompt_lower):
            st.toast("140% short interest... the audacity of these hedge funds", icon="📉")
        elif "transfer entropy" in prompt_lower:
            st.toast("Transfer entropy: the receipts of finance", icon="📊")
        elif "driver" in prompt_lower:
            st.toast("DRIVER framework activated — let's go", icon="🧭")
        elif "elon" in prompt_lower or "musk" in prompt_lower:
            st.toast("One tweet. One word. 92.7% gain. Wild.", icon="🐦")

        # Show user message
        st.session_state.messages.append(
            {"role": "user", "content": prompt, "timestamp": ts}
        )
        with st.chat_message("user", avatar="🧑‍🎓"):
            st.markdown(prompt)
            st.caption(f"🕐 {ts}")

        # Build messages for OpenAI API call
        api_messages = [{"role": "system", "content": system_prompt}] + [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]

        # Stream assistant response
        with st.chat_message("assistant", avatar="🦍"):
            try:
                stream = client.chat.completions.create(
                    model=settings["model"],
                    messages=api_messages,
                    temperature=settings["temperature"],
                    stream=True,
                )
                response = st.write_stream(stream)
            except Exception as exc:
                err = str(exc).lower()
                if "api_key" in err or "auth" in err:
                    response = (
                        "🔑 Yikes — OpenAI rejected the API key. Check "
                        "**Manage app → Settings → Secrets** and make sure "
                        "`OPENAI_API_KEY` is valid."
                    )
                elif "rate" in err or "429" in str(exc) or "quota" in err:
                    response = (
                        "⏳ Rate limited or quota exceeded — wait a moment "
                        "and try again, or switch to **gpt-4o-mini** in "
                        "the sidebar."
                    )
                else:
                    response = (
                        f"💀 Something went sideways: {exc}\n\n"
                        "Try again in a sec?"
                    )
                st.error(response)

            response_ts = get_timestamp()
            st.caption(f"🕐 {response_ts}")

            # Inline charts relevant to the answer
            topic = detect_topic(prompt + " " + (response if isinstance(response, str) else ""))
            render_inline_charts(topic)

        st.session_state.messages.append(
            {"role": "assistant", "content": response, "timestamp": response_ts}
        )

        # Follow-up question suggestions
        follow_ups = get_follow_up_questions(topic)
        st.markdown(
            '<div class="followup-label">💡 Want to keep going? Try one of these:</div>',
            unsafe_allow_html=True,
        )
        fu_cols = st.columns(len(follow_ups))
        for i, (col, fq) in enumerate(zip(fu_cols, follow_ups)):
            with col:
                if st.button(f"{'🔍📊🎯'[i]} {fq}", key=f"fu_{hash(fq)}", use_container_width=True):
                    st.session_state["prefill_question"] = fq
                    st.rerun()


if __name__ == "__main__":
    main()

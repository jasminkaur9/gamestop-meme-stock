"""Generate animated GIF explainers for the GameStop case study.

Run once locally: python3 generate_animations.py
Outputs GIFs to assets/ directory for embedding in the Streamlit app.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from pathlib import Path

ASSETS = Path(__file__).parent / "assets"
ASSETS.mkdir(exist_ok=True)

# Common style
BG_COLOR = "#0E1117"
TEXT_COLOR = "#FAFAFA"
GREEN = "#00E676"
RED = "#FF6B6B"
CYAN = "#4FC3F7"
YELLOW = "#FFD93D"
PURPLE = "#C084FC"

plt.rcParams.update({
    "figure.facecolor": BG_COLOR,
    "axes.facecolor": BG_COLOR,
    "axes.edgecolor": "#333",
    "text.color": TEXT_COLOR,
    "xtick.color": TEXT_COLOR,
    "ytick.color": TEXT_COLOR,
    "axes.labelcolor": TEXT_COLOR,
    "font.family": "sans-serif",
    "font.size": 11,
})


def make_price_squeeze_gif():
    """Animate GME price from $17 to $483 with key event annotations."""
    dates = [
        "Jan 4", "Jan 11", "Jan 13", "Jan 19", "Jan 22",
        "Jan 25", "Jan 26", "Jan 27", "Jan 28\n(peak)", "Jan 28\n(close)",
        "Jan 29", "Feb 19", "Feb 24",
    ]
    prices = [17.25, 19.94, 31.40, 39.36, 65.01, 76.79, 147.98, 347.51, 483.00, 193.60, 325.00, 38.50, 108.73]
    x = np.arange(len(dates))

    annotations = {
        2: ("Ryan Cohen\njoins board", GREEN),
        4: ("WSB goes\nparabolic", CYAN),
        6: ("Elon tweets\n'Gamestonk!!'", YELLOW),
        8: ("$483 PEAK\n>>> ALL TIME HIGH", GREEN),
        9: ("Robinhood\nHALTS buying", RED),
        11: ("Bleeds to $38\nR.I.P.", RED),
        12: ("2nd spike\n'not dead yet'", CYAN),
    }

    fig, ax = plt.subplots(figsize=(10, 5.5))
    fig.subplots_adjust(bottom=0.18, top=0.88, left=0.1, right=0.95)
    line, = ax.plot([], [], color=GREEN, linewidth=2.5, zorder=5)
    dot, = ax.plot([], [], 'o', color=GREEN, markersize=10, zorder=6)
    price_text = ax.text(0.5, 0.95, "", transform=ax.transAxes, fontsize=22,
                         fontweight="bold", ha="center", va="top", color=GREEN)

    ax.set_xlim(-0.5, len(dates) - 0.5)
    ax.set_ylim(0, 550)
    ax.set_xticks(x)
    ax.set_xticklabels(dates, rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("Price ($)", fontsize=12)
    ax.set_title("THE GAMESTOP SQUEEZE  --  $17 to $483 in 24 Days", fontsize=14, fontweight="bold", pad=12)
    ax.axhline(y=17.25, color="#444", linestyle="--", linewidth=0.8, alpha=0.5)
    ax.text(len(dates) - 0.7, 25, "Starting price: $17.25", fontsize=8, color="#666")
    ax.grid(axis="y", color="#222", linewidth=0.5, alpha=0.5)

    stored_annotations = []

    def animate(frame):
        if frame < len(dates):
            i = frame
            line.set_data(x[:i+1], prices[:i+1])
            dot.set_data([x[i]], [prices[i]])
            price_text.set_text(f"${prices[i]:,.2f}")

            if prices[i] > 200:
                price_text.set_color(GREEN)
            elif prices[i] < 50:
                price_text.set_color(RED)
            else:
                price_text.set_color(CYAN)

            if i in annotations:
                txt, clr = annotations[i]
                y_off = 35 if prices[i] < 300 else -55
                ann = ax.annotate(txt, (x[i], prices[i]),
                                  xytext=(0, y_off), textcoords="offset points",
                                  fontsize=7.5, color=clr, ha="center", fontweight="bold",
                                  arrowprops=dict(arrowstyle="->", color=clr, lw=1.2),
                                  zorder=10)
                stored_annotations.append(ann)
        return line, dot, price_text

    # 13 data frames + 8 hold frames at end
    total_frames = len(dates) + 8
    anim = animation.FuncAnimation(fig, animate, frames=total_frames, interval=400, blit=False)
    anim.save(ASSETS / "gme_squeeze.gif", writer="pillow", fps=3, dpi=100)
    plt.close(fig)
    print("Created gme_squeeze.gif")


def make_volume_explosion_gif():
    """Animate trading volume bars growing to show the insane spike."""
    dates = ["Jan 4", "Jan 13", "Jan 22", "Jan 25", "Jan 26", "Jan 27", "Jan 28", "Jan 29"]
    volumes = [7, 144, 197, 175, 178, 93, 58, 50]
    colors = ["#444", YELLOW, GREEN, YELLOW, YELLOW, CYAN, RED, RED]
    x = np.arange(len(dates))

    fig, ax = plt.subplots(figsize=(9, 5))
    fig.subplots_adjust(bottom=0.15, top=0.88, left=0.12, right=0.95)
    bars = ax.bar(x, [0]*len(dates), color=colors, width=0.6, edgecolor="#222", linewidth=0.5)

    ax.set_xlim(-0.5, len(dates) - 0.5)
    ax.set_ylim(0, 230)
    ax.set_xticks(x)
    ax.set_xticklabels(dates, rotation=45, ha="right", fontsize=9)
    ax.set_ylabel("Volume (Million Shares)", fontsize=11)
    ax.set_title("TRADING VOLUME EXPLOSION  --  Normal: 7M  >>  Peak: 197M", fontsize=13, fontweight="bold", pad=12)
    ax.axhline(y=7, color=RED, linestyle="--", linewidth=1, alpha=0.6)
    ax.text(len(dates) - 0.7, 14, "Normal volume: ~7M", fontsize=8, color=RED, alpha=0.7)
    ax.grid(axis="y", color="#222", linewidth=0.5, alpha=0.5)

    vol_text = ax.text(0.5, 0.92, "", transform=ax.transAxes, fontsize=20,
                       fontweight="bold", ha="center", va="top", color=YELLOW)
    mult_text = ax.text(0.5, 0.80, "", transform=ax.transAxes, fontsize=13,
                        ha="center", va="top", color="#888")

    def animate(frame):
        for i, bar in enumerate(bars):
            if i <= frame and frame < len(dates):
                bar.set_height(volumes[i])
            elif i <= frame:
                bar.set_height(volumes[i])

        if frame < len(dates):
            vol_text.set_text(f"{volumes[frame]}M shares")
            mult_text.set_text(f"{volumes[frame]/7:.0f}x normal volume" if volumes[frame] > 7 else "Normal day")
        return bars

    total_frames = len(dates) + 6
    anim = animation.FuncAnimation(fig, animate, frames=total_frames, interval=500, blit=False)
    anim.save(ASSETS / "volume_explosion.gif", writer="pillow", fps=2.5, dpi=100)
    plt.close(fig)
    print("Created volume_explosion.gif")


def make_contagion_cascade_gif():
    """Animate meme stock returns appearing one by one — contagion in action."""
    tickers = ["GME", "KOSS", "AMC", "BB", "BBBY", "NOK"]
    returns = [2739, 1800, 301, 280, 184, 69]
    bar_colors = [GREEN, PURPLE, CYAN, YELLOW, RED, "#888"]

    fig, ax = plt.subplots(figsize=(9, 5))
    fig.subplots_adjust(bottom=0.12, top=0.88, left=0.15, right=0.92)
    y = np.arange(len(tickers))

    bars = ax.barh(y, [0]*len(tickers), color=bar_colors, height=0.55, edgecolor="#222", linewidth=0.5)
    ax.set_yticks(y)
    ax.set_yticklabels(tickers, fontsize=12, fontweight="bold")
    ax.set_xlim(0, 3200)
    ax.set_xlabel("January 2021 Return (%)", fontsize=11)
    ax.set_title("MEME STOCK CONTAGION  --  GME Led, Others Followed", fontsize=13, fontweight="bold", pad=12)
    ax.grid(axis="x", color="#222", linewidth=0.5, alpha=0.5)
    ax.invert_yaxis()

    pct_texts = []
    for i in range(len(tickers)):
        t = ax.text(5, i, "", fontsize=10, fontweight="bold", va="center", color=TEXT_COLOR)
        pct_texts.append(t)

    title_text = ax.text(0.98, 0.95, "", transform=ax.transAxes, fontsize=11,
                         ha="right", va="top", color="#888", style="italic")

    captions = [
        "GME: Ground Zero 🚀",
        "KOSS: +1,800%... headphone company??",
        "AMC: The #2 meme stock",
        "BB: Nostalgia trade",
        "BBBY: Short squeeze sympathy",
        "NOK: Nice.",
    ]

    def animate(frame):
        # Each ticker gets ~4 frames to animate in
        steps_per_bar = 4
        current_bar = min(frame // steps_per_bar, len(tickers) - 1)
        sub_frame = frame % steps_per_bar

        for i in range(current_bar + 1):
            if i < current_bar:
                bars[i].set_width(returns[i])
                pct_texts[i].set_text(f"+{returns[i]:,}%")
                pct_texts[i].set_position((returns[i] + 40, i))
            elif i == current_bar:
                progress = min((sub_frame + 1) / steps_per_bar, 1.0)
                w = returns[i] * progress
                bars[i].set_width(w)
                if progress >= 1.0:
                    pct_texts[i].set_text(f"+{returns[i]:,}%")
                    pct_texts[i].set_position((returns[i] + 40, i))

        if current_bar < len(captions):
            title_text.set_text(captions[current_bar])

        return bars

    total_frames = len(tickers) * 4 + 6
    anim = animation.FuncAnimation(fig, animate, frames=total_frames, interval=350, blit=False)
    anim.save(ASSETS / "contagion_cascade.gif", writer="pillow", fps=3, dpi=100)
    plt.close(fig)
    print("Created contagion_cascade.gif")


def make_short_interest_meltdown_gif():
    """Animate short interest collapsing as shorts are forced to cover."""
    periods = ["Nov '20", "Dec '20", "Early\nJan", "Mid\nJan", "Late\nJan", "Feb", "Mar"]
    si_values = [130, 138, 140, 122, 78, 42, 28]
    x = np.arange(len(periods))

    fig, ax = plt.subplots(figsize=(9, 5))
    fig.subplots_adjust(bottom=0.15, top=0.88, left=0.12, right=0.95)

    bars = ax.bar(x, [0]*len(periods), width=0.55, edgecolor="#222", linewidth=0.5)
    ax.set_xlim(-0.5, len(periods) - 0.5)
    ax.set_ylim(0, 165)
    ax.set_xticks(x)
    ax.set_xticklabels(periods, fontsize=9)
    ax.set_ylabel("Short Interest (% of Float)", fontsize=11)
    ax.set_title("SHORT INTEREST MELTDOWN  --  From 140% to 28%", fontsize=13, fontweight="bold", pad=12)
    ax.axhline(y=100, color=RED, linestyle="--", linewidth=1.2, alpha=0.7)
    ax.text(len(periods) - 0.7, 104, "100% of float", fontsize=8, color=RED, alpha=0.7)
    ax.grid(axis="y", color="#222", linewidth=0.5, alpha=0.5)

    si_text = ax.text(0.5, 0.92, "", transform=ax.transAxes, fontsize=20,
                      fontweight="bold", ha="center", va="top")
    comment_text = ax.text(0.5, 0.80, "", transform=ax.transAxes, fontsize=11,
                           ha="center", va="top", color="#888", style="italic")

    comments = [
        "Building up... dangerous levels",
        "138% -- more shorts than shares exist (!)",
        "140% -- PEAK. This is the powder keg.",
        "Squeeze begins — shorts scrambling",
        "Mass covering -- losses mounting",
        "Exodus. Melvin lost $6.8B.",
        "28% — the wreckage. Funds closed.",
    ]

    def animate(frame):
        if frame < len(periods):
            for i in range(frame + 1):
                bars[i].set_height(si_values[i])
                if si_values[i] > 100:
                    bars[i].set_color(RED)
                elif si_values[i] > 70:
                    bars[i].set_color(YELLOW)
                else:
                    bars[i].set_color(GREEN)

            si_text.set_text(f"{si_values[frame]}%")
            si_text.set_color(RED if si_values[frame] > 100 else (YELLOW if si_values[frame] > 70 else GREEN))
            comment_text.set_text(comments[frame])
        return bars

    total_frames = len(periods) + 6
    anim = animation.FuncAnimation(fig, animate, frames=total_frames, interval=600, blit=False)
    anim.save(ASSETS / "short_interest_meltdown.gif", writer="pillow", fps=2, dpi=100)
    plt.close(fig)
    print("Created short_interest_meltdown.gif")


def make_info_flow_gif():
    """Animate information flow: Reddit → Twitter → Media → Price with transfer entropy."""
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.subplots_adjust(bottom=0.08, top=0.88, left=0.08, right=0.95)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.set_axis_off()
    ax.set_title("INFORMATION FLOW  --  Transfer Entropy in Action", fontsize=14, fontweight="bold", pad=12)

    # Node positions
    nodes = [
        (1.5, 3, "Reddit\n[WSB]", "DD posts\nYOLO updates", PURPLE),
        (4, 3, "Twitter\n[X]", "Elon tweets\nAmplification", CYAN),
        (6.5, 3, "Media\n[TV]", "CNBC/Bloomberg\n'Dumb money'", YELLOW),
        (9, 3, "GME\n[$$$]", "Price goes\nparabolic", GREEN),
    ]

    arrows = [(2.3, 3, 1.2, 0), (4.8, 3, 1.2, 0), (7.3, 3, 1.2, 0)]

    te_labels = [
        (3.0, 4.5, "TE = 0.42 bits", PURPLE),
        (5.5, 4.5, "TE = 0.31 bits", CYAN),
        (8.0, 4.5, "TE = 0.28 bits", YELLOW),
    ]

    bottom_text = ax.text(5, 0.5, "", ha="center", fontsize=10, color="#888", style="italic")

    node_patches = []
    node_labels = []
    node_details = []
    arrow_patches = []
    te_texts = []

    for (nx, ny, label, detail, color) in nodes:
        circle = plt.Circle((nx, ny), 0.7, facecolor=BG_COLOR, edgecolor=color, linewidth=2, alpha=0)
        ax.add_patch(circle)
        node_patches.append(circle)
        t = ax.text(nx, ny + 0.1, label, ha="center", va="center", fontsize=11,
                    fontweight="bold", color=color, alpha=0)
        node_labels.append(t)
        d = ax.text(nx, ny - 0.95, detail, ha="center", va="center", fontsize=7.5,
                    color="#888", alpha=0)
        node_details.append(d)

    for (ax_x, ay, dx, dy) in arrows:
        arr = ax.annotate("", xy=(ax_x + dx, ay), xytext=(ax_x, ay),
                          arrowprops=dict(arrowstyle="-|>", color="#444", lw=2.5),
                          alpha=0)
        arrow_patches.append(arr)

    for (tx, ty, label, color) in te_labels:
        t = ax.text(tx, ty, label, ha="center", fontsize=9, fontweight="bold",
                    color=color, alpha=0,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor=BG_COLOR, edgecolor=color, linewidth=1, alpha=0))
        te_texts.append(t)

    captions = [
        "",
        "Reddit: Where it all started — DD posts and diamond hands",
        "Twitter: Elon's tweet sent it +92.7% in one day",
        "Media: Coverage brought millions of new traders",
        "GME: Information cascade → price goes parabolic",
        "Transfer entropy proves: Reddit CAUSED the move, not the reverse",
        "TE(Reddit->Price) >> TE(Price->Reddit) -- the receipts",
    ]

    def animate(frame):
        # Reveal nodes one at a time (frames 1-4), then arrows (5-7), then TE (8-10)
        for i in range(min(frame, 4)):
            node_patches[i].set_alpha(1)
            node_labels[i].set_alpha(1)
            node_details[i].set_alpha(1)

        for i in range(min(max(frame - 4, 0), 3)):
            arrow_patches[i].set_alpha(1)
            a = arrow_patches[i]
            a.arrow_patch.set_edgecolor(nodes[i][4])
            a.arrow_patch.set_facecolor(nodes[i][4])

        for i in range(min(max(frame - 7, 0), 3)):
            te_texts[i].set_alpha(1)
            te_texts[i].get_bbox_patch().set_alpha(0.8)

        cap_idx = min(frame, len(captions) - 1)
        bottom_text.set_text(captions[cap_idx])
        return []

    total_frames = 14
    anim = animation.FuncAnimation(fig, animate, frames=total_frames, interval=700, blit=False)
    anim.save(ASSETS / "info_flow.gif", writer="pillow", fps=2, dpi=100)
    plt.close(fig)
    print("Created info_flow.gif")


if __name__ == "__main__":
    print("Generating animated explainer GIFs...")
    make_price_squeeze_gif()
    make_volume_explosion_gif()
    make_contagion_cascade_gif()
    make_short_interest_meltdown_gif()
    make_info_flow_gif()
    print(f"\nDone! GIFs saved to {ASSETS}/")

# Product Overview — GameStop Meme Stock Q&A

## DRIVER Framework Application

| Component | GameStop Application |
|-----------|---------------------|
| **D – Data** | Market data (price, volume, short interest, FTDs), alternative data (Reddit sentiment, Twitter mentions, WSB subscriber count), microstructure data (PFOF rates, dark pool %) |
| **R – Regime** | Pre-squeeze (dying retailer), squeeze (coordinated retail buying + short squeeze), post-squeeze (meme stocks as asset class) |
| **I – Information Transfer** | Transfer entropy: Reddit sentiment → GME price (confirmed causal). Cross-asset: GME → AMC → secondary meme stocks |
| **V – Volatility** | GME realized vol >800% annualized at peak. IV on weeklies >500%. VIX spiked but didn't capture idiosyncratic meme risk |
| **E – Equilibrium Disruption** | Short interest >140% of float = unstable equilibrium. Reddit broke the Nash equilibrium keeping retail uncoordinated |
| **R – Response** | Robinhood trading halt, DTCC margin calls, SEC report (Oct 2021), congressional hearings, accelerated T+1 settlement push |

## Product
- **Streamlit chat application** powered by OpenAI
- Ingests full case study as system context
- Answers questions about the GameStop short squeeze with structured, data-rich responses
- Includes interactive visualizations, timeline, and contagion flow diagrams
- Audit trail with timestamps for every interaction

## Architecture
```
Case Markdown → System Prompt → Streamlit Chat UI → OpenAI API
                                      ↕
                              Session State (audit trail)
```

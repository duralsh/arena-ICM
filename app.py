#!/usr/bin/env python3
"""
Token Economics Calculator for ICO/Presale - Web Version

Interactive calculator with sliders to adjust:
- Team allocation percentage (0-30%)
- Funds to raise ($10K-$2M)
- Public sale percentage (0-100%)
- LP percentage (auto-calculated as: LP = 100 - Team - Public)

20% of raised funds allocated to LP.
"""

import streamlit as st

# Page config
st.set_page_config(
    page_title="Token Economics Calculator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stAlert {
        background-color: #262730;
    }
    .metric-card {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    h1 {
        color: #00ff88;
    }
    h2, h3 {
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# Constants
TOTAL_SUPPLY = 10_000_000_000  # 10 billion
LP_FUND_PERCENT = 0.20  # 20% of funds go to LP

def format_number(num):
    """Format large numbers with commas."""
    if num >= 1_000_000_000:
        return f"{num / 1_000_000_000:,.2f}B"
    elif num >= 1_000_000:
        return f"{num / 1_000_000:,.2f}M"
    elif num >= 1_000:
        return f"{num / 1_000:,.2f}K"
    else:
        return f"{num:,.2f}"

def validate_allocation(team_percent, public_percent):
    """Check if allocation is valid"""
    lp_percent = 100 - team_percent - public_percent
    
    # LP must be > 0
    if lp_percent < 0.1:
        return False, lp_percent, "LP cannot be 0%"
    
    # LP FDV >= ICO FDV constraint
    if public_percent > 0.1 and lp_percent > 0.2 * public_percent:
        return False, lp_percent, "LP FDV would drop below ICO FDV"
    
    return True, lp_percent, ""

# Main title
st.title("🚀 Token Economics Calculator")
st.markdown("---")

# Sidebar for inputs
with st.sidebar:
    st.header("⚙️ Parameters")
    
    # Team allocation slider
    team_percent = st.slider(
        "Team Token Allocation (%)",
        min_value=0,
        max_value=30,
        value=10,
        step=1,
        help="Percentage of total supply allocated to the team"
    )
    
    # Funds to raise slider
    funds_to_raise = st.slider(
        "Funds to Raise ($)",
        min_value=10_000,
        max_value=2_000_000,
        value=100_000,
        step=10_000,
        format="$%d",
        help="Total amount of funds to raise"
    )
    
    # Public sale allocation slider
    public_percent = st.slider(
        "Public Sale Token Alloc (%)",
        min_value=0,
        max_value=100,
        value=70,
        step=1,
        help="Percentage of total supply for public sale"
    )
    
    st.markdown("---")
    
    # Validate and calculate LP
    is_valid, lp_percent, error_msg = validate_allocation(team_percent, public_percent)
    
    # Display LP allocation
    st.subheader("LP Alloc (%)")
    if is_valid:
        st.success(f"**{lp_percent:.1f}%**")
        st.progress(lp_percent / 100)
    else:
        st.error(f"**{lp_percent:.1f}%** ⚠️")
        st.warning(f"⚠️ {error_msg}")
        st.progress(0)

# Main content
if not is_valid:
    st.error(f"⚠️ Invalid Allocation: {error_msg}")
    st.stop()

# Calculate token allocations
team_tokens = TOTAL_SUPPLY * (team_percent / 100)
public_tokens = TOTAL_SUPPLY * (public_percent / 100)
lp_tokens = TOTAL_SUPPLY * (lp_percent / 100)

# Calculate funds distribution
lp_funds = funds_to_raise * LP_FUND_PERCENT
team_funds = funds_to_raise * (1 - LP_FUND_PERCENT)

# Calculate prices
if public_tokens > 0:
    ico_price = funds_to_raise / public_tokens
else:
    ico_price = 0

if lp_tokens > 0:
    lp_price = lp_funds / lp_tokens
else:
    lp_price = 0

# Calculate FDVs
fdv_ico = TOTAL_SUPPLY * ico_price
fdv_lp = TOTAL_SUPPLY * lp_price

if fdv_ico > 0:
    fdv_multiple = fdv_lp / fdv_ico
else:
    fdv_multiple = 0

# Display results in columns
col1, col2 = st.columns(2)

with col1:
    st.header("📊 Token Distribution")
    
    st.metric(
        label="Team Tokens",
        value=f"{format_number(team_tokens)} tokens",
        delta=f"{team_percent:.1f}%"
    )
    
    st.metric(
        label="Public Sale Tokens",
        value=f"{format_number(public_tokens)} tokens",
        delta=f"{public_percent:.1f}%"
    )
    
    st.metric(
        label="LP Tokens",
        value=f"{format_number(lp_tokens)} tokens",
        delta=f"{lp_percent:.1f}%"
    )
    
    st.metric(
        label="Total Allocation",
        value="100.0%",
        delta="✓ Valid"
    )

with col2:
    st.header("💰 Funds & Valuation")
    
    st.metric(
        label="Total Funds Raised",
        value=f"${format_number(funds_to_raise)}"
    )
    
    st.metric(
        label="LP Funds (20%)",
        value=f"${format_number(lp_funds)}"
    )
    
    st.metric(
        label="Team Funds (80%)",
        value=f"${format_number(team_funds)}"
    )

st.markdown("---")

# FDV Section
st.header("📈 Fully Diluted Valuations")

col3, col4, col5 = st.columns(3)

with col3:
    st.metric(
        label="Pre-Market FDV (ICO Price)",
        value=f"${format_number(fdv_ico)}",
        help="FDV at public sale price"
    )

with col4:
    st.metric(
        label="Market FDV (LP Price)",
        value=f"${format_number(fdv_lp)}",
        help="FDV at LP price"
    )

with col5:
    st.metric(
        label="FDV Multiple",
        value=f"{fdv_multiple:.2f}x",
        help="Market FDV / Pre-Market FDV"
    )

# Info section at bottom
st.markdown("---")
with st.expander("ℹ️ How It Works"):
    st.markdown("""
    ### Token Allocation
    - **Total Supply**: 10 billion tokens
    - **Team**: User-defined percentage (0-30%)
    - **Public Sale**: User-defined percentage (0-100%)
    - **LP**: Automatically calculated as `100 - Team - Public`
    
    ### Constraints
    1. **LP > 0%**: Team + Public must be < 100%
    2. **LP FDV ≥ ICO FDV**: Ensures LP tokens maintain minimum valuation
    
    ### Funds Distribution
    - **20% of raised funds** go to the Liquidity Pool (LP)
    - **80% of raised funds** go to the team/project
    
    ### Valuations
    - **Pre-Market FDV**: Valuation at ICO/public sale price
    - **Market FDV**: Valuation at LP price (typically higher)
    - **FDV Multiple**: Ratio showing how LP price compares to ICO price
    """)

# Footer
st.markdown("---")
st.caption("🚀 Token Economics Calculator | Built with Streamlit")


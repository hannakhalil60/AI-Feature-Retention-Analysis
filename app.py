# ============================================================
# STREAMLIT WEB-BASED BUSINESS REPORT
# Synapse Workspace AI-Powered Productivity Features
# Business Perspective: Product Management
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.stats import pearsonr

st.set_page_config(
    page_title="Synapse AI Feature Analytics",
    page_icon="📊",
    layout="wide"
)

# ------------------------------------------------------------
# Warm editorial styling
# ------------------------------------------------------------
st.markdown("""
<style>
    .stApp {
        background-color: #F7F3ED;
        color: #2F2A26;
    }

    .main-title {
        font-family: Georgia, serif;
        font-size: 42px;
        font-weight: 700;
        color: #2F2A26;
        margin-bottom: 5px;
    }

    .subtitle {
        font-family: Georgia, serif;
        font-size: 20px;
        color: #6B625A;
        margin-bottom: 25px;
    }

    .section-title {
        font-family: Georgia, serif;
        font-size: 28px;
        font-weight: 700;
        color: #2F2A26;
        margin-top: 30px;
    }

    .insight-box {
        background-color: #EFE7DC;
        border-left: 5px solid #A84B35;
        padding: 18px 22px;
        border-radius: 6px;
        margin: 15px 0;
    }

    .recommendation-box {
        background-color: #E8EEE9;
        border-left: 5px solid #527A62;
        padding: 18px 22px;
        border-radius: 6px;
        margin: 15px 0;
    }

    .small-text {
        color: #6B625A;
        font-size: 14px;
    }

    h1, h2, h3 {
        font-family: Georgia, serif !important;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# Load data
# ------------------------------------------------------------
@st.cache_data
def load_data():

    catalog = pd.read_csv(
        "feature_catalog.csv",
        encoding="utf-8-sig"
    )

    usage = pd.read_csv(
        "ai_feature_usage.csv",
        encoding="utf-8-sig"
    )

    feedback = pd.read_csv(
        "feature_feedback.csv",
        encoding="utf-8-sig"
    )

    df = (
        usage
        .merge(
            feedback,
            on=["FeatureName", "Month"],
            how="inner"
        )
        .merge(
            catalog,
            on="FeatureName",
            how="inner"
        )
    )

    # Derived metrics
    df["ReturningShare"] = (
        df["ReturningUsers"] / df["ActiveUsers"]
    )

    df["UsesPerActiveUser"] = (
        df["UsageCount"] / df["ActiveUsers"]
    )

    return df


df = load_data()

# ------------------------------------------------------------
# Header
# ------------------------------------------------------------
st.markdown(
    '<div class="main-title">Synapse AI Feature Analytics</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Understanding adoption and returning-user engagement across '
    'AI-powered productivity features'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="small-text">'
    '<b>Business Perspective:</b> Product Management'
    '</div>',
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# Business questions
# ------------------------------------------------------------
st.markdown(
    '<div class="section-title">Business Questions</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **1. Returning-user share over time**

    Over the twelve months covered by the data, is the share of
    users who return to each AI feature rising or falling, and
    which features retain users best?
    """)

with col2:
    st.markdown("""
    **2. Feature-specific or platform-wide?**

    Is the pattern in returning share feature-specific, or does
    it hold across the platform?
    """)

# ------------------------------------------------------------
# Shared calculations
# ------------------------------------------------------------
features = df["FeatureName"].nunique()

month1_users = df[df["Month"] == 1]["ActiveUsers"].sum()
month12_users = df[df["Month"] == 12]["ActiveUsers"].sum()

overall_growth = (
    (month12_users - month1_users) / month1_users
)

early = (
    df[df["Month"] <= 6]
    .groupby("FeatureName")["ReturningShare"]
    .mean()
)

late = (
    df[df["Month"] > 6]
    .groupby("FeatureName")["ReturningShare"]
    .mean()
)

# Expressed in percentage points, not as a percentage change
average_change_points = (
    (late - early).mean() * 100
)

best_feature = late.idxmax()
best_feature_share = late.max()

# ------------------------------------------------------------
# Key metrics
# ------------------------------------------------------------
st.markdown(
    '<div class="section-title">At a Glance</div>',
    unsafe_allow_html=True
)

metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:
    st.metric(
        "AI Features",
        features
    )

with metric2:
    st.metric(
        "Active User Growth",
        f"{overall_growth:.1%}",
        help="Total active users, Month 1 to Month 12"
    )

with metric3:
    st.metric(
        "Avg Returning-User Share Change",
        f"{average_change_points:.1f} pts",
        help="Change in returning share between Months 1-6 and Months 7-12, "
             "measured in percentage points"
    )

with metric4:
    st.metric(
        "Highest Late-Period Returning Share",
        f"{best_feature_share:.1%}",
        help=best_feature
    )

# ------------------------------------------------------------
# Section 1: Adoption context
# ------------------------------------------------------------
st.markdown(
    '<div class="section-title">1. Adoption Increased</div>',
    unsafe_allow_html=True
)

st.write(
    "Before examining returning-user behavior, it is useful to "
    "look at active-user growth. Active users increased from "
    "Month 1 to Month 12 across all five AI features."
)

# Month 1 vs Month 12
active_users = (
    df[df["Month"].isin([1, 12])]
    .pivot(
        index="FeatureName",
        columns="Month",
        values="ActiveUsers"
    )
)

fig1 = go.Figure()

fig1.add_trace(
    go.Bar(
        x=active_users.index,
        y=active_users[1],
        name="Month 1",
        marker_color="#B8CCE4"
    )
)

fig1.add_trace(
    go.Bar(
        x=active_users.index,
        y=active_users[12],
        name="Month 12",
        marker_color="#C0392B"
    )
)

fig1.update_layout(
    barmode="group",
    title="Active Users Increased Across All AI Features",
    xaxis_title="AI Feature",
    yaxis_title="Active Users",
    legend=dict(
        orientation="h",
        y=-0.2
    ),
    template="plotly_white"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.markdown("""
<div class="insight-box">
<b>Insight:</b> Adoption grew across every feature between Month 1
and Month 12, with total active users up 25.7%. On its own this looks
like a successful AI rollout, and it is the number leadership currently
sees. The sections that follow show that the composition of that growth
changed at the same time: more users arrived, but a smaller proportion
of them came back.
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# Section 2: Returning share over time
# ------------------------------------------------------------
st.markdown(
    '<div class="section-title">2. Returning Share Declined Over Time</div>',
    unsafe_allow_html=True
)

st.write(
    "Returning Share is calculated as Returning Users divided by "
    "Active Users. The line chart shows how this measure changed "
    "over the twelve months for each AI feature."
)

fig2 = go.Figure()

for name, group in df.groupby("FeatureName"):

    group = group.sort_values("Month")

    fig2.add_trace(
        go.Scatter(
            x=group["Month"],
            y=group["ReturningShare"],
            mode="lines+markers",
            name=name
        )
    )

fig2.update_layout(
    title="Returning Share Declined Across All Five AI Features",
    xaxis_title="Month",
    yaxis_title="Returning Share",
    yaxis_tickformat=".0%",
    legend=dict(
        orientation="h",
        y=-0.25
    ),
    template="plotly_white"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.markdown("""
<div class="insight-box">
<b>Insight:</b> Returning share trends downward over the twelve-month
period for all five AI features, and the five lines fall at close to the
same rate. This is the answer to the second business question: the
decline is platform-wide rather than concentrated in any one feature.
That distinction matters, because it means the issue is unlikely to be
solved by individual feature teams working separately.
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# Section 3: Early vs late returning-user share
# ------------------------------------------------------------
st.markdown(
    '<div class="section-title">3. Early vs. Late Returning-User Share</div>',
    unsafe_allow_html=True
)

st.write(
    "To make the change easier to compare across features, the "
    "twelve months are divided into an early period (Months 1-6) "
    "and a later period (Months 7-12)."
)

fig3 = go.Figure()

fig3.add_trace(
    go.Bar(
        x=early.index,
        y=early.values,
        name="Months 1-6",
        marker_color="#5B8DB8"
    )
)

fig3.add_trace(
    go.Bar(
        x=late.index,
        y=late.values,
        name="Months 7-12",
        marker_color="#C0392B"
    )
)

fig3.update_layout(
    barmode="group",
    title="Returning Share Was Lower in Months 7-12",
    xaxis_title="AI Feature",
    yaxis_title="Average Returning Share",
    yaxis_tickformat=".0%",
    yaxis_range=[0.70, 0.95],
    legend=dict(
        orientation="h",
        y=-0.2
    ),
    template="plotly_white"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.caption(
    "Note: the vertical axis starts at 70% rather than zero so the "
    "differences between periods are visible."
)

# Returning-user share change table
retention_table = pd.DataFrame({
    "Feature": early.index,
    "Early Returning Share (%)": (early.values * 100).round(1),
    "Late Returning Share (%)": (late.values * 100).round(1),
    "Change (percentage points)": ((late.values - early.values) * 100).round(1)
})

st.dataframe(
    retention_table,
    use_container_width=True,
    hide_index=True
)

st.markdown(
    f"""
<div class="insight-box">
<b>Insight:</b> All five features lost between 7.7 and 9.1 percentage
points of returning share, a range of only 1.4 points between the best
and worst performer. The feature with the highest late-period returning
share was <b>{best_feature}</b>, at <b>{best_feature_share:.1%}</b>, but
the gap between features is small enough that no single feature stands
out as the problem.
</div>
""",
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# Section 4: Association between ratings and returning-user share
# ------------------------------------------------------------
st.markdown(
    '<div class="section-title">4. Are Ratings Associated with Returning-User Share?</div>',
    unsafe_allow_html=True
)

st.write(
    "Average rating was examined as a possible explanation for "
    "differences in returning share. Pearson correlation measures "
    "the strength of the linear relationship between these two variables."
)

r, p = pearsonr(
    df["AvgRating"],
    df["ReturningShare"]
)

fig4 = go.Figure()

fig4.add_trace(
    go.Scatter(
        x=df["AvgRating"],
        y=df["ReturningShare"],
        mode="markers",
        marker=dict(
            size=9,
            color="#5B8DB8",
            opacity=0.7
        ),
        name="Feature-month"
    )
)

m, b = np.polyfit(
    df["AvgRating"],
    df["ReturningShare"],
    1
)

xs = np.linspace(
    df["AvgRating"].min(),
    df["AvgRating"].max(),
    50
)

fig4.add_trace(
    go.Scatter(
        x=xs,
        y=m * xs + b,
        mode="lines",
        name="Trend",
        line=dict(
            color="#C0392B",
            dash="dash"
        )
    )
)

fig4.update_layout(
    title=f"Returning Share vs. Average Rating (r = {r:.3f})",
    xaxis_title="Average Rating (1-5)",
    yaxis_title="Returning Share",
    yaxis_tickformat=".0%",
    template="plotly_white"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Pearson Correlation",
        f"{r:.3f}",
        help="Values near zero indicate no linear relationship"
    )

with col2:
    st.metric(
        "p-value",
        f"{p:.3f}",
        help="A p-value above 0.05 does not provide sufficient evidence "
             "of a linear association in this sample; it does not prove no association exists."
    )

# Rating trend over the same period
rating_trend = df.groupby("Month")["AvgRating"].mean()

st.markdown(
    f"""
<div class="insight-box">
<b>Insight:</b> Average rating and returning-user share were not significantly
linearly associated in this sample (r = {r:.3f}, p = {p:.3f}). During the
observed decline in returning-user share, average ratings ranged from
{rating_trend.min():.1f} to {rating_trend.max():.1f}. These results do not
establish that satisfaction is unrelated to engagement or lacks predictive
value in other settings. Ratings should be interpreted alongside behavioral
measures, especially because feedback may be subject to response bias.
</div>
""",
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# Section 5: Product Management implications
# ------------------------------------------------------------
st.markdown(
    '<div class="section-title">5. Product Management Implications</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="recommendation-box">

<b>1. Monitor returning share alongside adoption.</b>

Active-user growth alone does not show whether users continue to
come back to a feature. Returning Share should be monitored as a
separate product-health metric.


<br>

<b>2. Investigate the platform-wide decline in returning-user share.</b>

Because all five AI features show a similar downward pattern,
first decompose returning-user share into returning and new-user counts.
The observed change in share can reflect faster growth in new users,
not necessarily a loss of returning users. Investigate onboarding,
repeat usage, and feature-level differences before attributing the
pattern to a platform-wide engagement problem.


<br>

<b>3. Investigate repeat engagement with user-level cohorts.</b>

Monthly aggregate counts do not establish whether the same users
returned across periods or why behavior changed. Cohort-level histories
and targeted feedback from inactive users would help investigate repeat
engagement and possible barriers.


<br>

<b>4. Monitor satisfaction alongside behavioral engagement.</b>

In this sample, ratings were not significantly linearly associated
with returning-user share. Ratings alone did not capture the observed
change in share; combine them with returning-user counts, new-user
counts, and longitudinal engagement measures.

</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# Methodology
# ------------------------------------------------------------
with st.expander("Methodology and Data Preparation"):

    st.write("""
    **Data sources**

    The analysis combines three datasets:

    - Feature catalog
    - AI feature usage
    - Feature feedback

    The usage and feedback datasets were merged using FeatureName and
    Month. The resulting data was then merged with the feature catalog
    using FeatureName. The merge produced 60 rows, matching the input
    files, confirming no records were lost or duplicated. No duplicate
    rows or missing values were present in any file.

    **Derived measures**

    Returning Share = Returning Users / Active Users

    Uses Per Active User = Usage Count / Active Users

    A validation check confirmed that New Users + Returning Users equals
    Active Users in every row, so returning share and new-user share are
    mirror images. Only returning share is used.

    **Early vs. late comparison**

    Months 1-6 were classified as the early period and Months 7-12
    as the late period. A paired t-test on these two periods returned
    t = 33.20, p < 0.001, confirming the decline is statistically
    significant.

    **Statistical analysis**

    Pearson correlation was used to examine the relationship between
    Average Rating and Returning Share.

    **Known limitation**

    The feature catalog lists launch months of 1 through 5, but usage
    data begins at Month 1 for every feature. These contradict each
    other, so LaunchMonth was excluded from the analysis.
    """)

# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------
st.markdown("---")

st.markdown(
    '<div class="small-text">'
    'Synapse Workspace AI Feature Analytics | Product Management '
    'Perspective'
    '</div>',
    unsafe_allow_html=True
)
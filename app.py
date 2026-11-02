
import calendar
from datetime import date

import streamlit as st
import plotly.express as px

from analysis import (
    get_available_months,
    get_date_limits,
    get_financial_summary,
    get_category_dataframe
)


# ---------------------------------
# 1. Page configuration
# ---------------------------------

st.set_page_config(
    page_title="Bank Statement Analyser",
    page_icon="💳",
    layout="wide"
)


# ---------------------------------
# 2. Custom colours and styling
# ---------------------------------

st.markdown("""
<style>
    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    h1 {
        color: #2563EB;
        font-weight: 750;
    }

    div[data-testid="stMetric"] {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 20px;
    }

    div[data-testid="stMetricLabel"] {
        color: #475569;
    }

    div[data-testid="stMetricValue"] {
        color: #0F172A;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------
# 3. Dashboard heading
# ---------------------------------

st.title("💳 Bank Statement Analyser")
st.caption("Financial Overview | PostgreSQL")

st.divider()


# ---------------------------------
# 4. Load available transaction dates
# ---------------------------------

months = get_available_months()
min_date, max_date = get_date_limits()

if not months or min_date is None:
    st.warning("No bank transactions available.")
    st.stop()


# ---------------------------------
# 5. Date filtering
# ---------------------------------

st.subheader("📅 Reporting Period")

filter_type = st.radio(
    "Choose a reporting period",
    ["Month", "Custom Date Range", "All Dates"],
    horizontal=True
)

start_date = None
end_date = None

if filter_type == "Month":

    selected_month = st.selectbox(
        "Select Month",
        options=months,
        format_func=lambda m: date(
            int(m[:4]), int(m[5:7]), 1
        ).strftime("%B %Y")
    )

    year, month = map(
        int,
        selected_month.split("-")
    )

    start_date = date(year, month, 1)

    last_day = calendar.monthrange(
        year, month
    )[1]

    end_date = date(year, month, last_day)


elif filter_type == "Custom Date Range":

    selected_dates = st.date_input(
        "Select start and end dates",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        format="DD/MM/YYYY"
    )

    if len(selected_dates) != 2:
        st.info("Please select both dates.")
        st.stop()

    start_date, end_date = selected_dates


# Show current selection
if start_date is not None and end_date is not None:

    st.caption(
        f"Showing transactions from "
        f"{start_date:%d %B %Y} "
        f"to {end_date:%d %B %Y}"
    )

else:
    st.caption("Showing all imported transactions")

st.divider()


# ---------------------------------
# 6. Financial summary
# ---------------------------------

total_income, total_out, net_cash_flow = (
    get_financial_summary(
        start_date,
        end_date
    )
)

col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.metric(
        "🟢 Total Income",
        f"£{total_income:,.2f}"
    )

with col2:
    st.metric(
        "🔴 Total Money Out",
        f"£{total_out:,.2f}"
    )

with col3:
    st.metric(
        "🔵 Net Cash Flow",
        f"£{net_cash_flow:,.2f}"
    )


# ---------------------------------
# 7. Category analysis
# ---------------------------------

st.write("")

category_df = get_category_dataframe(
    start_date,
    end_date
)

st.subheader("📊 Money Out by Category")

if category_df.empty:

    st.info("No transactions found for this period.")

else:

    number_of_categories = len(category_df)

    options = sorted(
        set(
            [n for n in [5, 10, 15, 25]
             if n <= number_of_categories]
            + [number_of_categories]
        )
    )

    top_n = st.selectbox(
        "Number of categories",
        options=options
    )

    top_categories = (
        category_df
        .nlargest(top_n, "TotalMoneyOut")
        .sort_values("TotalMoneyOut")
    )


    # ---------------------------------
    # 8. Colourful Plotly chart
    # ---------------------------------

    fig = px.bar(
        top_categories,
        x="TotalMoneyOut",
        y="Category",
        orientation="h",
        color="Category",
        color_discrete_sequence=px.colors.qualitative.Set2,
        text="TotalMoneyOut"
    )

    fig.update_traces(
        texttemplate="£%{x:,.2f}",
        textposition="outside",
        cliponaxis=False
    )

    fig.update_layout(
        showlegend=False,
        height=max(350, top_n * 48),
        margin=dict(l=20, r=100, t=20, b=40),
        xaxis_title="Money Out (£)",
        yaxis_title=None,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    fig.update_xaxes(
        rangemode="tozero",
        showgrid=True,
        gridcolor="#E2E8F0"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ---------------------------------
    # 9. Category breakdown table
    # ---------------------------------

    st.subheader("Category Breakdown")

    st.dataframe(
        category_df.sort_values(
            "TotalMoneyOut",
            ascending=False
        ),
        hide_index=True,
        width="stretch",
        column_config={
            "Category": "Category",
            "TransactionCount": "Transactions",
            "TotalMoneyOut": st.column_config.NumberColumn(
                "Money Out",
                format="£%.2f"
            )
        }
    )


# ---------------------------------
# 10. Footer
# ---------------------------------

st.divider()

st.caption(
    "Money Out includes transfers, savings and credit card "
    "repayments. These will be classified separately "
    "in a future improvement."
)

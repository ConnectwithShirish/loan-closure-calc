import streamlit as st
from datetime import date

st.set_page_config(
    page_title="Loan Closure Calculator",
    page_icon="💰",
    layout="wide"
)

# -------------------- HEADER --------------------
st.markdown(
    """
    <h1 style='text-align:center;'>💰 Loan Closure Calculator</h1>
    <p style='text-align:center; color:gray;'>
    Simple interest • Exact days • Society-friendly
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# -------------------- LAST MONTH SUMMARY --------------------
st.subheader("📌 Last Month Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    interest_pending = st.number_input(
        "Interest Pending",
        min_value=0.0,
        step=100.0
    )

with col2:
    principal_pending = st.number_input(
        "Principal Pending",
        min_value=0.0,
        step=1000.0
    )

with col3:
    rate = st.number_input(
        "Rate of Interest (%)",
        min_value=0.0,
        step=0.1
    )

with col4:
    start_date = st.date_input(
        "Interest Start Date",
        value=date.today()
    )

st.divider()

# -------------------- TRANSACTIONS --------------------
st.subheader("🧾 Current Month Transactions")

if "rows" not in st.session_state:
    st.session_state.rows = 1

entries = []

for i in range(st.session_state.rows):
    c1, c2, c3 = st.columns([2, 2, 2])

    with c1:
        amt = st.number_input(
            f"Amount #{i+1}",
            min_value=0.0,
            key=f"amt_{i}"
        )

    with c2:
        dt = st.date_input(
            f"Date #{i+1}",
            key=f"date_{i}"
        )

    with c3:
        interest_display = st.empty()

    entries.append((amt, dt, interest_display))

st.button(
    "➕ Add Another Entry",
    on_click=lambda: st.session_state.update(
        {"rows": st.session_state.rows + 1}
    )
)

st.divider()

# -------------------- CLOSING --------------------
st.subheader("🔐 Closure")

c1, c2 = st.columns(2)

with c1:
    closing_date = st.date_input("Closing Date", value=date.today())

with c2:
    calculate = st.button("Calculate Total Amount")

# -------------------- CALCULATION --------------------
if calculate:
    principal = principal_pending
    total_interest = interest_pending
    last_date = start_date

    # Prepare valid payments
    payments = [
        (amt, dt, disp)
        for amt, dt, disp in entries
        if amt > 0
    ]

    payments.sort(key=lambda x: x[1])

    for amt, dt, disp in payments:
        days = (dt - last_date).days
        interest_for_period = principal * rate * days / (100 * 365)
        total_interest += interest_for_period

        disp.markdown(
            f"<span style='color:green; font-weight:bold;'>₹ {interest_for_period:.2f}</span>",
            unsafe_allow_html=True
        )

        # Apply payment
        if total_interest > 0:
            if amt >= total_interest:
                amt -= total_interest
                total_interest = 0
                principal -= amt
            else:
                total_interest -= amt
        else:
            principal -= amt

        last_date = dt

    # Interest till closing
    days = (closing_date - last_date).days
    if days > 0:
        total_interest += principal * rate * days / (100 * 365)

    total = principal + total_interest

    st.divider()
    st.success(f"💰 **Total Amount to Close: ₹ {total:.2f}**")

    st.caption(
        f"""
        Principal Pending: ₹ {principal:.2f}  
        Total Interest: ₹ {total_interest:.2f}
        """
    )

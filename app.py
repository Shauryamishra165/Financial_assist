import streamlit as st
import pandas as pd
import yfinance as yf
from helper import All_Companies, get_company_info, get_historical_data, get_financial_data, calculate_financial_metrics, get_additional_data,get_company_input, get_forecast, get_wacc, ask_query
from sentiment_analysis import get_sentiment_analysis
# Streamlit App


# Function to handle different types of values (None, list, int, etc.)
def format_value(value):
    if isinstance(value, list):
        return ", ".join([str(v) for v in value])  # Handle lists (like multiple earnings dates)
    elif value is None:
        return "N/A"  # Handle None values
    elif isinstance(value, (int, float)):
        return f"{value:,}"  # Format large numbers with commas
    return str(value)  # Convert other values to string
st.title("Company Financials and AI Valuation")


tab1, tab2 , tab3 = st.tabs(["Company Details", "Valuation prediction by AI" , "Sentiment Analysis"])

with tab1:
    # Sidebar to select company
    st.sidebar.title("Select Company")
    company_list = All_Companies()
    company_names = company_list['Company Name']
    selected_company = st.sidebar.selectbox("Choose a company", company_names)

    # Fetch the selected company's symbol
    selected_symbol = company_list[company_list['Company Name'] == selected_company]['Symbol'].values[0]

    # Display Company Information
    st.header(f"Company: {selected_company}")
    st.subheader("Company Info")
    company_info = get_company_info(selected_symbol)
    company_website = company_info["website"]
    company_summary = company_info["longBusinessSummary"]
    st.write(company_website)
    st.write(company_summary)

    # Date selection for historical data
    st.sidebar.subheader("Select Date Range for Historical Data")
    start_date = st.sidebar.date_input("Start Date", pd.to_datetime('2022-01-01'))
    end_date = st.sidebar.date_input("End Date", pd.to_datetime('today'))

    # Get historical data
    st.subheader("Historical Stock Data")
    historical_data = get_historical_data(selected_symbol, start_date, end_date)
    st.line_chart(historical_data['Close'])

    # Display Financial Metrics
    st.subheader("Financial Metrics")
    income_statement, balance_sheet, cash_flow, _, _, _ = get_financial_data(selected_symbol)
    financial_summary = calculate_financial_metrics(income_statement, balance_sheet, cash_flow)
    st.write(financial_summary)

    # Display Additional Data
    st.subheader("Additional Data")
    sustainability, institutional_holders, mutualfund_holders, news, calendar, actions, history, major_holders = get_additional_data(selected_symbol)

    # Sustainability Data
    st.subheader("Sustainability Data")
    if sustainability is not None:
        st.write(sustainability)
    else:
        st.write("No sustainability data available.")

    # Latest News
    st.subheader("Latest News")
    for article in news:
        st.write(f"**{article['title']}**")
        st.write(article['link'])
        # st.write(article)

    # Display Major Holders
    st.subheader("Major Holders")
    st.write(major_holders)

    # Display Calendar Events (e.g. Earnings)
    st.subheader("Upcoming Calendar Events")
    # st.write(calendar)
    # Loop through the calendar dictionary to display its content
    for key, value in calendar.items():
        st.markdown(f"**{key}:** {format_value(value)}")

with tab2:
    st.header("Valuation Prediction by AI")
    query = st.text_input("Ask Anything about any Company", value="")
    if st.button("Submit"):
        response = ask_query(query)
        st.write("Response by AI :")
        st.markdown(response)
    # Fetching the forecasts and WACC using the helper functions
    if st.button("Get Forecast"):
        forecast = get_forecast(selected_company)
        st.write("Forecast for Sales Growth and Operating Margins:")
        st.text(forecast)

    if st.button("Get WACC"):
        wacc = get_wacc(selected_company)
        st.write("Weighted Average Cost of Capital (WACC):")
        st.text(wacc)

with tab3:
    sustainability, institutional_holders, mutualfund_holders, news, calendar, actions, history, major_holders = get_additional_data(selected_symbol)
    st.header("Sentiment Analysis by AI")
    query = st.text_input("Ask Anything about any Company", value="" , key = "Sentiment-Analysis")
    if st.button("Get Sentiment Analysis"):
        response , docs = get_sentiment_analysis(query , news)
        output_text = response.get('output_text', 'No response')  # Extract the 'output_text' from the response
        st.markdown(output_text)
        # st.write(docs)


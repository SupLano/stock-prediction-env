import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR as MyCustomSVM



# Function to predict stock prices
# Function to predict stock prices
default_start_date = datetime.today() - timedelta(days=365)
def predict_stock_price(stock_data):
    # Feature engineering (assuming simple linear regression)
    stock_data['Date'] = stock_data.index
    stock_data['Date'] = range(len(stock_data))  # Assign a numerical index to the date
    X = stock_data[['Date']].values
    y = stock_data['Close'].values

    # Split the data into training and testing sets
    
    try:
    # Attempt to perform the train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    except ValueError:
    # Handle the error with a custom warning message
        st.warning("Insufficient data to perform train-test split. Please select a larger date range.")
        X_train, X_test, y_train, y_test = None, None, None, None


    # Create and train the linear regression model
    model = MyCustomSVM()
    model.fit(X_train, y_train)

    # Predict stock prices
    predictions = model.predict(X_test)

    return predictions[-1]

# List of popular stock options with company names
popular_stocks = {
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corporation",
    "GOOGL": "Alphabet Inc. (Google)",
    "TSLA": "Tesla, Inc.",
    "AMZN": "Amazon.com, Inc.",
    "NVDA": "NVIDIA Corporation",
    "NFLX": "Netflix, Inc.",
    "CRM": "Salesforce.com, Inc.",
    "ADBE": "Adobe Inc.",
    "SHOP": "Shopify Inc.",
    "SQ": "Square, Inc.",
    "PYPL": "PayPal Holdings, Inc.",
    "ZM": "Zoom Video Communications, Inc.",
    "DOCU": "DocuSign, Inc.",
    "SNAP": "Snap Inc.",
    "UBER": "Uber Technologies, Inc.",
    "PINS": "Pinterest, Inc.",
    "ROKU": "Roku, Inc.",
    "TWTR": "Twitter, Inc.",
    "AMD": "Advanced Micro Devices, Inc.",
    "INTC": "Intel Corporation",
    "TSM": "Taiwan Semiconductor Manufacturing Company Limited",
    "CSCO": "Cisco Systems, Inc.",
    "QCOM": "QUALCOMM Incorporated",
    "JPM": "JPMorgan Chase & Co.",
    "GS": "The Goldman Sachs Group, Inc.",
    "C": "Citigroup Inc.",
    "BAC": "Bank of America Corporation",
    "WFC": "Wells Fargo & Co.",
    "AMGN": "Amgen Inc.",
    "BIIB": "Biogen Inc.",
    "GILD": "Gilead Sciences, Inc.",
    "REGN": "Regeneron Pharmaceuticals, Inc.",
    "MRNA": "Moderna, Inc.",
    "XOM": "Exxon Mobil Corporation",
    "CVX": "Chevron Corporation",
    "TSLA": "Tesla, Inc.",
    "V": "Visa Inc.",
    "MA": "Mastercard Incorporated",
    "DIS": "The Walt Disney Company",
    "CMCSA": "Comcast Corporation",
    "T": "AT&T Inc.",
    "TMUS": "T-Mobile US, Inc.",
    "VZ": "Verizon Communications Inc.",
    "PFE": "Pfizer Inc.",
    "MRK": "Merck & Co., Inc.",
    "JNJ": "Johnson & Johnson",
    "ABBV": "AbbVie Inc.",
    "GSK": "GlaxoSmithKline plc",
    "WMT": "Walmart Inc.",
    "COST": "Costco Wholesale Corporation",
    "HD": "The Home Depot, Inc.",
    "LOW": "Lowe's Companies, Inc.",
    "TGT": "Target Corporation",
    "NKE": "NIKE, Inc.",
    "SBUX": "Starbucks Corporation",
    "MCD": "McDonald's Corporation",
    "YUM": "Yum! Brands, Inc.",
    "QSR": "Restaurant Brands International Inc.",
    "CVS": "CVS Health Corporation",
    "WBA": "Walgreens Boots Alliance, Inc.",
    "RAD": "Rite Aid Corporation",
    "UNH": "UnitedHealth Group Incorporated",
    "ANTM": "Anthem, Inc.",
    "AET": "Aetna Inc.",
    "HUM": "Humana Inc.",
    "CI": "Cigna Corporation",
    "AFL": "Aflac Incorporated",
    "MET": "MetLife, Inc.",
    "TMO": "Thermo Fisher Scientific Inc.",
    "DHR": "Danaher Corporation",
    "BMY": "Bristol-Myers Squibb Company",
    "REGN": "Regeneron Pharmaceuticals, Inc."
}


# Set Streamlit page configuration
st.set_page_config(
    page_title="Stock Price Prediction",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Calculate the default start date (1 year ago from the current date)
default_start_date = datetime.today() - timedelta(days=365)

# Create a Streamlit app
st.title("Stock Price Prediction Software")

# Centered description of how the program works
st.markdown(
    """
    <div>
    <h3>This web app allows you to predict stock prices for popular companies.</h3>
    <p>Select a stock symbol, choose a date range (Minimum: 6 Months), and the app will provide you with historical stock data and a predicted stock price.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar with buttons for popular stock options
# Create a dictionary mapping company names to stock symbols
company_to_symbol = {v: k for k, v in popular_stocks.items()}

# Sidebar with buttons for popular stock options
st.sidebar.markdown("<h2 style='font-size: 24px;'>Popular Stock Markets:</h2>", unsafe_allow_html=True)

# Use a separate variable for the selected stock symbol
selected_company = st.sidebar.radio("", list(popular_stocks.values()))

# Get the selected stock symbol based on the selected company name
selected_symbol = company_to_symbol[selected_company]

# Input widgets (stock symbol and date range)
col1, col2, col3 = st.columns(3)
stock_symbol = col1.text_input("Enter Stock Symbol:", value=selected_symbol)
start_date = col2.date_input("Start Date:", default_start_date)  # Set the default value
end_date = col3.date_input("End Date:")

# Retrieve stock data using yfinance
if stock_symbol and start_date and end_date:
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)

    # Create a custom function to apply color based on price comparison
    def color_price(val):
        color = 'color: red' if val < stock_data['Close'].iloc[-1] else 'color: green'
        return color

    # Apply the custom function to the DataFrame
    styled_stock_data = stock_data.style.applymap(color_price, subset=pd.IndexSlice[:, 'Open':'Volume'])

    # Display the styled DataFrame
    st.subheader(f"Historical Stock Data for {popular_stocks.get(stock_symbol, 'Unknown Company')}")
    st.dataframe(styled_stock_data, width=1000, height=500)

    # Model prediction (use your prediction model here)
    prediction = predict_stock_price(stock_data)
# Get the last actual price
    last_actual_price = stock_data["Close"].iloc[-1]

    # Compare the predicted price with the last actual price and set the color accordingly
    price_color = "green" if prediction > last_actual_price else "red"

    # Create a figure and axis for the chart
    # ... Your previous code ...

# Create a Plotly figure with a full-width layout
    fig = go.Figure()

    # Plot the historical stock data
    fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name='Historical Data', line=dict(color='blue')))

    # Plot the predicted stock price
    fig.add_trace(go.Scatter(x=[stock_data.index[-1]], y=[prediction], mode='markers', name='Predicted Price', marker=dict(color=price_color, size=10)))

    # Set chart labels and title
    fig.update_layout(
        title=f"Stock Price Prediction for {popular_stocks.get(stock_symbol, 'Unknown Company')}",
        xaxis_title="Date",
        yaxis_title="Stock Price"
    )

    # Set the width of the Plotly chart to occupy full width
    fig.update_layout(width=1000)  # You can adjust the width as needed

    # Show the chart using st.plotly_chart
    st.plotly_chart(fig, use_container_width=True)  # use_container_width=True for full width

    # Display the prediction with the determined color
    st.subheader("Result")
    centered_style = (
    "display: flex; justify-content: center; align-items: center; text-align: center;"
    )

# Center the "Predicted Stock Price" section using HTML formatting
    centered_prediction = (
    f"<div style='{centered_style}'>"
    f"<span style='color:{price_color}; font-size: 20px; text-align: center;'>Predicted Stock Price: ${prediction:.2f}</span>"
    "</div>"
    )

# Display the centered prediction using st.markdown()
    st.markdown(centered_prediction, unsafe_allow_html=True)

# Add a footer with acknowledgments
    st.markdown(
    """
    ---

    ## Acknowledgments

    - Special thanks to   DR D.J.S SAKO for their valuable contributions.


    *Built by DE.2017/4538 - ORAGWA CHINONYEREM LAWRENCE :heart:*
    """,
    unsafe_allow_html=True,
)

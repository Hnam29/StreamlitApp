from database import create_table, add_user, login_user, view_all
import pandas as pd 
# PAGE "HOME + STOCK"
from vnstock import * # import all functions
import streamlit as st 
from streamlit_option_menu import option_menu # config menu 
# PAGE "CONTACT"
from st_functions import st_button, load_css
from PIL import Image
import time
import sqlite3
import datetime
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go


# REAL TIME 
now = datetime.now()
current_time = now.strftime("%d/%m/%Y %H:%M:%S")
# CONFIG LAYOUT 
page_title = 'Vietnam Stock Dashboard'
page_icon = '💱'
layout = 'wide'
st.set_page_config(page_title=page_title, page_icon=page_icon,layout=layout)
# DELETE WATERMARK
hide = '''
        <style>
        #MainMenu {visibility:hidden}
        header {visibility:hidden}
        footer {visibility:hidden}
        </style>
        '''
st.markdown(hide, unsafe_allow_html=True)
# DATABASE
connect = sqlite3.connect('authentication.db')
c = connect.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS user (time TEXT, username TEXT, password TEXT)')

def add_user(time, username, password):
    c.execute('INSERT INTO user VALUES(?,?,?)', (time, username, password))
    connect.commit()

def login_user(username, password):
    c.execute('SELECT * FROM user WHERE username=? AND password=?', (username, password))
    data = c.fetchall()
    return data 

def view_all():
    c.execute('SELECT * FROM user')
    data = c.fetchall()
    return data 

# MAIN FUNCTION
def stock():
    list_com = listing_companies().ticker.sort_values(ascending=True)
    company_name = st.selectbox('Select your company:',list_com)
    if company_name is not None:
        st.write(company_overview(f'{company_name}'))
    else:
        st.warning("Type your company name first")
    # Historical Price
    start_date = st.date_input('Choose your start date:')
    end_date = st.date_input('Choose your end date:')
    # Convert date objects to strings
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    st.write(stock_historical_data(f'{company_name}',start_date_str,end_date_str,'1D'))
    df = stock_historical_data(f'{company_name}', start_date_str, end_date_str, '1D')
    # Convert the DataFrame to a CSV file in memory
    csv_file = df.to_csv(index=False)
    # Create a download link for the CSV file
    st.download_button(
                label='Download CSV',
                data=csv_file,
                file_name='data.csv',
                mime='text/csv'
    )
    with st.expander('Dashboard'):
        # LINE
        c1,c3,c2 = st.columns(3)
        last_2close = df['close'].tail(2)
        c1.metric(label="Close Price (compare with yesterday)",
                value=last_2close.iloc[-1],
                delta=int(last_2close.iloc[-1] - last_2close.iloc[0]))
        y_col1 = c1.selectbox('Select y column', options=df.columns[1:], key='y_co1l')
        fig1 = px.line(df, x=df['time'], y=y_col1)
        fig1.update_layout(
        width=400,  
        height=400  
        )
        c1.plotly_chart(fig1)
        # HISTOGRAM
        last_2vol = df['volume'].tail(2)
        c3.metric(label="Highest volume",
                value=df['volume'].max(),
                delta=int(last_2vol.iloc[-1] - last_2vol.iloc[0]))
        y_col3 = c3.selectbox('Select y column', options=df.columns[1:], key='y_col3')
        fig3 = px.histogram(df, x=df['time'], y=y_col3)
        fig3.update_layout(
        width=400,  
        height=400  
        )
        c3.plotly_chart(fig3)
        # SCATTER
        c2.metric(label="Total days",
                value=df.shape[0],
                delta=int(df.shape[0]/30))
        y_col2 = c2.selectbox('Select y column', options=df.columns[1:], key='y_col2')
        fig2 = px.scatter(df, x=df['time'], y=y_col2, size=df['volume'])
        fig2.update_layout(
        width=400,  
        height=400  
        )
        c2.plotly_chart(fig2)

    company = listing_companies()
    number_of_coms = st.write(f'There are {len(company)} companies.')
    # tickers = st.multiselect('See the specific company ?', company.ticker)
    index = st.sidebar.selectbox('Which index do you want to see ?',company['comGroupCode'].unique())
    sector = st.sidebar.selectbox('That company functions in which sector ?',company.sector.unique())
    filtered_company = company[(company['comGroupCode'] == index) & (company['sector'] == sector)]
    company_quantity = st.slider('How many companies do you want to see ?',1,filtered_company.shape[1])
    st.write(filtered_company[0:company_quantity])
    
    # # 📊 Price Table
    # with st.expander('Price Table'):
    #     st.write(price_depth(tickers))
    #     st.write(price_board(tickers))
    # 🔥 Intraday Trading Data
    # com = st.selectbox('Choose your company',options=listing_companies.ticker)
    # while True:
    #     st.dataframe(stock_intraday_data(symbol=com, page_size=1000))
    #     # Optionally, introduce a delay between executions
    #     time.sleep(60)  # Sleep for 60 seconds between executions







def main():
# MENU 
    # -- SIDE BAR --
    with st.sidebar:
        selected = option_menu(
            menu_title='Menu', #required (default:None)
            options=['Home','Stock','Contact'], #required
            icons=['house','currency-exchange','person-lines-fill'], #optional -> find on Bootstrap
            menu_icon='cast', #optional
            default_index=0 #optional
        )
    c1,c2 = st.columns([4.6,5.4])
    c2.title(f'{selected}')
    # ------------------------
    if selected == 'Home':
        # -- NAVIGATION BAR --
        options = option_menu(
            menu_title=None,
            options=['Data Entry','Data Visualization','Database'],
            icons=['pencil-fill','bar-chart-fill','database-check'],
            orientation='horizontal',
            styles={
                'container':{'padding':'0!important','background-color':'#e3ac71'},
                'icon':{'color':'#e37171','font-size':'25px'},
                'nav-link': {
                    'font-size':'25px',
                    'text-align':'center',
                    'margin': '0px',
                    '--hover-color': '#9bd3d4',
                },
                'nav-link-selected': {'background-color':'#5d9965'},
            },
        )
        if options == 'Data Entry':
            st.info('Tomorrow nhe')
        if options == 'Data Visualization':
            st.info('Still tomorrow nhe')
        if options == 'Database':
            st.warning('Wait')
            time.sleep(2)
            with st.expander('Here you go :)'):
                user_result = view_all()
                database = pd.DataFrame(user_result,columns=['Time','Username','Password'])
                st.dataframe(database)

    # ------------------------
    if selected == 'Contact':
        load_css()
        col1, col2 = st.columns([3,7])
        col1.image(Image.open('/Users/vuhainam/Documents/PROJECT_DA/VNStockMarket/StockDashboard/Hector.jpg'))
        col2.header('Hector Vu :flag-vn: Data Analyst')
        col2.info('An Analyst with an interest in Data Analytics, Data Engineering and Data Science (maybe also Analytics Engineering) :chart:')
        icon_size = 20

        st_button(icon='facebook', url='https://www.facebook.com/Hnam.2909', label='Facebook', iconsize=icon_size)
        st_button(icon='github',   url='https://github.com/Hnam29',  label='Github',   iconsize=icon_size)
        st_button(icon='instagram',url='https://www.instagram.com/namvh.29/',label='Instagram', iconsize=icon_size)
        st_button(icon='linkedin', url='https://www.linkedin.com/in/hector2909/', label='LinkedIn', iconsize=icon_size)
    # ------------------------
    if selected == 'Stock':
        stock()

# AUTHENTICATION
st.sidebar.title('Login Interface Authentication')
menu = ['Login','Sign Up']
choice = st.sidebar.selectbox('Menu',menu)
if choice == 'Login':
    username = st.sidebar.text_input('User name:')
    password = st.sidebar.text_input('Password:',type='password')
    # if st.sidebar.checkbox('Login'):
    login = st.sidebar.button('Login')
    # Initialize session state
    if 'load_state' not in st.session_state:
        st.session_state.load_state = False
    if login or st.session_state.load_state:
        st.session_state.load_state = True
        create_table()
        result = login_user(username,password)
        if result:
            st.sidebar.success(f'Hi {username}, hope you will have a good day.')
            st.sidebar.write(f'Log in at: {current_time}')
            main()
        else:
            st.warning('Incorrect password')
if choice == 'Sign Up':
    new_user = st.sidebar.text_input('Type your username')
    new_password = st.sidebar.text_input('Enter your password',type='password')
    if st.sidebar.button('Sign Up'):
        create_table()
        add_user(current_time, new_user, new_password)
        st.success('Account created, please log in')
    

# WORK FLOW
# if __name__ == '__main__': 
#     main()

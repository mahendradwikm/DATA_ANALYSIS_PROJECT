import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime
import datetime as dt

#load data csv
all_df = pd.read_csv("all_data.csv")

import streamlit as st

import streamlit as st

import streamlit as st

# Sidebar
with st.sidebar:
    st.markdown(
        """
        <div style='display: flex; align-items: center; justify-content: center;'>
            <img src='https://github.com/mahendradwikm/progres-belajarku/blob/main/logo.png' alt='Logo' style='width: 80px; height: 80px;'>
            <div style='margin-left: 10px; font-size: 24px; font-weight: bold; color: #53ECEC;'>Mahendra E-Commerce Projects</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<hr style='margin: 15px 0; border-color: #53ECEC;'>", unsafe_allow_html=True)

    st.markdown("### E-Commerce Dataset")
    st.markdown("[Kaggle E-Commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)")

    st.markdown("<hr style='margin: 15px 0; border-color: #53ECEC;'>", unsafe_allow_html=True)

    st.markdown("### About")
    st.markdown(
        """
        This dashboard displays insights from the E-Commerce dataset. 
        You can explore various visualizations and analyze the data accordingly.
        """
    )

    st.markdown("<hr style='margin: 15px 0; border-color: #53ECEC;'>", unsafe_allow_html=True)

    st.markdown("### Contact")
    st.markdown(
        """
        If you have any questions or feedback, feel free to reach out at:
        - Email: [mahendradwikm@gmail.com](mailto:mahendradwikm@gmail.com)
        - Linkedin: [mahendradwikm](https://www.linkedin.com/in/mahendradwikm)
        """,
        unsafe_allow_html=True
    )



# UBAH TIPE str/obj -> datetime
datetime_columns = ["order_approved_at"]
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

def number_order_per_month(df):
    monthly_df = df.resample(rule='M', on='order_approved_at').agg({
        "order_id": "size",
    })
    monthly_df.index = monthly_df.index.strftime('%B')
    monthly_df = monthly_df.reset_index()
    monthly_df.rename(columns={
        "order_id": "order_count",
    }, inplace=True)
    monthly_df = monthly_df.sort_values('order_count').drop_duplicates('order_approved_at', keep='last')
    month_mapping = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12
    }

    monthly_df["month_numeric"] = monthly_df["order_approved_at"].map(month_mapping)
    monthly_df = monthly_df.sort_values("month_numeric")
    monthly_df = monthly_df.drop("month_numeric", axis=1)
    return monthly_df

def customer_spend_df(df):
    sum_spend_df = df.resample(rule='M', on='order_approved_at').agg({
            "price": "sum"
    })
    sum_spend_df = sum_spend_df.reset_index()
    sum_spend_df.rename(columns={
                "price": "total_spend"
            }, inplace=True)
    sum_spend_df['order_approved_at'] = sum_spend_df['order_approved_at'].dt.strftime('%B') 
    sum_spend_df = sum_spend_df.sort_values('total_spend').drop_duplicates('order_approved_at', keep='last')
    custom_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


    sum_spend_df['month_cat'] = pd.Categorical(sum_spend_df['order_approved_at'], categories=custom_order, ordered=True)


    sorted_df = sum_spend_df.sort_values(by='month_cat')


    sorted_df = sorted_df.drop(columns=['month_cat'])
    return sorted_df


def create_by_product_df(df):
    product_id_counts = df.groupby('product_category_name_english')['product_id'].count().reset_index()
    sorted_df = product_id_counts.sort_values(by='product_id', ascending=False)
    return sorted_df

def rating_cust_df(df):
    rating_service = df['review_score'].value_counts().sort_values(ascending=False)
    
    max_score = rating_service.idxmax()

    df_cust=df['review_score']

    return (rating_service,max_score,df_cust)

def create_rfm(df):
    now=dt.datetime(2018,10,20)


    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    # Group by 'customer_id' and calculate Recency, Frequency, and Monetary
    recency = (now - df.groupby('customer_id')['order_purchase_timestamp'].max()).dt.days
    frequency = df.groupby('customer_id')['order_id'].count()
    monetary = df.groupby('customer_id')['price'].sum()

    # Create a new DataFrame with the calculated metrics
    rfm = pd.DataFrame({
        'customer_id': recency.index,
        'Recency': recency.values,
        'Frequency': frequency.values,
        'Monetary': monetary.values
    })
    #End alternative 2

    col_list = ['customer_id','Recency','Frequency','Monetary']
    rfm.columns = col_list
    return rfm


# MEMANGGIL KEMBALI functions
daily_orders_df=number_order_per_month(all_df)
most_and_least_products_df=create_by_product_df(all_df)
rating_service,max_score,df_rating_service=rating_cust_df(all_df)
customer_spend_df=customer_spend_df(all_df)
rfm=create_rfm(all_df)


# Header
st.markdown(
    """
    <div style='text-align: center;'>
        <h1 style='color: #53ECEC;'>DASHBOARD ANALISIS DATA E-COMMERCE 🙏</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Sub Header
st.markdown(
    """
    <div style='text-align: center;'>
        <h2 style='color: ##53ECEC;'>Visualisasi Data E-Commerce</h2>
    </div>
    """,
    unsafe_allow_html=True
)

# ================================= PERFORMA PENJUALAN ===================================

st.subheader('Performa Penjualan')
col1, col2 = st.columns(2)

with col1:
    high_order_num = daily_orders_df['order_count'].max()
    high_order_month = daily_orders_df[daily_orders_df['order_count'] == daily_orders_df['order_count'].max()]['order_approved_at'].values[0]

with col2:
    low_order = daily_orders_df['order_count'].min()
    low_order_month = daily_orders_df[daily_orders_df['order_count'] == daily_orders_df['order_count'].min()]['order_approved_at'].values[0]

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["order_approved_at"],
    daily_orders_df["order_count"],
    marker='o',
    linewidth=2,
    color="#53ECEC",
    mec='black',
    mew=1,
)
plt.xticks(rotation=45, fontsize=14)  # Menambahkan font size untuk sumbu x
plt.yticks(fontsize=12)  # Menambahkan font size untuk sumbu y
ax.set_title("Tren Jumlah Order Bulanan di 2018", fontsize=24)  # Menambahkan judul dengan font size 24
ax.set_xlabel("Bulan", fontsize=14)  # Menambahkan keterangan sumbu x dengan font size 14
ax.set_ylabel("Jumlah Order", fontsize=12)  # Menambahkan keterangan sumbu y dengan font size 12

st.pyplot(fig)


# ================================ PRODUK PALING LAKU =================================

import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Menampilkan subjudul untuk bagian "Most And Least Product"
st.subheader("Produk Paling Laris dan Tidak Laku")

# Membuat subplot untuk menampilkan dua plot bar
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(18, 6))  

colors = ["#53ECEC", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]  # Mengubah warna

# Plot untuk 5 produk teratas
most_products_df = create_by_product_df(all_df)  # asumsi 'all_df' adalah DataFrame yang sesuai
sns.barplot(x="product_id", y="product_category_name_english", data=most_products_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Top 5 Best Selling Products (Laku)", loc="center", fontsize=16)
ax[0].tick_params(axis='y', labelsize=12)

# Plot untuk 5 produk terbawah
least_products_df = create_by_product_df(all_df)  # asumsi 'all_df' adalah DataFrame yang sesuai
sns.barplot(x="product_id", y="product_category_name_english", data=least_products_df.sort_values(by="product_id", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Top 5 Least Selling Products(≠Laku)", loc="center", fontsize=16)
ax[1].tick_params(axis='y', labelsize=12)

# Menambahkan stroke hitam pada warna #53ECEC untuk ax[0] dan ax[1]
for bar in ax[0].patches:
    bar.set_edgecolor('black')
    bar.set_linewidth(1.5)

for bar in ax[1].patches:
    bar.set_edgecolor('black')
    bar.set_linewidth(1.5)

# Menampilkan plot menggunakan Streamlit
st.pyplot(fig)


# ============================= RATING LAYANAN PELANGGAN =================================

# Fungsi untuk menampilkan plot menggunakan Streamlit
def show_barplot(review_scores, most_common_score):
    plt.figure(figsize=(10, 5))
    sns.barplot(x=review_scores.index,
                y=review_scores.values,
                order=review_scores.index,
                palette=["#53ECEC" if score == most_common_score else "#D3D3D3" for score in review_scores.index],
                edgecolor=["black" if score == most_common_score else "none" for score in review_scores.index],
                linewidth=1.5)
    plt.title("Rating Layanan dari Pelanggan", fontsize=20)
    plt.xlabel("Rating", fontsize=14)
    plt.ylabel("Jumlah", fontsize=14)
    plt.xticks(fontsize=12)
    st.pyplot(plt)

# Fungsi rating_cust_df untuk mendapatkan data rating
def rating_cust_df(df):
    rating_service = df['review_score'].value_counts().sort_values(ascending=False)
    max_score = rating_service.idxmax()
    df_cust = df['review_score']
    return rating_service, max_score, df_cust

# Dummy DataFrame untuk keperluan contoh
import pandas as pd
import numpy as np

# Buat DataFrame dummy
data = {'review_score': np.random.randint(1, 6, size=100)}  # Generate random data for review scores
df = pd.DataFrame(data)

# Panggil fungsi rating_cust_df
rating_service, most_common_score, _ = rating_cust_df(df)

# Tampilkan plot menggunakan Streamlit
st.title("Rating Layanan dari Pelanggan")
show_barplot(rating_service, most_common_score)


# ======================================== RFM ===========================================
st.subheader("RFM Best Value")


colors = ["#53ECEC", "#53ECEC", "#53ECEC", "#53ECEC", "#53ECEC"]

######################################
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Define colors
colors = ["#53ECEC", "#53ECEC", "#53ECEC", "#53ECEC", "#53ECEC"]

# Create tabs
tab1, tab2, tab3 = st.columns(3)

with tab1:
    st.subheader("By Recency (days)")
    fig, ax = plt.subplots(figsize=(16, 8))
    sns.barplot(
        y="Recency",
        x="customer_id",
        data=rfm.sort_values(by="Recency", ascending=True).head(5),
        palette=colors,
        edgecolor='black',
        linewidth=1.5
    )
    plt.xlabel("customer_id")
    plt.xticks([])
    st.pyplot(fig)

with tab2:
    st.subheader("By Frequency")
    fig, ax = plt.subplots(figsize=(16, 8))
    sns.barplot(
        y="Frequency",
        x="customer_id",
        data=rfm.sort_values(by="Frequency", ascending=False).head(5),
        palette=colors,
        edgecolor='black',
        linewidth=1.5
    )
    plt.xlabel("customer_id")
    plt.xticks([])
    st.pyplot(fig)

with tab3:
    st.subheader("By Monetary")
    fig, ax = plt.subplots(figsize=(16, 8))
    sns.barplot(
        y="Monetary",
        x="customer_id",
        data=rfm.sort_values(by="Monetary", ascending=False).head(5),
        palette=colors,
        edgecolor='black',
        linewidth=1.5
    )
    plt.xlabel("customer_id")
    plt.xticks([])
    st.pyplot(fig)


# ========================================DEMOGRAFI=======================================

import streamlit as st
import pandas as pd

# Load data
all_df = pd.read_csv("all_data.csv")

# Calculate customer count by state
bystate_df = all_df.groupby(by="customer_state").customer_id.nunique().reset_index()
bystate_df.rename(columns={"customer_id": "customer_count"}, inplace=True)

# Main content
st.title("Demografi Pelanggan")

# Add empty columns to center the DataFrame
left_column, center_column, right_column = st.columns([1, 4, 1])

# Add the DataFrame to the center column
with center_column:
    st.write(bystate_df)


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
all_df = pd.read_csv("all_data.csv")

# Function to create visualization for customer city
def plot_customer_city():
    bycity_df = all_df['customer_city'].value_counts().head(10)

    plt.figure(figsize=(12, 6))

    most_common_city = bycity_df.idxmax()

    bycity_df = bycity_df.sort_values(ascending=False)

    # Define colors and edge colors
    colors = ["#53ECEC" if city == most_common_city else "#D3D3D3" for city in bycity_df.index]
    edge_colors = ["black" if city == most_common_city else "none" for city in bycity_df.index]

    sns.barplot(x=bycity_df.index,
                y=bycity_df.values,
                palette=colors,
                edgecolor=edge_colors,
                linewidth=1.5
                )

    plt.title("Jumlah Pelanggan dari Tiap Kota", fontsize=20)
    plt.xlabel("Kota", fontsize=14)
    plt.ylabel("Jumlah Pelanggan", fontsize=14)
    plt.xticks(rotation=45, fontsize=10)

    # Display the plot in Streamlit
    st.pyplot(plt)

# Function to create visualization for customer state
def plot_customer_state():
    bystate_df = all_df.groupby(by="customer_state").customer_id.nunique().reset_index()
    bystate_df.rename(columns={"customer_id": "customer_count"}, inplace=True)

    plt.figure(figsize=(12, 6))

    most_common_state = bystate_df.loc[bystate_df['customer_count'].idxmax(), 'customer_state']

    bystate_df = bystate_df.sort_values(by='customer_count', ascending=False)

    # Define colors and edge colors
    colors = ["#53ECEC" if state == most_common_state else "#D3D3D3" for state in bystate_df['customer_state']]
    edge_colors = ["black" if state == most_common_state else "none" for state in bystate_df['customer_state']]

    sns.barplot(x='customer_state',
                y='customer_count',
                data=bystate_df,
                palette=colors,
                edgecolor=edge_colors,
                linewidth=1.5
                )

    plt.title("Jumlah Pelanggan dari Tiap Negara Bagian", fontsize=20)
    plt.xlabel("Negara Bagian", fontsize=14)
    plt.ylabel("Jumlah Pelanggan", fontsize=14)
    plt.xticks(fontsize=10)

    # Display the plot in Streamlit
    st.pyplot(plt)

# Main content
st.title("DEMOGRAFI PELANGGAN E-COMMERCE")

# Add the visualizations to the Streamlit app side by side
st.subheader("Visualisasi Jumlah Pelanggan")
col1, col2 = st.columns(2)  # Membagi tata letak menjadi dua kolom

with col1:
    plot_customer_city()

with col2:
    plot_customer_state()

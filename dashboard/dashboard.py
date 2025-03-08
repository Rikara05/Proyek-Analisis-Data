import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Fungsi Pembantu
def get_top_revenue_categories(df, top_n=5):
    revenue = df.groupby('product_category_name')['price'].sum().reset_index()
    revenue = revenue.sort_values(by='price', ascending=False).head(top_n)
    revenue['formatted_price'] = revenue['price'].apply(lambda x: format_currency(x, 'IDR', locale='id_ID'))
    return revenue

def get_top_reviewed_categories(df, top_n=5):
    reviews = df.groupby('product_category_name')['review_score'].mean().reset_index()
    return reviews.sort_values(by='review_score', ascending=False).head(top_n)

def get_order_trend(df):
    df['order_month'] = df["order_purchase_timestamp"].dt.to_period('M')
    trend = df.groupby("order_month").size().reset_index(name="order_count")
    trend['order_month'] = trend['order_month'].astype(str)
    return trend

# Load data
df = pd.read_csv("dashboard/all_data.csv")  # Jika file ada di folder yang sama dengan script

df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
min_date = df["order_purchase_timestamp"].min().date()
max_date = df["order_purchase_timestamp"].max().date()

top_revenue_categories = get_top_revenue_categories(df)
top_reviewed_categories = get_top_reviewed_categories(df)
order_trend = get_order_trend(df)

# Hitung hasil analisis
total_orders = len(df)
total_revenue = df['price'].sum()
avg_review_score = df['review_score'].mean()
formatted_total_revenue = format_currency(total_revenue, 'IDR', locale='id_ID')

# Sidebar
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    st.title("Dicoding Colection")
    st.header("Rika Rostika Afipah")
    st.subheader("Universitas Logistik dan Bisnis Internasional")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Header Dashboard
st.header('📊 E-Commerce Dashboard')

# Tampilkan Hasil Analisis di Atas Dashboard
col1, col2, col3 = st.columns(3)
col1.metric(label="📦 Total Pesanan", value=total_orders)
col2.metric(label="💰 Total Pendapatan", value=formatted_total_revenue)
col3.metric(label="⭐ Rata-rata Skor Review", value=round(avg_review_score, 2))

# Kategori dengan Pendapatan Tertinggi
st.subheader("🛍️ 5 Kategori Produk dengan Pendapatan Tertinggi")
max_category = top_revenue_categories.iloc[0]['product_category_name']
max_revenue = top_revenue_categories.iloc[0]['formatted_price']
st.metric(label="🏆 Kategori Pendapatan Tertinggi", value=max_category, help=f"Pendapatan: {max_revenue}")
st.write("Kategori produk berikut memberikan kontribusi terbesar terhadap total pendapatan.")
fig, ax = plt.subplots(figsize=(12,6))
sns.barplot(x='price', y='product_category_name', data=top_revenue_categories,
            palette='Blues_r', ax=ax)
ax.set_xlabel("Total Pendapatan")
ax.set_ylabel("Kategori Produk")
ax.set_title("5 Kategori Produk dengan Pendapatan Tertinggi")
st.pyplot(fig)

# Produk dengan Skor Review Tertinggi
st.subheader("⭐ Produk dengan Skor Review Tertinggi")
max_review_category = top_reviewed_categories.iloc[0]['product_category_name']
max_review_score = round(top_reviewed_categories.iloc[0]['review_score'], 2)
st.metric(label="🏅 Kategori Review Tertinggi", value=max_review_category, help=f"Skor: {max_review_score}")
st.write("Produk dengan skor review tinggi menunjukkan kepuasan pelanggan yang baik.")
fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(x='review_score', y='product_category_name', data=top_reviewed_categories,
            palette='Reds_r', ax=ax)
ax.set_xlabel("Skor Review Rata-rata")
ax.set_ylabel("Kategori Produk")
ax.set_title("Produk dengan Skor Review Tertinggi")
st.pyplot(fig)

# Tren Penjualan per Bulan
st.subheader("📈 Tren Jumlah Pesanan per Bulan")
max_month = order_trend.iloc[order_trend['order_count'].idxmax()]['order_month']
max_orders = order_trend['order_count'].max()
st.metric(label="📅 Tahun dan Bulan dengan Pesanan Terbanyak", value=max_month, help=f"Total Pesanan: {max_orders}")
st.write("Grafik berikut menunjukkan bagaimana tren pesanan berkembang dari waktu ke waktu.")
fig, ax = plt.subplots(figsize=(12,6))
sns.lineplot(data=order_trend, x='order_month', y='order_count',
             marker='o', color='green', ax=ax)
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Pesanan")
ax.set_title("Tren Jumlah Pesanan per Bulan")
plt.xticks(rotation=45)
st.pyplot(fig)

st.caption('Copyright @ Rika Rostika Afipah 2025')

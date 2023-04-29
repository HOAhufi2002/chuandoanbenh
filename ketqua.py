import streamlit as st
import pandas as pd
import pyodbc
import matplotlib.pyplot as plt

# Connect to SQL Server database
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=MINHHOA\SQLEXPRESS;'
                      'Database=ganmantinh;'
                      'Trusted_Connection=yes;')

# Set page title
st.set_page_config(page_title="Lịch sử khám bệnh", page_icon=":hospital:", layout="wide")

# Define page header and subheader
st.title("Lịch sử khám bệnh")
st.write("Trang web này hiển thị thông tin về lịch sử khám bệnh của bệnh nhân.")

# Execute query to fetch data from table
query = """SELECT thongtinbenhnhan.id, tenbenhnhan, diachi, sdt, thongtinbenhnhan.tuoi, gioitinh, 
trieuchung.matrieuchung, trieuchung.tuoi as  huyetap, albumin, 
mucdoduongtrongnuoctieu, hongcautrongnuoctieu, tebaomutrongnuoctieu, bongumutrongnuoctieu, 
vikhuantrongnuoctieu, luongduonghuyet, nongdo_ure, nongdo_creatinine, nongdonatri, nongdokali, 
nongdo_hemoglobin, thetichhongcau, soluongbachcau, soluonghongcau, tanghuyetap, tieuduong, 
benhdongmachvanh, ngonmieng, phu_chan, lichsukhambenh.malichsukham,tilemacbenh,tilekhongmacbenh
FROM thongtinbenhnhan 
JOIN trieuchung ON thongtinbenhnhan.id = trieuchung.id 
LEFT JOIN lichsukhambenh ON trieuchung.matrieuchung = lichsukhambenh.matrieuchung
"""
df = pd.read_sql(query, conn)

# Display data on Streamlit app
st.write("")
st.write("## Thông tin khám bệnh:")
st.write("Dưới đây là bảng thông tin chi tiết về lịch sử khám bệnh của bệnh nhân.")
st.write("")
st.dataframe(df)

# Display age histogram
st.write("")
st.write("## Thống kê tuổi của bệnh nhân:")
st.write("Dưới đây là biểu đồ thống kê về tuổi của bệnh nhân.")
st.write("")
age_hist = pd.DataFrame(df["tuoi"].astype(int))
fig, ax = plt.subplots()
hist_values = age_hist.hist(bins=20, alpha=0.8, ax=ax)
st.pyplot(fig)

# Display gender count chart
st.write("")
st.write("## Thống kê giới tính của bệnh nhân:")
gender_counts = pd.DataFrame(df["gioitinh"].value_counts())
fig, ax = plt.subplots()
ax.bar(gender_counts.index, gender_counts["gioitinh"])
st.pyplot(fig)

# Display patient status count chart
st.write("")
st.write("## Thống kê tình trạng bệnh của bệnh nhân:")
status_counts = df["tilemacbenh"].value_counts(normalize=True)
fig, ax = plt.subplots()
ax.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%')
ax.axis('equal')
st.pyplot(fig)

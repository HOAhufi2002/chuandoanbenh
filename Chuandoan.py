import os
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import pyodbc
import random
import string
# Kết nối tới CSDL SQL Server
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=MINHHOA\SQLEXPRESS;'
                      'Database=ganmantinh;'
                      'Trusted_Connection=yes;')

st.title(" Hồ sơ bệnh nhân mới")
# Tạo đối tượng cursor để thao tác với CSDL
cursor = conn.cursor()
#Đọc dữ liệu từ file csv
df = pd.read_csv('D:/DoAnThML/kidney_disease.csv')

#Thay thế các giá trị "?" bằng giá trị null
df.replace("?", np.nan, inplace=True)

#Loại bỏ các dòng chứa giá trị null
df.dropna(inplace=True)

#Loại bỏ cột "id" không cần thiết
df.drop(['id'], axis=1, inplace=True)

#Chuyển đổi giá trị "normal" và "abnormal" sang 1 và 0 tương ứng
df['rbc'] = df['rbc'].map({'normal': 1, 'abnormal': 0})
df['pc'] = df['pc'].map({'normal': 1, 'abnormal': 0})
df['pcc'] = df['pcc'].map({'present': 1, 'notpresent': 0})
df['ba'] = df['ba'].map({'present': 1, 'notpresent': 0})
df['htn'] = df['htn'].map({'yes': 1, 'no': 0})
df['dm'] = df['dm'].map({'yes': 1, 'no': 0, '': 0})
df['cad'] = df['cad'].map({'yes': 1, 'no': 0})
df['appet'] = df['appet'].map({'good': 1, 'poor': 0})
df['pe'] = df['pe'].map({'yes': 1, 'no': 0})
df['ane'] = df['ane'].map({'yes': 1, 'no': 0})

#Tạo bộ dữ liệu đầu vào và đầu ra cho mô hình
X = df.drop(['classification'], axis=1).values
y = df['classification'].values

#Chuẩn hóa dữ liệu đầu vào
scaler = StandardScaler()
X = scaler.fit_transform(X)

#Khởi tạo mô hình Logistic Regression và huấn luyện trên dữ liệu
model = LogisticRegression()
model.fit(X, y)

def main():
    
    st.set_page_config(page_title="Kidney Disease Prediction", page_icon=":hospital:", layout="wide")
    st.title("Kidney Disease Prediction App")
# Add some explanation text
st.title("Đây là một ứng dụng web để dự đoán xem bệnh nhân có mắc bệnh thận hay không dựa trên một số thông số đầu vào.")
# Add input fields
trieu_chung = st.text_input(" Nhập mã khám bệnh")
id = st.text_input(" Vui lòng nhập lại ID bệnh nhân")
age = st.slider("Nhập tuổi của bệnh nhân", 1, 100, 25, 1)
bp = st.selectbox("Chọn huyết áp của bạn", ["normal", "above normal", "well above normal"])
sg = "abnormal"
al = st.selectbox("Chọn albumin của bạn",["normal", "abnormal"])
su = st.selectbox("Chọn đường huyết của bạn",["normal", "abnormal"])
rbc = st.selectbox("Chọn số lượng tế bào máu đỏ của bạn",["normal", "abnormal"])
pc = st.selectbox("Chọn số lượng tế bào ủ bằng của bạn", ["normal", "abnormal"])
pcc = st.selectbox("Chọn các cục máu trắng trong nước tiểu của bạn",["present", "notpresent"])
ba = st.selectbox("Chọn vi khuẩn trong nước tiểu của bạn",["present", "notpresent"])
bgr = st.slider("Chọn đường huyết ngẫu nhiên của bạn", 1, 500, 100, 1)
bu = st.slider("Chọn ure trong máu của bạn", 1, 200, 50, 1)
sc = st.slider("Chọn creatinin trong huyết tương của bạn", 1.0, 15.0, 1.2, 0.1)
sod = st.slider("Chọn nồng độ natri của bạn", 1, 200, 100, 1)
pot = st.slider("Chọn nồng độ kali của bạn", 1.0, 10.0, 4.0, 0.1)
hemo = st.slider("Chọn hồng cầu của bạn", 1.0, 200.0, 10.0, 0.1)
pcv = st.slider("Chọn thể tích hồng cầu được đóng gói của bạn", 1, 80, 40, 1)
wc = st.slider("Chọn số lượng tế bào bạch cầu của bạn", 1.0, 25000.0, 12000.0, 1000.0)
rc = st.slider("Chọn số lượng hồng cầu của bạn", 1.0, 10.0, 5.0, 0.1)
htn = st.selectbox("Bạn có bị tăng huyết áp không?",  ["yes", "no"])
dm = st.selectbox("Bạn có bị tiểu đường không?", ["yes", "no", "unknown"])
cad = st.selectbox("Bạn có bị bệnh động mạch vành không?",  ["yes", "no"])
appet = st.selectbox("Mức độ ngon miệng của bạn là gì?", ["good", "poor"])
pe = st.selectbox("Bạn có bị phù chân không?", ["yes", "no"])
ane = st.selectbox("Bạn có bị thiếu máu không?", ["yes", "no"])

input_data = {'age': age, 'blood_pressure': bp, 'specific_gravity': sg, 'albumin': al, 'sugar': su,
'red_blood_cells': rbc, 'pus_cell': pc, 'pus_cell_clumps': pcc, 'bacteria': ba, 'blood_glucose_random': bgr,
'blood_urea': bu, 'serum_creatinine': sc, 'sodium': sod, 'potassium': pot, 'hemoglobin': hemo,
'packed_cell_volume': pcv, 'white_blood_cell_count': wc, 'red_blood_cell_count': rc, 'hypertension': htn,
'diabetes_mellitus': dm, 'coronary_artery_disease': cad, 'appetite': appet, 'pedal_edema': pe, 'anemia': ane}

input_df = pd.DataFrame([input_data])

input_df['blood_pressure'] = input_df['blood_pressure'].map({'normal': 0, 'above normal': 1, 'well above normal': 2})
input_df['specific_gravity'] = input_df['specific_gravity'].map({'normal': 0, 'abnormal': 1})
input_df['albumin'] = input_df['albumin'].map({'normal': 0, 'abnormal': 1})
input_df['sugar'] = input_df['sugar'].map({'normal': 0, 'abnormal': 1})
input_df['red_blood_cells'] = input_df['red_blood_cells'].map({'normal': 1, 'abnormal': 0})
input_df['pus_cell'] = input_df['pus_cell'].map({'normal': 1, 'abnormal': 0})
input_df['pus_cell_clumps'] = input_df['pus_cell_clumps'].map({'present': 1, 'notpresent': 0})
input_df['bacteria'] = input_df['bacteria'].map({'present': 1, 'notpresent': 0})
input_df['hypertension'] = input_df['hypertension'].map({'yes': 1, 'no': 0})
input_df['diabetes_mellitus'] = input_df['diabetes_mellitus'].map({'yes': 1, 'no': 0, 'unknown': 0})
input_df['coronary_artery_disease'] = input_df['coronary_artery_disease'].map({'yes': 1, 'no': 0})
input_df['appetite'] = input_df['appetite'].map({'good': 1, 'poor': 0})
input_df['pedal_edema'] = input_df['pedal_edema'].map({'yes': 1, 'no': 0})
input_df['anemia'] = input_df['anemia'].map({'yes': 1, 'no': 0})


input_data = scaler.transform(input_df)
prediction = model.predict(input_data)
prediction_proba = model.predict_proba(input_data)

if st.button('Lưu dữ liệu triệu chứng xuống csdl'):
    try:
        # Thêm dữ liệu vào bảng thongtinbenhnhan
        cursor.execute("INSERT INTO trieuchung( matrieuchung,id,tuoi,huyetap,tytrongnuoctieu,albumin,mucdoduongtrongnuoctieu,hongcautrongnuoctieu,tebaomutrongnuoctieu,bongumutrongnuoctieu,vikhuantrongnuoctieu,luongduonghuyet,nongdo_ure,nongdo_creatinine,nongdonatri,nongdokali,nongdo_hemoglobin,thetichhongcau,soluongbachcau,soluonghongcau,tanghuyetap,tieuduong,benhdongmachvanh,ngonmieng,phu_chan)  VALUES (?, ?, ?, ?, ?, ?,?, ?, ?,?,?,?,?, ?, ?, ?,?, ?, ?, ?, ?,?, ?, ?, ?)", (trieu_chung,id,age, bp, sg, al, su, rbc,pc,pcc,ba,bgr,bu,sc,sod,pot,hemo,pcv,wc,rc,htn,dm,cad,appet,pe))
        conn.commit()
        st.success('Lưu thông tin bệnh nhân thành công!')
    except Exception as e:
        st.write('<span style="color:red">Lưu thông tin bệnh nhân thất bại!</span>', unsafe_allow_html=True)
if st.button('Trở về'):
    os.system("streamlit run D:/DoAnThML/thongtinbenhnhan.py")        
        
st.subheader("Xác suất dự đoán")
st.write("Xác suất dự đoán cho mỗi lớp là:")
st.write(f"- Bệnh nhân có thể mắc bệnh: {prediction_proba[0][0]*100:.2f}%")
st.write(f"- Bệnh nhân không thể mắc bệnh: {prediction_proba[0][1]*100:.2f}%") 


# tạo chuỗi ngẫu nhiên bao gồm các ký tự chữ cái và số, có độ dài là 5
random_string1 = ''.join(random.choices(string.ascii_lowercase + string.digits, k=2))
# thêm đoạn "tc" vào đầu chuỗi
malichsukham = "kq" + random_string1
if st.button('Lưu xuống kết quả chuẩn đoán '):
    try:
        # Thêm dữ liệu vào bảng thongtinbenhnhan
        cursor.execute("INSERT INTO lichsukhambenh(malichsukham,matrieuchung,tilemacbenh,tilekhongmacbenh) VALUES (?, ?,? ,?)", (malichsukham,trieu_chung, prediction_proba[0][0]*100, prediction_proba[0][1]*100))
        conn.commit()
        st.success('Lưu thông tin thành công!')
    except Exception as e:
        st.write('<span style="color:red">Lưu thông tin thất bại!</span>', unsafe_allow_html=True)


if st.button('Lịch sử khám bệnh'):
    os.system("streamlit run D:/DoAnThML/ketqua.py")
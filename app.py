import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# CẤU HÌNH TRANG & GIAO DIỆN (CSS TÙY CHỈNH)
# ==========================================
st.set_page_config(
    page_title="Data Analytics Hub | Đa Lĩnh Vực",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Tùy chỉnh thẻ KPI */
    div[data-testid="metric-container"] {
        background-color: #1E2530;
        border: 1px solid #2E3848;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    /* Tùy chỉnh hộp thông tin lý thuyết */
    .info-card {
        background-color: #F8F9FA;
        color: #1F2937;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4F46E5;
        margin-bottom: 20px;
    }
    @media (prefers-color-scheme: dark) {
        .info-card {
            background-color: #1E2530;
            color: #F3F4F6;
            border-left: 5px solid #6366F1;
        }
    }
    .info-title {
        font-weight: 700;
        font-size: 1.05rem;
        margin-bottom: 5px;
        color: #6366F1;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# HÀM TẠO DỮ LIỆU GIẢ LẬP (CACHED)
# ==========================================
@st.cache_data
def generate_data():
    np.random.seed(42)
    
    # 1. Dữ liệu E-commerce
    hours = [f"{h:02d}:00" for h in range(24)]
    ecom_hourly = pd.DataFrame({
        "Khung giờ": hours,
        "Lượt truy cập": np.random.randint(500, 5000, 24) * [0.4 if h < 7 else (1.8 if 19 <= h <= 22 else 1.0) for h in range(24)],
        "Giá trung bình (Dynamic Pricing)": [100 + (25 if 19 <= h <= 22 else (-10 if h < 7 else 5)) + np.random.randint(-3, 4) for h in range(24)],
        "Tỷ lệ chuyển đổi (%)": np.round(np.random.uniform(1.8, 4.5, 24), 2)
    })
    
    # 2. Dữ liệu FinTech
    n_tx = 300
    fintech_tx = pd.DataFrame({
        "Thời gian xử lý (ms)": np.random.exponential(scale=15, size=n_tx) + 5,
        "Giá trị giao dịch (Triệu VNĐ)": np.concatenate([np.random.lognormal(1.5, 0.8, 280), np.random.uniform(50, 150, 20)]),
        "Khoảng cách địa lý bất thường (km)": np.concatenate([np.random.uniform(0, 30, 280), np.random.uniform(500, 3000, 20)]),
        "Trạng thái": ["Hợp lệ"] * 280 + ["Cảnh báo Gian lận"] * 20
    })
    
    # 3. Dữ liệu Sports Analytics
    players = ["Nguyễn Quang Hải", "Nguyễn Hoàng Đức", "Phạm Tuấn Hải", "Đỗ Hùng Dũng", "Bùi Hoàng Việt Anh", "Vũ Văn Thanh", "Nguyễn Tiến Linh", "Phan Văn Đức"]
    sports_df = pd.DataFrame({
        "Cầu thủ": players,
        "xG (Bàn thắng kỳ vọng)": [0.45, 0.32, 0.68, 0.18, 0.12, 0.25, 0.74, 0.41],
        "xA (Kiến tạo kỳ vọng)": [0.58, 0.62, 0.24, 0.49, 0.08, 0.38, 0.19, 0.31],
        "Quãng đường (km)": [11.2, 11.8, 10.9, 12.4, 9.8, 11.5, 9.6, 10.7],
        "Nguy cơ chấn thương (%)": [42, 35, 78, 84, 25, 61, 48, 52],
        "Chuyền tịnh tiến (%)": [82, 88, 71, 85, 79, 76, 68, 74]
    })
    
    return ecom_hourly, fintech_tx, sports_df

ecom_df, fintech_df, sports_df = generate_data()

# ==========================================
# THANH ĐIỀU HƯỚNG BÊN TRÁI (SIDEBAR)
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2920/2920349.png", width=65)
    st.title("Data Analytics Hub")
    st.caption("Hệ thống phân tích dữ liệu đa ngành theo thời gian thực")
    st.divider()
    
    selected_domain = st.radio(
        "Chọn lĩnh vực phân tích:",
        [
            "🛒 Thương mại điện tử & Bán lẻ",
            "💳 Công nghệ Tài chính & Ngân hàng",
            "⚽ Thể thao & Giải trí (Sports)"
        ]
    )
    st.divider()
    st.info("💡 **Mẹo:** Tương tác trực tiếp với các biểu đồ và bộ lọc bên phải để mô phỏng kịch bản thực tế.")

# ==========================================
# HÀM HIỂN THỊ KHUNG THÔNG TIN LĨNH VỰC
# ==========================================
def render_domain_overview(goal, inputs, kpis, application):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="info-card">
            <div class="info-title">🎯 Mục tiêu phân tích</div>
            <div>{goal}</div><br>
            <div class="info-title">📥 Dữ liệu đầu vào</div>
            <div>{inputs}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="info-card">
            <div class="info-title">📊 Chỉ số trọng tâm (KPIs)</div>
            <div>{kpis}</div><br>
            <div class="info-title">🚀 Ứng dụng thực tế</div>
            <div>{application}</div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# NỘI DUNG TỪNG LĨNH VỰC
# ==========================================

# --- 1. E-COMMERCE & RETAIL ---
if selected_domain == "🛒 Thương mại điện tử & Bán lẻ":
    st.title("🛒 Thương mại điện tử & Bán lẻ (E-commerce & Retail)")
    st.markdown("*Sở hữu lượng dữ liệu hành vi người dùng khổng lồ theo thời gian thực.*")
    
    render_domain_overview(
        goal="Cá nhân hóa trải nghiệm mua sắm, dự báo nhu cầu tồn kho và tối ưu hóa chiến dịch tiếp thị.",
        inputs="Lịch sử click chuột, giỏ hàng bị bỏ quên, lịch sử giao dịch, đánh giá sản phẩm, dữ liệu nhân khẩu học.",
        kpis="Tỷ lệ chuyển đổi (Conversion Rate), Giá trị vòng đời khách hàng (CLV), Tỷ lệ rời bỏ (Churn Rate), Giá trị đơn hàng trung bình (AOV).",
        application="Hệ thống gợi ý sản phẩm (\"Người mua món này cũng mua...\"), định giá động (Dynamic Pricing) theo khung giờ cao điểm."
    )
    
    # Chỉ số KPI
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Tỷ lệ chuyển đổi (CR)", "3.42%", "+0.45%")
    k2.metric("Giá trị vòng đời (CLV)", "4.85M ₫", "+12.3%")
    k3.metric("Tỷ lệ rời bỏ (Churn)", "14.2%", "-1.8%", delta_color="inverse")
    k4.metric("Đơn hàng trung bình (AOV)", "620K ₫", "+35K ₫")
    
    st.subheader("📈 Mô phỏng Định giá động (Dynamic Pricing) & Lưu lượng truy cập")
    fig_ecom = go.Figure()
    fig_ecom.add_trace(go.Bar(
        x=ecom_df["Khung giờ"], y=ecom_df["Lượt truy cập"],
        name="Lượt truy cập", marker_color="#6366F1", opacity=0.7
    ))
    fig_ecom.add_trace(go.Scatter(
        x=ecom_df["Khung giờ"], y=ecom_df["Giá trung bình (Dynamic Pricing)"],
        name="Chỉ số giá động (%)", yaxis="y2", line=dict(color="#F59E0B", width=3)
    ))
    fig_ecom.update_layout(
        yaxis=dict(title="Lượt truy cập"),
        yaxis2=dict(title="Mức điều chỉnh giá (%)", overlaying="y", side="right"),
        legend=dict(orientation="h", y=1.12),
        height=400, margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig_ecom, use_container_width=True)
    
    # Bộ mô phỏng gợi ý sản phẩm
    st.subheader("🛍️ Demo Hệ thống Gợi ý Sản phẩm (Recommendation Engine)")
    selected_item = st.selectbox("Chọn sản phẩm khách hàng đang xem:", ["Laptop Ultrabook X1", "Tai nghe Chống ồn Pro", "Bàn phím Cơ Không dây"])
    recommendations = {
        "Laptop Ultrabook X1": ["Chuột không dây Ergonomic (Tỷ lệ mua kèm: 68%)", "Túi chống sốc cao cấp (Tỷ lệ mua kèm: 54%)", "Hub chuyển đổi Type-C (Tỷ lệ mua kèm: 49%)"],
        "Tai nghe Chống ồn Pro": ["Hộp đựng bảo vệ cứng (Tỷ lệ mua kèm: 45%)", "Cáp sạc nhanh 65W (Tỷ lệ mua kèm: 32%)", "Giá treo tai nghe hợp kim (Tỷ lệ mua kèm: 28%)"],
        "Bàn phím Cơ Không dây": ["Kê tay gỗ Óc chó (Tỷ lệ mua kèm: 61%)", "Bộ Keycap PBT (Tỷ lệ mua kèm: 39%)", "Lót chuột cỡ lớn (Tỷ lệ mua kèm: 52%)"]
    }
    cols = st.columns(3)
    for idx, rec in enumerate(recommendations[selected_item]):
        cols[idx].success(f"**Gợi ý #{idx+1}:** {rec}")

# --- 2. FINTECH & BANKING ---
elif selected_domain == "💳 Công nghệ Tài chính & Ngân hàng":
    st.title("💳 Công nghệ Tài chính & Ngân hàng (FinTech & Banking)")
    st.markdown("*Dữ liệu đòi hỏi độ chính xác tuyệt đối, tính bảo mật cao và tốc độ xử lý cực nhanh.*")
    
    render_domain_overview(
        goal="Phát hiện gian lận, chấm điểm tín dụng và quản trị rủi ro đầu tư.",
        inputs="Lịch sử giao dịch thẻ, biến động thị trường chứng khoán, hồ sơ vay vốn, hành vi đăng nhập thiết bị.",
        kpis="Tỷ lệ nợ xấu (NPL), Biên lãi ròng (NIM), Độ chính xác mô hình cảnh báo gian lận (Precision/Recall).",
        application="Tự động khóa thẻ trong vài mili-giây khi phát hiện giao dịch ở vị trí lạ; duyệt vay tự động qua dữ liệu thay thế."
    )
    
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Tỷ lệ nợ xấu (NPL)", "1.48%", "-0.22%", delta_color="inverse")
    k2.metric("Biên lãi ròng (NIM)", "4.15%", "+0.18%")
    k3.metric("Độ chính xác (Precision)", "99.4%", "+0.3%")
    k4.metric("Tốc độ khóa thẻ TB", "18 ms", "-4 ms", delta_color="inverse")
    
    st.subheader("🛡️ Giám sát Giao dịch & Phát hiện Gian lận Thời gian thực")
    fig_fin = px.scatter(
        fintech_df,
        x="Khoảng cách địa lý bất thường (km)",
        y="Giá trị giao dịch (Triệu VNĐ)",
        color="Trạng thái",
        size="Thời gian xử lý (ms)",
        color_discrete_map={"Hợp lệ": "#10B981", "Cảnh báo Gian lận": "#EF4444"},
        hover_data=["Thời gian xử lý (ms)"],
        height=420
    )
    fig_fin.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_fin, use_container_width=True)
    
    # Bộ mô phỏng chấm điểm tín dụng
    st.subheader("⚡ Mô phỏng Duyệt Khoản Vay Tự Động (Alternative Data)")
    c1, c2, c3 = st.columns(3)
    telco_score = c1.slider("Lịch sử thanh toán cước viễn thông đúng hạn (%)", 50, 100, 95)
    ewallet_tx = c2.number_input("Số giao dịch ví điện tử/tháng", 0, 200, 45)
    requested_loan = c3.number_input("Khoản vay đề xuất (Triệu VNĐ)", 5, 100, 25)
    
    credit_score = int((telco_score * 5.5) + min(ewallet_tx * 1.5, 200) - (requested_loan * 0.8))
    if credit_score >= 620:
        st.success(f"✅ **PHÊ DUYỆT TỰ ĐỘNG** | Điểm tín dụng thay thế: **{credit_score}/850** (Giải ngân trong 30 giây)")
    else:
        st.warning(f"⚠️ **CẦN THẨM ĐỊNH THỦ CÔNG** | Điểm tín dụng thay thế: **{credit_score}/850** (Yêu cầu bổ sung hồ sơ)")

# --- 3. SPORTS ANALYTICS ---
elif selected_domain == "⚽ Thể thao & Giải trí (Sports)":
    st.title("⚽ Thể thao & Giải trí (Sports Analytics)")
    st.markdown("*Thay đổi hoàn toàn cách các đội bóng chuyên nghiệp tuyển trạch cầu thủ và xây dựng chiến thuật.*")
    
    render_domain_overview(
        goal="Đánh giá hiệu suất vận động viên, phòng ngừa chấn thương và tối ưu hóa sơ đồ chiến thuật.",
        inputs="Dữ liệu cảm biến GPS gắn trên áo đấu, camera theo dõi quỹ đạo bóng (Optical Tracking), nhịp tim, quãng đường di chuyển.",
        kpis="Bàn thắng kỳ vọng (xG), Kiến tạo kỳ vọng (xA), Bản đồ nhiệt di chuyển (Heatmap), Tỷ lệ chuyền bóng tịnh tiến.",
        application="Cảnh báo nguy cơ căng cơ để thay người kịp thời; tuyển trạch cầu thủ bị định giá thấp dựa trên đóng góp thực tế."
    )
    
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Tổng xG toàn đội", "2.45", "+0.65")
    k2.metric("Tổng xA toàn đội", "1.92", "+0.40")
    k3.metric("Chuyền tịnh tiến TB", "77.9%", "+3.2%")
    k4.metric("Cảnh báo chấn thương", "2 Cầu thủ", "Cần thay người", delta_color="off")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("🎯 Đóng góp Tấn công (xG vs xA)")
        fig_sport1 = px.scatter(
            sports_df,
            x="xG (Bàn thắng kỳ vọng)",
            y="xA (Kiến tạo kỳ vọng)",
            text="Cầu thủ",
            size="Chuyền tịnh tiến (%)",
            color="Chuyền tịnh tiến (%)",
            color_continuous_scale="Viridis",
            height=400
        )
        fig_sport1.update_traces(textposition="top center")
        st.plotly_chart(fig_sport1, use_container_width=True)
        
    with col_chart2:
        st.subheader("🔥 Bản đồ nhiệt Di chuyển (Optical Tracking)")
        # Tạo dữ liệu ma trận sân bóng (10x6)
        pitch_z = np.random.poisson(lam=4, size=(6, 10))
        pitch_z[2:4, 6:9] += 9  # Khu vực hoạt động mạnh ở hành lang trong cánh phải
        fig_heat = px.imshow(
            pitch_z,
            labels=dict(x="Chiều dài sân (Phòng ngự -> Tấn công)", y="Chiều rộng sân", color="Mật độ"),
            color_continuous_scale="YlOrRd",
            height=400
        )
        st.plotly_chart(fig_heat, use_container_width=True)
        
    st.subheader("🩺 Giám sát Thể lực & Cảnh báo Nguy cơ Chấn thương (GPS Vest)")
    st.dataframe(
        sports_df.style.background_gradient(subset=["Nguy cơ chấn thương (%)"], cmap="Reds"),
        use_container_width=True
    )


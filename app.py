import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="阿伦尼乌斯公式工具",
    page_icon="🌸",
    layout="wide",
)

# 粉嫩主题 CSS
st.markdown("""
<style>
    .stApp { background-color: #FFF5F7; }
    h1 { color: #FF85A2; font-weight: bold; }
    h2, h3 { color: #FF9BB3; }
    .stSlider > div > div > div { background-color: #FF9BB3 !important; }
    .stButton > button { background-color: #FF85A2; color: white; border-radius: 10px; }
    .stButton > button:hover { background-color: #FF668E; }
    .stMarkdown { color: #6D5D6B; }
</style>
""", unsafe_allow_html=True)

st.title("🌸 阿伦尼乌斯公式交互工具")
st.markdown(r"""
**公式：** $\displaystyle k = A \cdot e^{-\frac{E_a}{RT}}$  
取对数：$\ln k = -\dfrac{E_a}{R} \cdot \dfrac{1}{T} + \ln A$  
**斜率 = $-\dfrac{E_a}{R}$**
""")

st.subheader("参数设置")
col1, col2 = st.columns(2)

with col1:
    A = st.number_input("指前因子 A (s⁻¹)", value=1e10, format="%e")
    Ea = st.slider("活化能 Ea (kJ/mol)", 10, 200, 50, 5)

with col2:
    T = st.slider("温度 T (K)", 273, 1000, 298, 10)
    compare = st.checkbox("对比不同活化能")

R = 8.314
Ea_J = Ea * 1000
k = A * np.exp(-Ea_J / (R * T))
slope = -Ea_J / R  # 阿伦尼乌斯斜率

st.subheader("计算结果")
c1, c2 = st.columns(2)
with c1:
    st.metric("速率常数 k", f"{k:.4e}")
with c2:
    st.metric("直线斜率", f"{slope:.2f}")

st.subheader("阿伦尼乌斯图")
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor('#FFF5F7')
ax.set_facecolor('#FFFFFF')

T_range = np.linspace(273, 1000, 100)
x = 1 / T_range

if compare:
    Ea_list = [30, 50, 80, 100]
    colors = ['#FF85A2', '#FF9BB3', '#FFC0DD', '#FFD6E5']
    for i, ea in enumerate(Ea_list):
        ea_j = ea * 1000
        k_vals = A * np.exp(-ea_j / (R * T_range))
        y = np.log(k_vals)
        ax.plot(x, y, lw=2.5, color=colors[i], label=f'Ea={ea} kJ/mol')
    ax.legend()
else:
    k_vals = A * np.exp(-Ea_J / (R * T_range))
    y = np.log(k_vals)
    ax.plot(x, y, color='#FF85A2', lw=3, label=f'斜率 = {slope:.2f}')
    ax.scatter(1/T, np.log(k), color='#FF668E', s=80, zorder=5)
    ax.legend()

ax.set_xlabel('1/T (K⁻¹)', color='#6D5D6B')
ax.set_ylabel('ln(k)', color='#6D5D6B')
ax.grid(alpha=0.2, color='#FFC0DD')
st.pyplot(fig)

st.info(r"""
💡 说明：
- 阿伦尼乌斯直线斜率 = $\boldsymbol{-\dfrac{E_a}{R}}$
- 活化能 Ea 越大，斜率绝对值越大
- 由斜率可反算活化能：$E_a = -R \times $ 斜率
""")

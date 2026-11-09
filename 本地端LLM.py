from streamlit import chat_input, chat_message, columns, components, empty, error, rerun, selectbox, session_state, set_page_config, slider, subheader, success, title, write
from json import loads
import streamlit as st
import math
import json
import openai

# --- 1. 系統初始化與硬體/大腦設定 ---
# 初始化本地端的 OpenAI 相容客戶端 (vLLM / Ollama 佈署的 Qwen/DeepSeek)
if "llm_client" not in st.session_state:
    st.session_state.llm_client = openai.OpenAI(
        base_url="http://localhost:8000/v1",  # 依您本地佈署的 port 調整
        api_key="local-token"
    )

# 初始化 Streamlit 全局狀態機（用於儲存大腦與物理引擎共享的變數）
if "W" not in st.session_state: st.session_state.W = 10.0
if "H" not in st.session_state: st.session_state.H = 20.0
if "material" not in st.session_state: st.session_state.material = "Rogers RO4003C"
if "freq" not in st.session_state: st.session_state.freq = 8.0
if "chat_history" not in st.session_state: st.session_state.chat_history = []

# 材料庫常數
MATERIAL_MAP = {"Rogers RO4003C": 3.38, "PTFE": 2.10, "High-Res Silicon": 11.70}

# --- 2. 物理引擎模組 (4-12 GHz 微波計算) ---
def calc_impedance_and_loss(W, H, Er, freq):
    """ 快速解析阻抗與微波介質損耗 """
    T = 1.4  # 固定 1oz 銅厚
    try:
        ln_term = math.log(5.98 * H / (0.8 * W + T))
        Z0 = (87 / math.sqrt(Er + 1.41)) * ln_term
        loss_factor = 0.0027 if Er < 4 else 0.0001
        alpha_d = 0.0912 * freq * math.sqrt(Er) * loss_factor
        return round(Z0, 2), round(alpha_d, 4)
    except Exception:
        return 50.0, 0.0  # 避免極端極限值導致計算崩潰

# --- 3. 大腦工具定義 (LLM Function Calling Schema) ---
# 定義大腦可以調用的工具：當大腦想修改物理參數時，會呼叫此函式
tools = [
    {
        "type": "function",
        "function": {
            "name": "update_transmission_line_parameters",
            "description": "當使用者想要設定、修改、優化傳輸線的線寬(W)、介質厚度(H)、工作頻率或材料時呼叫此工具。",
            "parameters": {
                "type": "object",
                "properties": {
                    "W": {"type": "number", "description": "線寬 (mils)，範圍 2.0 至 30.0"},
                    "H": {"type": "number", "description": "介質厚度 (mils)，範圍 5.0 至 50.0"},
                    "material": {"type": "string", "enum": ["Rogers RO4003C", "PTFE", "High-Res Silicon"], "description": "基材名稱"},
                    "freq": {"type": "number", "description": "量子讀取微波工作頻率 (GHz)，範圍 4.0 至 12.0"}
                }
            }
        }
    }
]

def execute_brain_tool(function_args):
    """ 將大腦輸出的工具決策，直接寫入 Streamlit 狀態機，實現滑桿與圖表同步變更 """
    if "W" in function_args: st.session_state.W = float(function_args["W"])
    if "H" in function_args: st.session_state.H = float(function_args["H"])
    if "material" in function_args: st.session_state.material = function_args["material"]
    if "freq" in function_args: st.session_state.freq = float(function_args["freq"])

# --- 4. Streamlit UI 介面配置 ---
st.set_page_config(layout="wide")
st.title("🧠 Qwen/DeepSeek 大腦核心 - 量子微波傳輸線智能平台")

# 切分左右兩大區塊：左邊是物理硬體操控板，右邊是大腦對話視窗
col_phys, col_brain = st.columns([3, 2])

with col_phys:
    st.subheader("⚡ 物理硬體與實時畫布")
    
    # 這裡的 Slider 與 session_state 綁定，當大腦改了狀態，Slider 會自動跟著滑動！
    W = st.slider("線寬 W (mils)", 2.0, 30.0, key="W", step=0.1)
    H = st.slider("介質厚度 H (mils)", 5.0, 50.0, key="H", step=0.5)
    material = st.selectbox("選擇微波基材", ["Rogers RO4003C", "PTFE", "High-Res Silicon"], key="material")
    freq = st.slider("工作頻率 (GHz)", 4.0, 12.0, key="freq", step=0.5)
    
    # 執行計算
    Er = MATERIAL_MAP[material]
    Z0, alpha_d = calc_impedance_and_loss(W, H, Er, freq)
    
    # 動態 SVG 渲染 (不卡頓設計)
    svg_w, svg_h = W * 10, H * 4
    svg_code = f"""
    <svg width="100%" height="160" viewBox="0 0 600 160" xmlns="http://w3.org">
        <rect width="600" height="160" fill="#151515" />
        <rect x="50" y="80" width="500" height="{max(20, svg_h)}" fill="#1E4620" opacity="0.9" rx="3"/>
        <text x="60" y="{80 + max(15, svg_h/2)}" fill="#A0E0A0" font-family="sans-serif" font-size="11">{material} (Dk={Er})</text>
        <rect x="{300 - svg_w/2}" y="72" width="{max(15, svg_w)}" height="8" fill="#F4B41A" rx="1"/>
        <rect x="50" y="{80 + max(20, svg_h)}" width="500" height="6" fill="#888888" />
    </svg>
    """
    st.components.v1.html(svg_code, height=180)
    
    # 指標看板
    c1, c2 = st.columns(2)
    c1.metric(label="🎯 特性阻抗", value=f"{Z0} Ω")
    c2.metric(label="📉 介質損耗 (4-12 GHz)", value=f"{alpha_d} dB/cm")
    
    if abs(Z0 - 50.0) > 5.0:
        st.error(f"❌ 阻抗失配！偏離 50Ω 達 {round(abs(Z0-50),1)}Ω (會造成微波訊號反射)")
    else:
        st.success("✅ 阻抗匹配完美 (50Ω 附近)")

with col_brain:
    st.subheader("🧠 大腦認知與多輪引導")
    
    # 渲染對話歷史
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    # 使用者輸入自然語言指令
    if user_input := st.chat_input("對本地大腦說：例如『幫我把材料換成高阻矽，並把阻抗調到接近50歐姆』"):
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
            
        # 呼叫本地大腦 (Qwen / DeepSeek)
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            response_placeholder.write("🧠 大腦思考中...")
            
            try:
                # 建立 LLM 提示詞：告知當前硬體狀態，供大腦做決策評估
                system_prompt = f"""你是一個精通量子位元微波傳輸線的資深硬體工程師 AI。
目前平台的物理硬體狀態如下：線寬W={W}mils, 厚度H={H}mils, 材料={material}(Dk={Er}), 頻率={freq}GHz。當前算出的阻抗為 {Z0} 歐姆。
如果使用者的參數不足（例如只說要50歐姆，沒說要換什麼材料或寬度），請你進行多輪對話引導補全，或者主動調用工具進行參數調整。"""

                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ]
                
                # 發送給本地 LLM
                response = st.session_state.llm_client.chat.completions.create(
                    model="qwen2.5-7b-instruct",  # 依您本地佈署的模型標籤為準
                    messages=messages,
                    tools=tools,
                    tool_choice="auto"
                )
                
                response_message = response.choices[0].message
                
                # 檢查大腦是否決定調用函式變更硬體
                if response_message.tool_calls:
                    for tool_call in response_message.tool_calls:
                        args = json.loads(tool_call.function.arguments)
                        execute_brain_tool(args)
                    
                    # 工具執行後，重新刷新頁面讓物理引擎跟上大腦的思維
                    st.rerun()
                else:
                    # 如果大腦只是想講話（多輪引導問話）
                    reply = response_message.content
                    response_placeholder.write(reply)
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})
                    
            except Exception as e:
                response_placeholder.error(f"大腦連線失敗，請檢查本地 vLLM/Ollama 是否啟動。錯誤資訊: {str(e)}")

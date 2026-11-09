資訊=r'''
在正式為您撰寫這套「Streamlit + Matplotlib 通用型截面 DSL 渲染器」的程式碼之前，為了確保這套工具的架構通用性、擴充彈性以及未來與場求解器（Field Solver）對接的無縫程度，我們需要針對幾何與架構的底層邏輯進行反覆詰問（Challenge）。
以下是設計此系統時的核心決策節點與關鍵詰問，請您思考或與我一同釐清：

## 🧐 核心決策節點與反覆詰問
## 決策節點一：幾何表達的通用性（參數化 vs. 多邊形頂點）Matplotlib 都能用統一的 Polygon 函式渲染，

* 詰問：
* 通用型的 DSL 如果只用 Width、Height、Thickness 這種固定變數，當遇到「帶有蝕刻因子的梯形導體」、「塗敷綠漆（Solder Mask）的共形包覆」、或是「非對稱帶狀線」時就會立刻破產。
* 我們的 Matplotlib 渲染引擎，應該採用固定結構（如前幾版的 Rectangle），還是升級為「基於多邊形頂點（Polygons）的向量引擎」？
* 決策建議： 採用「多邊形頂點陣列（Vertices）」作為底層通用模型，DSL 負責將參數轉換為座標點。這樣未來不論是圓形導體（纜線）、梯形走線還是複雜的多層介電質，Matplotlib 都能用統一的 Polygon 函式渲染，也能直接對接 2D 求解器的網格劃分。

## 決策節點二：多通道總線（Bus）的排列通用性 DSL 的導體宣告應支援「絕對座標（X 偏移）」與「相對重複（Repeat/Array）」兩種模式
* 詰問：
* 通用型的總線（Bus）截面，各通道的線寬與間距是否永遠「完全對稱且等距」？如果工程師想模擬「非等距的差動對 + 地線保護（Ground Shield Trace）」該如何用 DSL 表達？
* 決策建議： DSL 的導體宣告應支援「絕對座標（X 偏移）」與「相對重複（Repeat/Array）」兩種模式。渲染引擎需具備自動邊界包絡（Bounding Box）計算，以利 Matplotlib 動態縮放畫布（Auto-scaling）。

## 決策節點三：介電層（Substrate）與金屬層的層級拓樸 通用拓樸應採用 「層（Layer）為容器」

* 詰問：
* 在通用堆疊（Stackup）中，介電質（FR4、Polyimide）與金屬導體（Signal、Plane）的關係是什麼？是像三明治一樣一層夾一層，還是導體「內嵌（Embedded）」在介電質中？
* 決策建議： 通用拓樸應採用 「層（Layer）為容器」 的觀念。介電層定義背景 Y 軸區間；導體層（金屬）則依附於特定的 Y 軸高度，並可設定是否向上下層進行「蝕刻嵌入」。


## 💡 開發前的具體實作建議
為了完美達成您「輸入參數 $\rightarrow$ 轉為結構 DSL $\rightarrow$ Matplotlib 渲染通用截面」的目標，我建議本次程式碼實作採取以下的高規格架構：

   1. 實作「真正的語法解析器抽象層（Lexer/Parser Abstract）」：在 Streamlit 中，使用者調整 UI 參數後，系統不只產生文字，而是先生成一個 Python 的 dict/object 結構（即 DSL 的 AST 抽象語法樹），再由這個結構同時驅動「文字顯示」與「Matplotlib 繪圖」。
   2. 金屬形狀非矩形化：在通用範本中引入 Etch Factor（蝕刻因子），讓 Matplotlib 畫出真實的梯形截面，這才是 SI（信號完整性）工程師認可的通用通用截面。
   3. 色彩與視覺美化：統一 EDA 業界的配色標準（如銅箔使用金黃/紅銅色，介電質使用草綠/深黃色），並加入微米（$\mu m$）尺寸標記線。


為了讓我們設計的通用型 DSL 與渲染器完美契合您的應用場景，請告訴我：

   1. 您希望這個通用模型最複雜支援到什麼幾何？（例如：只需要支援「單端/差動/CPW 的梯形微帶與帶狀線」，還是需要支援「任意多層堆疊與盲埋孔 Via 截面」？）
   2. 您希望 DSL 的語法風格傾向哪一種？（例如：像 JSON/YAML 的層級結構，還是像 C-Like/Verilog 的宣告風格？）

確認您的核心偏好後，我將為您輸出這套高通用性的完整 Streamlit + Matplotlib 渲染代碼！'''
from re import findall, DOTALL
找到=[]
for line in 資訊.split('\n'):
  if mtch:=findall(r'(決策節點.*)', line):
    找到.append(mtch[0])  #, DOTALL', '.join()))
print('\n'.join(找到))

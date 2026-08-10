# 加一組新主題

從一張色票到一組可用主題的完整流程。每一步都有實測依據，不要憑眼睛跳過。

底層原理在 `layer-color.md`，這裡只講怎麼操作。

---

## 1. 判斷色票的型別

| 型別 | 特徵 | 處理 |
|---|---|---|
| **類別色票** | 色相分散、明度也分散 | 通常可直接用 |
| **連續漸層** | 色相依序過渡，相鄰色明度差 5–10 | **必須跳著取** |
| **UI 色系** | 同一階跨色相時明度刻意齊平 | **必須換階取** |

後兩者是多數現成色票的樣子。Bootstrap、Tailwind、Solarized 都屬第三類，
它們為螢幕調色，那裡只要求換色時視覺重量不變——與類別編碼的需求相反。

## 2. 量明度，不要看

```bash
python - <<'PY'
import sys; sys.path.insert(0,'scripts')
from derive import hex2rgb, luminance
for h in ['#54478C','#2C699A','#048BA8']:   # 換成你的色票
    print(h, f'{luminance(hex2rgb(h))*100:.1f}%')
PY
```

**相鄰兩個類別的相對亮度必須差 ≥10**（列印主題 15）。
這是全部規則裡最常擋人的一條，也是唯一在黑白影印後還活著的通道。

## 3. 挑類別色

**先用明度篩，再用色相刪。** 明度貪婪法會挑出一批合格的候選，
但其中可能有幾個擠在同一個色相家族裡——灰階閘門看不見那件事。

貪婪法：明度排序後從最暗的開始，每次取下一個間距 ≥10 的。

```bash
python - <<'PY'
import sys; sys.path.insert(0,'scripts')
from derive import hex2rgb, luminance
L=lambda h: luminance(hex2rgb(h))*100
P=['#54478C','#2C699A','#048BA8','#0DB39E','#16DB93','#83E377','#B9E769']
xs=sorted((L(h),h) for h in P); out=[xs[0]]
for l,h in xs[1:]:
    if l-out[-1][0]>=10: out.append((l,h))
print([h for _,h in out], [round(l) for l,_ in out])
PY
```

再檢查**色相**：兩兩至少差 30°，否則彩色閱讀時仍會混。
明度間距解決黑白，色相間距解決彩色，**兩者都要顧**。

也檢查**飽和度**。低於 20% 的色在小面積卡片上讀起來是灰或褐，不是顏色——
連續漸層的中段常有這種近灰過渡色。閘門不會擋（灰階與對比都合格），但圖會看起來髒。

### 保灰階提飽和

要提飽和又不動間距，**重新解明度把相對亮度釘回原位**。
直接調飽和會連帶改明度、打破間距。

```python
import sys, colorsys; sys.path.insert(0, 'scripts')
from derive import hex2rgb, rgb2hex, luminance
L = lambda h: luminance(hex2rgb(h)) * 100
un = lambda h, l, s: rgb2hex([c * 255 for c in colorsys.hls_to_rgb(h, l, s)])

def resat(hx, mult):
    H, _, S = colorsys.rgb_to_hls(*[c / 255 for c in hex2rgb(hx)])
    S2, target = min(S * mult, 1.0), L(hx)
    lo, hi = 0.0, 1.0
    for _ in range(60):
        m = (lo + hi) / 2
        if L(un(H, m, S2)) < target:
            lo = m
        else:
            hi = m
    return un(H, (lo + hi) / 2, S2)

print([resat(c, 2.2) for c in ['#4D455C', '#7B947E']])
```

挑剩下的色裡，選一個色相離所有類別都遠的當 `accent`。
最搶眼的那個色通常適合當 accent 而不是類別——放進類別會讓那一階永遠壓過其他階。

## 4. 決定模式

主題檔必須有一行 `mode:`，**不能省略**——省略了讀者無從知道它走哪條階梯。

| `mode:` | 何時用 |
|---|---|
| `standard` | 一般情況 |
| `vivid` | 色票飽和，預設階梯會洗掉特色 |
| `print` | 會被印出或影印 |
| `outline` | 純框線線稿 |
| `print vivid` | 兩者都要，走 vivid 階梯＋print 的其餘規則 |

`outline` 不與其他並用：它讓表面完全不填色，濃度設定沒有作用對象。

## 5. 補齊單值

- `canvas` — 近白或紙白。`print` 模式必須 `#FFFFFF`。
- `ink-strong` — 對每個 `card` 階都要 ≥4.5:1。用色票最暗的色通常剛好。
- `ink-muted`、`infra` — 中性，不搶類別色。
- `terminal` — 深色實心，且**不要與 cat-1 同值**。
- `accent` — 見步驟 3；投影片的 `--slide-emphasis` 會由它針對所選 canvas 解出可讀文字色。
- `highlight` — 見下。

### highlight 的解法

三個決定：**色相 H52**（單色主題用自身主色相）、
**飽和度**取類別色平均的 0.95 倍但**下限 0.70**、上限 0.85、
**明度**解到對畫布 1.33:1。

下限 0.70 是關鍵。跟著低飽和主題一起降下去會得到米褐色——
暖色相加低飽和就是泛黃的紙，那不是畫記。

```bash
python - <<'PY'
import sys, colorsys; sys.path.insert(0,'scripts')
from derive import hex2rgb, rgb2hex, contrast
un=lambda h,l,s: rgb2hex([c*255 for c in colorsys.hls_to_rgb(h/360,l,s)])
CV=hex2rgb('#FFFFFF')          # 換成你的 canvas
HUE=52                          # 黃；單色主題用自身主色相
SAT=0.75                        # max(0.70, 類別平均 × 0.95)，上限 0.85
lo,hi=0.25,0.95
for _ in range(60):
    m=(lo+hi)/2
    if contrast(hex2rgb(un(HUE,m,SAT)),CV)>=1.33: lo=m
    else: hi=m
print(un(HUE,lo,SAT))
PY
```

黃色是螢光筆的慣例，慣例本身就是一個通道，值得保留。
若它與某個暖色類別的色相很近，`derive.py` 會提醒——那只影響
`surface/emphasis`（卡片後方的偏移塊），底線式畫記不受影響，兩者幾何不同。

## 6. 跑閘門

```bash
python scripts/derive.py themes/<新主題>.md
```

**exit 0 才算完成。** 擋下來時修因不修果：

| 訊息 | 該做的事 |
|---|---|
| 灰階間距不足 | 換色階或重排明度，**不要**加徽章硬過 |
| 文字對比不足 | 加深 `ink-strong`，不要調淡卡片底 |
| 螢光筆對紙太淡 | 壓暗一點，但別超過 1.4——過濃會蓋過文字 |
| 純框線超過 3 類 | 分組，或改用填色 |

## 7. 收尾

```bash
python scripts/test_themes.py --update     # 檢查 diff 後再重建基準
python scripts/render_reference.py         # 更新 docs/style-reference.html
```

最後**開參考頁按一次灰階檢視**。所有規則的目的都是那一眼——
新主題的類別在黑白下若還分得開，這組主題就成立了。

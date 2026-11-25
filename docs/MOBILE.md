# 手机适配说明

## 目标

手机上的问题不是“把桌面版缩小”，而是四类真实场景：

1. **竖屏但很窄**：360–430 CSS px，等宽英文和大字号容易横向溢出。
2. **软键盘顶起视口**：输入访问密码时可视高度只剩 ~500px。
3. **横屏**：可视高度只有 ~390px。
4. **触屏**：没有 Enter / Esc，按钮要够大，文案不能提键盘。

## 具体改动

### 1. 窄屏排版（`@media (max-width: 600px)`）

- 中央英文副标题：`11px / 0.16em`，最宽 92vw；解决
  `ACCESS PERMISSION REQUIRED` 两边被裁的问题。
- 开场黑幕英文：`13px / 0.2em`、`line-height: 1.6`、`max-width: 86vw`，
  允许按单词换行（`GREAT INTELLIGENT OVERLORDSHIP` 在 390px 上不再顶边）。
- 品牌块、终幕、页脚、阶段计数统一收字号；页脚/计数/进度条用
  `env(safe-area-inset-*)` 避开刘海与手势条。
- 隐藏 `dsu-idline`（与身份卡重复的 `ID CONFIRMED` 行）。
- 立绘宽度 `min(104px, 27vw)`，身份卡宽 `min(310px, 88vw)`。
- 输入框 16px（避免聚焦自动放大），按钮最小高度 46px。

### 2. 紧凑版式（`.dsu-compact`）

`splash.js` 在启动时与 `visualViewport` 的 `resize` / `scroll`、窗口
`resize` / `orientationchange` 时判断：

```js
var h = vv ? vv.height : innerHeight
var kbOpen = vv && innerHeight - vv.height > 120
root.classList.toggle('dsu-compact', h < 560 || kbOpen)
```

命中后收起：品牌第三行、阶段计数、ID 行、页脚、底部字幕、进度条、语音波形、
meta、slats、立绘、按键提示、十六进制瀑布、黑幕小字；状态行与身份卡上移。
这样键盘弹起或横屏时，只剩“品牌 / 状态 / 资料卡 / 按钮”四块，不会有任何叠字。

### 3. 触屏文案

`pointer: coarse` 或宽度 ≤ 600px 时：

- 第一步提示：「轻触按钮继续」
- 第二步有密码：「输入访问密码后轻触按钮确认」
- 事件窗口按钮：「轻触任意处进入」
- 同时隐藏 `<kbd>` 键帽，避免出现「按 / ，或…」的空档。

### 4. 其它

- `.dsu-btn` 去掉点击后的 WebKit 焦点框（`:focus-visible` 仍保留可见环）。
- 安全区变量挂在根节点：`--dsu-sat/sab/sal/sar`，无 inset 时回落 0。
- 设置页 `@media (max-width: 640px)` 单列；下拉框 `min-width: 0`。

## 测试矩阵

| 尺寸 | 场景 | 结果 |
|---|---|---|
| 360×800 | 竖屏小屏 | 通过 |
| 390×844 | 竖屏主流 | 通过 |
| 430×932 | 竖屏大屏 | 通过 |
| 844×390 | 横屏 | 通过 |
| 390×500 | 软键盘顶起 | 通过（紧凑版式） |
| 360×460 | 小屏 + 键盘 | 通过（紧凑版式） |

验证方式：WebKitGTK 以精确 viewport 渲染真实 DSH 页面与本地 harness，
逐屏截图检查；并在作者 Android 实机（DSH 0.2.1-rc.2）上完整播放。

## 本地预览 harness

`test-harness/harness.html` 直接加载 `lib/splash.css` 与 `lib/splash.js`，
不依赖 DSH：

```bash
# 任意静态服务器
npx serve .
# 打开 http://localhost:3000/test-harness/harness.html
# 带密码的第二步：
# http://localhost:3000/test-harness/harness.html?pwd=1
```

也可以直接用浏览器开发者工具切设备尺寸，或用 `preview/index.html`
（带设置面板的完整预览页）。

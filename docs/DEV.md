# 开发说明

## 目录

```
lib/
  index.js      Host 半侧：注入 index.html、注册 /dsh-startup/* 路由、读写配置
  splash.js     浏览器端动画运行时（DOM、序列、音频、事件窗口）
  splash.css    动画样式（含手机适配段，文件末尾）
  client.js     设置页「启动动画」面板（ModuleLoader bundle）
  asset-data.js 内联音频素材（window.__DSA_ASSETS__）
  assets/*.mp3  真声素材源文件
preview/index.html   带控制台的离线预览页
test/                265 项断言的冒烟测试
test-harness/        手机布局调试页（不随 npm 包发布）
docs/                安装 / 手机适配 / 设置 / 开发文档
```

## 运行测试

```bash
npm test
```

包含 host 路由、注入、DOM 桩跑完整动画、设置页、桌面启动、密码校验。

## 手机布局调试

`test-harness/harness.html` 是零依赖的本地页，直接加载 `lib/splash.css`
与 `lib/splash.js`：

- `?pwd=1` 打开第二步密码输入
- 浏览器设备模拟切 360×800 / 390×844 / 844×390
- 键盘场景把视口高度调到 500 左右，`dsu-compact` 会自动生效

在无头环境（如 Linux 服务器）可用 WebKitGTK 精确渲染：

```bash
xvfb-run -a python3 tools/gshot.py 390 844 "file://$PWD/test-harness/harness.html" out.png 1.2
```

（`tools/gshot.py` 是作者用的快照脚本，可按需自建：Gtk.Window + WebKit2.WebView +
`get_snapshot`。）

## 发布

1. 改 `package.json` 版本与 `RELEASE-NOTES-x.y.z.md`
2. `npm test`
3. `npm pack` 生成 `dsh-startup-secret-x.y.z.tgz`
4. 在 GitHub 建 `vx.y.z` 标签和 Release，把 tgz 作为附件上传
5. 仓库根目录也保留一份 tgz，方便直接下载

手机用户只认 Release 或仓库根目录里的 `.tgz`，所以**每次发版都必须跑一次打包**。

### 可选：Actions 自动发版

想让推标签时自动打包，可在 `.github/workflows/release.yml` 放：

```yaml
name: release
on: { push: { tags: ['v*'] } }
permissions: { contents: write }
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22 }
      - run: npm test
      - run: npm pack
      - uses: softprops/action-gh-release@v2
        with:
          files: dsh-startup-secret-*.tgz
          generate_release_notes: true
```

创建/更新 workflow 文件需要 token 带 `workflow` 权限（经典 token 勾选 `workflow`）。

## 改手机样式时的注意事项

- 手机适配都放在 `lib/splash.css` 末尾，避免与桌面规则互相覆盖。
- 新增断点请同时考虑 `@media (max-width: 600px)` 与 `.dsu-compact`
  （键盘/横屏不会触发宽度断点）。
- 不要在 `.dsu-compact` 里隐藏身份卡或按钮本身。
- 触屏文案统一用 `COARSE` 判断，不要写死 `innerWidth`。

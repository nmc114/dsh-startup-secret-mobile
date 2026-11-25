# 安装

## 手机（DSHA，推荐）

不需要电脑、不需要终端。

1. 用手机浏览器打开本仓库的 **Releases** 页面，下载最新的
   `dsh-startup-secret-x.y.z.tgz`。**不要解压**（DSHA 直接读这个包）。
2. 打开 DSHA → **设置 → 插件管理 → 导入插件包**，选择刚下载的 `.tgz`。
3. 插件列表出现 `dsh-startup-secret` 后，按提示**重启 Web**
   （或把 DSHA 从后台划掉再打开）。
4. 重新进入 DSH，启动动画会播放。第一步点「授予访问权限」继续。

> 如果系统文件选择器看不到下载的包，先在文件管理器里确认它已下载完成；
> 部分机型会把它放在 `Download/`。

## 桌面端（DSH Web / Desktop）

### 脚本安装

- macOS / Linux：`./install.sh`（可加 `desktop` 装到桌面端）
- Windows：解压后双击 `安装.cmd`

### 手动安装（两步，缺一不可）

DSH 加载插件依赖 `dsh.profile.bundles` 层堆栈，`dsh plugin add` 只写依赖、
不会自动把包名加入 bundles；漏掉第二步会“装上了但完全没效果”。

```bash
dsh plugin --profile web add ./dsh-startup-secret-1.5.3.tgz
```

然后编辑 `~/.dsh/profiles/web/package.json`，在 `dsh.profile.bundles` 里加入
`"dsh-startup-secret"`，重启 `dsh web`。

## 卸载

- 手机：DSHA 插件管理里删除 `dsh-startup-secret`，重启 Web。
- 桌面：`dsh plugin --profile web remove dsh-startup-secret`，并从 bundles 移除。

## 排错

| 现象 | 处理 |
|---|---|
| 装完没有任何变化 | 确认重启过 Web；确认 bundles 里有 `dsh-startup-secret` |
| 设置里没有「启动动画」 | 同上；或到插件管理确认插件处于启用状态 |
| 动画只出现一次 | 默认按会话播放，新开页面 / 重开 App 会再播 |
| 导入报“不兼容” | 记录 DSHA / DSH 版本后提 Issue；本版在 DSH 0.2.1-rc.2 实测通过 |

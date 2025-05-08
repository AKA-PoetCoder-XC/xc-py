# Appium 自动化测试项目

## 环境配置

1. 安装Node.js
   - 下载并安装最新版Node.js: [Node.js官网](https://nodejs.org/)
   - 验证安装: `node -v` 和 `npm -v`

2. 安装Appium
   ```bash
   npm i -g appium
   npm update -g appium
   ```

3. 安装UiAutomator2驱动
   ```bash
   appium driver install uiautomator2
   ```

4. 安装Python依赖
   ```bash
   pip install appium-python-client
   ```

5. 安装Android Debug Bridge (ADB)
   - 下载Android Platform Tools: [官方下载](https://developer.android.com/studio/releases/platform-tools)
   - 解压zip文件到指定目录(如C:\platform-tools)
   - 配置环境变量:
     1. 右键"此电脑" → 属性 → 高级系统设置 → 环境变量
     2. 在系统变量Path中添加platform-tools目录路径(如C:\platform-tools)
   - 验证安装:
     ```bash
     adb version
     adb devices
     ```

6. 安装安卓模拟器（这里以雷电模拟器为例）
   - 下载雷电模拟器: [官网下载](https://www.ldmnq.com/)
   - 安装并启动雷电模拟器
   - 配置模拟器:
     1. 打开模拟器设置 → 性能设置 → 选择合适的内存和CPU配置
     2. 打开开发者选项 → 启用USB调试
   - 连接模拟器:
     ```bash
     adb connect 127.0.0.1:5555
     adb devices
     ```

## 项目说明

本项目是一个基于Appium的Android自动化测试框架，支持多设备并行测试。

主要功能:
- 自动获取APP包名
- 自动获取APP启动Activity
- 支持多设备并行测试

## 使用说明

1. 确保设备已连接(adb devices)
2. 修改appium_test.py中的设备列表
3. 运行测试:
   ```bash
   python appium_test.py
   ```
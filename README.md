要创建一个虚拟环境并安装所需的依赖项，您可以按照以下步骤进行操作：

1. **创建虚拟环境**：
   在您的项目目录中打开终端并运行以下命令：
   ```bash
   python -m venv venv
   ```

2. **激活虚拟环境**：
   - 在Windows上：
     ```bash
     venv\Scripts\activate
     ```
   - 在macOS或Linux上：
     ```bash
     source venv/bin/activate
     ```

3. **安装依赖项**：
   使用`pip`安装所需的库：
   ```bash
   pip install opencv-python numpy pillow
   ```

4. **运行**：
   确保虚拟环境处于激活状态，然后运行您的Python脚本：
   ```bash
   python hw.py
   ```
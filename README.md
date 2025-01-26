<div align="center">

![logo](./logo.svg)  

# ScratchToolkit
![GitHub repo size](https://img.shields.io/github/repo-size/EricDing618/Scratch-To-Pygame)
![GitHub Repo stars](https://img.shields.io/github/stars/EricDing618/Scratch-To-Pygame?style=flat)
![GitHub branch status](https://img.shields.io/github/checks-status/EricDing618/Scratch-To-Pygame/main)
![GitHub commit activity](https://img.shields.io/github/commit-activity/t/EricDing618/Scratch-To-Pygame)
![GitHub last commit](https://img.shields.io/github/last-commit/EricDing618/Scratch-To-Pygame)
![GitHub Created At](https://img.shields.io/github/created-at/EricDing618/Scratch-To-Pygame)  

</div>

# STP: Scratch-To-Pygame
## 描述
- Scratch-To-Pygame（STP）是一个用Python实现的将Scratch转换为Pygame的脚本工具，现已支持`.sb3`文件。
## 快速使用
在本仓库目录下使用`cmd`执行：
```bash
python ./STP/stp.py <your .sb3 file path>
```
更多使用方法：
- `-h`和`--help`：显示命令帮助列表。
- `-r`和`--run`：转换完毕后自动执行output文件。
- `-nl`和`--no-log`：不显示输出日志。
## 将不考虑支持以下功能：
- 变量、列表显示功能
- “说”“思考”“询问...并等待”显示功能
- 除画笔、音乐以外的Scratch3扩展功能  

（注：你可以提交建议添加这些功能的Issue，但[EricDing618](https://github.com/EricDing618)可能不会添加，需要等待他人的PR。）
# 第三方库&软件
库：
- loguru==0.7.2
- cairosvg==2.7.1
- pillow==9.5.0
- pygame==2.5.2
- numpy==1.26.2
- colorama==0.4.6

软件：
- GTK+ 3.24.31

若您还没有安装这些第三方库或已经遇到了`ImportError`，请使用`pip install -r requirements.txt`，以及解压并安装`dependencies`分支下的软件（仅支持Windows x64）。
## 报错解决
- `ImportError`：详见**第三方库&软件**。

若这仍不能解决您的问题，请确保该问题没有在issues被提出并解决，然后创建issue并等待解决。
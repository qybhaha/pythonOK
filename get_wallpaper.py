import requests
import os
import tkinter as tk
from tkinter import messagebox


def download_wallpapers():
    try:
        # 获取输入框中的值
        num_images = int(entry.get())
        if 1 <= num_images <= 30:
            # 创建 WallPaper 文件夹（如果不存在）
            if not os.path.exists('WallPaper'):
                os.makedirs('WallPaper')
            for i in range(num_images):
                url = f"https://bingw.jasonzeng.dev?resolution=UHD&index={i}"
                print(url)
                res = requests.get(url)
                # 保存图片到 WallPaper 文件夹
                file_path = os.path.join('WallPaper', f"wallpaper{i}.jpg")
                with open(file_path, "wb") as w:
                    w.write(res.content)
            messagebox.showinfo("提示", "图片下载完成！")
        else:
            messagebox.showerror("错误", "请输入 1 到 30 之间的整数。")
    except ValueError:
        messagebox.showerror("错误", "请输入有效的整数。")


# 创建主窗口
root = tk.Tk()
root.title("必应壁纸下载器")

# 创建标签
label = tk.Label(root, text="请输入要下载的图片数量 (1-30):")
label.pack(pady=10)

# 创建输入框
entry = tk.Entry(root)
entry.pack(pady=5)

# 创建下载按钮
button = tk.Button(root, text="下载", command=download_wallpapers)
button.pack(pady=20)

# 运行主循环
root.mainloop()

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import numpy as np
import matplotlib.pyplot as plt
import csv

class BlacknessCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("XXXX厂图片黑色度计算")
        self.root.geometry("400x400")  # 设置窗口初始大小
        self.pic_list = []  # 存储选中图片路径
        self.results = []  # 存储计算结果：[(名片名, 黑色度), ...]
        
        # 创建界面组件
        self.create_widgets()
        
    def create_widgets(self):
        # 标题标签
        title_label = ttk.Label(
            self.root, 
            text="图片黑色度计算（黑色度=255-图片灰度）", 
            font=("微软雅黑", 12)
        )
        title_label.pack(pady=5)
        
        # 分隔线
        separator = ttk.Separator(self.root, orient="horizontal")
        separator.pack(fill="x", padx=5, pady=3)
        
        # 选择图片区域
        select_frame = ttk.Frame(self.root)
        select_frame.pack(fill="x", padx=5, pady=3)
        
        self.select_btn = ttk.Button(
            select_frame, 
            text="选择图片", 
            command=self.select_images
        )
        self.select_btn.pack(side="left", padx=3)
        
        ttk.Label(select_frame, text="共选择了").pack(side="left", padx=2)
        self.count_label = ttk.Label(select_frame, text="0")
        self.count_label.pack(side="left", padx=2)
        ttk.Label(select_frame, text="张图片").pack(side="left", padx=2)
        
        # 查看结果按钮
        self.result_btn = ttk.Button(
            self.root, 
            text="查看结果", 
            command=self.calculate_blackness
        )
        self.result_btn.pack(pady=3)
        
        # 结果显示区域
        ttk.Label(self.root, text="计算结果:").pack(anchor="w", padx=5)
        self.result_text = tk.Text(self.root, height=10, width=50)
        self.result_text.pack(padx=5, pady=3, fill="both", expand=True)
        
        # 导出CSV按钮
        self.export_btn = ttk.Button(
            self.root, 
            text="导出CSV", 
            command=self.export_csv
        )
        self.export_btn.pack(pady=5)
        
    def select_images(self):
        """选择图片文件并更新计数"""
        filetypes = [("图片文件", "*.jpg;*.png"), ("所有文件", "*.*")]
        paths = filedialog.askopenfilenames(
            title="选择图片",
            filetypes=filetypes,
            initialdir=os.getcwd()
        )
        if paths:
            self.pic_list = list(paths)
            self.count_label.config(text=str(len(self.pic_list)))
            
    def calculate_blackness(self):
        """计算选中图片的黑色度并显示结果"""
        self.result_text.delete(1.0, tk.END)  # 清空文本框
        self.results.clear()  # 清空历史结果
        
        if not self.pic_list:
            messagebox.showinfo("提示", "未选择图片！")
            return
            
        for img_path in self.pic_list:
            # 获取文件名（不含路径和扩展名）
            filename = os.path.basename(img_path)
            card_name = os.path.splitext(filename)[0]  # 移除.png/.jpg
            
            try:
                # 读取图片并计算黑色度（保留原计算逻辑）
                img_data = plt.imread(img_path)
                rgb_weights = np.array([0.299, 0.587, 0.114])
                gray_mean = np.dot(img_data, rgb_weights).mean()
                blackness = 255 - gray_mean
                blackness_str = f"{blackness:.2f}"  # 保留两位小数
                
                # 存储结果并显示
                self.results.append((card_name, blackness_str))
                self.result_text.insert(tk.END, f"{card_name} 的黑色度为 {blackness_str}\n\n")
                
            except Exception as e:
                self.result_text.insert(tk.END, f"{card_name} 处理失败: {str(e)}\n\n")
                
    def export_csv(self):
        """导出结果到CSV文件"""
        if not self.results:
            messagebox.showinfo("提示", "无结果可导出！")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")],
            title="保存CSV文件"
        )
        if not file_path:
            return  # 用户取消保存
            
        try:
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["图片名", "计算结果"])  # 表头
                writer.writerows(self.results)  # 数据行
            messagebox.showinfo("成功", f"CSV已导出至:\n{file_path}")
        except Exception as e:
            messagebox.showerror("导出失败", f"保存文件时出错: {str(e)}")

if __name__ == "__main__":
    # 移除证书年份检查，直接启动应用
    root = tk.Tk()
    app = BlacknessCalculator(root)
    root.mainloop()

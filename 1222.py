import tkinter as tk
from tkinter import font
import random
import os

class LotteryApp:
    def __init__(self, root, total_numbers, third_prize_count, second_prize_count, first_prize_count):
        self.root = root
        self.root.title("双旦趴抽奖程序")
        self.root.geometry("1000x300")

        self.label_font = font.Font(family="Helvetica", size=20)
        self.result_font = font.Font(family="Helvetica", size=20, weight="bold")

        self.label = tk.Label(root, text="点击按钮进行抽奖", font=self.label_font)
        self.label.pack(pady=10)

        self.btn_third_prize = tk.Button(root, text="三等奖", command=self.draw_third_prize)
        self.btn_third_prize.pack(pady=5)
        self.btn_third_prize.bind("<Enter>", lambda event: self.change_button_color(self.btn_third_prize, "red"))
        self.btn_third_prize.bind("<Leave>", lambda event: self.change_button_color(self.btn_third_prize, "black"))

        self.btn_second_prize = tk.Button(root, text="二等奖", command=self.draw_second_prize)
        self.btn_second_prize.pack(pady=5)
        self.btn_second_prize.bind("<Enter>", lambda event: self.change_button_color(self.btn_second_prize, "red"))
        self.btn_second_prize.bind("<Leave>", lambda event: self.change_button_color(self.btn_second_prize, "black"))

        self.btn_first_prize = tk.Button(root, text="一等奖", command=self.draw_first_prize)
        self.btn_first_prize.pack(pady=5)
        self.btn_first_prize.bind("<Enter>", lambda event: self.change_button_color(self.btn_first_prize, "red"))
        self.btn_first_prize.bind("<Leave>", lambda event: self.change_button_color(self.btn_first_prize, "black"))

        self.result_label = tk.Label(root, text="", font=self.result_font, fg="red")
        self.result_label.pack(pady=10)

        self.third_prize_label = tk.Label(root, text="", font=self.result_font, fg="red")
        self.second_prize_label = tk.Label(root, text="", font=self.result_font, fg="red")
        self.first_prize_label = tk.Label(root, text="", font=self.result_font, fg="red")

        self.total_numbers = total_numbers
        self.all_numbers = list(range(1, total_numbers + 1))
        self.drawn_numbers_third = []
        self.drawn_numbers_second = []
        self.drawn_numbers_first = []

        # 记录每个奖项已中奖的数量
        self.drawn_count_third = 0
        self.drawn_count_second = 0
        self.drawn_count_first = 0

        # 三等奖、二等奖和一等奖的数量
        self.third_prize_count = third_prize_count
        self.second_prize_count = second_prize_count
        self.first_prize_count = first_prize_count

        # 读取jiang文件
        self.load_saved_numbers()

    def get_save_path(self):
        # 获取用户主目录下的桌面路径
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        return os.path.join(desktop_path, 'jiang')

    def load_saved_numbers(self):
        try:
            file_path = self.get_save_path()
            with open(file_path, "r") as file:
                lines = file.readlines()
                if len(lines) >= 3:
                    self.drawn_numbers_third = [int(num) for num in lines[0].strip().split(',') if num]
                    self.drawn_numbers_second = [int(num) for num in lines[1].strip().split(',') if num]
                    self.drawn_numbers_first = [int(num) for num in lines[2].strip().split(',') if num]

                    # 计算每个奖项已中奖的数量
                    self.drawn_count_third = len(self.drawn_numbers_third)
                    self.drawn_count_second = len(self.drawn_numbers_second)
                    self.drawn_count_first = len(self.drawn_numbers_first)

                    if self.drawn_count_third >= self.third_prize_count:
                        self.show_result("三等奖", self.drawn_numbers_third, self.third_prize_label)
                    if self.drawn_count_second >= self.second_prize_count:
                        self.show_result("二等奖", self.drawn_numbers_second, self.second_prize_label)
                    if self.drawn_count_first >= self.first_prize_count:
                        self.show_result("一等奖", self.drawn_numbers_first, self.first_prize_label)

        except FileNotFoundError:
            # 如果文件不存在，创建一个空的jiang文件
            open(self.get_save_path(), "w").close()

    def save_numbers_to_file(self):
        try:
            file_path = self.get_save_path()
            with open(file_path, "w") as file:
                file.write(','.join(map(str, self.drawn_numbers_third)) + '\n')
                file.write(','.join(map(str, self.drawn_numbers_second)) + '\n')
                file.write(','.join(map(str, self.drawn_numbers_first)) + '\n')
        except Exception as e:
            print(f"保存文件时出现错误: {e}")

    def change_button_color(self, button, color):
        button.config(fg=color)

    def draw_third_prize(self):
        if self.drawn_count_third < self.third_prize_count:
            number = self.get_unique_random_number(self.all_numbers, self.drawn_numbers_third)
            self.drawn_numbers_third.append(number)
            self.all_numbers.remove(number)
            self.save_numbers_to_file()
            self.show_result_after_delay("三等奖", self.drawn_numbers_third, self.third_prize_label)
            self.drawn_count_third += 1
        else:
            self.show_result("三等奖", self.drawn_numbers_third + ["已抽完"], self.third_prize_label)

    def draw_second_prize(self):
        if self.drawn_count_third < self.third_prize_count:
            self.show_result_after_delay("请先抽取三等奖", [], self.second_prize_label)
        elif self.drawn_count_second < self.second_prize_count:
            number = self.get_unique_random_number(self.all_numbers, self.drawn_numbers_second + self.drawn_numbers_third)
            self.drawn_numbers_second.append(number)
            self.all_numbers.remove(number)
            self.save_numbers_to_file()
            self.show_result_after_delay("二等奖", self.drawn_numbers_second, self.second_prize_label)
            self.drawn_count_second += 1
        else:
            self.show_result("二等奖", self.drawn_numbers_second + ["已抽完"], self.second_prize_label)

    def draw_first_prize(self):
        if self.drawn_count_third < self.third_prize_count or self.drawn_count_second < self.second_prize_count:
            self.show_result_after_delay("请先抽取三等奖和二等奖", [], self.first_prize_label)
        elif self.drawn_count_first < self.first_prize_count:
            number = self.get_unique_random_number(
                self.all_numbers,
                self.drawn_numbers_first + self.drawn_numbers_second + self.drawn_numbers_third
            )
            self.drawn_numbers_first.append(number)
            self.all_numbers.remove(number)
            self.save_numbers_to_file()
            self.show_result_after_delay("一等奖", self.drawn_numbers_first, self.first_prize_label)
            self.drawn_count_first += 1
        else:
            self.show_result("一等奖", self.drawn_numbers_first + ["已抽完"], self.first_prize_label)

    def show_result_after_delay(self, prize_type, numbers, label_widget):
        self.root.after(1000, self.show_result, prize_type, numbers, label_widget)

    def show_result(self, prize_type, numbers, label_widget):
        result_text = f"{prize_type}：{', '.join(map(str, numbers))}"
        self.result_label.config(text=result_text)

        if label_widget:
            label_widget.config(text=result_text)

    def get_unique_random_number(self, all_numbers, drawn_numbers):
        # 从all_numbers中随机选择一个数字，直到选择一个不在drawn_numbers中的数字
        while True:
            number = random.choice(all_numbers)
            if number not in drawn_numbers:
                return number

if __name__ == "__main__":
    root = tk.Tk()
    total_numbers = 51  # 设置抽奖总数
    third_prize_count = 20
    second_prize_count = 5
    first_prize_count = 2
    app = LotteryApp(root, total_numbers, third_prize_count, second_prize_count, first_prize_count)
    root.mainloop()

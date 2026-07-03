import tkinter as tk

def main():
    # Создаем главное окно
    root = tk.Tk()
    root.title("Простое окно")
    root.geometry("400x300")
    root.configure(bg="#2c3e50")

    # Добавляем текстовую метку
    label = tk.Label(
        root, 
        text="Привет, мир!", 
        font=("Arial", 20, "bold"), 
        fg="#ecf0f1", 
        bg="#2c3e50"
    )
    label.pack(pady=50)

    # Функция обработчика кнопки
    def on_click():
        label.config(text="Кнопка нажата!")

    # Добавляем кнопку
    button = tk.Button(
        root, 
        text="Нажми меня", 
        font=("Arial", 12), 
        command=on_click,
        bg="#3498db", 
        fg="white", 
        activebackground="#2980b9", 
        activeforeground="white",
        bd=0,
        padx=20,
        pady=10
    )
    button.pack()

    # Запуск главного цикла
    root.mainloop()

if __name__ == "__main__":
    main()

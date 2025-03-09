import os
import pywhatkit as pywt
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
import tkinter.filedialog as fd
import subprocess

selected_image = None


def send_message(name: str, number: str, message: str, image: str):
    """
    Отправляет сообщение через WhatsApp с изображением.

    :param name: Имя получателя.
    :param number: Номер телефона получателя.
    :param message: Текст сообщения.
    :param image: Путь к изображению, которое будет отправлено.
    """
    try:
        pywt.sendwhats_image(
            receiver=number,
            img_path=image,
            caption=message,
            tab_close=True
        )
    except Exception as e:
        messagebox.showinfo(f"Failed to send message to {name} ({number}): {e}")


def read_contacts(contacts_path):
    """
    Читает контакты из файла и возвращает их в виде списка словарей.

    :param contacts_path: Путь к файлу с контактами.
    :return: Список контактов, где каждый контакт — это словарь с ключами 'name' и 'number'.
    """
    contacts = []
    try:
        with open(contacts_path, 'r', encoding='utf-8') as file:
            for line in file:
                name, number = line.strip().split(':')
                contacts.append({'name': name, 'number': number})
    except Exception as e:
        messagebox.showerror("Error", f"Ошибка чтения файла контактов!, {e}")
    return contacts


def read_message(message_path):
    """
    Читает текст сообщения из файла.

    :param message_path: Путь к файлу с сообщением.
    :return: Текст сообщения.
    """
    try:
        with open(message_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        messagebox.showerror("Error", f"Ошибка чтения файла сообщения!, {e}")
    return None


def send_messages():
    """
    Отправляет сообщение с изображением всем контактам из файла.
    Перед отправкой проверяет наличие файлов контактов, сообщений и выбранного изображения.
    """
    global selected_image

    contacts_path = Path('contacts.txt')
    if not contacts_path.exists():
        messagebox.showerror("Error", "Файл контактов не найден!")
        return

    contacts = read_contacts(contacts_path)
    if not contacts:
        return

    message_path = Path('text.txt')
    if not message_path.exists():
        messagebox.showerror("Error", "Файл сообщения не найден!")
        return

    message_template = read_message(message_path)
    if not message_template:
        return

    if not selected_image:
        messagebox.showerror("Error", "Картинка не выбрана!")
        return

    for contact in contacts:
        name = contact['name']
        number = contact['number']
        message = message_template.replace("имя", name)
        send_message(name, number, message, selected_image)

    messagebox.showinfo("Success", "Сообщения успешно отправлены!")


def choose_image():
    """
    Открывает диалог выбора изображения и сохраняет путь к нему в глобальной переменной selected_image.
    Также обновляет текстовую метку с именем выбранного изображения.
    """
    global selected_image
    image = fd.askopenfilename(title="Открыть файл", initialdir=".")
    if image:
        selected_image = image  # Сохраняем путь к выбранной картинке
        image_name = os.path.basename(image)
        image_label.config(text=f'Картинка выбрана: {image_name}')


def open_file(filename):
    """
    Открывает указанный файл с помощью стандартного приложения.

    :param filename: Путь к файлу, который нужно открыть.
    """
    try:
        subprocess.run(['open', filename], check=True)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open {filename}: {e}")


def main():
    """Создает графический интерфейс программы."""
    global image_label
    root = tk.Tk()
    root.title("WhatsApp Message Sender")
    root.geometry("400x200")
    font = ("Times New Roman", 20)

    btn_contacts = tk.Button(root, text="Контакты", command=lambda: open_file('contacts.txt'), font=font)
    btn_contacts.grid(row=0, column=0, padx=5, pady=10)

    btn_text = tk.Button(root, text="Текст", command=lambda: open_file('text.txt'), font=font)
    btn_text.grid(row=0, column=1, padx=1, pady=1)

    image_btn = tk.Button(root, text="Картинка", command=choose_image, font=font)
    image_btn.grid(row=0, column=2, padx=1, pady=1)

    image_label = tk.Label(root, text="")
    image_label.grid(row=1, column=0, columnspan=3)

    btn_send = tk.Button(root, text="Отправить", command=send_messages, font=font)
    btn_send.grid(row=3, column=1, padx=10, pady=10)

    exit_button = tk.Button(root, text="Выход", command=root.quit, font=font)
    exit_button.grid(row=4, column=1, padx=10, pady=10)

    root.mainloop()


if __name__ == '__main__':
    main()

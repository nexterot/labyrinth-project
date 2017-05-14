# Скрипт, который меняет ip адрес в статических файлах и js-скриптах
# на внешний ip сервера (для запуска и отладки локально(

pattern = "0.0.0.0"
ip = "37.139.2.176"


def replace_ips(file_name):
    with open(file_name, "r") as file:
        content = file.read()
        while content.find(pattern) != -1:
                content = content.replace(pattern, ip)
        result = content

    with open(file_name, "w") as file:
        file.write(result)

files = [
    "http_server//front_server//templates//info.html",
    "js_frontend//game//game.js",
    "js_frontend//game//client_mechanics_3.js",
    "js_frontend//game//graphical_functions.js"
]

if __name__ == "__main__":
    answer = input("Вы действитльно хотите заменить адреса? ('y'/'n') ")
    if answer == "y":
        for file in files:
            replace_ips(file)


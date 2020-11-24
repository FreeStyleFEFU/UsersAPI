import requests
import time

def gui():

    key_list = ["id", "first_name", "last_name", "city"]
    name_key = ["id - ", "имя - ", "фамилия - ", "город - "]
    user_list=[]

    print("Введите идентификатор пользователя")
    id = input()
    if len(id) < 1:
        print("Все фигня, давай по-новой")
        gui()
        return
    id = parent(id, key_list, name_key, user_list)
    childrens(id, key_list, name_key, user_list)

    with open("users.txt", "w", encoding='utf-8') as file:
        count=1
        for line in user_list:
            row=f"{count} "
            count+=1
            for value in range(len(line)):
                row += str(line[value])
                if (value+1)%2 == 0:
                    row+="; "
            file.writelines(f"{row}\n")
    
    
    

def parent(id, key_list, name_key, user_list):
    requestStringUser = f"https://api.vk.com/method/users.get?access_token=3c10b57e3c10b57e3c10b57ef33c645bb533c103c10b57e63a01af78fd985745dfee641&v=5.126&user_ids={id}&fields=city"
    response = requests.get(requestStringUser)
    errors(response)
    
    user = response.json()['response']
    index = response.json()['response'][0]['id']
    print(user)

    user_list.append([])

    for key in range(len(key_list)):
        user_list[0].append(name_key[key])
        if key == len(key_list)-1:
            try:          
                user_list[0].append(user[0][key_list[key]]['title'])
            except:
                user_list[0].append("Неизвестен")
        else:
            user_list[0].append(user[0][key_list[key]])

    return index

def childrens(id, key_list, name_key, user_list):
    requestStringFriends = f"https://api.vk.com/method/users.getFollowers?access_token=3c10b57e3c10b57e3c10b57ef33c645bb533c103c10b57e63a01af78fd985745dfee641&v=5.126&user_id={id}"
    response = requests.get(requestStringFriends)
    errors(response)

    size = response.json()['response']['count']
    users=[]
    offset=0
    while offset < size:

        response = requests.get(f"https://api.vk.com/method/users.getFollowers?access_token=3c10b57e3c10b57e3c10b57ef33c645bb533c103c10b57e63a01af78fd985745dfee641&v=5.126&user_id={id}&count=1000&offset={offset}&fields=city")
        data = response.json()['response']['items']
        offset+=1000
        print(offset)
        users.extend(data)
        time.sleep(0.1)

    for user in range(len(users)):
        user_list.append([])
        for key in range(len(key_list)):
            user_list[user+1].append(name_key[key])
            if key == len(key_list)-1:
                try:
                    user_list[user+1].append(users[user][key_list[key]]['title'])
                except:
                    user_list[user+1].append("Неизвестен")
            else:
                try:
                    user_list[user+1].append(users[user][key_list[key]])
                except:
                    user_list[user+1].append("Неизвестен")

def errors(response):
    if response.status_code != 200:
        print("Запрос не выполнен. Проверьте правильность идентификатора пользователя")
        gui()
        return
    try:
        response.json()['response']
    except:
        print(response.json()['error']['error_msg'])
        gui()
        return
    if len(response.json()['response']) < 1:
        print("Ошибка запроса")
        gui()
        return


if __name__ == "__main__":
    gui()
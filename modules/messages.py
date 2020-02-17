class Message():
    language = "default"

    button_try_another = "Try another"
    button_add_meal = "Add meal"
    button_exact_dish = "No, I exactly mean that dish"
    button_back_main_menu = "<- Back to main menu  "
    button_edit_name = "Edit name"
    button_edit_weight = "Edit weight"
    button_edit_birthday = "Edit birthday"
    button_edit_lenght = "Edit lenght"
    button_private_policy = "Private Policy"
    button_accept_policy = "I accept private policy"
    button_turn_on_diet = "High cholesterol diet: TURN ON"
    button_turn_off_diet = "High cholesterol diet: TURN OFF"
    button_notication_on = "Turn ON notifications"
    button_notication_off = "Turn OFF notifications"
    button_gmail_on = "Connect Gmail account"
    button_gmail_off = "Disconnect Gmail account"
    button_withings_on = "Connect WiThings account"
    button_withings_off = "Disconnect WiThings account"

    main_menu = "/main_menu"
    weight = "/weight"
    recomendations = "/recomendations"
    meal = "/meal"
    about_you = "/about_you"

    text_meal_info = "Add this dish as a meal or try another"
    text_loading = "Updating, please wait..."
    text_too_much_similar = 'I found too much similar dishes.\nChoose one from the list'
    text_entered_dish = "You entered dish {}"
    text_meal_added = "Your meal added"
    text_enter_dish = "Please, enter dish that plan to eat or already ate"
    text_main_menu = "You are in a main menu"
    text_enter_weight = "Please, enter your weight"
    text_weight_added = "Your weight added"
    text_about_user = """Name: {}\nBirthday: {}\nWeight: {}\nLenght: {}\n"""
    text_empty = "Empty"
    text_more_inforamtion_add = "More information you add, more personalised recomendations will be"
    text_eat_too_much = "Looks like you already eat too much for today. Take a break and drink water"
    text_recomended_dishes = "Here is recomended dishes for you.\nChoose one from the list or add yours"
    text_enter_info = "Please, enter new {}"
    text_wrong_birthday_format = "Wrong format of data\nPlease enter your birthday like 14.11.2019"
    text_updated_info = "Your {} updated"
    text_hello = "Hi!\nI'm Louie-Louie personal nutrition assistant.\nI was developed by @berryrock to demostrate possibilities of Mealmapp, food management platform."
    text_accept_policy = "Please accept Private Policy to continue"
    text_welcome = "Thank you for interest for the project. Hope your enjoy it"
    text_spamming = "Looks like you are spamming. Just don't"
    text_error = 'Something went wrong.\nTry again later or write your problem to @berryrock'
    text_diet_on = "High cholesterol diet turned on"
    text_diet_off = "High cholesterol diet turned off"
    text_settings = "Set up your settings"
    text_connected_services = "We use special service to automatically collect your information about meals"
    text_notification_update = "Notification status updated"
    text_gmail_update = "Gmail account deleted"
    text_connect_gmail = "Connect your Gmail account for automatical collection of your meals from food delivery services"
    text_withings_update = "WiThings account deleted"
    text_connect_withings = "Connect your WiThings account for automatical weight collection"

    edit_personal = {"weight": "weight", "lenght": "lenght", "birthday": "birthday", "name": "name"}

class RussianTranslation(Message):
    language = "Русский"

    button_try_another = "Выбрать другое"
    button_add_meal = "Записать прием пищи"
    button_exact_dish = "Я имел в виду именно это блюдо"
    button_back_main_menu = "<- Назад в главное меню  "
    button_edit_name = "Имя"
    button_edit_weight = "Вес"
    button_edit_birthday = "День рождения"
    button_edit_lenght = "Рост"
    button_private_policy = "Политика конфиденциальности"
    button_accept_policy = "Я принимаю политику конфиденциальности"
    button_turn_on_diet = "Диета при высоком холестерине: ВКЛЮЧИТЬ"
    button_turn_off_diet = "Диета при высоком холестерине: ВЫКЛЮЧИТЬ"
    button_notication_on = "Включить уведомления"
    button_notication_off = "Выключить уведомления"
    button_gmail_on = "Подключить Gmail аккаунт"
    button_gmail_off = "Отключить Gmail аккаунт"
    button_withings_on = "Подключить WiThings аккаунт"
    button_withings_off = "Отключить WiThings аккаунт"

    text_meal_info = "Запишите, что съели это блюдо или выберите другое"
    text_loading = "Обновляю данные, пожалуйста, подождите..."
    text_too_much_similar = "Я нашел слишком много похожих блюд.\nВыберите одно из списка"
    text_entered_dish = "Вы выбрали блюдо {}"
    text_meal_added = "Вы добавили прием пищи"
    text_enter_dish = "Введите блюдо, которые вы съели или планируете съесть"
    text_main_menu = "Вы в главном меню"
    text_enter_weight = "Введите свой вес"
    text_weight_added = "Вес записан"
    text_about_user = """Имя: {}\nДень рождения: {}\nВес: {}\nРост: {}\n\nВыберите, какую информацию вы хотите отредактировать"""
    text_empty = "Пусто"
    text_more_inforamtion_add = "Чем больше вы добавите информации, тем более персонализированные будут рекомендации"
    text_eat_too_much = "Похоже вы сегодня уже съели слишком много. Возьмите перерыв и попейте воды :)"
    text_recomended_dishes = "Рекомендую вам эти блюда.\nВыберите одно из списка или введите свое"
    text_enter_info = "Введите {}"
    text_wrong_birthday_format = "Неверный формат\nВведите дату в формате: 14.11.2019"
    text_updated_info = "{} обновлено"
    text_hello = "Привет!\nЯ Louie-Louie персональный ассистент питания.\nЯ был разработан для демонстрации возможностей платформы Mealmapp. Создатель @berryrock"
    text_accept_policy = "Примите политику конфиденциальности, чтобы продолжить"
    text_welcome = "Спасибо за проявленный инетрес к проекту. Надеюсь, он Вам понравится"
    text_spamming = "Похоже, вы спамите. Пожалуй, не стоит."
    text_error = 'Что-то пошло не так\nПопробуйте еще раз позже или напишите свою проблему @berryrock'
    text_diet_on = "Диета при высоком холестерине включена"
    text_diet_off = "Диета при высоком холестерине выключена"
    text_settings = "Ваши настройки"
    text_connected_services = "При подключении Gmail-аккаунта будут прочитаны только письма, отправителями которых значатся сервисы доставки. Прочая почта останется конфиденциальной"
    text_notification_update = "Статус уведомлений обновлен"
    text_gmail_update = "Gmail аккаунт удален"
    text_connect_gmail = "Подключите ваш Gmail аккаунт, чтобы информацию о заказах из сервисов доставки добавлялась автоматически"
    text_withings_update = "WiThings аккаунт удален"
    text_connect_withings = "Подключите аккаунт WiThings, чтобы автоматически добавлять информацию об изменении веса"

    edit_personal = {"weight": "вес", "lenght": "рост", "birthday": "день рождения", "name": "имя"}

russian = RussianTranslation()
translation = {"rus": russian}

import config
from json.decoder import JSONDecodeError

def message_handler(message, dbhelper, uihelper, backend):
    try:
        step = dbhelper.get_step(message.chat.id)[0]
        dbhelper.clear_call(message.chat.id)

        if message.text == config.Menu_RU.MAIN_MENU.value:
            dbhelper.set_step(message.chat.id, config.Step.MAIN_MENU.value)
            daily_info = backend.daily_info(message.chat.id)
            uihelper.main_menu(message.chat.id, diets=daily_info['diets'], kcal_consumpted=daily_info['consumpted_kcal'], kcal_daily=daily_info['daily_kcal'])
            if len(alleged) > 0:
                uihelper.alleged_message(message.chat.id)
                for alleged in daily_info['alleged'][:3]:
                    uihelper.alleged(message.chat.id, alleged)

        elif message.text == config.Menu_RU.RECOMENDATIONS.value:
            dbhelper.set_step(message.chat.id, config.Step.MEAL.value)
            uihelper.loading(message.chat.id)
            recomendations = backend.recomendations(message.chat.id)
            dbhelper.set_data(message.chat.id, config.UserData.RECOMENDATIONS.value, recomendations)
            uihelper.recomendations(message.chat.id, recomendations)

        elif message.text == config.Menu_RU.MEAL.value:
            dbhelper.set_step(message.chat.id, config.Step.MEAL.value)
            uihelper.enter_meal(message.chat.id)

        elif message.text == config.Menu_RU.WEIGHT.value:
            dbhelper.set_step(message.chat.id, config.Step.WEIGHT.value)
            uihelper.add_weight(message.chat.id)

        elif message.text == config.Menu_RU.ABOUT.value:
            dbhelper.set_step(message.chat.id, config.Step.ABOUT.value)
            user_info = backend.user_info(message.chat.id)
            user_name = user_info.get('name', 'Empty')
            user_weight = user_info.get('weight', 'Empty')
            user_lenght = user_info.get('lenght', 'Empty')
            user_birth = user_info.get('birthday', 'Empty')
            dbhelper.set_data(message.chat.id, config.UserData.NAME.value, user_name)
            dbhelper.set_data(message.chat.id, config.UserData.WEIGHT.value, user_weight)
            dbhelper.set_data(message.chat.id, config.UserData.LENGHT.value, user_lenght)
            dbhelper.set_data(message.chat.id, config.UserData.BIRTH.value, user_birth)
            uihelper.about_user(message.chat.id, user_info)

        elif message.text == config.Menu_RU.SETTINGS.value:
            dbhelper.set_step(message.chat.id, config.Step.SETTINGS.value)
            settings = backend.user_settings(message.chat.id)
            uihelper.settings(message.chat.id, settings)

        else:
            try:
                if step == config.Step.MAIN_MENU.value:
                    if message.text == "test_user_data":
                        dbhelper.print_user_data(message.chat.id)

                    elif message.text == config.Step.START_ACCEPT.value or message.text == config.Step.START_ACCEPT_RU.value:
                        print('NEW USER', message.chat.id)

                    else:
                        dish_info = backend.dish_info(message.chat.id, message.text)
                        dbhelper.set_data(message.chat.id, config.UserData.DISH.value, message.text)
                        if dish_info[1] == True:
                            dbhelper.set_step(message.chat.id, config.Step.MEAL_INFO.value)
                            uihelper.meal_info(message.chat.id, dish_info[0])

                        elif dish_info[1] == False:
                            similar_dishes = dish_info[0]['similar_dishes'].split(';')
                            uihelper.choose_dish_from_list(message.chat.id, similar_dishes)
                            uihelper.dish_entered_correct(message.chat.id, message.text)

                elif step == config.Step.ABOUT.value:
                    user_info = backend.user_info(message.chat.id)
                    user_name = user_info.get('name', 'Empty')
                    user_weight = user_info.get('weight', 'Empty')
                    user_lenght = user_info.get('lenght', 'Empty')
                    user_birth = user_info.get('birthday', 'Empty')
                    dbhelper.set_data(message.chat.id, config.UserData.NAME.value, user_name)
                    dbhelper.set_data(message.chat.id, config.UserData.WEIGHT.value, user_weight)
                    dbhelper.set_data(message.chat.id, config.UserData.LENGHT.value, user_lenght)
                    dbhelper.set_data(message.chat.id, config.UserData.BIRTH.value, user_birth)
                    uihelper.about_user(message.chat.id, user_info)

                elif step == config.Step.ABOUT_NAME.value:
                    user_info = backend.update_info(message.chat.id, 'name', message.text)
                    dbhelper.set_data(message.chat.id, config.UserData.NAME.value, message.text)
                    uihelper.updated_user(message.chat.id, 'name')
                    uihelper.about_user(message.chat.id, user_info)

                elif step == config.Step.ABOUT_LENGHT.value:
                    user_info = backend.update_info(message.chat.id, 'lenght', message.text)
                    dbhelper.set_data(message.chat.id, config.UserData.LENGHT.value, message.text)
                    uihelper.updated_user(message.chat.id, 'lenght')
                    uihelper.about_user(message.chat.id, user_info)

                elif step == config.Step.ABOUT_BIRTH.value:
                    try:
                        birthday = message.text.split('.')
                        birthday = "{}-{}-{}".format(birthday[2],birthday[1],birthday[0])
                        user_info = backend.update_info(message.chat.id, 'birthday', birthday)
                        dbhelper.set_data(message.chat.id, config.UserData.BIRTH.value, birthday)
                        uihelper.updated_user(message.chat.id, 'birthday')
                        uihelper.about_user(message.chat.id, user_info)
                    except IndexError:
                        uihelper.wrong_data_format(message.chat.id)

                elif step == config.Step.ABOUT_WEIGHT.value:
                    backend.send_weight(message.chat.id, message.text)
                    user_info = backend.user_info(message.chat.id)
                    dbhelper.set_data(message.chat.id, config.UserData.WEIGHT.value, user_info.get('name','Empty'))
                    uihelper.updated_user(message.chat.id, 'weight')
                    uihelper.about_user(message.chat.id, user_info)

                elif step == config.Step.WEIGHT.value:
                    dbhelper.set_step(message.chat.id, config.Step.MAIN_MENU.value)
                    #dbhelper.set_data(message.chat.id, config.UserData.WEIGHT.value, message.text)
                    backend.send_weight(message.chat.id, message.text)
                    uihelper.weight_added(message.chat.id)
                    uihelper.main_menu(message.chat.id)

                elif step == config.Step.MEAL.value:
                    dish_info = backend.dish_info(message.chat.id, message.text)
                    if dish_info[1] == True:
                        print(dish_info)
                        dbhelper.set_step(message.chat.id, config.Step.MEAL_INFO.value)
                        dbhelper.set_data(message.chat.id, config.UserData.DISH.value, dish_info[0]["dish"])
                        uihelper.meal_info(message.chat.id, dish_info[0])

                    elif dish_info[1] == False:
                        similar_dishes = dish_info[0]['similar_dishes'].split(';')
                        dbhelper.set_data(message.chat.id, config.UserData.DISH.value, message.text)
                        dbhelper.set_step(message.chat.id, config.Step.MEAL.value)
                        uihelper.choose_dish_from_list(message.chat.id, similar_dishes)
                        uihelper.dish_entered_correct(message.chat.id, message.text)

                elif step == config.Step.START_LOG.value:
                    dbhelper.add_user(message.chat.id, message.text)

            except KeyError:
                dbhelper.set_step(message.chat.id, config.Step.MAIN_MENU.value)
                uihelper.error_message(message.chat.id)
                uihelper.main_menu(message.chat.id)

            except IndexError:
                dbhelper.set_step(message.chat.id, config.Step.MAIN_MENU.value)
                uihelper.main_menu(message.chat.id)

            except JSONDecodeError:
                dbhelper.set_step(message.chat.id, config.Step.MAIN_MENU.value)
                uihelper.error_message(message.chat.id)
                uihelper.main_menu(message.chat.id)

    except IndexError:
        if message.text == config.Step.START_ACCEPT.value or message.text == config.Step.START_ACCEPT_RU.value:
            backend.add_user(message.chat.id)
            dbhelper.set_step(message.chat.id, config.Step.MAIN_MENU.value)
            uihelper.welcome_message(message.chat.id)
            uihelper.main_menu(message.chat.id)

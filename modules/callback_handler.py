import config
from json.decoder import JSONDecodeError

def callback_handler(call, dbhelper, uihelper, backend):
    step = dbhelper.get_step(call.message.chat.id)[0]
    print(step)
    previous_calls = dbhelper.get_call(call.message.chat.id)
    print('previous calls', previous_calls)
    if len(previous_calls) < 3:
        previous_calls.append(None)
        previous_calls.append(None)
    if call.data == previous_calls[0] and call.data == previous_calls[1] and call.data == previous_calls[2]:
        print(call.message.chat.id, 'spamming')
        pass
    elif call.data == previous_calls[0] and call.data == previous_calls[1]:
        dbhelper.set_call(call.message.chat.id, call.data)
        uihelper.spamming(call.message.chat.id)
    else:
        dbhelper.set_call(call.message.chat.id, call.data)
        try:
            if call.data == config.Step.MEAL_ADD.value:
                if step == config.Step.MEAL_INFO.value:
                    dbhelper.set_step(call.message.chat.id, config.Step.MAIN_MENU.value)
                    data = dbhelper.get_data(call.message.chat.id, config.UserData.DISH.value)[0]
                    print(data)
                    try:
                        dish = data['dish']
                    except TypeError:
                        dish = data
                    backend.send_meal(call.message.chat.id, dish)
                    uihelper.meal_added(call.message.chat.id)
                    uihelper.main_menu(call.message.chat.id)

            elif call.data == config.Step.MEAL.value:
                dbhelper.set_step(call.message.chat.id, config.Step.MEAL.value)
                uihelper.enter_meal(call.message.chat.id)

            elif call.data == config.Step.MEAL_EXACT.value:
                dbhelper.set_step(call.message.chat.id, config.Step.MEAL_INFO.value)
                dish_data = dbhelper.get_data(call.message.chat.id, config.UserData.DISH.value)[0]
                dish_info = backend.exact_dish(call.message.chat.id, dish_data)
                uihelper.meal_info(call.message.chat.id, dish_info[0])

            elif call.data[:4] == 'rec_':
                recomended_dishes = dbhelper.get_data(call.message.chat.id, config.UserData.RECOMENDATIONS.value)[0]
                recomended_dishes = recomended_dishes.split(';')
                dish = recomended_dishes[int(call.data[4]) - 1]
                dish_info = backend.dish_info(call.message.chat.id, dish)
                dbhelper.set_data(call.message.chat.id, config.UserData.DISH.value, call.message.text)
                if dish_info[1] == True:
                    dbhelper.set_step(call.message.chat.id, config.Step.MEAL_INFO.value)
                    uihelper.meal_info(call.message.chat.id, dish_info[0])

                elif dish_info[1] == False:
                    similar_dishes = dish_info[0]['similar_dishes'].split(';')
                    uihelper.choose_dish_from_list(call.message.chat.id, similar_dishes)
                    uihelper.dish_entered_correct(call.message.chat.id, call.message.text)

            elif call.data == config.Step.RECOMENDATIONS_REFRESH.value:
                dbhelper.set_step(call.message.chat.id, config.Step.MEAL.value)
                recomendations = backend.recomendations(call.message.chat.id)
                dbhelper.set_data(call.message.chat.id, config.UserData.RECOMENDATIONS.value, recomendations)
                uihelper.recomendations(call.message.chat.id)

            elif call.data == config.Step.MAIN_MENU.value:
                dbhelper.set_step(call.message.chat.id, config.Step.MAIN_MENU.value)
                uihelper.main_menu(call.message.chat.id)

            elif call.data[:4] == config.Step.ALLEGED_ACCEPT.value:
                dbhelper.set_step(call.message.chat.id, config.Step.MAIN_MENU.value)
                backend.accept_alleged(call.message.chat.id,call.data[4:])
                uihelper.alleged_accept(call.message.chat.id)

            elif call.data[:4] == config.Step.ALLEGED_DECLINE.value:
                dbhelper.set_step(call.message.chat.id, config.Step.MAIN_MENU.value)
                backend.accept_alleged(call.message.chat.id,call.data[4:],accept=False)
                uihelper.alleged_decline(call.message.chat.id)

            elif call.data == config.Step.ALLEGED_DECLINE.value:
                dbhelper.set_step(call.message.chat.id, config.Step.MAIN_MENU.value)
                uihelper.alleged_accepted(call.message.chat.id)

            elif call.data == config.Step.ABOUT_NAME.value:
                dbhelper.set_step(call.message.chat.id, config.Step.ABOUT_NAME.value)
                uihelper.edit_personal(call.message.chat.id, 'name')

            elif call.data == config.Step.ABOUT_LENGHT.value:
                dbhelper.set_step(call.message.chat.id, config.Step.ABOUT_LENGHT.value)
                uihelper.edit_personal(call.message.chat.id, 'lenght')

            elif call.data == config.Step.ABOUT_WEIGHT.value:
                dbhelper.set_step(call.message.chat.id, config.Step.ABOUT_WEIGHT.value)
                uihelper.edit_personal(call.message.chat.id, 'weight')

            elif call.data == config.Step.ABOUT_BIRTH.value:
                dbhelper.set_step(call.message.chat.id, config.Step.ABOUT_BIRTH.value)
                uihelper.edit_personal(call.message.chat.id, 'birthday')

            elif call.data == config.Step.DIET_ON.value:
                dbhelper.set_step(call.message.chat.id, config.Step.ABOUT.value)
                backend.user_diet(call.message.chat.id,config.Step.DIET_ON.value)
                uihelper.diet_on(call.message.chat.id)
                user_info = backend.user_info(call.message.chat.id)
                user_name = user_info.get('name', 'Empty')
                user_weight = user_info.get('weight', 'Empty')
                user_lenght = user_info.get('lenght', 'Empty')
                user_birth = user_info.get('birthday', 'Empty')
                dbhelper.set_data(call.message.chat.id, config.UserData.NAME.value, user_name)
                dbhelper.set_data(call.message.chat.id, config.UserData.WEIGHT.value, user_weight)
                dbhelper.set_data(call.message.chat.id, config.UserData.LENGHT.value, user_lenght)
                dbhelper.set_data(call.message.chat.id, config.UserData.BIRTH.value, user_birth)
                uihelper.about_user(call.message.chat.id, user_info)

            elif call.data == config.Step.DIET_OFF.value:
                dbhelper.set_step(call.message.chat.id, config.Step.ABOUT.value)
                backend.user_diet(call.message.chat.id,config.Step.DIET_OFF.value)
                uihelper.diet_off(call.message.chat.id)
                user_info = backend.user_info(call.message.chat.id)
                user_name = user_info.get('name', 'Empty')
                user_weight = user_info.get('weight', 'Empty')
                user_lenght = user_info.get('lenght', 'Empty')
                user_birth = user_info.get('birthday', 'Empty')
                dbhelper.set_data(call.message.chat.id, config.UserData.NAME.value, user_name)
                dbhelper.set_data(call.message.chat.id, config.UserData.WEIGHT.value, user_weight)
                dbhelper.set_data(call.message.chat.id, config.UserData.LENGHT.value, user_lenght)
                dbhelper.set_data(call.message.chat.id, config.UserData.BIRTH.value, user_birth)
                uihelper.about_user(call.message.chat.id, user_info)

            elif call.data == config.Step.NOTIFICATION_ON.value:
                dbhelper.set_step(call.message.chat.id, config.Step.SETTINGS.value)
                backend.notifications_turn(call.message.chat.id, config.Step.NOTIFICATION_ON.value)
                uihelper.notification_update(call.message.chat.id)
                settings = backend.user_settings(call.message.chat.id)
                uihelper.settings(call.message.chat.id, settings)

            elif call.data == config.Step.NOTIFICATION_OFF.value:
                dbhelper.set_step(call.message.chat.id, config.Step.SETTINGS.value)
                backend.notifications_turn(call.message.chat.id, config.Step.NOTIFICATION_OFF.value)
                uihelper.notification_update(call.message.chat.id)
                settings = backend.user_settings(call.message.chat.id)
                uihelper.settings(call.message.chat.id, settings)

            elif call.data == config.Step.GMAIL_OFF.value:
                dbhelper.set_step(call.message.chat.id, config.Step.SETTINGS.value)
                settings = backend.clear_service(call.message.chat.id, config.GMAIL_SERVICE)
                uihelper.gmail_update(call.message.chat.id)
                uihelper.settings(call.message.chat.id, settings)

            elif call.data == config.Step.GMAIL_OFF.value:
                dbhelper.set_step(call.message.chat.id, config.Step.SETTINGS.value)
                settings = backend.clear_service(call.message.chat.id, config.WITHINGS_SERVICE)
                uihelper.gmail_update(call.message.chat.id)
                uihelper.settings(call.message.chat.id, settings)

            else:
                dbhelper.set_step(call.message.chat.id, config.Step.MAIN_MENU.value)
                uihelper.error_message(call.message.chat.id)
                uihelper.main_menu(call.message.chat.id)

        except JSONDecodeError:
            dbhelper.set_step(call.message.chat.id, config.Step.MAIN_MENU.value)
            uihelper.error_message(call.message.chat.id)
            uihelper.main_menu(call.message.chat.id)

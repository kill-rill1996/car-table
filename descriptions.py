from typing import List


TEXT_1 = "ОБРАТИТЕ ВНИМАНИЕ!!! В нашем магазине представлены запчасти преимущественно с ПРАВОРУЛЬНЫХ автомобилей (если иное не указано в комментарии), ряд из которых НЕ ПОДХОДЯТ на леворульные авто. Будьте внимательны при заказе."
TEXT_2 = "Перед заказом ОБЯЗАТЕЛЬНО уточняйте наличие и комплектацию товара. МЫ ПРОДАЕМ ТОВАР, КОТОРЫЙ УКАЗАН В НАЗВАНИИ ОБЪЯВЛЕНИЯ! На фото могут находиться несколько товаров!\nВ редких случаях цена может отличаться от цены в объявлении."
TEXT_3 = "Отправка габаритных деталей возможна ТОЛЬКО транспортными компаниями (СДЭК или Энергия), курьерская доставка до ТК — 500рублей. Авито доставкой не отправляем! Либо Вы можете самостоятельно оформить доставку в любой другой ТК с забором груза из нашего офиса. Стоимость и сроки доставки уточняйте в ТК. А также рекомендуем заказывать в ТК обрешетку и страховать груз!"
TEXT_4 = "Для ряда деталей номера OEM носят справочный характер, ПРОСИМ ВАС самостоятельно сверять их по фото или маркировке с самой детали до покупки (покраски, установки), либо обратиться за помощью к менеджеру!"
TEXT_5 = "Мы предлагаем только контрактные запчасти из Японии с аукционных авто с минимальным пробегом, но и такие детали являются Б/У и могут содержать в себе скрытые дефекты, которые невозможно выявить без установки на авто. Со своей стороны по просьбе покупателя мы готовы произвести проверки, возможные без установки (доп. фото наружного состояния, толщину ЛКП, эндоскопию ДВС). А также даем гарантию на детали КРОМЕ ЭЛЕКТРОТОВАРОВ - 14 дней. Пожалуйста принимайте решение о покупке с учетом этих условий."
TEXT_6 = "Если Вы не нашли какую-то запчасть среди наших товаров отправьте VIN/Номер кузова, мы проверим наличие индивидуально, а, так же, при ее отсутствии, поможем привезти из Японии или заказать новую."
TEXT_7 = "УСЛОВИЯ ВОЗВРАТА ТОВАРА!!!\n\nПриобретая товар Вы соглашаетесь с тем, что автозапчасть бывшая в употреблении (Б/У), после установки может не работать и/или работать некорректно. Вы разделяете риск того, что запчасть может оказаться нерабочей. Обмен и возврат товара возможен, но только до истечения гарантийного срока, при условии сохранения товарного вида и целостности детали, без следов разбора и нарушения маркерных меток. Возврат денежных средств возможен только после получения товара нами. Все расходы по замене, установке, транспортировке, стоимость тех жидкостей сальников, фильтров оплачивает покупатель. СОВЕРШАЯ ПОКУПКУ ТОВАРА БЫВШЕГО В УПОТРЕБЛЕНИИ ВЫ ПРИНИМАЕТЕ ВСЕ УСЛОВИЯ НАШЕГО МАГАЗИНА. Приобретая запчасть бывшую в употреблении Вы готовы понести указанные выше расходы без требований к их компенсации и согласны с данными условиями договора. Всегда есть возможность вернуть запчасть. Возврат возможен только уплаченной суммы за деталь. Пожалуйста принимайте решение о покупке с учетом этих условий."

TEXT_8 = "Цены на ДВИГАТЕЛИ, указаны БЕЗ навесного оборудования! До установки сличайте датчики, Иногда клапан VVTI, датчики уровня и другое не совпадает. Сальники, прокладки, катушки, датчики, водяной насос, термостат и т.д. являются расходным материалом и не являются предметом претензий относительно работоспособности, а так же не входят в стоимость товара."
TEXT_9 = "Сверяйте АКПП до установки, датчики, селекторы, диаметры привода, шлицевую"
TEXT_10 = "особенности продажи электрики"
TEXT_11 = "Компрессор кондиционера в состоянии Б/У. Продается исключительно на запчасти, НЕ для использования в СБОРЕ. За время доставки из Японии а так же во время хранения компрессор может испортиться. Расходы на проверку компрессора, установку, промывку системы, замену осушителя превышают стоимость самой запчасти, и это расходы которые мы не будем компенсировать. Приобретая компрессор кондиционера Вы понимаете и принимаете риски. Купите лучше новый."
TEXT_12 = "Цена на  ДВЕРИ указана за голую дверь.(только железо), Если Вас интересует запчасть с двери или дверь в сборе напишите нам, обсудим цену."


def get_description(row: List) -> str:
    """Общая функция для подготовки description по группам и подгруппам из 1С файла"""
    group = row[12]
    sub_group = row[13]

    # rule 1
    if group == "ДВИГАТЕЛЬ" and sub_group != "ДВС":
        return get_description_rule_1(row)

    # rule 1.1
    if group == "ДВИГАТЕЛЬ" and sub_group == "ДВС":
        return get_description_rule_1(row, rule1_1=True)

    # rule 2
    if group == "КУЗОВ_НАРУЖНЫЕ_ЭЛЕМЕНТЫ": # TODO убрать пробел КУЗОВ_ НАРУЖНЫЕ_ЭЛЕМЕНТЫ
        if sub_group == "Двери":
            return get_description_rule_2(row, rule2_1=True)
        else:
            return get_description_rule_2(row)

    # rule 2
    if group in ["КУЗОВ_ВНУТРИ", "ОПТИКА", "СИСТЕМА_БЕЗОПАСНОСТИ_SRS", "СТЕКЛА_КУЗОВНЫЕ"]:
        return get_description_rule_2(row)

    # rule 3
    if group == "ПОДВЕСКА_ПЕРЕДНИХ_И_ЗАДНИХ КОЛЕС":
        if sub_group not in ["Колпак_колеса", "Диск_колпак_колесный", "Колесо"]:
            return get_description_rule_3(row)
        else:
            if sub_group == "Колпак_колеса":
                return "ПРАВИЛО 4" # TODO
            elif sub_group == "Диск_колпак_колесный":
                return "ПРАВИЛО 5" # TODO
            elif sub_group == "Колесо":
                return "ПРАВИЛО 6" # TODO

    # rule 3.1
    if group in ["РУЛЕВОЕ_УПРАВЛЕНИЕ", "СИСТЕМА_ВЫПУСКА_ОТРАБОТАННЫХ_ГАЗОВ", "ТОРМОЗНАЯ_СИСТЕМА", "ЭЛЕКТРООСНАЩЕНИЕ"]:
        return get_description_rule_3(row)

    # rule 3.2
    if group == "СИСТЕМА_ОХЛАЖДЕНИЯ_И_ОТОПЛЕНИЯ":
        if sub_group == "Компрессор_кондиционера":
            return get_description_rule_3(row, rule3_2=True)
        else:
            return get_description_rule_3(row)

    # rule 3.3
    if group == "ТРАНСМИССИЯ_И_ПРИВОД":
        if sub_group == "Коробка_Переменных_Передач_(КПП)":
            return get_description_rule_3(row, rule3_3=True)
        else:
            return get_description_rule_3(row)


def get_description_rule_1(row: List, rule1_1: bool = None) -> str:
    """Группа «ДВИГАТЕЛЬ» все подгруппы за исключением подгруппы «ДВС»"""
    cell_c = row[2].strip() + " " if row[2].strip() else ""
    cell_b = row[1].strip() + " " if row[1].strip() else ""
    cell_v = f"Модель двигателя {row[21].strip()}" + " " if row[21].strip() else ""
    cell_w = row[22].strip() + " " if row[22].strip() else ""
    cell_x = f'Объем {row[23].replace("R", "").strip()}' + " " if row[23].replace("R", "").strip() else ''
    cell_u = f"Привод {row[20].strip()}" + " " if row[20].strip() else ""

    if row[9].strip() == "Б.У" or row[9].strip() == "":
        if row[15].strip() == "ALL" or row[15].strip() == "":
            cell_j = ""
        else:
            cell_j = f"Производитель {row[15].strip()}" + " "
    else:
        cell_j = f"Производитель {row[9].strip()}" + " "

    if row[15].strip() == "ALL" or row[15].strip() == "":
        cell_p = ""
    else:
        cell_p = f"На авто {row[15].strip()}" + " "

    if row[16].strip() == "ALL" or row[16].strip() == " ":
        cell_q = ""
    else:
        cell_q = f"модель {row[16].strip()}" + " "

    if row[17].strip() == "ALL" or row[17].strip() == "":
        cell_r = ""
    else:
        cell_r = f"Поколение {row[17].strip()}" + " "

    cell_ae = f"Доп инф {row[30].strip()}" + " " if row[30].strip() else ""
    cell_h = f"Номер детали {row[7].strip()}" + " " if row[7].strip() else ""
    cell_f = f"ОЕМ {row[5].strip()}" + " " if row[5].strip() else ""
    cell_d = f"Крос номер {row[3].strip()}" + " " if row[3].strip() else ""
    cell_ac = f"Состояние {row[28].strip()}" + " " if row[28].strip() else ""
    cell_g = f"На детали указано {row[6].strip()}" + " " if row[6].strip() else ""
    cell_e = f"код {row[4].strip()}" + " " if row[4].strip() else ""

    if rule1_1:
        text = f"{cell_c}{cell_b}{cell_v}{cell_w}{cell_x}{cell_u}{cell_j}{cell_p}{cell_q}{cell_r}{cell_ae}" \
               f"{cell_h}{cell_f}{cell_d}{cell_ac}{cell_g}{cell_e}\n{TEXT_1}\n{TEXT_2}\n{TEXT_3}\n{TEXT_8}\n{TEXT_5}\n" \
               f"{TEXT_6}\n{TEXT_7}"
    else:
        text = f"{cell_c}{cell_b}{cell_v}{cell_w}{cell_x}{cell_u}{cell_j}{cell_p}{cell_q}{cell_r}{cell_ae}" \
               f"{cell_h}{cell_f}{cell_d}{cell_ac}{cell_g}{cell_e}\n{TEXT_1}\n{TEXT_2}\n{TEXT_3}\n{TEXT_4}\n{TEXT_5}\n" \
               f"{TEXT_6}\n{TEXT_7}"

    return text


def get_description_rule_2(row: List, rule2_1: bool = None) -> str:
    """Группы «КУЗОВ»,«ОПТИКА», СИСТЕМА_БЕЗОПАСНОСТИ_SRS СТЕКЛА_КУЗОВНЫЕ"""
    cell_c = row[2].strip() + " " if row[2].strip() else ""
    cell_b = row[1].strip() + " " if row[1].strip() else ""
    cell_z = f"сторона {row[25].strip()}" + " " if row[25].strip() else ""
    cell_aa = f"положение {row[26].strip()}" + " " if row[26].strip() else ""
    cell_ab = f"расположение {row[27].strip()}" + " " if row[27].strip() else ""

    if row[9].strip() == "Б.У" or row[9].strip() == "":
        if row[15].strip() == "ALL" or row[15].strip() == "":
            cell_j = ""
        else:
            cell_j = f"Производитель {row[15].strip()}" + " "
    else:
        cell_j = f"Производитель {row[9].strip()}" + " "

    if row[15].strip() == "ALL" or row[15].strip() == "":
        cell_p = ""
    else:
        cell_p = f"На авто {row[15].strip()}" + " "

    if row[16].strip() == "ALL" or row[16].strip() == " ":
        cell_q = ""
    else:
        cell_q = f"модель {row[16].strip()}" + " "

    if row[17].strip() == "ALL" or row[17].strip() == "":
        cell_r = ""
    else:
        cell_r = f"Поколение {row[17].strip()}" + " "

    cell_ae = f"Доп инф {row[30].strip()}" + " " if row[30].strip() else ""
    cell_h = f"Номер детали {row[7].strip()}" + " " if row[7].strip() else ""
    cell_f = f"ОЕМ {row[5].strip()}" + " " if row[5].strip() else ""
    cell_d = f"Крос номер {row[3].strip()}" + " " if row[3].strip() else ""
    cell_ac = f"Состояние {row[28].strip()}" + " " if row[28].strip() else ""
    cell_g = f"На детали указано {row[6].strip()}" + " " if row[6].strip() else ""
    cell_i = f"цена указана за {row[8].strip()}" + " " if row[8].strip() else ""
    cell_e = f"код {row[4].strip()}" + " " if row[4].strip() else ""

    if rule2_1:
        text = f"{cell_c}{cell_b}{cell_z}{cell_aa}{cell_ab}{cell_j}{cell_p}{cell_q}{cell_r}{cell_ae}{cell_h}{cell_f}{cell_d}" \
               f"{cell_ac}{cell_g}{cell_i}{cell_e}\n{TEXT_12}\n{TEXT_1}\n{TEXT_2}\n{TEXT_3}\n{TEXT_4}\n{TEXT_5}\n{TEXT_6}\n{TEXT_7}"
    else:
        text = f"{cell_c}{cell_b}{cell_z}{cell_aa}{cell_ab}{cell_j}{cell_p}{cell_q}{cell_r}{cell_ae}{cell_h}{cell_f}{cell_d}" \
               f"{cell_ac}{cell_g}{cell_i}{cell_e}\n{TEXT_1}\n{TEXT_2}\n{TEXT_3}\n{TEXT_4}\n{TEXT_5}\n{TEXT_6}\n{TEXT_7}"

    return text


def get_description_rule_3(row: List, rule3_2: bool = None, rule3_3: bool = None) -> str:
    """Группы ПОДВЕСКА_ПЕРЕДНИХ_ И_ЗАДНИХ КОЛЕС (за исключением подгруппы Колпак_колеса, Диск_колпак_колесный, Колесо),
    РУЛЕВОЕ_УПРАВЛЕНИЕ, СИСТЕМА_ВЫПУСКА_ОТРАБОТАННЫХ_ГАЗОВ, СИСТЕМА_ОХЛАЖДЕНИЯ_И_ОТОПЛЕНИЯ (за исключением подгруппы Компрессор_кондиционера),
    ТОРМОЗНАЯ_СИСТЕМА, ТРАНСМИССИЯ_И_ПРИВОД, ЭЛЕКТРООСНАЩЕНИЕ"""
    cell_c = row[2].strip() + " " if row[2].strip() else ""
    cell_b = row[1].strip() + " " if row[1].strip() else ""
    cell_v = f"Модель двигателя {row[21].strip()}" + " " if row[21].strip() else ""
    cell_w = row[22].strip() + " " if row[22].strip() else ""
    cell_x = f'Объем {row[23].replace("R", "").strip()}' + " " if row[23].replace("R", "").strip() else ''
    cell_u = f"Привод {row[20].strip()}" + " " if row[20].strip() else ""
    cell_z = f"сторона {row[25].strip()}" + " " if row[25].strip() else ""
    cell_aa = f"положение {row[26].strip()}" + " " if row[26].strip() else ""
    cell_ab = f"расположение {row[27].strip()}" + " " if row[27].strip() else ""

    if row[9].strip() == "Б.У" or row[9].strip() == "":
        if row[15].strip() == "ALL" or row[15].strip() == "":
            cell_j = ""
        else:
            cell_j = f"Производитель {row[15].strip()}" + " "
    else:
        cell_j = f"Производитель {row[9].strip()}" + " "

    if row[15].strip() == "ALL" or row[15].strip() == "":
        cell_p = ""
    else:
        cell_p = f"На авто {row[15].strip()}" + " "

    if row[16].strip() == "ALL" or row[16].strip() == " ":
        cell_q = ""
    else:
        cell_q = f"модель {row[16].strip()}" + " "

    if row[17].strip() == "ALL" or row[17].strip() == "":
        cell_r = ""
    else:
        cell_r = f"Поколение {row[17].strip()}" + " "

    cell_ae = f"Доп инф {row[30].strip()}" + " " if row[30].strip() else ""
    cell_h = f"Номер детали {row[7].strip()}" + " " if row[7].strip() else ""
    cell_f = f"ОЕМ {row[5].strip()}" + " " if row[5].strip() else ""
    cell_d = f"Крос номер {row[3].strip()}" + " " if row[3].strip() else ""
    cell_ac = f"Состояние {row[28].strip()}" + " " if row[28].strip() else ""
    cell_g = f"На детали указано {row[6].strip()}" + " " if row[6].strip() else ""
    cell_e = f"код {row[4].strip()}" + " " if row[4].strip() else ""

    if rule3_2:
        text = f"{cell_c}{cell_b}{cell_v}{cell_w}{cell_x}{cell_u}{cell_z}{cell_aa}{cell_ab}{cell_j}{cell_p}{cell_q}{cell_r}" \
               f"{cell_ae}{cell_h}{cell_f}{cell_d}{cell_ac}{cell_g}{cell_e}\n{TEXT_11}\n{TEXT_1}\n{TEXT_2}\n{TEXT_3}\n{TEXT_4}\n{TEXT_5}\n" \
               f"{TEXT_6}\n{TEXT_7}"
    elif rule3_3:
        text = f"{cell_c}{cell_b}{cell_v}{cell_w}{cell_x}{cell_u}{cell_z}{cell_aa}{cell_ab}{cell_j}{cell_p}{cell_q}{cell_r}" \
               f"{cell_ae}{cell_h}{cell_f}{cell_d}{cell_ac}{cell_g}{cell_e}\n{TEXT_1}\n{TEXT_2}\n{TEXT_3}\n{TEXT_4}\n{TEXT_9}\n{TEXT_5}\n" \
               f"{TEXT_6}\n{TEXT_7}"
    else:
        text = f"{cell_c}{cell_b}{cell_v}{cell_w}{cell_x}{cell_u}{cell_z}{cell_aa}{cell_ab}{cell_j}{cell_p}{cell_q}{cell_r}" \
               f"{cell_ae}{cell_h}{cell_f}{cell_d}{cell_ac}{cell_g}{cell_e}\n{TEXT_1}\n{TEXT_2}\n{TEXT_3}\n{TEXT_4}\n{TEXT_5}\n" \
               f"{TEXT_6}\n{TEXT_7}"

    return text


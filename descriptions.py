from typing import List


TEXT_1 = "ОБРАТИТЕ ВНИМАНИЕ!!! В нашем магазине много запчастей с ПРАВОРУЛЬНЫХ авто и некоторые из них НЕ ПОДХОДЯТ на леворульные авто."
TEXT_2 = "Уточняйте наличие, цену и комплектацию. На фото могут находиться несколько товаров!\nИногда цена запчасти может отличаться от цены в объявлении."
TEXT_3 = "Авито доставкой мы отправляем небольшие запчасти. Отправка габаритных деталей возможна транспортными компаниями (курьерская доставка до ТК СДЭК или Энергия 500рублей) либо Вы можете оформить забор груза в  ТК. Мы рекомендуем заказывать в ТК обрешетку и страховать груз!"
TEXT_4 = "Для ряда деталей номера OEM  носят справочный характер, ПРОСИМ ВАС самостоятельно сверять запчасти по фото и маркировке с самой детали до ПОКУПКИ (ПОКРАСКИ, УСТАНОВКИ)."
TEXT_5 = "Мы предлагаем Б/У контрактные запчасти из Японии с аукционных авто с минимальным пробегом. Но детали Б/У  могут содержать в себе скрытые дефекты, которые невозможно выявить без установки на авто. По просьбе покупателя мы готовы дополнительно осмотреть запчасти, (прислать доп. фото наружного состояния, толщину ЛКП, эндоскопию ДВС). Пожалуйста принимайте решение о покупке с учетом этих условий."
TEXT_6 = ""
TEXT_7 = "Приобретая товар, Вы соглашаетесь с тем, что автозапчасть бывшая в употреблении (Б/У), после установки может не работать и/или работать некорректно. Вы разделяете риск того, что запчасть может оказаться нерабочей. Гарантийный срок на Б/У запчасти 14 дней. Обмен и возврат товара возможен, в течении 14 дней с момента получения товара, но при условии сохранения товарного вида и целостности детали, без следов разбора и нарушения маркерных меток. Возврат денежных средств происходит  после получения товара нами. Все расходы по замене, установке, транспортировке, стоимость расходных материалов оплачивает покупатель. СОВЕРШАЯ ПОКУПКУ ТОВАРА БЫВШЕГО В УПОТРЕБЛЕНИИ ВЫ ПРИНИМАЕТЕ ВСЕ УСЛОВИЯ НАШЕГО МАГАЗИНА. Приобретая запчасть бывшую в употреблении Вы готовы понести указанные выше расходы без требований к их компенсации и согласны с данными условиями договора. Возврат возможен только уплаченной суммы за деталь. Пожалуйста принимайте решение о покупке с учетом этих условий."
TEXT_8 = "Цены на ДВИГАТЕЛИ, указаны БЕЗ навесного оборудования! Иногда датчики и другое не совпадают. Сальники, прокладки, катушки, свечи, датчики, водяной насос, термостат и т.д. являются расходным материалом и не являются предметом претензий относительно работоспособности, а так же не входят в стоимость товара."
TEXT_9 = "Сверяйте АКПП до установки, датчики, селекторы, привода и т.д."
TEXT_10 = "особенности продажи электрики"
TEXT_11 = "Компрессор кондиционера состоянии Б/У. Продается исключительно на запчасти, НЕ для использования в СБОРЕ. Расходы на проверку компрессора и установку превышают стоимость самой запчасти, и это расходы которые мы не будем компенсировать. Приобретая компрессор кондиционера Вы понимаете и принимаете риски. Купите лучше новый."
TEXT_12 = "Цена на ДВЕРИ указана за голую дверь (только железо). Если Вас интересует запчасть с двери или дверь в сборе мы уточним цену."

HEADER_BEFORE_TEXTS = "Условия продажи:"


def get_description(row: List, mmg: List) -> str:
    """Общая функция для подготовки description по группам и подгруппам из 1С файла
    Make Model Generation (mmg) берутся не из исходной строки"""
    group = row[12]
    sub_group = row[13]
    mmg = [str(i) for i in mmg]

    # rule 1
    if (group == "ДВИГАТЕЛЬ" and sub_group != "ДВС") \
        or (group == "ГРУЗОВИК" and sub_group == "ДВИГАТЕЛЬ"):
        return get_description_rule_1(row, mmg)

    # rule 1.1
    if group == "ДВИГАТЕЛЬ" and sub_group == "ДВС":
        return get_description_rule_1(row, mmg, rule1_1=True)

    # rule 2
    if group == "КУЗОВ_НАРУЖНЫЕ_ЭЛЕМЕНТЫ":
        if sub_group == "Двери":
            return get_description_rule_2(row, mmg, rule2_1=True)
        else:
            return get_description_rule_2(row, mmg)

    # rule 2
    if group in ["КУЗОВ_ВНУТРИ", "ОПТИКА", "СИСТЕМА_БЕЗОПАСНОСТИ_SRS", "СТЕКЛА_КУЗОВНЫЕ"] \
            or (group == "ГРУЗОВИК" and sub_group in ["КАБИНА", "ЭЛЕКТРИКА"]):
        return get_description_rule_2(row, mmg)

    # rule 3
    if group == "ПОДВЕСКА_ПЕРЕДНИХ_И_ЗАДНИХ КОЛЕС":
        if sub_group not in ["Колпак_колеса", "Диск_колпак_колесный", "Колесо"]:
            return get_description_rule_3(row, mmg)
        else:
            if sub_group == "Колпак_колеса":
                return "ПРАВИЛО 4" # TODO
            elif sub_group == "Диск_колпак_колесный":
                return "ПРАВИЛО 5" # TODO
            elif sub_group == "Колесо":
                return "ПРАВИЛО 6" # TODO

    if group == "ГРУЗОВИК" and sub_group == "ХОДОВАЯ":
        return get_description_rule_3(row, mmg)

    # rule 3.1
    if group in ["РУЛЕВОЕ_УПРАВЛЕНИЕ", "СИСТЕМА_ВЫПУСКА_ОТРАБОТАННЫХ_ГАЗОВ", "ТОРМОЗНАЯ_СИСТЕМА", "ЭЛЕКТРООСНАЩЕНИЕ"]:
        return get_description_rule_3(row, mmg)

    # rule 3.2
    if group == "СИСТЕМА_ОХЛАЖДЕНИЯ_И_ОТОПЛЕНИЯ":
        if sub_group == "Компрессор_кондиционера":
            return get_description_rule_3(row, mmg, rule3_2=True)
        else:
            return get_description_rule_3(row, mmg)

    # rule 3.3
    if group == "ТРАНСМИССИЯ_И_ПРИВОД":
        if sub_group == "Коробка_Переменных_Передач_(КПП)":
            return get_description_rule_3(row, mmg, rule3_3=True)
        else:
            return get_description_rule_3(row, mmg)

    # rule 3.4
    if group == "ГРУЗОВИК" and sub_group == "ТРАНСМИССИЯ":
        return get_description_rule_3(row, mmg, rule3_4=True)


def get_description_rule_1(row: List, mmg: List, rule1_1: bool = None) -> str:
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

    if mmg[0].strip() == "ALL" or mmg[0].strip() == "":
        cell_p = ""
    else:
        cell_p = f"На авто {mmg[0].strip()}" + " "

    if mmg[1].strip() == "ALL" or mmg[1].strip() == "":
        cell_q = ""
    else:
        cell_q = f"модель {mmg[1].strip()}" + " "

    if mmg[2].strip() == "ALL" or mmg[2].strip() == "":
        cell_r = ""
    else:
        cell_r = f"Поколение {mmg[2].strip()}" + " "

    cell_ae = f"Доп инф {row[30].strip()}" + " " if row[30].strip() else ""
    cell_h = f"Номер детали {row[7].strip()}" + " " if row[7].strip() else ""
    cell_f = f"ОЕМ {row[5].strip()}" + " " if row[5].strip() else ""
    cell_d = f"Крос номер {row[3].strip()}" + " " if row[3].strip() else ""
    cell_ac = f"Состояние {row[28].strip()}" + " " if row[28].strip() else ""
    cell_g = f"На детали указано {row[6].strip()}" + " " if row[6].strip() else ""
    cell_am = f"(код {row[38].strip().replace('_', '')})" + " " if row[38].strip() else ""

    # разные тексты для "Б/у" и "Новое"
    if row[1] == "Б/у":
        if rule1_1:
            text = f"{cell_c}{cell_b}{cell_v}{cell_w}{cell_x}{cell_u}{cell_j}{cell_p}{cell_q}{cell_r}{cell_ae}" \
                   f"{cell_h}{cell_f}{cell_d}{cell_ac}{cell_g}{cell_am}\n\n{HEADER_BEFORE_TEXTS}\n{TEXT_1}\n{TEXT_2}\n{TEXT_3}\n{TEXT_4}\n" \
                   f"{TEXT_8}\n{TEXT_5}\n{TEXT_7}"
        else:
            text = f"{cell_c}{cell_b}{cell_v}{cell_w}{cell_x}{cell_u}{cell_j}{cell_p}{cell_q}{cell_r}{cell_ae}" \
                   f"{cell_h}{cell_f}{cell_d}{cell_ac}{cell_g}{cell_am}\n\n{HEADER_BEFORE_TEXTS}\n{TEXT_1}\n{TEXT_2}\n{TEXT_3}\n{TEXT_4}\n{TEXT_5}\n" \
                   f"{TEXT_7}"
    # Новое
    else:
        if rule1_1:
            text = f"{cell_c}{cell_b}{cell_v}{cell_w}{cell_x}{cell_u}{cell_j}{cell_p}{cell_q}{cell_r}{cell_ae}" \
                   f"{cell_h}{cell_f}{cell_d}{cell_ac}{cell_g}{cell_am}\n\n{HEADER_BEFORE_TEXTS}\n{TEXT_2}\n{TEXT_3}\n{TEXT_4}"
        else:
            text = f"{cell_c}{cell_b}{cell_v}{cell_w}{cell_x}{cell_u}{cell_j}{cell_p}{cell_q}{cell_r}{cell_ae}" \
                   f"{cell_h}{cell_f}{cell_d}{cell_ac}{cell_g}{cell_am}\n\n{HEADER_BEFORE_TEXTS}\n{TEXT_2}\n{TEXT_3}\n{TEXT_4}"

    return text


def get_description_rule_2(row: List, mmg: List, rule2_1: bool = None) -> str:
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

    if mmg[0].strip() == "ALL" or mmg[0].strip() == "":
        cell_p = ""
    else:
        cell_p = f"На авто {mmg[0].strip()}" + " "

    if mmg[1].strip() == "ALL" or mmg[1].strip() == "":
        cell_q = ""
    else:
        cell_q = f"модель {mmg[1].strip()}" + " "

    if mmg[2].strip() == "ALL" or mmg[2].strip() == "":
        cell_r = ""
    else:
        cell_r = f"Поколение {mmg[2].strip()}" + " "

    cell_u = f"Тип кузова {row[18].strip()}" + " " if row[18].strip() else ""
    cell_ae = f"Доп инф {row[30].strip()}" + " " if row[30].strip() else ""
    cell_h = f"Номер детали {row[7].strip()}" + " " if row[7].strip() else ""
    cell_f = f"ОЕМ {row[5].strip()}" + " " if row[5].strip() else ""
    cell_d = f"Крос номер {row[3].strip()}" + " " if row[3].strip() else ""
    cell_ac = f"Состояние {row[28].strip()}" + " " if row[28].strip() else ""
    cell_g = f"На детали указано {row[6].strip()}" + " " if row[6].strip() else ""
    cell_i = f"цена указана за {row[8].strip()}" + " " if row[8].strip() else ""
    cell_am = f"(код {row[38].strip().replace('_', '')})" + " " if row[38].strip() else ""

    # разные тексты для "Б/у" и "Новое"
    if row[1] == "Б/у":
        if rule2_1:
            text = f"{cell_c}{cell_b}{cell_z}{cell_aa}{cell_ab}{cell_j}{cell_p}{cell_q}{cell_r}{cell_u}{cell_ae}{cell_h}{cell_f}{cell_d}" \
                   f"{cell_ac}{cell_g}{cell_i}{cell_am}\n\n{HEADER_BEFORE_TEXTS}\n{TEXT_12}\n{TEXT_1}\n{TEXT_2}\n{TEXT_3}\n{TEXT_4}\n{TEXT_5}\n{TEXT_7}"
        else:
            text = f"{cell_c}{cell_b}{cell_z}{cell_aa}{cell_ab}{cell_j}{cell_p}{cell_q}{cell_r}{cell_u}{cell_ae}{cell_h}{cell_f}{cell_d}" \
                   f"{cell_ac}{cell_g}{cell_i}{cell_am}\n\n{HEADER_BEFORE_TEXTS}\n{TEXT_1}\n{TEXT_2}\n{TEXT_3}\n{TEXT_4}\n{TEXT_5}\n{TEXT_7}"

    # Новое
    else:
        if rule2_1:
            text = f"{cell_c}{cell_b}{cell_z}{cell_aa}{cell_ab}{cell_j}{cell_p}{cell_q}{cell_r}{cell_u}{cell_ae}{cell_h}{cell_f}{cell_d}" \
                   f"{cell_ac}{cell_g}{cell_i}{cell_am}\n\n{HEADER_BEFORE_TEXTS}\n{TEXT_2}\n{TEXT_3}\n{TEXT_4}"
        else:
            text = f"{cell_c}{cell_b}{cell_z}{cell_aa}{cell_ab}{cell_j}{cell_p}{cell_q}{cell_r}{cell_u}{cell_ae}{cell_h}{cell_f}{cell_d}" \
                   f"{cell_ac}{cell_g}{cell_i}{cell_am}\n\n{HEADER_BEFORE_TEXTS}\n{TEXT_2}\n{TEXT_3}\n{TEXT_4}"

    return text


def get_description_rule_3(row: List, mmg: List, rule3_2: bool = None, rule3_3: bool = None, rule3_4: bool = None) -> str:
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

    if mmg[0].strip() == "ALL" or mmg[0].strip() == "":
        cell_p = ""
    else:
        cell_p = f"На авто {mmg[0].strip()}" + " "

    if mmg[1].strip() == "ALL" or mmg[1].strip() == "":
        cell_q = ""
    else:
        cell_q = f"модель {mmg[1].strip()}" + " "

    if mmg[2].strip() == "ALL" or mmg[2].strip() == "":
        cell_r = ""
    else:
        cell_r = f"Поколение {mmg[2].strip()}" + " "

    cell_ae = f"Доп инф {row[30].strip()}" + " " if row[30].strip() else ""
    cell_h = f"Номер детали {row[7].strip()}" + " " if row[7].strip() else ""
    cell_f = f"ОЕМ {row[5].strip()}" + " " if row[5].strip() else ""
    cell_d = f"Крос номер {row[3].strip()}" + " " if row[3].strip() else ""
    cell_ac = f"Состояние {row[28].strip()}" + " " if row[28].strip() else ""
    cell_g = f"На детали указано {row[6].strip()}" + " " if row[6].strip() else ""
    cell_am = f"(код {row[38].strip().replace('_', '')})" + " " if row[38].strip() else ""

    # разные тексты для "Б/у" и "Новое"
    if row[1] == "Б/у":
        if rule3_2:
            text = f"{cell_c}{cell_b}{cell_v}{cell_w}{cell_x}{cell_u}{cell_z}{cell_aa}{cell_ab}{cell_j}{cell_p}{cell_q}{cell_r}" \
                   f"{cell_ae}{cell_h}{cell_f}{cell_d}{cell_ac}{cell_g}{cell_am}\n\n{HEADER_BEFORE_TEXTS}\n{TEXT_11}\n{TEXT_1}\n{TEXT_2}\n{TEXT_3}\n{TEXT_4}\n{TEXT_5}\n" \
                   f"{TEXT_7}"
        elif rule3_3:
            text = f"{cell_c}{cell_b}{cell_v}{cell_w}{cell_x}{cell_u}{cell_z}{cell_aa}{cell_ab}{cell_j}{cell_p}{cell_q}{cell_r}" \
                   f"{cell_ae}{cell_h}{cell_f}{cell_d}{cell_ac}{cell_g}{cell_am}\n\n{HEADER_BEFORE_TEXTS}\n{TEXT_1}\n{TEXT_2}\n{TEXT_3}\n{TEXT_4}\n{TEXT_9}\n{TEXT_5}\n" \
                   f"{TEXT_7}"
        elif rule3_4:
            text = f"{cell_c}{cell_b}{cell_v}{cell_w}{cell_x}{cell_u}{cell_z}{cell_aa}{cell_ab}{cell_j}{cell_p}{cell_q}{cell_r}" \
                   f"{cell_ae}{cell_h}{cell_f}{cell_d}{cell_ac}{cell_g}{cell_am}\n\n{HEADER_BEFORE_TEXTS}\n{TEXT_1}\n{TEXT_2}\n{TEXT_3}\n{TEXT_4}\n{TEXT_9}\n{TEXT_5}\n" \
                   f"{TEXT_7}"
        else:
            text = f"{cell_c}{cell_b}{cell_v}{cell_w}{cell_x}{cell_u}{cell_z}{cell_aa}{cell_ab}{cell_j}{cell_p}{cell_q}{cell_r}" \
                   f"{cell_ae}{cell_h}{cell_f}{cell_d}{cell_ac}{cell_g}{cell_am}\n\n{HEADER_BEFORE_TEXTS}\n{TEXT_1}\n{TEXT_2}\n{TEXT_3}\n{TEXT_4}\n{TEXT_5}\n" \
                   f"{TEXT_7}"

    # Новое
    else:
        if rule3_2:
            text = f"{cell_c}{cell_b}{cell_v}{cell_w}{cell_x}{cell_u}{cell_z}{cell_aa}{cell_ab}{cell_j}{cell_p}{cell_q}{cell_r}" \
                   f"{cell_ae}{cell_h}{cell_f}{cell_d}{cell_ac}{cell_g}{cell_am}\n\n{HEADER_BEFORE_TEXTS}\n{TEXT_2}\n{TEXT_3}\n{TEXT_4}"
        elif rule3_3:
            text = f"{cell_c}{cell_b}{cell_v}{cell_w}{cell_x}{cell_u}{cell_z}{cell_aa}{cell_ab}{cell_j}{cell_p}{cell_q}{cell_r}" \
                   f"{cell_ae}{cell_h}{cell_f}{cell_d}{cell_ac}{cell_g}{cell_am}\n\n{HEADER_BEFORE_TEXTS}\n{TEXT_2}\n{TEXT_3}\n{TEXT_4}"
        else:
            text = f"{cell_c}{cell_b}{cell_v}{cell_w}{cell_x}{cell_u}{cell_z}{cell_aa}{cell_ab}{cell_j}{cell_p}{cell_q}{cell_r}" \
                   f"{cell_ae}{cell_h}{cell_f}{cell_d}{cell_ac}{cell_g}{cell_am}\n\n{HEADER_BEFORE_TEXTS}\n{TEXT_2}\n{TEXT_3}\n{TEXT_4}"

    return text


def get_description_drom(desc_avito: str) -> str:
    """Изменение описания Авито для дрома"""
    additional_text = "\n\nМы продаем именно тот товар который на фото, но цена может отличаться в зависимости от коплектации.\n\n" \
                      "Возможна отправка СДЕК, Энергия."

    if desc_avito:
        result = desc_avito.split("\n\n")[0] + additional_text
    else:
        return additional_text
    return result


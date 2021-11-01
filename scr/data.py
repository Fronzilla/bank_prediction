from typing import NoReturn

import pandas as pd
import streamlit as st

IS_NA = 'В .csv файле есть пропущенные значения'

# маппинг типов данных
df_types_mapping = {

    "Портфель": "object",
    "Возраст": "int64",
    "Пол": "object",
    "Регион выдачи паспорта": "object",
    "Регион регистрации (стандартизировано)": "object",
    "Город выдачи": "object",
    "Место работы": "object",
    "Должность": "object",
    "Тип займа": "object",
    "Дата договора стандартизированная": "object",
    "Сумма договора стандартизированная": "object",
    "Отношение осз к сумме договора": "object",
    "Возраст ИД": "object",
    "количество кредитов с просрочкой по бки": "int64",
    "odv": "int64",
    "HasEDO": "bool",
    "Город ФМЖ": "object",
    "Город регистрации": "object",
    "Статус": "object"
}


def load_data(session_state) -> NoReturn:
    st.subheader('Загрузка данных')
    st.write("""
    Загрузите 'csv' файл одним листом.
    Колонки должны идти в следующем порядке:
    
        'Портфель', 'Возраст', 'Пол', 'Регион выдачи паспорта',
        'Регион регистрации (стандартизировано)', 'Город выдачи',
        'Место работы', 'Должность', 'Тип займа',
        'Дата договора стандартизированная',
        'Сумма договора стандартизированная', 'Отношение осз к сумме договора',
        'Возраст ИД', 'количество кредитов с просрочкой по бки', 'odv',
        'HasEDO', 'Город ФМЖ', 'Город регистрации', 'Статус'
             
        """)
    error_columns = []

    data_file = st.file_uploader("Файл формата 'csv', ", type=['csv'])
    if data_file is not None:
        df_data = pd.read_csv(data_file, dtype=df_types_mapping)

        if df_data.isna().sum().sum():
            st.error(IS_NA)

        for i in list(df_data.columns):
            if i not in df_types_mapping.keys():
                error_columns.append(i)

        if error_columns:
            st.error(f"Название {error_columns} колонок не соответствует шаблону")
            return

        if not list(df_types_mapping.keys()) == list(df_data.columns):
            st.error(f"Порядок колонок не соответствует шаблону")
            return

        st.write(df_data.head(5))
        session_state.df_data = df_data

import streamlit as st
import pandas as pd

import scr.session_state as session
from scr.data import load_data
from scr.download import csv_download_link
from scr.model import load_model

st.set_page_config(page_title='Domain classification', layout='wide')
SECRET = 'KobanBanan'


def main():
    st.sidebar.header(""" Введите секретную фразу """)
    pwd = st.sidebar.text_input("Password:", value="", type="password")

    if pwd and pwd != SECRET:
        st.error('Ошибка аутентификации')

    if pwd == SECRET:

        session_state = session.get(df_data=None, domain_column=None, encoder=None, model=None)
        st.header(""" Сервис классификации банков""")

        st.sidebar.subheader('FAQ')

        with st.sidebar.beta_expander('Как использовать?'):
            st.write("""
                    1. Загрузить .csv файл:
                    2. Скачать .csv файл с результатами классификации
            """)

        with st.sidebar.beta_expander('Какие колонки должны быть в .csv файле '):
            st.write(""" 
            
            .csv файл должен содержать следующие данные для каждого банка 
            
                        {'Портфель', 'Возраст', 'Пол', 'Регион выдачи паспорта',
                        'Регион регистрации (стандартизировано)', 'Город выдачи',
                        'Место работы', 'Должность', 'Тип займа',
                        'Дата договора стандартизированная',
                        'Сумма договора стандартизированная', 'Отношение осз к сумме договора',
                        'Возраст ИД', 'количество кредитов с просрочкой по бки', 'odv',
                        'HasEDO', 'Город ФМЖ', 'Город регистрации', 'Статус'}
            
            """)

        with st.sidebar.beta_expander('Какие банки классифицируются?'):
            st.write(""" 
    
            Классификатор умеет работать со следующими банками
    
                        (0004) Азиатско-Тихоокеанский Банк (ПАО)	
                        (0117) АО Банк Русский Стандарт	
                        (0227) АО Райффайзенбанк	
                        (0275) АО ЮниКредит Банк	
                        (0414) КБ Ренессанс Кредит (ООО)	
                        (0434) КИВИ Банк (АО)
                        (0706) ПАО Банк Санкт-Петербург
                        (0729) ПАО КБ УБРиР	
                        (0737) ПАО МОСКОВСКИЙ КРЕДИТНЫЙ БАНК	
                        (0748) ПАО Промсвязьбанк
            """)

        with st.sidebar.beta_expander('Пример входных данных?'):
            st.write(f"{csv_download_link(pd.read_csv('model/test.csv'), name='bank_example')}")

        with st.spinner('Загрузка метаданных...'):
            load_data(session_state)  # загрузка данных в сессию
            load_model(session_state)  # загрузка модели в сессию

        if session_state.df_data is not None:
            df = session_state.df_data

            with st.spinner('Классификация банков...'):
                try:
                    result = pd.DataFrame(session_state.model.predict_proba(df), columns=session_state.model.classes_)
                except Exception as e:
                    st.write(f'Ошибка классификации банков, проверьте входные данные: {e}')

            # res = pd.concat([df, result], axis=1)
            st.write(result.head(10))

            st.write('Ссылка на скачивание')
            csv_download_link(result)


if __name__ == '__main__':
    main()

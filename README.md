# Косатка-Analytics: Холодный старт

Демо: http://51.250.29.17:8000/rutube-recommendations/

✨ Косатка-Analytics: Холодный старт - Горячие результаты для новых пользователей RUTUBE 🎬  

Каждый новый пользователь RUTUBE сталкивается с огромным количеством видео. В этом многообразии контента важно с самого начала предлагать именно то, что зацепит и удержит внимание. Наша команда Косатка-Analytics решает одну из ключевых проблем платформы – холодный старт – с помощью передовых технологий машинного обучения.

# Гибридный подход: FAISS + SVD

### 🚀 FAISS – Быстрый поиск по эмбеддингам
FAISS (Facebook AI Similarity Search) используется для поиска схожих видео на основе их эмбеддингов. Эмбеддинги представляют собой числовые векторы, которые описывают видео (например, его описание, категорию и другие характеристики). Для создания эмбеддингов используется модель RuBERT-tiny2, которая показала наилучшие результаты в кодировании русскоязычного контента.

#### Процесс: 
> FAISS находит 50 схожих видео для каждого пользователя на основе эмбеддингов, закодированных RuBERT-tiny2.

### 📊 SVD – Коллаборативная фильтрация
После выбора 50 видео с помощью FAISS, используется SVD (Singular Value Decomposition) для предсказания того, насколько эти видео понравятся пользователю, основываясь на его истории просмотров.

#### Ключевой момент:
> Модель SVD обучена на истории просмотров пользователей платформы, что позволяет учитывать их индивидуальные предпочтения и взаимодействия с контентом.

#### Процесс:
> Для каждого из 50 видео SVD предсказывает вероятность того, что это видео понравится пользователю, на основе его предыдущего поведения.
Видео получают рейтинг, который отражает вероятность положительной реакции пользователя.

### 🤝 FAISS + SVD - Гибридный подход
#### Таким образом, система использует:
- FAISS для поиска 50 наиболее схожих видео на основе контентных характеристик, закодированных RuBERT-tiny2.
- SVD, обученную на истории просмотров пользователей платформы, для предсказания рейтинга этих видео.
- Из этих 50 видео выбираются 10 лучших, которые предлагаются пользователю, исходя из их рейтинга.

# Описание работы приложения
1. Изначально пользователю показывается 10 видео
2. Пользователь выбирает понравившееся видео на просмотр
3. Под ним сразу подгружается 10 видео, которые похожи на выбранное видео
4. Дальше у пользователя 2 варианта:
   - Поставить лайк/дизлайк выбранному видео - тогда выдача внизу обновится с соответствии с реакцией
   - Ничего не ставить и просто выбрать одно из видео ниже - в таком случае мы это засчитываем как "пропуск/игнор", новое видео становится выбранным, выдача внизу обновляется и показывает похожие видео
 
# Описание файловой структуры
- [Обучение моделей.ipynb](https://github.com/yuliya-karimova/rutube-recommendations/blob/main/%D0%9E%D0%B1%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%BC%D0%BE%D0%B4%D0%B5%D0%BB%D0%B5%D0%B9.ipynb) - ноутбук с процессом индексирования FAISS и обучение модели SVD, также в ноутбуке представлена работа по очистке датасета и подробные комментарии процесса работы, показано создание эмбедингов для текста
- [frontend](https://github.com/yuliya-karimova/rutube-recommendations/tree/main/frontend) - содержит код фронтовой части приложения, проект написан на Vue + Pinia
- [backend](https://github.com/yuliya-karimova/rutube-recommendations/tree/main/backend) - содержит код сервера, а также алгоритмов рекомендации, подробнее ниже

### Подробнее о бэкенде и алгоритмах: 
- [backend/app](https://github.com/yuliya-karimova/rutube-recommendations/blob/main/backend/app.py) - отвечает за запуск сервера и обработку запросов
- [backend/pop_video](https://github.com/yuliya-karimova/rutube-recommendations/tree/main/backend/pop_video) - подборки топ видео из каждой категории
- [backend/modules/video](https://github.com/yuliya-karimova/rutube-recommendations/blob/main/backend/modules/video.py) - содержит алгоритмы поиска видео:
    - **get_top_videos** - получение топа видео (по одному из каждой категории) для первой выдачи
    - **get_related_videos** - получение списка видео, похожих на выбранное
    - **get_recommended_videos** - получение списка видео в зависимости от реакции пользователя на видео - лайк, дизлайк или игнор (когда юзер просто листает на следующее)

Также в папке backend предполагаются следующие 3 файла, но они слишком большие для гитхаба, поэтому залиты на яндекс диск:
- [df_indexed.pkl](https://disk.yandex.ru/d/FRFrLfUG2z-jJg) - датафрейм с информацией о видео
- [faiss_index.bin](https://disk.yandex.ru/d/M0H0a4ClihTjJQ) - FAISS индекс
- [svd_model.pkl](https://disk.yandex.ru/d/KuG5zhTDrJv6JA) -  обученная модель SVD



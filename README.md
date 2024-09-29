# Косатка-Analytics: Холодный старт

Демо: http://51.250.29.17:8000/rutube-recommendations/

✨ Косатка-Analytics: Холодный старт - Горячие результаты для новых пользователей RUTUBE 🎬
Каждый новый пользователь RUTUBE сталкивается с огромным количеством видео. В этом многообразии контента важно с самого начала предлагать именно то, что зацепит и удержит внимание. Наша команда Косатка-Analytics решает одну из ключевых проблем платформы – холодный старт – с помощью передовых технологий машинного обучения.

🚀 FAISS – Молниеносный кластерный анализ по эмбеддингам для поиска наиболее релевантных видео.  Для создания этих эмбеддингов мы используем модель RuBERT-tiny2, специально оптимизированную для работы с русскоязычным контентом.

📊 SVD – Коллаборативная фильтрация для точных рекомендаций После выбора контентно-похожих видео с помощью FAISS, наша система использует SVD (Singular Value Decomposition), чтобы предсказать, насколько видео понравится пользователю. Модель обучена на данных о взаимодействии пользователей с платформой и учитывает их поведенческие паттерны.

🤝 Гибридный подход: FAISS + SVD

FAISS: Поиск 50 наиболее похожих видео по контентным характеристикам.
SVD: Предсказание вероятности того, что видео понравится, на основе истории взаимодействий.
🎯 Решение проблемы "холодного старта" Наш алгоритм создан для того, чтобы мгновенно определять предпочтения новых пользователей, предлагать им релевантный контент и улучшать их опыт на платформе. Косатка-Analytics разработала систему, которая быстро учится на нескольких реакциях пользователя и начинает предлагать именно то, что будет интересно.

📱 Итоговый продукт представлен в виде веб-приложения, где каждый пользователь может получать персонализированные рекомендации, а система будет обновляться на основе обратной связи.

## Описание работы приложения
1. Изначально пользователю показывается 10 видео
2. Пользователь выбирает понравившееся видео на просмотр
3. Под ним сразу подгружается 10 видео, которые похожи на выбранное видео
4. Дальше у пользователя 2 варианта:
   - Поставить лайк/дизлайк выбранному видео - тогда выдача внизу обновится с соответствии с реакцией
   - Ничего не ставить и просто выбрать одно из видео ниже - в таком случае мы это засчитываем как "пропуск/игнор", новое видео становится выбранным, выдача внизу обновляется и показывает похожие видео
 
## Описание файловой структуры
- frontend - содержит код фронтовой части приложения, проект написан на Vue + Pinia
- backend - содержит код сервера, а также алгоритмов рекомендации, подробнее ниже.

### Подробнее о бэкенде и алгоритмах: 
- файл app - отвечает за запуск сервера и обработку запросов
- pop_video - подборки топ видео из каждой категории
- modules/video - содержит алгоритмы поиска видео:
    - get_top_videos - получение топа видео (по одному из каждой категории) для первой выдачи
    - get_related_videos - получение списка видео, похожих на выбранное
    - get_recommended_videos - получение списка видео в зависимости от реакции пользователя на видео - лайк, дизлайк или игнор (когда юзер просто листает на следующее)

Также в папке backend предполагаются следующие 3 файла, но они слишком большие для гитхаба, поэтому залиты на яндекс диск:
- [df_indexed.pkl](https://disk.yandex.ru/d/FRFrLfUG2z-jJg) - изначальный датафрейм с информацией о видео - НАПИСАТЬ ОПИСАНИЕ И ДОБАВИТЬ ССЫЛКУ
- [faiss_index.bin](https://disk.yandex.ru/d/M0H0a4ClihTjJQ) - FAISS индекс - НАПИСАТЬ ОПИСАНИЕ И ДОБАВИТЬ ССЫЛКУ
- [svd_model.pkl](https://disk.yandex.ru/d/KuG5zhTDrJv6JA) -  обученная модели SVD - НАПИСАТЬ ОПИСАНИЕ И ДОБАВИТЬ ССЫЛКУ



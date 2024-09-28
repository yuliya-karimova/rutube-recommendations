import pandas as pd
import random
import numpy as np
import faiss
import pandas as pd
from surprise import Dataset, Reader, SVD
from sklearn.metrics import f1_score
from tqdm import tqdm
import joblib
import csv






# ЗАГРУЗКА МОДЕЛЕЙ

# Загрузка сохраненного DataFrame и FAISS индекса
df = pd.read_pickle('df_indexed.pkl')
index = faiss.read_index('faiss_index.bin')
# Создание массива эмбеддингов из загруженного DataFrame
df['combined_embeddings'] = df.apply(
    lambda row: np.hstack((row['title_embeddings'], row['description_embeddings'])),
    axis=1
)
video_embeddings = np.vstack(df['combined_embeddings'].values).astype('float32')
# Загрузка обученной модели SVD
svd_model = joblib.load('svd_model.pkl')












# ТОП ВИДЕО

# Функция для выбора случайного видео из каждой категории
def get_random_videos_by_category():
    categories = [
        'Разное', 'Сериалы', 'Телепередачи', 'Видеоигры', 'Музыка', 
        'Развлечения', 'Фильмы', 'Лайфстайл', 'Детям', 'Обучение'
    ]
    
    results = []

    for category_name in categories:
        # Открываем CSV-файл для каждой категории
        try:
            df_category = pd.read_csv(f'pop_video/top_20_videos_{category_name}.csv')
        except FileNotFoundError:
            print(f"Файл для категории {category_name} не найден.")
            continue

        # Выбираем случайное видео из категории
        random_row = df_category.sample(1).iloc[0]
        
        # Преобразуем данные в требуемый формат
        video_data = {
            "video_id": random_row["video_id"],
            "title": random_row["title"],
            "description": random_row["description"] if pd.notnull(random_row["description"]) else "",
            "category_id": random_row["category_id"],
            "v_pub_datetime": pd.to_datetime(random_row["v_pub_datetime"]).isoformat(),
            "v_total_comments": int(random_row["v_total_comments"]),
            "v_year_views": int(random_row["v_year_views"]),
            "v_likes": int(random_row["v_likes"]),
            "v_dislikes": int(random_row["v_dislikes"]),
            "v_duration": int(random_row["v_duration"]),
            "author_id": random_row["author_id"]
        }
        
        results.append(video_data)
            
    return results

def get_top_videos():
    return get_random_videos_by_category()











# RELATED VIDEO (ПОХОЖИЕ ВИДЕО)

def get_related_videos(video_id, top_k=10):
    # Проверка, существует ли видео в DataFrame
    if video_id not in df['video_id'].values:
        raise ValueError(f"Video ID '{video_id}' не найдено в DataFrame")
    
    # Получаем индекс данного видео в DataFrame
    video_idx = df[df['video_id'] == video_id].index[0]
    
    # Эмбеддинг данного видео
    query_vector = video_embeddings[video_idx].reshape(1, -1)
    
    # Поиск ближайших соседей (находим top_k * 2, чтобы выполнить фильтрацию)
    distances, indices = index.search(query_vector, top_k * 2 + 1)
    
    # Исключаем само видео
    indices = indices[0][1:]
    distances = distances[0][1:]
    
    # Получаем видео, соответствующие найденным индексам
    recommended_videos = df.iloc[indices]
    
    # Фильтрация по количеству просмотров за год
    filtered_videos = recommended_videos[recommended_videos['v_year_views'] >= 500]
    
    # Ограничиваем список до top_k после фильтрации
    filtered_videos = filtered_videos.head(top_k)
    
    # Оценка каждого видео с помощью SVD модели
    results = []
    for i, row in filtered_videos.iterrows():
        # Используем модель SVD для предсказания реакции пользователя на каждое видео
        prediction = svd_model.predict(uid='current_user_id', iid=row['video_id'])
        
        video_data = {
            "video_id": row["video_id"],
            "title": row["title"],
            "description": row["description"],
            "category_id": row["category_id"],
            "v_pub_datetime": row["v_pub_datetime"].isoformat(),
            "v_total_comments": row["v_total_comments"],
            "v_year_views": row["v_year_views"],
            "v_likes": row["v_likes"],
            "v_dislikes": row["v_dislikes"],
            "v_duration": row["v_duration"],
            "author_id": row["author_id"],
            "svd_score": prediction.est  # Оценка от модели SVD
        }
        results.append(video_data)
    
    # Сортируем по svd_score и выбираем топ-10
    sorted_results = sorted(results, key=lambda x: x['svd_score'], reverse=True)[:top_k]
    
    return sorted_results










# РЕКОМЕНДУЕМЫЕ ВИДЕО

# Функция для поиска похожих видео и записи информации с учетом реакций
# Функция для поиска похожих видео и оценки их с помощью SVD
def recommend_videos_with_svd(
    user_id, video_id, df, index, model, top_k=10, reaction=1, 
    log_file='user_reaction.csv', recommendations_file='user_recommendations.csv', max_neighbors=1000
):
    # Логирование реакции
    with open(log_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([user_id, video_id, reaction])  # Сохраняем переданную реакцию
    
    # Проверка, существует ли видео в DataFrame
    if video_id not in df['video_id'].values:
        raise ValueError(f"Video ID '{video_id}' не найдено в DataFrame")
    
    # Чтение всех реакций пользователя из файла логов
    log_data = pd.read_csv(log_file, names=['user_id', 'video_id', 'reaction'])
    log_data['reaction'] = log_data['reaction'].astype(int)  # Убедимся, что реакции - целые числа
    user_logs = log_data[log_data['user_id'] == user_id]
    
    # Чтение предыдущих рекомендаций из файла
    try:
        rec_data = pd.read_csv(recommendations_file, names=['user_id', 'input_video_id', 'recommended_video_ids'])
    except FileNotFoundError:
        # Если файла нет, создаём пустой DataFrame
        rec_data = pd.DataFrame(columns=['user_id', 'input_video_id', 'recommended_video_ids'])

    # Получаем множество видео, уже рекомендованных пользователю
    user_rec_logs = rec_data[rec_data['user_id'] == user_id]
    recommended_video_ids_set = set()
    for idx, row in user_rec_logs.iterrows():
        rec_video_ids = str(row['recommended_video_ids']).split(';')
        recommended_video_ids_set.update(rec_video_ids)
    # Удаляем пустые строки из множества
    recommended_video_ids_set.discard('')
    
    if user_logs.empty:
        # Если у пользователя нет истории взаимодействий
        print("У пользователя нет истории взаимодействий. Возвращаем популярные видео.")
        # Здесь можно вернуть популярные видео или обработать этот случай иначе
        return [], user_logs[['video_id', 'reaction']]
    else:
        # Инициализируем массив для накопления счетов для каждого видео
        cumulative_scores = np.zeros(len(df))
        
        # Получаем список индексов видео, с которыми взаимодействовал пользователь
        user_history_indices = []
        for idx, row in user_logs.iterrows():
            vid = row['video_id']
            reaction = int(row['reaction'])  # Убедимся, что реакция - целое число
            if vid in df['video_id'].values:
                vid_idx = df[df['video_id'] == vid].index[0]
                user_history_indices.append((vid_idx, reaction))
            else:
                # Видео не найдено в df
                continue
        
        # Проверяем, что у нас есть история взаимодействий
        if not user_history_indices:
            print("Не удалось найти эмбеддинги для видео пользователя. Возвращаем популярные видео.")
            return [], user_logs[['video_id', 'reaction']]
        
        # Задаём максимальное количество соседей для ускорения вычислений
        max_neighbors = 1000
        
        # Проходим по каждому видео из истории пользователя
        for vid_idx, reaction in user_history_indices:
            # Пропускаем видео с реакцией 1 (нет реакции)
            if reaction == 1:
                continue
            
            # Эмбеддинг текущего видео из истории пользователя
            user_video_embedding = video_embeddings[vid_idx].reshape(1, -1)
            
            # Вычисляем сходства с top-N ближайшими видео
            distances, indices = index.search(user_video_embedding, max_neighbors)
            
            # Сходства для выбранных видео
            similarities = distances[0]
            video_indices = indices[0]
            
            # Применяем вес в зависимости от реакции
            if reaction == 2:
                weight = 1  # Лайк, добавляем сходства
                
            elif reaction == 0:
                weight = -1  # Дизлайк, вычитаем сходства
    
            else:
                # Неизвестная реакция, пропускаем
                continue
            
            # Накопление счетов
            cumulative_scores[video_indices] += weight * similarities
        
        # Исключаем видео, с которыми пользователь уже взаимодействовал
        user_history_video_ids = set(user_logs['video_id'])
        user_history_indices_set = set([df[df['video_id'] == vid].index[0] for vid in user_history_video_ids if vid in df['video_id'].values])
        
        # Исключаем видео, которые уже были рекомендованы ранее
        recommended_video_indices_set = set([df[df['video_id'] == vid].index[0] for vid in recommended_video_ids_set if vid in df['video_id'].values])
        
        # Создаем DataFrame с результатами
        results_df = df.copy()
        results_df['score'] = cumulative_scores
        
        # Исключаем видео из истории пользователя и ранее рекомендованные видео
        exclude_indices = user_history_indices_set.union(recommended_video_indices_set)
        results_df = results_df.drop(index=exclude_indices)
        
        # Удаляем видео с нулевым счетом
        results_df = results_df[results_df['score'] != 0]
        
        # Сортируем результаты по накопленным счетам
        results_df = results_df.sort_values(by='score', ascending=False)
        
        # Фильтрация по количеству просмотров за год (если необходимо)
        results_df = results_df[results_df['v_year_views'] >= 500]
        
        # Ограничиваем список до top_N (например, 50) для дальнейшей оценки
        initial_top_N = 50
        initial_recommendations = results_df.head(initial_top_N)
        print(initial_recommendations)
        
        # Оценка каждого видео с помощью модели SVD
        results = []
        for i, row in initial_recommendations.iterrows():
            # Используем модель SVD для предсказания оценки пользователя на каждое видео
            prediction = model.predict(uid=user_id, iid=row['video_id'])
            
            video_data = {
                "video_id": row["video_id"],
                "title": row["title"],
                "description": row["description"],
                "category_id": row["category_id"],
                "v_pub_datetime": row["v_pub_datetime"].isoformat() if pd.notnull(row["v_pub_datetime"]) else None,
                "v_total_comments": row["v_total_comments"],
                "v_year_views": row["v_year_views"],
                "v_likes": row["v_likes"],
                "v_dislikes": row["v_dislikes"],
                "v_duration": row["v_duration"],
                "author_id": row["author_id"],
                "score": row["score"],
                "svd_score": prediction.est  # Оценка от модели SVD
            }
            results.append(video_data)
        
        # Сортируем результаты по svd_score и выбираем топ_k
        sorted_results = sorted(results, key=lambda x: x['svd_score'], reverse=True)[:top_k]
        
        # Сохраняем рекомендованные видео в файл рекомендаций
        recommended_video_ids = [video['video_id'] for video in sorted_results]
        with open(recommendations_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([user_id, video_id, ';'.join(recommended_video_ids)])
        
        return sorted_results

def get_recommended_videos(video_id, reaction, user_id):
    return recommend_videos_with_svd(user_id, video_id, df, index, svd_model, 10, reaction)

import redis
import json
import os
import uuid
from django.utils import timezone
from django.conf import settings

class RedisClient:
   
    def __init__(self, host=None, port=6379, db=0):
        """Подключение к Redis"""
        self.client = redis.StrictRedis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=settings.REDIS_DECODE_RESPONSES
        )


    def save_progress(self, user_id, template_name, file_path, max_history=50):
        """Сохраняем каждую запись с TTL = 1 день"""
        #уникальный ключ для записи
        record_id = str(uuid.uuid4())
        record_key = f"user_progress_item:{user_id}:{record_id}"
        
        data = {
            "template_name": template_name,
            "file": file_path,
            "date": timezone.now().strftime("%d-%m-%Y")
        }

        #1 день
        self.client.set(record_key, json.dumps(data), ex=86400)
        
        history_key = f"user_progress_history:{user_id}"
        pipe = self.client.pipeline()
        pipe.lpush(history_key, record_key)
        pipe.ltrim(history_key, 0, max_history - 1)
        pipe.execute()

    def load_progress(self, user_id, limit=10):
        """Загружаем последние limit записей, пропуская истекшие"""
        history_key = f"user_progress_history:{user_id}"
        record_keys = self.client.lrange(history_key, 0, limit - 1)
        if not record_keys:
            return []

        # MGET для ускорения
        records = self.client.mget(record_keys)
        result = []
        for rec in records:
            if rec: 
                result.append(json.loads(rec))
        return result
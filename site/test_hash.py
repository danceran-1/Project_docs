import bcrypt

# Генерируем новый хеш для "123"
new_hash = bcrypt.hashpw("Iuser".encode('utf-8'), bcrypt.gensalt())
print("Новый хеш:", new_hash.decode())  # Для вставки в БД
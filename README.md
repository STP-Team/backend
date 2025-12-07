# Структура проекта

- core - Инициализация, конфигурация и зависимости
- api - Роуты
- schemas - Схемы (модели) для роутов

# Переменные окружения

<table class="tg"><thead>
  <tr>
    <th class="tg-0pky">Переменная</th>
    <th class="tg-0pky">Значение</th>
  </tr></thead>
<tbody>
  <tr>
    <td class="tg-0lax">API_PORT</td>
    <td class="tg-0lax">Порт сервера API</td>
  </tr>
  <tr>
    <td class="tg-0pky">DB_HOST</td>
    <td class="tg-0pky">Адрес сервера базы данных</td>
  </tr>
  <tr>
    <td class="tg-0lax">DB_PORT</td>
    <td class="tg-0lax">Порт сервера базы данных</td>
  </tr>
  <tr>
    <td class="tg-0pky">DB_USER</td>
    <td class="tg-0pky">Пользователь базы данных</td>
  </tr>
  <tr>
    <td class="tg-0pky">DB_PASS</td>
    <td class="tg-0pky">Пароль пользователя базы данных</td>
  </tr>
  <tr>
    <td class="tg-0lax">DB_NAME</td>
    <td class="tg-0lax">Название базы данных</td>
  </tr>
</tbody>
</table>

# Генерация ключей

Приватный ключ

```bash
openssl genpkey -algorithm Ed25519 -out app/certs/private_key.pem
```

Публичный ключ:

```bash
openssl pkey -in app/certs/jwt_private.pem -pubout -out app/certs/jwt_public.pem
```

Ключи не должны быть в репозитории и хранятся в едином экземпляре на машине, где запускается backend
Простий валідатор http, socks4/5 проксі. У додатку наявна можливість автоматичного уникання заборонених підмереж (AWS, Google і т.п.), що буде корисно для розгортання на хмарних серверах.
Версія додатку розрахована для домашнього використання в дослідницьких цілях.

Аргументи запуску:
-p, --proxies - шлях до файлу зі списком проксі адрес для завантаження (за замовчуванням data/proxies.txt)
-j, --judge - шлях до файлу зі списком адрес суддів проксі (за замовчуванням data/judge.txt)
-e, --exclude - шлях до файлу зі списком адрес для завантаження підмереж, проксі з яких ігноруватимуться (за замовчуванням data/exclude.txt)
-o, --output - шлях до файлу для складання проксі, що пройшли перевірку (може бути створений автоматично)
-t, --threads - кількість паралельних потоків тестування
-r, --reload - перерва між спробами завантаження списків проксі з зовнішніх ресурсів у секундах (за замовчуванням 15 хвилин)
-w, --werbouse - додаток буде показувати результат роботи для кожної адреси та усі дрібні поточні помилки, навантажує систему

Формат подання даних:
1. Файл зі списком адрес проксі (-p) для завантаження має бути сформований у форматі "URL,METHOD" (Наприклад: http://proxy.list/http.txt,http), самі дані, які надає ресурс мають бути у вигляді порядкового списку у форматі "IP:PORT". Працювати з проксі з авторизацією додаток не вміє, парсити більш складні спсики теж.
2. Файл зі списком суддів (-j) має бути порядковим списком з URL-адрес. Кожна адреса початково перевіряється, якщо суддя не доступний, він не буде використовуватися в процесі роботи.
3. Файл зі списком адрес для завантаження заборонених підмереж (-e) має бути порядковим списком з URL-адрес. Самі дані для завантаження мають подаватися у форматі "IP/MASK". Прикладом ресурсу, що надає надійні дані про мережі хмарних сервісів у відповідному форматі є "https://github.com/lord-alfred/ipranges".
4. Проксі, що пройшли перевірку, зберігаються в форматі "METHOD://IP:PORT".
5. У всіх файлах можна використовувати символ "#" на початку рядка для створення коментарів
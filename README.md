# Paylin
CLI-инструмент для поиска поставщиков на Made-in-China с AI-анализом релевантности.

`Paylin` умеет:
- искать компании по ключевому слову;
- собирать подробную информацию о компании;
- экспортировать результаты в CSV;
- анализировать компании через LLM;
- автоматически оценивать релевантность поставщиков для импорта.

## Возможности
- Поиск компаний на Made-in-China
- Detailed scraping профилей компаний
- Поддержка HTTP / HTTPS / SOCKS5 proxy
- Параллельный сбор данных
- AI scoring и фильтрация
- Экспорт в CSV
- Separate filtered CSV по minimum score

# Установка
Проект использует [uv](https://github.com/astral-sh/uv).

## 1. Установите uv
### Linux / macOS
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```
### Windows
```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
## 2. Клонируйте проект
```
git clone https://github.com/rillazz/paylin-cli.git
cd paylin-cli
```
## 3. Установите зависимости
```
uv sync
```
# Запуск
```
uv run -m paylin.cli <ключевое слово> <ОКВЭД> <API токен DeepSeek>
```
# AI-анализ
После сбора компаний Paylin отправляет их в DeepSeek API и добавляет поля:

| Поле             | Описание                              |
| ---------------- | ------------------------------------- |
| relevance_score  | Оценка релевантности (1-10)           |
| relevance_reason | Почему компания получила эту оценку   |
| import_potential | import potential: high / medium / low |
| flag             | Причина сомнения (может быть null)    |

# Фильтрация по min_score
Опция `--min-score` позволяет автоматически отфильтровать компании по AI score.

- полный CSV будет содержать все компании;
- filtered CSV будет содержать только компании с `relevance_score >= 8`.

Это удобно для быстрого отбора лучших поставщиков.

# Основные опции
Для полуения всех допустимых значений и общей помощи по инструменту:
```
uv run -m paylin.cli --help
```

| Опция             | Описание                         |
| ----------------- | -------------------------------- |
| `--query`         | Поисковый запрос                 |
| `--okved`         | Код ОКВЭД                        |
| `--api-key`       | API ключ DeepSeek                |
| `--proxy`         | HTTP/HTTPS/SOCKS proxy           |
| `--province`      | Провинция Китая                  |
| `--business-type` | Тип бизнеса                      |
| `--certification` | Сертификация                     |
| `--category`      | Категория                        |
| `--revenue`       | Revenue filter                   |
| `--employees`     | Размер компании                  |
| `--min-score`     | Минимальный AI score             |
| `--limit`         | Максимальное количество компаний |
| `--output-dir`    | Директория для сохранения CSV    |

# Detailed parsing
Paylin собирает:
- описание компании;
- адрес;
- размер предприятия;
- количество работников;
- OEM / ODM support;
- экспортную информацию;
- сертификаты;
- производственные возможности;
- торговые возможности;
- R&D данные;
- и многое другое.

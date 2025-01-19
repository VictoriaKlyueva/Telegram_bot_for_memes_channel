# Общая задумка
Создать тг бота для генерации мема с фото кота и текстом и отправки его в тг канал по сообщению от пользователя

## Пайплайн
1. Пользователь пишет сообщение боту
2. Генерируется фото кота (безусловная генерация)
3. Генерируется текст (промпт берется из заранее заданного списка промптов)
4. Выбирается шрифт, текст накладывается на фото
5. Бот отправляет полученную картинку в тг канал с сообщением пользователя или без сообщения, если пользователь ввел "Мем"

# Ноутбуки с обучением:
1. [Текстовая моделька](https://colab.research.google.com/drive/1i6B6yzJtCokjFKQU89B3yicZcuDcKeDa?usp=sharing)
2. [Обучение диффузионки](https://colab.research.google.com/drive/1mq-WdiPeW-NgMZCzzzb97CvfAMwM4Wn1) и [сама моделька](https://drive.google.com/drive/folders/1_nQRtehUKjdYto8APpmaEAZv0PvMipdy?usp=sharing)
3. [Классификация котеек для отбора генераций диффузионной модели](https://colab.research.google.com/drive/1PQCtzCpJ5OQYBGyS9WoYfXCC8jYSykwl)

# Данные:
1. [Датасет с мемными котиками](https://www.kaggle.com/datasets/vekosek/cats-from-memes) (сама собирала!)
2. [Датасет с мемными фразочками](https://drive.google.com/file/d/1mkrV1Ull45YXchKemoJzriMazVxcu8z-/view?usp=drive_link)

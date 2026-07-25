from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from PIL import Image
import io

from функция_предсказания import predict_image_class

app = FastAPI(title="ЭКО Сканер API")

# Чтобы HTML мог обращаться к API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Описание категорий
RESULTS = {
    "plastic": {
        "type": "Пластик",
        "badge": "♻️ перерабатывается",
        "description": "На фото изображён пластиковый мусор. Его можно сдавать в контейнеры для пластика."
    },

    "paper": {
        "type": "Бумага",
        "badge": "📄 перерабатывается",
        "description": "На фото изображена бумага или картон. Их можно сдавать в макулатуру."
    },

    "glass": {
        "type": "Стекло",
        "badge": "🍾 перерабатывается",
        "description": "На фото изображено стекло. Его следует выбрасывать в контейнеры для стекла."
    },

    "metal": {
        "type": "Металл",
        "badge": "🥫 перерабатывается",
        "description": "На фото изображён металлический мусор. Его можно сдавать в пункты приёма металла."
    },

    "organic": {
        "type": "Органика",
        "badge": "🌱 компостируется",
        "description": "На фото изображены органические отходы. Они подходят для компостирования."
    }
}


@app.get("/")
def home():
    return {
        "message": "ЭКО Сканер API работает"
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:

        # читаем изображение
        image_bytes = await file.read()

        image = Image.open(io.BytesIO(image_bytes))

        # вызываем твою модель
        result = predict_image_class(image)

        if result not in RESULTS:
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Неизвестный класс",
                    "prediction": result
                }
            )

        return JSONResponse(RESULTS[result])

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e)
            }
        )
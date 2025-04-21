import keras.src
from api import bot
from log import check
from telebot import types
import numpy as np
from PIL import Image
import io
import tensorflow as tf
import keras


CLASS_NAMES = ["СО", "что-то другое"]
MODEL_PATH = "./AI/nlc_or_cloud/have_nlc.h5"


try:
    from tensorflow.keras.layers import DepthwiseConv2D
    original_init = DepthwiseConv2D.__init__
    
    def patched_init(self, *args, **kwargs):
        kwargs.pop('groups', None)  
        return original_init(self, *args, **kwargs)
    
    DepthwiseConv2D.__init__ = patched_init
except Exception as e:
    print(f"Внимание: Не удалось применить патч для DepthwiseConv2D: {str(e)}")


try:
    model = tf.keras.models.load_model(
        MODEL_PATH,
        compile=False,
        custom_objects={'DepthwiseConv2D': DepthwiseConv2D}
    )
    print(f"Модель успешно загружена. Входной размер: {model.input_shape}")
except Exception as e:
    print(f"Критическая ошибка загрузки модели: {str(e)}")
    exit()


def prepare_image(image_bytes, target_size):
    try:
        img = Image.open(io.BytesIO(image_bytes))
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img = img.resize(target_size)
        x = np.asarray(img)
        x = np.expand_dims(x, axis=0)
        return x / 255.0
    except Exception as e:
        print(f"Ошибка обработки изображения: {str(e)}")
        raise


def handle_photo(image_bytes):
    try:
        target_size = model.input_shape[1:3]  
        image = prepare_image(image_bytes, target_size)
        preds = model.predict(image, verbose=0)[0]
        result = [
            f"{name}: {prob*100:.1f}%"
            for name, prob in zip(CLASS_NAMES, preds)
        ]
        best_class = CLASS_NAMES[np.argmax(preds)]
        check(best_class == "СО", "AI")
        return best_class == "СО"
        
    except Exception as e:
        error_msg = f"❌ Ошибка обработки: {str(e)}"
        print(error_msg)
        return False
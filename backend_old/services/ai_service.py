# services/ai_service.py
import os
from transformers import ViTForImageClassification, ViTImageProcessor
import torch
from typing import Dict, Any
from PIL import Image
from config.settings import get_settings
from enum import Enum

settings = get_settings()

class Species(str, Enum):
    ALOE_VERA = "Aloe Vera"
    ARECA_PALM = "Areca Palm (Dypsis lutescens)"
    BEGONIA = "Begonia (Begonia spp.)"
    BOSTON_FERN = "Boston Fern (Nephrolepis exaltata)"
    CALATHEA = "Calathea"
    CHRYSANTHEMUM = "Chrysanthemum"
    MONEY_TREE = "Money Tree (Pachira aquatica)"
    MONSTERA_DELICIOSA = "Monstera Deliciosa (Monstera deliciosa)"
    ORCHID = "Orchid"
    RUBBER_PLANT = "Rubber Plant (Ficus elastica)"
    SCHEFFLERA = "Schefflera"
    ZZ_PLANT = "ZZ Plant (Zamioculcas zamiifolia)"

class AIService:
    def __init__(self):
        self.model = None
        self.feature_extractor = None
        # Путь к директории с моделью относительно корня проекта
        self.model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "plants_classification")
        
    def load_model(self):
        """Загрузка модели и токенизатора"""
        try:
            # Загружаем модель из локальной директории
            self.model = ViTForImageClassification.from_pretrained(self.model_path)
            self.feature_extractor = ViTImageProcessor.from_pretrained(
                'google/vit-base-patch16-224-in21k'
            )
            
            print(f"Модель успешно загружена из {self.model_path}")
            return True
        except Exception as e:
            print(f"Ошибка при загрузке модели: {str(e)}")
            return False
    
    def predict(self, image_path: str) -> Dict[str, Any]:
        """Получение предсказания от модели"""
        if not self.model or not self.feature_extractor:
            raise ValueError("Модель не загружена")
        
        image = Image.open(image_path)
        inputs = self.feature_extractor(images=image, return_tensors="pt")
        
        with torch.no_grad():
            outputs = self.model(**inputs)

        # Получение предсказаний
        logits = outputs.logits
        predicted_class_idx = logits.argmax(-1).item()
        
        # Получаем вероятности для всех классов
        probabilities = torch.nn.functional.softmax(logits, dim=-1)[0]
        
        # Создаем словарь с вероятностями для каждого класса
        class_probabilities = {}
        for idx, prob in enumerate(probabilities):
            class_name = self.model.config.id2label[idx]
            class_probabilities[class_name] = round(float(prob), 4)
        
        # Получаем название предсказанного класса и его вероятность
        predicted_class = self.model.config.id2label[predicted_class_idx]
        confidence = class_probabilities[predicted_class]
        if confidence < sum(class_probabilities.values()) * 0.5:
            predicted_class = "Not found"

        # Формируем результат
        result = {
            "predicted_class": predicted_class,
            "confidence": confidence,
            "probabilities": class_probabilities
        }
        
        return result

# Создаем синглтон для сервиса модели
ai_service = AIService()
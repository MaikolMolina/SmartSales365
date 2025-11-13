from django.core.management.base import BaseCommand
from backend.sales.models import SalesPrediction, TrainedModel
from backend.commercial.models import Venta
from datetime import datetime, timedelta
import random
import numpy as np
import joblib
from io import BytesIO
from sklearn.ensemble import RandomForestRegressor

class Command(BaseCommand):
    help = 'Crea datos de prueba para el módulo de IA y predicciones'

    def handle(self, *args, **options):
        self.stdout.write('Creando datos de IA y predicciones...')
        
        # 1. Crear un modelo pre-entrenado de ejemplo
        self.create_pretrained_model()
        
        # 2. Crear predicciones de ejemplo
        self.create_sample_predictions()
        
        self.stdout.write(
            self.style.SUCCESS('Datos de IA creados exitosamente!')
        )

    def create_pretrained_model(self):
        """Crea un modelo Random Forest pre-entrenado con datos de ejemplo"""
        
        # Verificar si ya existe un modelo entrenado
        if TrainedModel.objects.filter(model_name='sales_predictor').exists():
            self.stdout.write('Modelo ya existe, saltando creación...')
            return

        # Generar datos de ejemplo para entrenamiento
        np.random.seed(42)
        n_samples = 500
        
        # Características para el modelo
        X = np.column_stack([
            np.random.randint(1, 13, n_samples),  # month
            np.random.randint(1, 32, n_samples),  # day_of_month
            np.random.randint(0, 7, n_samples),   # day_of_week
            np.random.uniform(10, 500, n_samples), # price
            np.random.randint(1, 6, n_samples),   # category_id
            np.random.randint(1, 20, n_samples)   # total_quantity
        ])
        
        # Target (ventas) con relación no lineal
        y = (
            X[:, 0] * 100 +           # Mes tiene mayor impacto
            X[:, 1] * 10 +            # Día del mes
            X[:, 2] * 50 +            # Día de la semana
            X[:, 3] * X[:, 5] * 0.8 + # Precio * cantidad
            X[:, 4] * 200 +           # Categoría
            np.random.normal(0, 50, n_samples)  # Ruido
        )
        
        # Asegurar que no haya valores negativos
        y = np.maximum(y, 0)
        
        # Entrenar modelo Random Forest
        model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(X, y)
        
        # Evaluar el modelo
        y_pred = model.predict(X)
        accuracy = max(0, np.corrcoef(y, y_pred)[0, 1])  # Coeficiente de correlación como "precisión"
        
        # Serializar el modelo
        model_buffer = BytesIO()
        joblib.dump({
            'model': model,
            'feature_columns': ['month', 'day_of_month', 'day_of_week', 'price', 'category_id', 'total_quantity'],
            'training_date': datetime.now(),
            'metrics': {'r2': accuracy, 'samples': n_samples}
        }, model_buffer)
        
        # Crear el modelo en la base de datos
        trained_model = TrainedModel.objects.create(
            model_name='sales_predictor',
            model_file=model_buffer.getvalue(),
            accuracy=accuracy,
            feature_columns=['month', 'day_of_month', 'day_of_week', 'price', 'category_id', 'total_quantity'],
            training_samples=n_samples
        )
        
        self.stdout.write(f'Modelo pre-entrenado creado - Precisión: {accuracy:.4f}')

    def create_sample_predictions(self):
        """Crea predicciones de ejemplo para los próximos 30 días"""
        
        # Limpiar predicciones existentes
        SalesPrediction.objects.all().delete()
        
        # Generar predicciones para los próximos 30 días
        start_date = datetime.now().date()
        predictions = []
        
        for i in range(30):
            current_date = start_date + timedelta(days=i)
            
            # Crear una predicción "realista" con tendencia y estacionalidad
            base_sales = 1000 + (i * 20)  # Tendencia creciente
            
            # Estacionalidad semanal (menos ventas los fines de semana)
            day_of_week = current_date.weekday()
            if day_of_week >= 5:  # Fin de semana
                base_sales *= 0.7
            else:  # Día de semana
                base_sales *= 1.2
            
            # Variación aleatoria
            variation = random.uniform(0.8, 1.2)
            predicted_sales = base_sales * variation
            
            # Intervalo de confianza (10% del valor)
            confidence = predicted_sales * 0.1
            
            predictions.append(
                SalesPrediction(
                    date=current_date,
                    predicted_sales=predicted_sales,
                    confidence_interval=confidence
                )
            )
        
        # Guardar todas las predicciones
        SalesPrediction.objects.bulk_create(predictions)
        
        self.stdout.write(f'Predicciones creadas: {len(predictions)} días')
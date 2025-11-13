import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from django.db import connection
import joblib
import io
from datetime import datetime, timedelta
from django.utils import timezone
from backend.commercial.models import Venta, Producto, Cliente, Categoria

class SalesPredictor:
    def __init__(self):
        self.model = None
        self.feature_columns = []
        
    def get_training_data(self):
        """Obtiene datos históricos de ventas para entrenamiento usando tus modelos commercial"""
        try:
            # Verificar si hay datos reales en la base de datos
            if Venta.objects.count() == 0:
                print("No hay ventas en la base de datos. Creando datos de ejemplo...")
                return self.create_sample_data()
            
            # Usar el ORM de Django para obtener los datos de tus modelos commercial
            ventas = Venta.objects.select_related('producto', 'cliente', 'producto__categoria').all()
            
            if not ventas:
                return self.create_sample_data()
                
            # Preparar datos para el DataFrame
            data = []
            for venta in ventas:
                data.append({
                    'month': venta.fecha_venta.month,
                    'day_of_month': venta.fecha_venta.day,
                    'day_of_week': venta.fecha_venta.weekday(),
                    'price': float(venta.precio_unitario),
                    'category_id': venta.producto.categoria.id if venta.producto.categoria else 1,
                    'total_quantity': venta.cantidad,
                    'total_sales': float(venta.total) if venta.total else float(venta.cantidad * venta.precio_unitario)
                })
            
            df = pd.DataFrame(data)
            return df
            
        except Exception as e:
            print(f"Error obteniendo datos reales: {e}. Creando datos de ejemplo...")
            return self.create_sample_data()
    
    def create_sample_data(self):
        """Crea datos de ejemplo para entrenamiento cuando no hay datos reales"""
        # Generar datos sintéticos para demostración
        np.random.seed(42)
        n_samples = 1000
        
        data = {
            'month': np.random.randint(1, 13, n_samples),
            'day_of_month': np.random.randint(1, 32, n_samples),
            'day_of_week': np.random.randint(0, 7, n_samples),
            'price': np.random.uniform(10, 500, n_samples),
            'category_id': np.random.randint(1, 6, n_samples),
            'total_quantity': np.random.randint(1, 20, n_samples),
        }
        
        # Calcular ventas basadas en las características (con algo de ruido)
        base_sales = (
            data['month'] * 100 +  # Mes afecta ventas
            data['day_of_week'] * 50 +  # Día de semana afecta
            data['price'] * data['total_quantity'] * 0.8 +  # Precio y cantidad
            data['category_id'] * 200  # Categoría afecta
        )
        
        # Agregar ruido
        noise = np.random.normal(0, 100, n_samples)
        data['total_sales'] = np.maximum(base_sales + noise, 0)  # Evitar ventas negativas
        
        df = pd.DataFrame(data)
        return df
    
    def train_model(self):
        """Entrena el modelo Random Forest"""
        try:
            print("Comenzando entrenamiento del modelo...")
            
            # Obtener datos
            df = self.get_training_data()
            print(f"Datos obtenidos: {len(df)} registros")
            
            if len(df) < 10:
                return {"error": "No hay suficientes datos para entrenar el modelo (mínimo 10 registros)"}
            
            # Preparar características y objetivo
            feature_columns = ['month', 'day_of_month', 'day_of_week', 'price', 'category_id', 'total_quantity']
            X = df[feature_columns]
            y = df['total_sales']
            
            self.feature_columns = feature_columns
            
            print("Dividiendo datos en entrenamiento y prueba...")
            # Dividir datos
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            print("Entrenando modelo Random Forest...")
            # Entrenar modelo con parámetros optimizados
            self.model = RandomForestRegressor(
                n_estimators=50,  # Reducido para mayor velocidad
                max_depth=8,
                min_samples_split=5,
                random_state=42,
                n_jobs=-1
            )
            
            self.model.fit(X_train, y_train)
            
            # Evaluar modelo
            y_pred = self.model.predict(X_test)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            print(f"Modelo entrenado - R²: {r2:.4f}, MAE: {mae:.2f}")
            
            # Guardar modelo serializado
            model_buffer = io.BytesIO()
            joblib.dump({
                'model': self.model,
                'feature_columns': self.feature_columns,
                'training_date': datetime.now(),
                'metrics': {'mae': mae, 'r2': r2}
            }, model_buffer)
            
            return {
                'success': True,
                'accuracy': r2,
                'mae': mae,
                'model_data': model_buffer.getvalue(),
                'feature_columns': self.feature_columns,
                'training_samples': len(df)
            }
            
        except Exception as e:
            error_msg = f"Error en entrenamiento: {str(e)}"
            print(error_msg)
            return {"error": error_msg}
    
    def predict_sales(self, days=30):
        """Genera predicciones para los próximos días"""
        try:
            from .models import TrainedModel
            
            # Cargar último modelo entrenado
            latest_model = TrainedModel.objects.filter(
                model_name='sales_predictor'
            ).order_by('-training_date').first()
            
            if not latest_model:
                return {"error": "No hay modelo entrenado disponible. Entrene el modelo primero."}
            
            # Cargar modelo
            model_data = joblib.load(io.BytesIO(latest_model.model_file))
            self.model = model_data['model']
            self.feature_columns = model_data['feature_columns']
            
            print(f"Modelo cargado. Características: {self.feature_columns}")
            
            # Generar fechas futuras
            future_dates = []
            predictions = []
            
            start_date = timezone.now().date()
            for i in range(days):
                current_date = start_date + timedelta(days=i)
                
                # Crear características para la fecha (valores promedio/razonables)
                features = {
                    'month': current_date.month,
                    'day_of_month': current_date.day,
                    'day_of_week': current_date.weekday(),
                    'price': 150.0,  # Valor promedio razonable
                    'category_id': 3,  # Categoría promedio
                    'total_quantity': 8  # Cantidad promedio
                }
                
                # Asegurar que todas las características estén presentes
                feature_array = [features.get(col, 0) for col in self.feature_columns]
                prediction = self.model.predict([feature_array])[0]
                
                future_dates.append(current_date)
                predictions.append(float(max(0, prediction)))  # Evitar valores negativos
            
            print(f"Predicciones generadas: {len(predictions)} días")
            
            return {
                'dates': [d.isoformat() for d in future_dates],
                'predictions': predictions,
                'model_accuracy': latest_model.accuracy,
                'last_training': latest_model.training_date.isoformat()
            }
            
        except Exception as e:
            error_msg = f"Error en predicción: {str(e)}"
            print(error_msg)
            return {"error": error_msg}

# Instancia global
predictor = SalesPredictor()
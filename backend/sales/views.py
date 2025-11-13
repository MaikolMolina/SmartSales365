import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from .ml_service import predictor
from .models import TrainedModel, SalesPrediction
from datetime import datetime

@method_decorator(csrf_exempt, name='dispatch')
class TrainModelView(APIView):
    def post(self, request):
        """CU12 - Entrenar modelo de predicción"""
        try:
            result = predictor.train_model()
            
            if 'error' in result:
                return Response({'error': result['error']}, status=400)
            
            # Guardar modelo en base de datos
            trained_model = TrainedModel.objects.create(
                model_name='sales_predictor',
                model_file=result['model_data'],
                accuracy=result['accuracy'],
                feature_columns=result['feature_columns'],
                training_samples=result['training_samples']
            )
            
            return Response({
                'success': True,
                'message': 'Modelo entrenado exitosamente',
                'accuracy': result['accuracy'],
                'mae': result['mae'],
                'training_samples': result['training_samples'],
                'model_id': trained_model.id
            })
            
        except Exception as e:
            return Response({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class GetPredictionsView(APIView):
    def get(self, request):
        """CU11 - Obtener predicciones para dashboard"""
        try:
            days = int(request.GET.get('days', 30))
            result = predictor.predict_sales(days)
            
            if 'error' in result:
                return Response({'error': result['error']}, status=400)
            
            # Guardar predicciones en base de datos
            SalesPrediction.objects.all().delete()  # Limpiar predicciones anteriores
            
            for date_str, prediction in zip(result['dates'], result['predictions']):
                SalesPrediction.objects.create(
                    date=datetime.fromisoformat(date_str),
                    predicted_sales=prediction,
                    confidence_interval=prediction * 0.1  # 10% de intervalo de confianza
                )
            
            return Response({
                'success': True,
                'predictions': [
                    {'date': date, 'sales': sales} 
                    for date, sales in zip(result['dates'], result['predictions'])
                ],
                'model_accuracy': result['model_accuracy'],
                'last_training': result['last_training']
            })
            
        except Exception as e:
            return Response({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class ModelStatusView(APIView):
    def get(self, request):
        """Obtener estado del modelo"""
        latest_model = TrainedModel.objects.filter(
            model_name='sales_predictor'
        ).order_by('-training_date').first()
        
        if not latest_model:
            return Response({'trained': False})
        
        return Response({
            'trained': True,
            'last_training': latest_model.training_date.isoformat(),
            'accuracy': latest_model.accuracy,
            'feature_columns': latest_model.feature_columns,
            'training_samples': latest_model.training_samples
        })
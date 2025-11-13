from django.urls import path
from .views import TrainModelView, GetPredictionsView, ModelStatusView

urlpatterns = [
    
    # Rutas para IA
    path('api/train-model/', TrainModelView.as_view(), name='train_model'),
    path('api/get-predictions/', GetPredictionsView.as_view(), name='get_predictions'),
    path('api/model-status/', ModelStatusView.as_view(), name='model_status'),
]
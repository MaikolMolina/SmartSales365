import joblib
import numpy as np
import pandas as pd
from django.db import models
from django.contrib.auth.models import User

class SalesPrediction(models.Model):
    date = models.DateField()
    predicted_sales = models.DecimalField(max_digits=10, decimal_places=2)
    confidence_interval = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Predicción {self.date} - ${self.predicted_sales}"
    
    class Meta:
        db_table = 'sales_prediction'
        verbose_name = 'Predicción de Ventas'
        verbose_name_plural = 'Predicciones de Ventas'

class TrainedModel(models.Model):
    model_name = models.CharField(max_length=100, default='sales_predictor')
    model_file = models.BinaryField(null=True, blank=True)
    accuracy = models.FloatField(null=True, blank=True)
    training_date = models.DateTimeField(auto_now_add=True)
    feature_columns = models.JSONField(default=list)
    training_samples = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.model_name} - {self.training_date.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        db_table = 'trained_model'
        verbose_name = 'Modelo Entrenado'
        verbose_name_plural = 'Modelos Entrenados'
        ordering = ['-training_date']
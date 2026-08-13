from django.urls import path
from . import views

app_name = "pacientes"

urlpatterns = [
    path("", views.inicio, name="inicio"),

    # ==========================================================
    # PACIENTES
    # ==========================================================
    path("nuevo/", views.paciente_nuevo, name="paciente_nuevo"),
    path("<int:pk>/", views.paciente_ver, name="paciente_ver"),
    path("<int:pk>/editar/", views.paciente_editar, name="paciente_editar"),

    # ==========================================================
    # INTERNACIÓN
    # ==========================================================
    path(
        "<int:paciente_pk>/internaciones/",
        views.internaciones_paciente,
        name="internaciones_paciente",
    ),
    path(
        "<int:paciente_pk>/internaciones/nueva/",
        views.internacion_nueva,
        name="internacion_nueva",
    ),
    path(
        "internaciones/<int:pk>/",
        views.internacion_detalle,
        name="internacion_detalle",
    ),
    # La URL de recorrido_agregar fue eliminada porque el modelo ya no existe
    path(
        "internaciones/<int:pk>/comorbilidades/",
        views.comorbilidades_view,
        name="comorbilidades",
    ),
    path(
        "internaciones/<int:pk>/microbiologia/",
        views.microbiologia_view,
        name="microbiologia",
    ),
    path(
        "microbiologia/muestras/<int:muestra_pk>/aislamientos/agregar/",
        views.aislamiento_agregar,
        name="aislamiento_agregar",
    ),
    path("microbiologia/estudios/<int:estudio_pk>/resultados-tbc/", 
         views.resultados_tbc, 
         name="resultados_tbc"),
    
    path(
        "microbiologia/aislamientos/<int:aislamiento_pk>/sensibilidades/agregar/",
        views.sensibilidad_agregar,
        name="sensibilidad_agregar",
    ),
    path(
        "microbiologia/muestras/<int:pk>/editar/", 
         views.muestra_editar, 
         name="muestra_editar"),
    path(
        "microbiologia/muestras/<int:pk>/eliminar/", 
        views.muestra_eliminar, 
        name="muestra_eliminar"),
    
    path(
        "microbiologia/aislamientos/<int:pk>/editar/", 
         views.aislamiento_editar, 
         name="aislamiento_editar"),
    
    path(
        "microbiologia/aislamientos/<int:pk>/eliminar/", 
         views.aislamiento_eliminar, 
         name="aislamiento_eliminar"),
    
    path(
        "internaciones/<int:pk>/estudios_procedimientos/", 
         views.estudios_procedimientos_view, 
         name="estudios_procedimientos"),
    
    path(
        "internaciones/<int:internacion_pk>/tomografia/agregar/", 
         views.tomografia_agregar, 
         name="tomografia_agregar"),
    
    path(
        "tomografia/<int:pk>/editar/", 
         views.tomografia_editar, 
         name="tomografia_editar"),
    path(
        "tomografia/<int:pk>/eliminar/", 
         views.tomografia_eliminar, 
         name="tomografia_eliminar"),
    
    path(
        "internaciones/<int:pk>/tratamiento/",
        views.tratamiento_view,
        name="tratamiento",
    ),
]
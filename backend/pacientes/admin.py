from django.contrib import admin

from .models import (
    TipoCatalogo,
    Catalogo,
    Paciente,
    Internacion,
    RecorridoInternacion,
    InternacionCatalogo,
    InternacionSoporteRespiratorio,
    InternacionTratamientoAntimicrobiano,
    MuestraMicrobiologica,
    AislamientoMicrobiologico,
    SensibilidadMicrobiologica,
)

# ==========================================================
# INLINES
# ==========================================================


class RecorridoInternacionInline(admin.TabularInline):
    model = RecorridoInternacion
    extra = 0


class InternacionCatalogoInline(admin.TabularInline):
    model = InternacionCatalogo
    extra = 0


class InternacionSoporteRespiratorioInline(admin.TabularInline):
    model = InternacionSoporteRespiratorio
    extra = 0


class InternacionTratamientoAntimicrobianoInline(admin.TabularInline):
    model = InternacionTratamientoAntimicrobiano
    extra = 0


class MuestraMicrobiologicaInline(admin.TabularInline):
    model = MuestraMicrobiologica
    extra = 0


class AislamientoMicrobiologicoInline(admin.TabularInline):
    model = AislamientoMicrobiologico
    extra = 0


class SensibilidadMicrobiologicaInline(admin.TabularInline):
    model = SensibilidadMicrobiologica
    extra = 0
    
# ==========================================================
# TIPOS DE CATÁLOGOS
# ==========================================================

@admin.register(TipoCatalogo)
class TipoCatalogoAdmin(admin.ModelAdmin):

    list_display = (
    "codigo",
    "nombre",
    "protegido",
    "orden",
    "activo",
)

    search_fields = (
        "codigo",
        "nombre",
    )

    list_filter = (
    "protegido",
    "activo",
)

    ordering = (
    "orden",
    "nombre",
)


# ==========================================================
# CATÁLOGOS
# ==========================================================

@admin.register(Catalogo)
class CatalogoAdmin(admin.ModelAdmin):

    list_display = (
        "descripcion",
        "codigo",
        "tipo",
        "grupo",
        "subgrupo",
        "orden",
        "activo",
    )

    search_fields = (
        "descripcion",
        "codigo",
    )

    list_filter = (
        "tipo",
        "grupo",
        "activo",
    )

    ordering = (
        "tipo",
        "grupo",
        "subgrupo",
        "orden",
        "descripcion",
    )

    autocomplete_fields = (
        "tipo",
    )

    list_select_related = (
        "tipo",
    )
    
# ==========================================================
# PACIENTES
# ==========================================================

class InternacionInline(admin.TabularInline):
    model = Internacion
    extra = 0

    fields = (
        "fecha_ingreso",
        "fecha_egreso",
        "procedencia",
        "destino_egreso",
    )

    autocomplete_fields = (
        "procedencia",
        "destino_egreso",
    )


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):

    list_display = (
        "apellido",
        "nombre",
        "numero_documento",
        "sexo",
        "fecha_nacimiento",
        "cobertura",
        "estado_vital",
    )

    search_fields = (
        "apellido",
        "nombre",
        "numero_documento",
    )

    list_filter = (
        "sexo",
        "estado_vital",
        "cobertura",
    )

    ordering = (
        "apellido",
        "nombre",
    )

    autocomplete_fields = (
        "tipo_documento",
        "cobertura",
    )

    list_select_related = (
        "tipo_documento",
        "cobertura",
    )

    inlines = [
        InternacionInline,
    ] 
    
# ==========================================================
# INTERNACIONES
# ==========================================================

@admin.register(Internacion)
class InternacionAdmin(admin.ModelAdmin):

    list_display = (
        "paciente",
        "fecha_ingreso",
        "fecha_egreso",
        "procedencia",
        "destino_egreso",
        "insuficiencia_respiratoria",
    )

    search_fields = (
        "paciente__apellido",
        "paciente__nombre",
        "paciente__numero_documento",
    )

    list_filter = (
        "procedencia",
        "destino_egreso",
        "insuficiencia_respiratoria",
    )

    ordering = (
        "-fecha_ingreso",
    )

    autocomplete_fields = (
        "paciente",
        "procedencia",
        "destino_egreso",
        "insuficiencia_respiratoria",
    )

    list_select_related = (
        "paciente",
        "procedencia",
        "destino_egreso",
        "insuficiencia_respiratoria",
    )

    inlines = [
        RecorridoInternacionInline,
        InternacionCatalogoInline,
        InternacionSoporteRespiratorioInline,
        InternacionTratamientoAntimicrobianoInline,
        MuestraMicrobiologicaInline,
    ]

    fieldsets = (
        (
            "Paciente",
            {
                "fields": (
                    "paciente",
                )
            },
        ),
        (
            "Internación",
            {
                "fields": (
                    ("fecha_ingreso", "fecha_egreso"),
                    ("procedencia", "destino_egreso"),
                    "insuficiencia_respiratoria",
                )
            },
        ),
        (
            "Observaciones",
            {
                "fields": (
                    "observaciones",
                )
            },
        ),
    )   

# ==========================================================
# MICROBIOLOGÍA
# ==========================================================

@admin.register(MuestraMicrobiologica)
class MuestraMicrobiologicaAdmin(admin.ModelAdmin):

    list_display = (
        "internacion",
        "fecha_toma",
        "tipo_muestra",
        "resultado",
    )

    search_fields = (
        "internacion__paciente__apellido",
        "internacion__paciente__nombre",
        "internacion__paciente__numero_documento",
    )

    list_filter = (
        "tipo_muestra",
        "resultado",
    )

    autocomplete_fields = (
        "internacion",
        "tipo_muestra",
    )

    list_select_related = (
        "internacion",
        "tipo_muestra",
    )

    inlines = [
        AislamientoMicrobiologicoInline,
    ]


@admin.register(AislamientoMicrobiologico)
class AislamientoMicrobiologicoAdmin(admin.ModelAdmin):

    list_display = (
        "muestra",
        "germen",
        "significativo",
    )

    search_fields = (
        "germen__descripcion",
    )

    list_filter = (
        "significativo",
    )

    autocomplete_fields = (
        "muestra",
        "germen",
    )

    list_select_related = (
        "muestra",
        "germen",
    )

    inlines = [
        SensibilidadMicrobiologicaInline,
    ]


@admin.register(SensibilidadMicrobiologica)
class SensibilidadMicrobiologicaAdmin(admin.ModelAdmin):

    list_display = (
        "aislamiento",
        "antibiotico",
        "resultado",
    )

    search_fields = (
        "antibiotico__descripcion",
    )

    list_filter = (
        "resultado",
    )

    autocomplete_fields = (
        "aislamiento",
        "antibiotico",
    )

    list_select_related = (
        "aislamiento",
        "antibiotico",
    )


# ==========================================================
# SOPORTES RESPIRATORIOS
# ==========================================================

@admin.register(InternacionSoporteRespiratorio)
class InternacionSoporteRespiratorioAdmin(admin.ModelAdmin):

    list_display = (
        "internacion",
        "soporte",
        "fecha_desde",
        "fecha_hasta",
    )

    autocomplete_fields = (
        "internacion",
        "soporte",
    )

    list_select_related = (
        "internacion",
        "soporte",
    )


# ==========================================================
# TRATAMIENTOS ANTIMICROBIANOS
# ==========================================================

@admin.register(InternacionTratamientoAntimicrobiano)
class InternacionTratamientoAntimicrobianoAdmin(admin.ModelAdmin):

    list_display = (
        "internacion",
        "antimicrobiano",
        "via",
        "indicacion",
        "fecha_desde",
        "fecha_hasta",
    )

    autocomplete_fields = (
        "internacion",
        "antimicrobiano",
        "via",
        "indicacion",
    )

    list_select_related = (
        "internacion",
        "antimicrobiano",
        "via",
        "indicacion",
    )
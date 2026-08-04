from django.db import migrations


def cargar_catalogos_exposicion(apps, schema_editor):

    TipoCatalogo = apps.get_model("pacientes", "TipoCatalogo")
    Catalogo = apps.get_model("pacientes", "Catalogo")

    def crear_tipo(codigo, nombre):
        return TipoCatalogo.objects.get_or_create(
            codigo=codigo,
            defaults={
                "nombre": nombre,
                "descripcion": "",
                "protegido": True,
                "orden": 0,
                "activo": True,
            },
        )[0]

    def crear_item(tipo, codigo, descripcion, grupo, orden):
        Catalogo.objects.get_or_create(
            tipo=tipo,
            codigo=codigo,
            defaults={
                "descripcion": descripcion,
                "grupo": grupo,
                "subgrupo": "",
                "orden": orden,
                "activo": True,
            },
        )

    # ==========================================================
    # ANTECEDENTES RESPIRATORIOS
    # ==========================================================

    tipo = crear_tipo(
        "ANTECEDENTE_RESPIRATORIO",
        "Antecedente respiratorio",
    )
    # Obstructivas
    crear_item(tipo, "ASMA", "Asma", "Obstructivas", 1)
    crear_item(tipo, "EPOC", "EPOC", "Obstructivas", 2)
    crear_item(tipo, "BRONQUIECTASIAS", "Bronquiectasias", "Obstructivas", 3)
    crear_item(tipo, "FIBROSIS_QUISTICA", "Fibrosis quística", "Obstructivas", 4)

    # Intersticiales
    crear_item(tipo, "EPI", "Enfermedad pulmonar intersticial", "Intersticiales", 5)
    crear_item(tipo, "SARCOIDOSIS", "Sarcoidosis", "Intersticiales", 6)

    # Infecciosas
    crear_item(tipo, "TUBERCULOSIS", "Tuberculosis", "Infecciosas", 7)
    crear_item(tipo, "MICOBACTERIOSIS", "Micobacteriosis no tuberculosa", "Infecciosas", 8)
    crear_item(tipo, "ASPERGILOSIS_ABPA", "Aspergilosis / ABPA", "Infecciosas", 9)
    crear_item(tipo, "PULMON_SECUELAR", "Pulmón secuelar", "Infecciosas", 10)

    # Vasculares
    crear_item(tipo, "HIPERTENSION_PULMONAR", "Hipertensión pulmonar", "Vasculares", 11)
    crear_item(tipo, "TEP_CRONICO", "Tromboembolismo pulmonar crónico", "Vasculares", 12)
    crear_item(tipo, "MALFORMACION_AV", "Malformación arteriovenosa", "Vasculares", 13)
    crear_item(tipo, "HEMOPTISIS", "Hemoptisis", "Vasculares", 14)

    # Pleurales
    crear_item(tipo, "ENFERMEDAD_PLEURAL", "Enfermedad pleural", "Pleurales", 15)

    # Oncológicas
    crear_item(tipo, "CANCER_PULMON", "Cáncer de pulmón", "Oncológicas", 16)
    crear_item(tipo, "MESOTELIOMA", "Mesotelioma", "Oncológicas", 17)

    # Vía aérea
    crear_item(tipo, "ESTENOSIS_TRAQUEAL", "Estenosis traqueal", "Vía aérea", 18)
    crear_item(tipo, "PARALISIS_CUERDAS_VOCALES", "Parálisis de cuerdas vocales", "Vía aérea", 19)
    
    
        # ==========================================================
    # OTROS HÁBITOS INHALATORIOS
    # ==========================================================

    tipo = crear_tipo(
        "OTROS_HABITOS_INHALATORIOS",
        "Otros hábitos inhalatorios",
    )

    crear_item(tipo, "TAB_PASIVO", "Tabaquismo pasivo", "", 1)
    crear_item(tipo, "VAPING", "Vaping", "", 2)
    crear_item(tipo, "CANNABIS", "Cannabis inhalado", "", 3)
    crear_item(tipo, "COCAINA", "Cocaína inhalada", "", 4)
    crear_item(tipo, "OTRAS_DROGAS", "Otras drogas inhaladas", "", 5)

    # ==========================================================
    # EXPOSICIÓN OCUPACIONAL
    # ==========================================================

    tipo = crear_tipo(
        "EXPOSICION_OCUPACIONAL",
        "Exposición ocupacional",
    )

    crear_item(tipo, "SILICE", "Sílice", "", 1)
    crear_item(tipo, "ASBESTO", "Asbesto", "", 2)
    crear_item(tipo, "CARBON", "Carbón", "", 3)
    crear_item(tipo, "METALES", "Humos metálicos", "", 4)
    crear_item(tipo, "HARINAS", "Harinas", "", 5)
    crear_item(tipo, "ALGODON", "Algodón", "", 6)
    crear_item(tipo, "AVES", "Aves", "", 7)
    crear_item(tipo, "AGROQUIMICOS", "Agroquímicos", "", 8)
    crear_item(tipo, "ISOCIANATOS", "Isocianatos", "", 9)
    crear_item(tipo, "CLORO", "Cloro", "", 10)
    crear_item(tipo, "OTRA", "Otra", "", 11)

    # ==========================================================
    # EXPOSICIÓN AMBIENTAL
    # ==========================================================

    tipo = crear_tipo(
        "EXPOSICION_AMBIENTAL",
        "Exposición ambiental",
    )

    crear_item(tipo, "BIOMASA", "Humo de biomasa", "", 1)
    crear_item(tipo, "MOHO", "Moho / humedad", "", 2)
    crear_item(tipo, "AVES", "Aves", "", 3)
    crear_item(tipo, "AIRE", "Contaminación ambiental", "", 4)
    crear_item(tipo, "OTRA", "Otra", "", 5)
    
class Migration(migrations.Migration):

        dependencies = [
            ("pacientes", "0030_remove_internacion_exposicion_pasiva_and_more"),
        ]

        operations = [
            migrations.RunPython(cargar_catalogos_exposicion),
        ]
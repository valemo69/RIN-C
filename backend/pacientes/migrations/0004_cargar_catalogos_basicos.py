from django.db import migrations


def cargar_catalogos_basicos(apps, schema_editor):

    TipoCatalogo = apps.get_model("pacientes", "TipoCatalogo")
    Catalogo = apps.get_model("pacientes", "Catalogo")

    def agregar(tipo_codigo, codigo, descripcion, orden):

        tipo = TipoCatalogo.objects.get(codigo=tipo_codigo)

        Catalogo.objects.get_or_create(
            tipo=tipo,
            codigo=codigo,
            defaults={
                "descripcion": descripcion,
                "grupo": "",
                "subgrupo": "",
                "orden": orden,
                "activo": True,
            },
        )

    # ======================================================
    # TIPO DOCUMENTO
    # ======================================================

    agregar("TIPO_DOCUMENTO", "DNI", "DNI", 1)
    agregar("TIPO_DOCUMENTO", "OTRO", "Otro", 2)

    # ======================================================
    # ESTADO VITAL
    # ======================================================

    agregar("ESTADO_VITAL", "A", "Activo", 1)
    agregar("ESTADO_VITAL", "F", "Fallecido", 2)

    # ======================================================
    # TABAQUISMO
    # ======================================================

    agregar("TABAQUISMO", "NUNCA", "Nunca fumó", 1)
    agregar("TABAQUISMO", "ACTIVO", "Fumador activo", 2)
    agregar("TABAQUISMO", "EX", "Exfumador", 3)

    # ======================================================
    # TIPO IR
    # ======================================================

    agregar("TIPO_IR", "1", "Hipoxémica", 1)
    agregar("TIPO_IR", "2", "Hipercápnica", 2)
    agregar("TIPO_IR", "3", "Mixta", 3)

    # ======================================================
    # SENSIBILIDAD
    # ======================================================

    agregar("SENSIBILIDAD", "S", "Sensible", 1)
    agregar("SENSIBILIDAD", "I", "Intermedio", 2)
    agregar("SENSIBILIDAD", "R", "Resistente", 3)

    # ======================================================
    # SEXO
    # ======================================================

    agregar("SEXO", "M", "Masculino", 1)
    agregar("SEXO", "F", "Femenino", 2)
    agregar("SEXO", "X", "No binario", 3)

    # ======================================================
    # COBERTURA
    # ======================================================

    agregar("COBERTURA", "PUBLICA", "Sin cobertura / Pública", 1)
    agregar("COBERTURA", "OBRA_SOCIAL", "Obra social", 2)
    agregar("COBERTURA", "PREPAGA", "Prepaga", 3)

    # ======================================================
    # VIA ADMINISTRACION
    # ======================================================

    agregar("VIA_ADMINISTRACION", "VO", "Vía oral", 1)
    agregar("VIA_ADMINISTRACION", "EV", "Endovenosa", 2)
    agregar("VIA_ADMINISTRACION", "IM", "Intramuscular", 3)
    agregar("VIA_ADMINISTRACION", "SC", "Subcutánea", 4)
    agregar("VIA_ADMINISTRACION", "INH", "Inhalatoria", 5)


def deshacer(apps, schema_editor):

    Catalogo = apps.get_model("pacientes", "Catalogo")

    Catalogo.objects.filter(
        tipo__codigo__in=[
            "TIPO_DOCUMENTO",
            "ESTADO_VITAL",
            "TABAQUISMO",
            "TIPO_IR",
            "SENSIBILIDAD",
            "VIA_ADMINISTRACION",
            "SEXO",
            "COBERTURA",
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("pacientes", "0003b_cargar_tipos_catalogo_faltantes"),
    ]

    operations = [
        migrations.RunPython(
            cargar_catalogos_basicos,
            deshacer,
        ),
    ]
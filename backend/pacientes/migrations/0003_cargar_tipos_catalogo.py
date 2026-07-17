from django.db import migrations


def cargar_tipos_catalogo(apps, schema_editor):

    TipoCatalogo = apps.get_model("pacientes", "TipoCatalogo")

    tipos = [
        (70, "PROCEDENCIA", "Procedencia", False),
        (80, "DESTINO_EGRESO", "Destino al egreso", False),
        (90, "SECTOR", "Sector de internación", False),
        (100, "COMORBILIDAD", "Comorbilidad", False),
        (110, "TABAQUISMO", "Tabaquismo", False),
        (120, "TIPO_IR", "Tipo de insuficiencia respiratoria", False),
        (130, "SOPORTE_RESPIRATORIO", "Soporte respiratorio", False),
        (140, "GAS_MEDICINAL", "Gas medicinal", False),
        (150, "TIPO_MUESTRA", "Tipo de muestra", False),
        (160, "GERMEN", "Germen", False),
        (170, "ANTIMICROBIANO", "Antimicrobiano", False),
        (180, "VIA_ADMINISTRACION", "Vía de administración", False),
        (190, "INDICACION_ATB", "Indicación del antimicrobiano", False),
        (200, "RESULTADO_MICRO", "Resultado microbiológico", False),
        (210, "SENSIBILIDAD", "Sensibilidad", True),
        (220, "ESTUDIO_PROCEDIMIENTO", "Estudio / Procedimiento", False),
        (230, "MEDICAMENTO", "Medicamento", False),
    ]

    for orden, codigo, nombre, protegido in tipos:
        TipoCatalogo.objects.get_or_create(
            codigo=codigo,
            defaults={
                "nombre": nombre,
                "descripcion": "",
                "orden": orden,
                "protegido": protegido,
                "activo": True,
            },
        )


def deshacer(apps, schema_editor):

    TipoCatalogo = apps.get_model("pacientes", "TipoCatalogo")

    codigos = [
        "PROCEDENCIA",
        "DESTINO_EGRESO",
        "SECTOR",
        "COMORBILIDAD",
        "TABAQUISMO",
        "TIPO_IR",
        "SOPORTE_RESPIRATORIO",
        "GAS_MEDICINAL",
        "TIPO_MUESTRA",
        "GERMEN",
        "ANTIMICROBIANO",
        "VIA_ADMINISTRACION",
        "INDICACION_ATB",
        "RESULTADO_MICRO",
        "SENSIBILIDAD",
        "ESTUDIO_PROCEDIMIENTO",
        "MEDICAMENTO",
    ]

    TipoCatalogo.objects.filter(codigo__in=codigos).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("pacientes", "0002_alter_tipocatalogo_options_tipocatalogo_orden_and_more"),
    ]

    operations = [
        migrations.RunPython(
            cargar_tipos_catalogo,
            deshacer,
        ),
    ]
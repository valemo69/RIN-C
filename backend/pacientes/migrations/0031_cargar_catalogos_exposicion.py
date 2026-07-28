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

    def crear_item(tipo, codigo, descripcion, orden):
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

    tipo = crear_tipo(
        "OTROS_HABITOS_INHALATORIOS",
        "Otros hábitos inhalatorios",
    )

    crear_item(tipo, "TAB_PASIVO", "Tabaquismo pasivo", 1)
    crear_item(tipo, "VAPING", "Vaping", 2)
    crear_item(tipo, "CANNABIS", "Cannabis inhalado", 3)
    crear_item(tipo, "COCAINA", "Cocaína inhalada", 4)
    crear_item(tipo, "OTRAS_DROGAS", "Otras drogas inhaladas", 5)

    tipo = crear_tipo(
        "EXPOSICION_OCUPACIONAL",
        "Exposición ocupacional",
    )

    crear_item(tipo, "SILICE", "Sílice", 1)
    crear_item(tipo, "ASBESTO", "Asbesto", 2)
    crear_item(tipo, "CARBON", "Carbón", 3)
    crear_item(tipo, "METALES", "Humos metálicos", 4)
    crear_item(tipo, "HARINAS", "Harinas", 5)
    crear_item(tipo, "ALGODON", "Algodón", 6)
    crear_item(tipo, "AVES", "Aves", 7)
    crear_item(tipo, "AGROQUIMICOS", "Agroquímicos", 8)
    crear_item(tipo, "ISOCIANATOS", "Isocianatos", 9)
    crear_item(tipo, "OTRA", "Otra", 10)

    tipo = crear_tipo(
        "EXPOSICION_AMBIENTAL",
        "Exposición ambiental",
    )

    crear_item(tipo, "BIOMASA", "Humo de biomasa", 1)
    crear_item(tipo, "MOHO", "Moho / humedad", 2)
    crear_item(tipo, "AVES", "Aves", 3)
    crear_item(tipo, "AIRE", "Contaminación ambiental", 4)
    crear_item(tipo, "OTRA", "Otra", 5)


class Migration(migrations.Migration):

    dependencies = [
        ("pacientes", "0030_remove_internacion_exposicion_pasiva_and_more"),
    ]

    operations = [
        migrations.RunPython(cargar_catalogos_exposicion),
    ]

from django.db import migrations

# ==========================================================
# POR QUÉ ESTA MIGRACIÓN
# ==========================================================
#
# PROCEDENCIA, DESTINO_EGRESO, SECTOR y TIPO_IR ya existían como
# TipoCatalogo desde 0003, pero -igual que pasaba con COMORBILIDAD
# antes de la migración 0006- estaban vacíos: sin ítems cargados,
# esos <select> del formulario de Internación no tenían ninguna
# opción para elegir (por eso se veían con "---------" o, peor,
# quedaban confundidos con ítems de otros tipos si el campo no
# filtraba correctamente).
#
# Las opciones de acá abajo son una transcripción de las que ya
# tenía el mockup original de internacion.html, para no inventar
# nada nuevo.


def cargar(apps, schema_editor):

    TipoCatalogo = apps.get_model("pacientes", "TipoCatalogo")
    Catalogo = apps.get_model("pacientes", "Catalogo")

    def cargar_items(codigo_tipo, items):
        tipo = TipoCatalogo.objects.get(codigo=codigo_tipo)
        for codigo, descripcion, orden in items:
            Catalogo.objects.get_or_create(
                tipo=tipo,
                codigo=codigo,
                defaults={"descripcion": descripcion, "orden": orden},
            )

    cargar_items("PROCEDENCIA", [
        ("GUARDIA", "Guardia", 1),
        ("UTI", "UTI", 2),
        ("QUIROFANO", "Cirugía / Quirófano", 3),
        ("OTRO_HOSPITAL", "Otro hospital", 4),
    ])

    cargar_items("DESTINO_EGRESO", [
        ("DOMICILIO", "Domicilio", 1),
        ("SALA", "Sala", 2),
        ("UTI", "UTI", 3),
        ("REHABILITACION", "Rehabilitación", 4),
        ("OTRO_HOSPITAL", "Otro hospital", 5),
        ("FALLECIMIENTO", "Fallecimiento", 6),
    ])

    cargar_items("SECTOR", [
        ("GUARDIA", "Guardia", 1),
        ("SALA", "Sala", 2),
        ("UTI", "UTI", 3),
        ("QUIROFANO", "Cirugía / Quirófano", 4),
    ])

    # TIPO_IR: "Hipoxémica"/"Hipercápnica"/"Mixta" ya los había
    # cargado la migración 0004 (con otros códigos). Acá solo
    # agregamos la opción "No" que faltaba, para no duplicar.
    cargar_items("TIPO_IR", [
        ("NO", "No", 0),
    ])


def deshacer(apps, schema_editor):

    Catalogo = apps.get_model("pacientes", "Catalogo")

    Catalogo.objects.filter(
        tipo__codigo__in=["PROCEDENCIA", "DESTINO_EGRESO", "SECTOR"]
    ).delete()

    # TIPO_IR: solo borramos "NO" (lo único que agregó esta
    # migración); "Hipoxémica"/"Hipercápnica"/"Mixta" son de 0004
    # y no nos corresponde borrarlos acá.
    Catalogo.objects.filter(tipo__codigo="TIPO_IR", codigo="NO").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("pacientes", "0007_cargar_catalogos_microbiologia"),
    ]

    operations = [
        migrations.RunPython(cargar, deshacer),
    ]

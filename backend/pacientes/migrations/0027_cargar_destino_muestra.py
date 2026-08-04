from django.db import migrations


DESTINOS_MUESTRA = [
    ("BAC", "Bacteriología", 1),
    ("MTB", "Micobacterias", 2),
    ("MIC", "Micología", 3),
    ("VIR", "Virología", 4),
    ("PAT", "Anatomía patológica", 6),
    ("PAR", "Parasitología", 5),
]


def cargar(apps, schema_editor):

    TipoCatalogo = apps.get_model("pacientes", "TipoCatalogo")
    Catalogo = apps.get_model("pacientes", "Catalogo")

    tipo, _ = TipoCatalogo.objects.get_or_create(
        codigo="DESTINO_MUESTRA",
        defaults={
            "nombre": "Destino de la muestra",
            "descripcion": "",
            "orden": 155,
            "protegido": False,
            "activo": True,
        },
    )

    for codigo, descripcion, orden in DESTINOS_MUESTRA:
        Catalogo.objects.get_or_create(
            tipo=tipo,
            codigo=codigo,
            defaults={
                "descripcion": descripcion,
                "orden": orden,
            },
        )


def deshacer(apps, schema_editor):

    Catalogo = apps.get_model("pacientes", "Catalogo")
    TipoCatalogo = apps.get_model("pacientes", "TipoCatalogo")

    Catalogo.objects.filter(
        tipo__codigo="DESTINO_MUESTRA"
    ).delete()

    TipoCatalogo.objects.filter(
        codigo="DESTINO_MUESTRA"
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("pacientes", "0026_muestramicrobiologica_destino"),
    ]

    operations = [
        migrations.RunPython(cargar, deshacer),
    ]
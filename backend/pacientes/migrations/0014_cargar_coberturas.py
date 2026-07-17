from django.db import migrations


COBERTURAS = [
    "Sin cobertura / Pública",
    "Accord Salud",
    "AMFFA Salud",
    "Andar",
    "ASE",
    "Avalian",
    "Boreal",
    "Bristol Medicine",
    "Federada Salud",
    "Galeno",
    "Hospital Alemán",
    "Hospital Británico",
    "Hospital Italiano",
    "IOMA",
    "IOSFA",
    "Jerárquicos Salud",
    "Luis Pasteur",
    "Medicus",
    "Medifé",
    "Omint",
    "OSDE",
    "OSECAC",
    "OSPE",
    "OSPLAD",
    "OSPJN",
    "PAMI",
    "Poder Judicial",
    "Prevención Salud",
    "Sancor Salud",
    "Swiss Medical",
    "Unión Personal",
]


def cargar(apps, schema_editor):

    TipoCatalogo = apps.get_model("pacientes", "TipoCatalogo")
    Catalogo = apps.get_model("pacientes", "Catalogo")

    tipo = TipoCatalogo.objects.get(codigo="COBERTURA")

    primer_item = COBERTURAS[0]
    resto = sorted(COBERTURAS[1:])

    for orden, descripcion in enumerate([primer_item] + resto, start=1):

        codigo = (
            descripcion.upper()
            .replace(" ", "_")
            .replace("/", "_")
            .replace(".", "")
            .replace("Á", "A")
            .replace("É", "E")
            .replace("Í", "I")
            .replace("Ó", "O")
            .replace("Ú", "U")
        )

        Catalogo.objects.get_or_create(
            tipo=tipo,
            codigo=codigo,
            defaults={
                "descripcion": descripcion,
                "orden": orden,
            },
        )


def deshacer(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ("pacientes", "0013_cargar_indicacion_y_mas_antimicrobianos"),
    ]

    operations = [
        migrations.RunPython(cargar, deshacer),
    ]
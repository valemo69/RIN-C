from django.db import migrations

# ==========================================================
# POR QUÉ ESTA MIGRACIÓN
# ==========================================================
#
# La migración 0007 cargó un set inicial de gérmenes y
# antimicrobianos pensado para bacterias comunes. Faltaban los
# hongos respiratorios más relevantes en clínica neumonológica
# (Aspergillus y compañía) y los antifúngicos correspondientes,
# a pedido.


GERMENES_HONGOS = [
    ("ASPERGILLUS_FUMIGATUS", "Aspergillus fumigatus", 11),
    ("ASPERGILLUS_FLAVUS", "Aspergillus flavus", 12),
    ("ASPERGILLUS_NIGER", "Aspergillus niger", 13),
    ("ASPERGILLUS_OTRO", "Aspergillus spp. (otra especie)", 14),
    ("MUCORALES", "Mucorales", 15),
    ("CRYPTOCOCCUS_NEOFORMANS", "Cryptococcus neoformans", 16),
    ("PNEUMOCYSTIS_JIROVECII", "Pneumocystis jirovecii", 17),
    ("CANDIDA_GLABRATA", "Candida glabrata", 18),
    ("CANDIDA_KRUSEI", "Candida krusei", 19),
]

ANTIMICROBIANOS_ANTIFUNGICOS = [
    ("VORICONAZOL", "Voriconazol", 11),
    ("ITRACONAZOL", "Itraconazol", 12),
    ("POSACONAZOL", "Posaconazol", 13),
    ("ANFOTERICINA_B", "Anfotericina B", 14),
    ("CASPOFUNGINA", "Caspofungina", 15),
    ("MICAFUNGINA", "Micafungina", 16),
]


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

    cargar_items("GERMEN", GERMENES_HONGOS)
    cargar_items("ANTIMICROBIANO", ANTIMICROBIANOS_ANTIFUNGICOS)


def deshacer(apps, schema_editor):

    Catalogo = apps.get_model("pacientes", "Catalogo")

    codigos_germenes = [codigo for codigo, _, _ in GERMENES_HONGOS]
    codigos_antimicrobianos = [codigo for codigo, _, _ in ANTIMICROBIANOS_ANTIFUNGICOS]

    Catalogo.objects.filter(
        tipo__codigo="GERMEN", codigo__in=codigos_germenes
    ).delete()

    Catalogo.objects.filter(
        tipo__codigo="ANTIMICROBIANO", codigo__in=codigos_antimicrobianos
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("pacientes", "0009_limitar_catalogos_y_genexpert"),
    ]

    operations = [
        migrations.RunPython(cargar, deshacer),
    ]

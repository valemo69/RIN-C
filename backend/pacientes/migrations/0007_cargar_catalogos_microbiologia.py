from django.db import migrations

# ==========================================================
# POR QUÉ ESTA MIGRACIÓN
# ==========================================================
#
# TIPO_MUESTRA, GERMEN y ANTIMICROBIANO ya existían como
# TipoCatalogo desde la migración 0003, pero estaban vacíos: sin
# ítems cargados, el <select> de esos campos en el formulario de
# Microbiología aparece sin ninguna opción para elegir.
#
# Esta es una lista INICIAL, pensada para cubrir los casos más
# frecuentes en clínica neumonológica (incluye GeneXpert MTB/RIF,
# a pedido). No pretende ser exhaustiva: se puede seguir ampliando
# después desde el panel de administración de Django, sin tocar
# código ni migraciones.


TIPOS_MUESTRA = [
    ("HEMOCULTIVO", "Hemocultivo", 1),
    ("ASPIRADO_TRAQUEAL", "Aspirado traqueal", 2),
    ("ESPUTO", "Esputo", 3),
    ("BAL", "Lavado broncoalveolar (BAL)", 4),
    ("UROCULTIVO", "Urocultivo", 5),
    ("LIQUIDO_PLEURAL", "Líquido pleural", 6),
    ("PUNTA_CATETER", "Punta de catéter", 7),
    ("GENEXPERT", "GeneXpert MTB/RIF", 8),
]

GERMENES = [
    ("S_AUREUS", "Staphylococcus aureus", 1),
    ("S_EPIDERMIDIS", "Staphylococcus epidermidis", 2),
    ("E_COLI", "Escherichia coli", 3),
    ("K_PNEUMONIAE", "Klebsiella pneumoniae", 4),
    ("P_AERUGINOSA", "Pseudomonas aeruginosa", 5),
    ("A_BAUMANNII", "Acinetobacter baumannii", 6),
    ("E_FAECALIS", "Enterococcus faecalis", 7),
    ("C_ALBICANS", "Candida albicans", 8),
    ("S_PNEUMONIAE", "Streptococcus pneumoniae", 9),
    ("M_TUBERCULOSIS", "Mycobacterium tuberculosis", 10),
]

ANTIMICROBIANOS = [
    ("VANCOMICINA", "Vancomicina", 1),
    ("PIP_TAZO", "Piperacilina-tazobactam", 2),
    ("MEROPENEM", "Meropenem", 3),
    ("CEFTRIAXONA", "Ceftriaxona", 4),
    ("CIPROFLOXACINA", "Ciprofloxacina", 5),
    ("AMIKACINA", "Amikacina", 6),
    ("COLISTINA", "Colistina", 7),
    ("LINEZOLID", "Linezolid", 8),
    ("FLUCONAZOL", "Fluconazol", 9),
    ("RIFAMPICINA", "Rifampicina", 10),
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

    cargar_items("TIPO_MUESTRA", TIPOS_MUESTRA)
    cargar_items("GERMEN", GERMENES)
    cargar_items("ANTIMICROBIANO", ANTIMICROBIANOS)


def deshacer(apps, schema_editor):

    Catalogo = apps.get_model("pacientes", "Catalogo")

    Catalogo.objects.filter(
        tipo__codigo__in=["TIPO_MUESTRA", "GERMEN", "ANTIMICROBIANO"]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("pacientes", "0006_cargar_comorbilidades_e_inmunizaciones"),
    ]

    operations = [
        migrations.RunPython(cargar, deshacer),
    ]

from django.db import migrations

# ==========================================================
# POR QUÉ ESTA MIGRACIÓN
# ==========================================================
#
# Listado clínico completo para microbiología de internación:
# gramnegativos (Enterobacterales + no fermentadores), anaerobios,
# micobacterias no tuberculosas, hongos que faltaban, virus
# respiratorios, y la batería completa de antimicrobianos
# organizada por familia. No se repite nada de lo ya cargado en
# 0007/0010/0011.
#
# Los virus quedan dentro del mismo TipoCatalogo "GERMEN" que las
# bacterias y hongos (no un tipo aparte): estructuralmente un virus
# identificado en una muestra es lo mismo que una bacteria
# identificada -un Aislamiento con su germen y si es significativo-
# nada más que, al no tener antibiograma, esa muestra
# simplemente no va a tener filas de Sensibilidad cargadas. El
# modelo ya lo permite tal cual está (Sensibilidad es opcional).


GERMENES = [
    # Enterobacterales
    ("K_OXYTOCA", "Klebsiella oxytoca", 30),
    ("ENTEROBACTER_CLOACAE", "Enterobacter cloacae", 31),
    ("CITROBACTER_FREUNDII", "Citrobacter freundii", 32),
    ("CITROBACTER_KOSERI", "Citrobacter koseri", 33),
    ("SERRATIA_MARCESCENS", "Serratia marcescens", 34),
    ("MORGANELLA_MORGANII", "Morganella morganii", 35),
    ("PROTEUS_MIRABILIS", "Proteus mirabilis", 36),
    ("PROTEUS_VULGARIS", "Proteus vulgaris", 37),
    ("PROVIDENCIA_STUARTII", "Providencia stuartii", 38),

    # No fermentadores / otros gramnegativos
    ("STENOTROPHOMONAS_MALTOPHILIA", "Stenotrophomonas maltophilia", 39),
    ("BURKHOLDERIA_CEPACIA", "Burkholderia cepacia", 40),
    ("HAEMOPHILUS_INFLUENZAE", "Haemophilus influenzae", 41),
    ("MORAXELLA_CATARRHALIS", "Moraxella catarrhalis", 42),

    # Anaerobios
    ("BACTEROIDES_FRAGILIS", "Bacteroides fragilis", 43),
    ("PREVOTELLA", "Prevotella spp.", 44),
    ("FUSOBACTERIUM", "Fusobacterium spp.", 45),
    ("CLOSTRIDIOIDES_DIFFICILE", "Clostridioides difficile", 46),

    # Micobacterias
    ("MICOBACTERIA_NO_TUBERCULOSA", "Micobacterias no tuberculosas", 47),

    # Hongos que faltaban
    ("CANDIDA_TROPICALIS", "Candida tropicalis", 48),
    ("CANDIDA_PARAPSILOSIS", "Candida parapsilosis", 49),

    # Virus respiratorios
    ("INFLUENZA_A", "Influenza A", 50),
    ("INFLUENZA_B", "Influenza B", 51),
    ("SARS_COV_2", "SARS-CoV-2", 52),
    ("VSR", "Virus sincicial respiratorio", 53),
    ("METAPNEUMOVIRUS", "Metapneumovirus", 54),
    ("PARAINFLUENZA", "Parainfluenza", 55),
    ("ADENOVIRUS", "Adenovirus", 56),
    ("RINOVIRUS_ENTEROVIRUS", "Rinovirus / Enterovirus", 57),
]

ANTIMICROBIANOS = [
    # Penicilinas
    ("PENICILINA", "Penicilina", 20),
    ("AMPICILINA", "Ampicilina", 21),
    ("AMOXICILINA", "Amoxicilina", 22),
    ("AMOXI_CLAVULANICO", "Amoxicilina/Clavulánico", 23),
    ("AMPI_SULBACTAM", "Ampicilina/Sulbactam", 24),

    # Cefalosporinas
    ("CEFAZOLINA", "Cefazolina", 25),
    ("CEFUROXIMA", "Cefuroxima", 26),
    ("CEFOTAXIMA", "Cefotaxima", 27),
    ("CEFTAZIDIMA", "Ceftazidima", 28),
    ("CEFEPIME", "Cefepime", 29),
    ("CEFTOLOZANO_TAZOBACTAM", "Ceftolozano/Tazobactam", 30),
    ("CEFTAZIDIMA_AVIBACTAM", "Ceftazidima/Avibactam", 31),

    # Carbapenems / monobactam
    ("ERTAPENEM", "Ertapenem", 32),
    ("IMIPENEM", "Imipenem", 33),
    ("AZTREONAM", "Aztreonam", 34),

    # Aminoglucósidos
    ("GENTAMICINA", "Gentamicina", 35),
    ("TOBRAMICINA", "Tobramicina", 36),

    # Quinolonas
    ("LEVOFLOXACINA", "Levofloxacina", 37),
    ("MOXIFLOXACINA", "Moxifloxacina", 38),

    # Macrólidos
    ("AZITROMICINA", "Azitromicina", 39),
    ("CLARITROMICINA", "Claritromicina", 40),
    ("ERITROMICINA", "Eritromicina", 41),

    # Tetraciclinas
    ("DOXICICLINA", "Doxiciclina", 42),
    ("MINOCICLINA", "Minociclina", 43),

    # Otros
    ("TMS", "Trimetoprima/Sulfametoxazol", 44),
    ("TEICOPLANINA", "Teicoplanina", 45),
    ("TEDIZOLID", "Tedizolid", 46),
    ("CLINDAMICINA", "Clindamicina", 47),
    ("METRONIDAZOL", "Metronidazol", 48),
    ("NITROFURANTOINA", "Nitrofurantoína", 49),
    ("FOSFOMICINA", "Fosfomicina", 50),
    ("POLIMIXINA_B", "Polimixina B", 51),
    ("TIGECICLINA", "Tigeciclina", 52),
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

    cargar_items("GERMEN", GERMENES)
    cargar_items("ANTIMICROBIANO", ANTIMICROBIANOS)


def deshacer(apps, schema_editor):

    Catalogo = apps.get_model("pacientes", "Catalogo")

    codigos_germenes = [codigo for codigo, _, _ in GERMENES]
    codigos_antimicrobianos = [codigo for codigo, _, _ in ANTIMICROBIANOS]

    Catalogo.objects.filter(
        tipo__codigo="GERMEN", codigo__in=codigos_germenes
    ).delete()

    Catalogo.objects.filter(
        tipo__codigo="ANTIMICROBIANO", codigo__in=codigos_antimicrobianos
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("pacientes", "0011_cargar_germenes_internacion"),
    ]

    operations = [
        migrations.RunPython(cargar, deshacer),
    ]

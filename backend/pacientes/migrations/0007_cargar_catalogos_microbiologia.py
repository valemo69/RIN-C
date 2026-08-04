from django.db import migrations

TIPOS_MUESTRA = [
    ("HEMOCULTIVO", "Hemocultivo"),
    ("ASPIRADO_TRAQUEAL", "Aspirado traqueal"),
    ("ESPUTO", "Esputo"),
    ("ESPUTO_INDUCIDO", "Esputo inducido"),
    ("BAL", "BAL (Lavado broncoalveolar)"),
    ("LAVADO_BRONQUIAL", "Lavado bronquial"),
    ("HISOPADO_NASOFARINGEO", "Hisopado nasofaríngeo"),
    ("ORINA", "Orina"),
    ("LIQUIDO_PLEURAL", "Líquido pleural"),
    ("LIQUIDO_PERICARDICO", "Líquido pericárdico"),
    ("LCR", "Líquido cefalorraquídeo (LCR)"),
    ("SUERO", "Suero"),
    ("PUNTA_CATETER", "Punta de catéter"),
    ("TEJIDO_BIOPSIA", "Tejido / Biopsia"),
]

DESTINOS_MUESTRA = [
    ("BAC", "Bacteriología"),
    ("MTB", "Micobacterias"),
    ("MIC", "Micología"),
    ("VIR", "Virología"),
    ("PAR", "Parasitología"),
    ("PAT", "Anatomía patológica"),
]

TIPOS_ESTUDIO_MICROBIOLOGICO = [

    ("BACILOSCOPIA", "Baciloscopía"),
    ("CULTIVO", "Cultivo"),
    ("GENEXPERT", "GeneXpert MTB/RIF"),
    ("PCR", "PCR"),
    ("PANEL_VIRAL", "Panel viral"),
    ("GALACTOMANANO", "Galactomanano"),
    ("BETA_D_GLUCANO", "Beta-D-glucano"),
    ("INMUNODIFUSION", "Inmunodifusión"),
    ("TINCION", "Tinción"),
    ("ANATOMIA_PATOLOGICA", "Anatomía patológica"),

]

# ==========================================================
# GÉRMENES - BACTERIAS
# ==========================================================

GERMENES_BACTERIAS = [
    # Gram positivos
    ("STAPH_AUREUS", "Staphylococcus aureus"),
    ("STAPH_EPIDERMIDIS", "Staphylococcus epidermidis"),
    ("STAPH_HAEMOLYTICUS", "Staphylococcus haemolyticus"),
    ("STAPH_HOMINIS", "Staphylococcus hominis"),
    ("STAPH_LUGDUNENSIS", "Staphylococcus lugdunensis"),
    ("STREP_PNEUMONIAE", "Streptococcus pneumoniae"),
    ("STREP_PYOGENES", "Streptococcus pyogenes"),
    ("STREP_AGALACTIAE", "Streptococcus agalactiae"),
    ("STREP_ANGINOSUS", "Streptococcus anginosus"),
    ("ENTEROCOCCUS_FAECALIS", "Enterococcus faecalis"),
    ("ENTEROCOCCUS_FAECIUM", "Enterococcus faecium"),
    ("CORYNEBACTERIUM_STRIATUM", "Corynebacterium striatum"),
    ("NOCARDIA", "Nocardia spp."),
    # Gram negativos
    ("ESCHERICHIA_COLI", "Escherichia coli"),
    ("KLEBSIELLA_PNEUMONIAE", "Klebsiella pneumoniae"),
    ("KLEBSIELLA_OXYTOCA", "Klebsiella oxytoca"),
    ("ENTEROBACTER_CLOACAE", "Enterobacter cloacae"),
    ("CITROBACTER_FREUNDII", "Citrobacter freundii"),
    ("CITROBACTER_KOSERI", "Citrobacter koseri"),
    ("SERRATIA_MARCESCENS", "Serratia marcescens"),
    ("PROTEUS_MIRABILIS", "Proteus mirabilis"),
    ("PROTEUS_VULGARIS", "Proteus vulgaris"),
    ("MORGANELLA_MORGANII", "Morganella morganii"),
    ("PROVIDENCIA_STUARTII", "Providencia stuartii"),
    ("PSEUDOMONAS_AERUGINOSA", "Pseudomonas aeruginosa"),
    ("ACINETOBACTER_BAUMANNII", "Acinetobacter baumannii"),
    ("STENOTROPHOMONAS_MALTOPHILIA", "Stenotrophomonas maltophilia"),
    ("BURKHOLDERIA_CEPACIA", "Complejo Burkholderia cepacia"),
    ("HAEMOPHILUS_INFLUENZAE", "Haemophilus influenzae"),
    ("MORAXELLA_CATARRHALIS", "Moraxella catarrhalis"),
    ("ACHROMOBACTER_XYLOSOXIDANS", "Achromobacter xylosoxidans"),
    # Anaerobios
    ("BACTEROIDES_FRAGILIS", "Bacteroides fragilis"),
    ("PREVOTELLA", "Prevotella spp."),
    ("FUSOBACTERIUM_NUCLEATUM", "Fusobacterium nucleatum"),
    ("CLOSTRIDIUM_PERFRINGENS", "Clostridium perfringens"),
    ("CLOSTRIDIOIDES_DIFFICILE", "Clostridioides difficile"),
    ("CUTIBACTERIUM_ACNES", "Cutibacterium acnes"),
    # Respiratorios especiales
    ("BORDETELLA_PERTUSSIS", "Bordetella pertussis"),
    ("LEGIONELLA_PNEUMOPHILA", "Legionella pneumophila"),
    # Muestras estériles
    ("NEISSERIA_MENINGITIDIS", "Neisseria meningitidis"),
    ("LISTERIA_MONOCYTOGENES", "Listeria monocytogenes"),
]

# ==========================================================
# GÉRMENES - MICOBACTERIAS
# ==========================================================

GERMENES_MICOBACTERIAS = [
    # Complejo tuberculosis
    ("MTB_COMPLEX", "Complejo Mycobacterium tuberculosis"),
    ("M_TUBERCULOSIS", "Mycobacterium tuberculosis"),
    ("M_BOVIS", "Mycobacterium bovis"),
    # Complejo avium
    ("MAC", "Complejo Mycobacterium avium"),
    ("M_AVIUM", "Mycobacterium avium"),
    ("M_INTRACELLULARE", "Mycobacterium intracellulare"),
    ("M_CHIMAERA", "Mycobacterium chimaera"),
    # No tuberculosas frecuentes
    ("M_KANSASII", "Mycobacterium kansasii"),
    ("M_XENOPI", "Mycobacterium xenopi"),
    ("M_MALMOENSE", "Mycobacterium malmoense"),
    ("M_SZULGAI", "Mycobacterium szulgai"),
    # Crecimiento rápido
    ("M_ABSCESSUS", "Mycobacterium abscessus"),
    ("M_CHELONAE", "Mycobacterium chelonae"),
    ("M_FORTUITUM", "Mycobacterium fortuitum"),
    # Habitualmente contaminantes o poco patógenas
    ("M_GORDONAE", "Mycobacterium gordonae"),
    ("M_TERRAE", "Mycobacterium terrae"),
    ("MYCOBACTERIUM_SPP", "Mycobacterium spp."),
]
# ==========================================================
# GÉRMENES - HONGOS
# ==========================================================

GERMENES_HONGOS = [
    # Candida
    ("C_ALBICANS", "Candida albicans"),
    ("C_GLABRATA", "Candida glabrata"),
    ("C_TROPICALIS", "Candida tropicalis"),
    ("C_PARAPSILOSIS", "Candida parapsilosis"),
    ("C_KRUSEI", "Candida krusei"),
    # Aspergillus
    ("A_FUMIGATUS", "Aspergillus fumigatus"),
    ("A_FLAVUS", "Aspergillus flavus"),
    ("A_NIGER", "Aspergillus niger"),
    ("A_TERREUS", "Aspergillus terreus"),
    # Criptococo
    ("CRYPTOCOCCUS_NEOFORMANS", "Cryptococcus neoformans"),
    # Endémicos
    ("HISTOPLASMA_CAPSULATUM", "Histoplasma capsulatum"),
    ("PARACOCCIDIOIDES_SPP", "Paracoccidioides spp."),
    # Otros oportunistas
    ("SCEDOSPORIUM_APIOSPERMUM", "Scedosporium apiospermum"),
    ("LOMENTOSPORA_PROLIFICANS", "Lomentospora prolificans"),
    # Mucorales
    ("MUCORALES", "Mucorales"),
    # Pneumocystis
    ("PNEUMOCYSTIS_JIROVECII", "Pneumocystis jirovecii"),
]

# ==========================================================
# GÉRMENES - VIRUS
# ==========================================================

GERMENES_VIRUS = [

    # Virus respiratorios

    ("SARS_COV_2", "SARS-CoV-2"),
    ("INFLUENZA_A", "Influenza A"),
    ("INFLUENZA_B", "Influenza B"),
    ("VSR", "Virus sincicial respiratorio"),
    ("METAPNEUMOVIRUS", "Metapneumovirus humano"),
    ("ADENOVIRUS", "Adenovirus"),
    ("PARAINFLUENZA_1", "Parainfluenza 1"),
    ("PARAINFLUENZA_2", "Parainfluenza 2"),
    ("PARAINFLUENZA_3", "Parainfluenza 3"),
    ("PARAINFLUENZA_4", "Parainfluenza 4"),
    ("RINOVIRUS", "Rinovirus"),
    ("ENTEROVIRUS", "Enterovirus"),
    ("CORONAVIRUS_229E", "Coronavirus 229E"),
    ("CORONAVIRUS_NL63", "Coronavirus NL63"),
    ("CORONAVIRUS_OC43", "Coronavirus OC43"),
    ("CORONAVIRUS_HKU1", "Coronavirus HKU1"),

    # Virus oportunistas

    ("CMV", "Citomegalovirus"),
    ("HSV1", "Virus Herpes Simplex 1"),
    ("HSV2", "Virus Herpes Simplex 2"),
    ("VZV", "Virus Varicela-Zóster"),
    ("EBV", "Virus Epstein-Barr"),

]

# ==========================================================
# GÉRMENES - PARÁSITOS
# ==========================================================

GERMENES_PARASITOS = [
    ("STRONGYLOIDES_STERCORALIS", "Strongyloides stercoralis"),
    ("ECHINOCOCCUS_GRANULOSUS", "Echinococcus granulosus"),
    ("TOXOPLASMA_GONDII", "Toxoplasma gondii"),
    ("PARAGONIMUS_SPP", "Paragonimus spp."),
    ("ASCARIS_LUMBRICOIDES", "Ascaris lumbricoides"),
    ("TOXOCARA_SPP", "Toxocara spp."),
    ("ENTAMOEBA_HISTOLYTICA", "Entamoeba histolytica"),
]


# ==========================================================
# ANTIMICROBIANOS - ANTIBACTERIANOS
# ==========================================================

ANTIBACTERIANOS = [
    # Penicilinas
    ("PENICILINA_G", "Penicilina G"),
    ("AMPICILINA", "Ampicilina"),
    ("AMOXICILINA", "Amoxicilina"),
    ("AMOXICILINA_CLAVULANATO", "Amoxicilina / Ácido clavulánico"),
    ("PIPERACILINA_TAZOBACTAM", "Piperacilina / Tazobactam"),
    # Cefalosporinas
    ("CEFAZOLINA", "Cefazolina"),
    ("CEFUROXIMA", "Cefuroxima"),
    ("CEFOTAXIMA", "Cefotaxima"),
    ("CEFTRIAXONA", "Ceftriaxona"),
    ("CEFTAZIDIMA", "Ceftazidima"),
    ("CEFEPIME", "Cefepime"),
    ("CEFTOLOZANO_TAZOBACTAM", "Ceftolozano / Tazobactam"),
    ("CEFTAZIDIMA_AVIBACTAM", "Ceftazidima / Avibactam"),
    # Carbapenémicos
    ("IMIPENEM", "Imipenem"),
    ("MEROPENEM", "Meropenem"),
    ("ERTAPENEM", "Ertapenem"),
    # Monobactámicos
    ("AZTREONAM", "Aztreonam"),
    # Aminoglucósidos
    ("GENTAMICINA", "Gentamicina"),
    ("AMIKACINA", "Amikacina"),
    ("TOBRAMICINA", "Tobramicina"),
    # Quinolonas
    ("CIPROFLOXACINA", "Ciprofloxacina"),
    ("LEVOFLOXACINA", "Levofloxacina"),
    ("MOXIFLOXACINA", "Moxifloxacina"),
    # Macrólidos
    ("AZITROMICINA", "Azitromicina"),
    ("CLARITROMICINA", "Claritromicina"),
    # Tetraciclinas
    ("DOXICICLINA", "Doxiciclina"),
    ("MINOCICLINA", "Minociclina"),
    # Glicopéptidos
    ("VANCOMICINA", "Vancomicina"),
    ("TEICOPLANINA", "Teicoplanina"),
    # Oxazolidinonas
    ("LINEZOLID", "Linezolid"),
    # Lipopéptidos
    ("DAPTOMICINA", "Daptomicina"),
    # Polimixinas
    ("COLISTINA", "Colistina"),
    # Otros
    ("TRIMETOPRIMA_SULFAMETOXAZOL", "Trimetoprima / Sulfametoxazol"),
    ("TIGECICLINA", "Tigeciclina"),
]

# ==========================================================
# ANTIMICROBIANOS - ANTITUBERCULOSOS
# ==========================================================

ANTITUBERCULOSOS = [
    # Primera línea
    ("ISONIAZIDA", "Isoniazida"),
    ("RIFAMPICINA", "Rifampicina"),
    ("PIRAZINAMIDA", "Pirazinamida"),
    ("ETAMBUTOL", "Etambutol"),
    # Fluoroquinolonas
    ("LEVOFLOXACINA", "Levofloxacina"),
    ("MOXIFLOXACINA", "Moxifloxacina"),
    # Aminoglucósidos
    ("AMIKACINA", "Amikacina"),
    ("ESTREPTOMICINA", "Estreptomicina"),
    # Segunda línea
    ("ETIONAMIDA", "Etionamida"),
    ("CICLOSERINA", "Cicloserina"),
    ("PAS", "Ácido paraaminosalicílico (PAS)"),
    # Nuevos fármacos
    ("LINEZOLID", "Linezolid"),
    ("CLOFAZIMINA", "Clofazimina"),
    ("BEDAQUILINA", "Bedaquilina"),
    ("DELAMANID", "Delamanid"),
    ("PRETOMANID", "Pretomanid"),
]

# ==========================================================
# ANTIMICROBIANOS - ANTIFÚNGICOS
# ==========================================================

ANTIFUNGICOS = [
    # Polienos
    ("ANFOTERICINA_B", "Anfotericina B"),
    ("ANFOTERICINA_B_LIPOSOMAL", "Anfotericina B liposomal"),
    # Azoles
    ("FLUCONAZOL", "Fluconazol"),
    ("ITRACONAZOL", "Itraconazol"),
    ("VORICONAZOL", "Voriconazol"),
    ("POSACONAZOL", "Posaconazol"),
    ("ISAVUCONAZOL", "Isavuconazol"),
    # Equinocandinas
    ("CASPOFUNGINA", "Caspofungina"),
    ("MICAFUNGINA", "Micafungina"),
    ("ANIDULAFUNGINA", "Anidulafungina"),
    # Alilaminas
    ("TERBINAFINA", "Terbinafina"),
    # Otros
    ("FLUCITOSINA", "Flucitosina"),
]


def cargar(apps, schema_editor):

    TipoCatalogo = apps.get_model("pacientes", "TipoCatalogo")
    Catalogo = apps.get_model("pacientes", "Catalogo")

    def cargar_items(TipoCatalogo, Catalogo, tipo_codigo, items):

        tipo = TipoCatalogo.objects.get(codigo=tipo_codigo)

        for orden, (codigo, descripcion) in enumerate(items, start=1):

            Catalogo.objects.get_or_create(
                tipo=tipo,
                codigo=codigo,
                defaults={
                    "descripcion": descripcion,
                    "orden": orden,
                    "activo": True,
                },
            )

    cargar_items(TipoCatalogo, Catalogo, "TIPO_MUESTRA", TIPOS_MUESTRA)
    cargar_items(TipoCatalogo, Catalogo, "DESTINO_MUESTRA", DESTINOS_MUESTRA)
    cargar_items(TipoCatalogo, Catalogo, "TIPO_ESTUDIO_MICROBIOLOGICO", TIPOS_ESTUDIO_MICROBIOLOGICO)
    cargar_items(TipoCatalogo, Catalogo, "GERMEN", GERMENES_BACTERIAS)
    cargar_items(TipoCatalogo, Catalogo, "GERMEN", GERMENES_MICOBACTERIAS)
    cargar_items(TipoCatalogo, Catalogo, "GERMEN", GERMENES_HONGOS)
    cargar_items(TipoCatalogo, Catalogo, "GERMEN", GERMENES_VIRUS)
    cargar_items(TipoCatalogo, Catalogo, "GERMEN", GERMENES_PARASITOS)
    cargar_items(TipoCatalogo, Catalogo, "ANTIMICROBIANO", ANTIBACTERIANOS)
    cargar_items(TipoCatalogo, Catalogo, "ANTIMICROBIANO", ANTITUBERCULOSOS)
    cargar_items(TipoCatalogo, Catalogo, "ANTIMICROBIANO", ANTIFUNGICOS)


def deshacer(apps, schema_editor):

    Catalogo = apps.get_model("pacientes", "Catalogo")

    Catalogo.objects.filter(
        tipo__codigo__in=[
            "TIPO_MUESTRA",
            "DESTINO_MUESTRA",
            "TIPO_ESTUDIO_MICROBIOLOGICO",
            "GERMEN",
            "ANTIMICROBIANO",
         ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("pacientes", "0006_cargar_comorbilidades_e_inmunizaciones"),
    ]

    operations = [
        migrations.RunPython(cargar, deshacer),
    ]

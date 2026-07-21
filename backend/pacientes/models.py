from django.db import models

# ==========================================================
# MODELO BASE
# ==========================================================


class ModeloBase(models.Model):

    creado = models.DateTimeField(auto_now_add=True, verbose_name="Creado")

    modificado = models.DateTimeField(auto_now=True, verbose_name="Modificado")

    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        abstract = True
        
# ==========================================================
# EVENTOS DE LA INTERNACIÓN
# ==========================================================

class EventoInternacion(ModeloBase):

    fecha_desde = models.DateField(
        verbose_name="Fecha desde"
    )

    fecha_hasta = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha hasta"
    )

    class Meta:
        abstract = True


# ==========================================================
# TIPOS DE CATÁLOGOS
# ==========================================================


class TipoCatalogo(ModeloBase):

    codigo = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Código",
    )

    nombre = models.CharField(
        max_length=100,
        verbose_name="Nombre",
    )

    descripcion = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="Descripción",
    )

    protegido = models.BooleanField(
        default=False,
        verbose_name="Protegido",
        help_text="Impide modificaciones desde la administración funcional.",
    )

    orden = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Orden",
    )

    class Meta:
        verbose_name = "Tipo de catálogo"
        verbose_name_plural = "Tipos de catálogos"
        ordering = ["orden", "nombre"]

    def __str__(self):
        return self.nombre


# ==========================================================
# CATÁLOGOS
# ==========================================================


class Catalogo(ModeloBase):

    tipo = models.ForeignKey(
        TipoCatalogo,
        on_delete=models.PROTECT,
        related_name="items",
        verbose_name="Tipo",
    )

    codigo = models.CharField(max_length=30, verbose_name="Código")

    descripcion = models.CharField(max_length=200, verbose_name="Descripción")

    grupo = models.CharField(max_length=100, blank=True, verbose_name="Grupo")

    subgrupo = models.CharField(max_length=100, blank=True, verbose_name="Subgrupo")

    orden = models.PositiveIntegerField(default=0, verbose_name="Orden")

    class Meta:
        verbose_name = "Catálogo"
        verbose_name_plural = "Catálogos"

        ordering = [
            "tipo",
            "orden",
            "descripcion",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["tipo", "codigo"], name="uk_catalogo_tipo_codigo"
            )
        ]

    def __str__(self):
        return f"{self.tipo.nombre} - {self.descripcion}"


# ==========================================================
# PACIENTES
# ==========================================================


class Paciente(ModeloBase):

    tipo_documento = models.ForeignKey(
        Catalogo,
        on_delete=models.PROTECT,
        related_name="pacientes_tipo_documento",
        limit_choices_to={"tipo__codigo": "TIPO_DOCUMENTO", "activo": True},
        verbose_name="Tipo de documento",
    )

    numero_documento = models.CharField(
        max_length=20,
        verbose_name="Número de documento",
    )

    apellido = models.CharField(
        max_length=100,
        verbose_name="Apellido",
    )

    nombre = models.CharField(
        max_length=100,
        verbose_name="Nombre",
    )

    sexo = models.ForeignKey(
        Catalogo,
        on_delete=models.PROTECT,
        related_name="pacientes_sexo",
        limit_choices_to={"tipo__codigo": "SEXO", "activo": True},
        verbose_name="Sexo",
    )

    fecha_nacimiento = models.DateField(
        verbose_name="Fecha de nacimiento",
    )

    cobertura = models.ForeignKey(
        Catalogo,
        on_delete=models.PROTECT,
        related_name="pacientes_cobertura",
        limit_choices_to={"tipo__codigo": "COBERTURA", "activo": True},
        verbose_name="Cobertura",
    )

    numero_afiliado = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Número de afiliado",
    )

    estado_vital = models.ForeignKey(
        Catalogo,
        on_delete=models.PROTECT,
        related_name="pacientes_estado_vital",
        limit_choices_to={"tipo__codigo": "ESTADO_VITAL", "activo": True},
        verbose_name="Estado vital",
    )

    fecha_fallecimiento = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de fallecimiento",
    )

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

        ordering = [
            "apellido",
            "nombre",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "tipo_documento",
                    "numero_documento",
                ],
                name="uk_paciente_tipo_numero_documento",
            ),
        ]

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"

    @property
    def edad(self):
        """
        Calcula la edad en años a partir de fecha_nacimiento.

        Por qué una @property y no un campo en la base de datos:
        la edad cambia todos los días, así que si la guardáramos
        como un campo normal, quedaría desactualizada al día
        siguiente de calcularla. Al ser una property, Django la
        recalcula cada vez que se accede a paciente.edad, tomando
        siempre la fecha actual como referencia.
        """
        if not self.fecha_nacimiento:
            return None

        from datetime import date

        hoy = date.today()

        edad = hoy.year - self.fecha_nacimiento.year

        # Si todavía no pasó el cumpleaños este año, restamos 1.
        cumplio_este_anio = (hoy.month, hoy.day) >= (
            self.fecha_nacimiento.month,
            self.fecha_nacimiento.day,
        )

        if not cumplio_este_anio:
            edad -= 1

        return edad

class Internacion(ModeloBase):
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.PROTECT,
        related_name="internaciones",
        verbose_name="Paciente",
    )

    fecha_ingreso = models.DateField(verbose_name="Fecha de ingreso")
    fecha_egreso = models.DateField(null=True, blank=True, verbose_name="Fecha de egreso")

    procedencia = models.ForeignKey(
        Catalogo,
        on_delete=models.PROTECT,
        related_name="internaciones_procedencia",
        limit_choices_to={"tipo__codigo": "PROCEDENCIA", "activo": True},
        verbose_name="Procedencia",
    )

    destino_egreso = models.ForeignKey(
        Catalogo,
        on_delete=models.PROTECT,
        related_name="internaciones_destino",
        limit_choices_to={"tipo__codigo": "DESTINO_EGRESO", "activo": True},
        verbose_name="Destino al egreso",
        null=True,
        blank=True,
    )

    insuficiencia_respiratoria = models.ForeignKey(
        Catalogo,
        on_delete=models.PROTECT,
        related_name="internaciones_ir",
        limit_choices_to={"tipo__codigo": "TIPO_IR", "activo": True},
        verbose_name="Insuficiencia respiratoria",
        null=True,
        blank=True,
    )

    # =====================================================
    # MOTIVOS DE INTERNACIÓN (UNO POR CATEGORÍA - FK)
    # =====================================================
    motivo_infeccioso = models.ForeignKey(
        Catalogo,
        on_delete=models.PROTECT,
        related_name='+',
        limit_choices_to={"tipo__codigo": "MOTIVO_INFECCIOSO", "activo": True},
        null=True,
        blank=True,
        verbose_name="Motivo infeccioso",
    )
    motivo_obstructivo = models.ForeignKey(
        Catalogo,
        on_delete=models.PROTECT,
        related_name='+',
        limit_choices_to={"tipo__codigo": "MOTIVO_OBSTRUCTIVO", "activo": True},
        null=True,
        blank=True,
        verbose_name="Motivo obstructivo",
    )
    motivo_intersticial = models.ForeignKey(
        Catalogo,
        on_delete=models.PROTECT,
        related_name='+',
        limit_choices_to={"tipo__codigo": "MOTIVO_INTERSTICIAL", "activo": True},
        null=True,
        blank=True,
        verbose_name="Motivo intersticial",
    )
    motivo_pleural = models.ForeignKey(
        Catalogo,
        on_delete=models.PROTECT,
        related_name='+',
        limit_choices_to={"tipo__codigo": "MOTIVO_PLEURAL", "activo": True},
        null=True,
        blank=True,
        verbose_name="Motivo pleural",
    )
    motivo_vascular = models.ForeignKey(
        Catalogo,
        on_delete=models.PROTECT,
        related_name='+',
        limit_choices_to={"tipo__codigo": "MOTIVO_VASCULAR", "activo": True},
        null=True,
        blank=True,
        verbose_name="Motivo vascular",
    )
    motivo_oncologico = models.ForeignKey(
        Catalogo,
        on_delete=models.PROTECT,
        related_name='+',
        limit_choices_to={"tipo__codigo": "MOTIVO_ONCOLOGICO", "activo": True},
        null=True,
        blank=True,
        verbose_name="Motivo oncológico",
    )
    motivo_otro = models.ForeignKey(
        Catalogo,
        on_delete=models.PROTECT,
        related_name='+',
        limit_choices_to={"tipo__codigo": "MOTIVO_OTRO", "activo": True},
        null=True,
        blank=True,
        verbose_name="Otro motivo",
    )

  
    

    # =====================================================
    # EXPOSICIÓN INHALATORIA
    # =====================================================
    tabaquismo = models.CharField(
        max_length=20,
        choices=[
            ("NUNCA", "Nunca fumó"),
            ("ACTIVO", "Fumador activo"),
            ("EXFUMADOR", "Exfumador"),
        ],
        blank=True,
        verbose_name="Tabaquismo",
    )

    exposicion_pasiva = models.ManyToManyField(
        Catalogo,
        related_name='+',
        limit_choices_to={"tipo__codigo": "EXPOSICION_PASIVA", "activo": True},
        blank=True,
        verbose_name="Exposición pasiva al humo de tabaco",
    )

    otros_habitos = models.ManyToManyField(
        Catalogo,
        related_name='+',
        limit_choices_to={"tipo__codigo": "HABITO_INHALATORIO", "activo": True},
        blank=True,
        verbose_name="Otros hábitos inhalatorios",
    )

    exposiciones_laborales = models.ManyToManyField(
        Catalogo,
        related_name='+',
        limit_choices_to={"tipo__codigo": "EXPOSICION_LABORAL", "activo": True},
        blank=True,
        verbose_name="Exposiciones laborales y ambientales",
    )


    # =====================================================
    # ANTECEDENTES RESPIRATORIOS
    # =====================================================
    antecedentes_respiratorios = models.ManyToManyField(
        Catalogo,
        related_name='+',
        limit_choices_to={"tipo__codigo": "ANTECEDENTE_RESPIRATORIO", "activo": True},
        blank=True,
        verbose_name="Antecedentes respiratorios",
    )

    # =====================================================
    # SOPORTE RESPIRATORIO
    # =====================================================
    soporte_respiratorio = models.ManyToManyField(
        Catalogo,
        related_name='+',
        limit_choices_to={"tipo__codigo": "SOPORTE_RESPIRATORIO", "activo": True},
        blank=True,
        verbose_name="Soporte respiratorio",
    )

    cigarrillos_por_dia = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name="Cigarrillos por día",
    )

    anos_fumando = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name="Años fumando",
    )

    indice_paquetes_anio = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
        verbose_name="Índice paquetes-año",
    )

    class Meta:
        verbose_name = "Internación"
        verbose_name_plural = "Internaciones"
        ordering = ["-fecha_ingreso", "paciente"]

    def __str__(self):
        return f"{self.paciente} - {self.fecha_ingreso:%d/%m/%Y}"


   
# ==========================================================
# TRATAMIENTO ANTIMICROBIANO
# ==========================================================

class InternacionTratamientoAntimicrobiano(EventoInternacion):

    internacion = models.ForeignKey(
        Internacion,
        on_delete=models.CASCADE,
        related_name="tratamientos_antimicrobianos",
        verbose_name="Internación",
    )

    antimicrobiano = models.ForeignKey(
        Catalogo,
        on_delete=models.PROTECT,
        related_name="tratamientos_antimicrobianos",
        limit_choices_to={"tipo__codigo": "ANTIMICROBIANO", "activo": True},
        verbose_name="Antimicrobiano",
    )

    indicacion = models.ForeignKey(
        Catalogo,
        on_delete=models.PROTECT,
        related_name="indicaciones_antimicrobianos",
        limit_choices_to={"tipo__codigo": "INDICACION_ATB", "activo": True},
        verbose_name="Indicación",
    )

    via = models.ForeignKey(
        Catalogo,
        on_delete=models.PROTECT,
        related_name="vias_antimicrobianos",
        limit_choices_to={"tipo__codigo": "VIA_ADMINISTRACION", "activo": True},
        verbose_name="Vía de administración",
    )

    dosis = models.CharField(
        max_length=100,
        verbose_name="Dosis",
    )

    observaciones = models.TextField(
        blank=True,
        verbose_name="Observaciones",
    )

    class Meta:
        verbose_name = "Tratamiento antimicrobiano"
        verbose_name_plural = "Tratamientos antimicrobianos"

        ordering = [
            "internacion",
            "fecha_desde",
        ]

    def __str__(self):
        return f"{self.antimicrobiano.descripcion}"

# ==========================================================
# RELACIÓN ENTRE INTERNACIÓN Y CATÁLOGOS
# (se mantiene igual, no se toca)
# ==========================================================


class InternacionCatalogo(ModeloBase):

    internacion = models.ForeignKey(
        Internacion,
        on_delete=models.CASCADE,
        related_name="catalogos",
        verbose_name="Internación",
    )

    catalogo = models.ForeignKey(
        Catalogo,
        on_delete=models.PROTECT,
        related_name="internaciones",
        verbose_name="Catálogo",
    )

    class Meta:
        verbose_name = "Elemento de la internación"
        verbose_name_plural = "Elementos de la internación"

        ordering = [
            "internacion",
            "catalogo",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["internacion", "catalogo"],
                name="uk_internacion_catalogo",
            )
        ]
        
        indexes = [
            models.Index(fields=["internacion"]),
            models.Index(fields=["catalogo"]),
        ]

    def __str__(self):
        return f"{self.internacion} - {self.catalogo.descripcion}"


# ==========================================================
# MUESTRAS MICROBIOLÓGICAS
# (se mantiene igual, no se toca)
# ==========================================================


class MuestraMicrobiologica(ModeloBase):

    class Resultado(models.TextChoices):
        POSITIVO = "P", "Positivo"
        NEGATIVO = "N", "Negativo"
        CONTAMINADO = "C", "Contaminado"
        PENDIENTE = "PE", "Pendiente"

    class ResultadoGeneXpert(models.TextChoices):
        """
        Escala separada de Resultado (arriba) a propósito: un
        GeneXpert es una PCR (resultado genotípico: ¿está el gen
        de resistencia, sí o no?), no un antibiograma por disco
        (resultado fenotípico: sensible/intermedio/resistente). Son
        preguntas clínicas distintas, así que conviene no mezclarlas
        en la misma escala aunque a veces se parezcan.
        "Indeterminado" existe porque en la práctica un cartucho de
        GeneXpert puede fallar (muestra insuficiente, error del
        equipo) y ese resultado NO es lo mismo que "no detectado".
        """
        DETECTADO = "D", "Detectado"
        NO_DETECTADO = "ND", "No detectado"
        INDETERMINADO = "I", "Indeterminado"

    internacion = models.ForeignKey(
        Internacion,
        on_delete=models.CASCADE,
        related_name="muestras_microbiologicas",
        verbose_name="Internación",
    )

    fecha_toma = models.DateField(verbose_name="Fecha de toma")

    tipo_muestra = models.ForeignKey(
        Catalogo,
        on_delete=models.PROTECT,
        related_name="muestras_tipo",
        limit_choices_to={"tipo__codigo": "TIPO_MUESTRA", "activo": True},
        verbose_name="Tipo de muestra",
    )

    resultado = models.CharField(
        max_length=2,
        choices=Resultado.choices,
        default=Resultado.PENDIENTE,
        verbose_name="Resultado",
    )

    # Los dos campos siguientes solo tienen sentido cuando
    # tipo_muestra es "GeneXpert MTB/RIF" (por eso null=True,
    # blank=True: en cualquier otro tipo de muestra quedan vacíos).
    # No usamos el modelo Catalogo para esto porque son solo 3
    # opciones fijas, específicas de este campo, sin necesidad de
    # administrarlas desde el panel de catálogos.

    mtb_detectado = models.CharField(
        max_length=2,
        choices=ResultadoGeneXpert.choices,
        null=True,
        blank=True,
        verbose_name="Mycobacterium tuberculosis detectada (GeneXpert)",
    )

    resistencia_rifampicina = models.CharField(
        max_length=2,
        choices=ResultadoGeneXpert.choices,
        null=True,
        blank=True,
        verbose_name="Resistencia a rifampicina (GeneXpert)",
    )

    class Meta:
        verbose_name = "Muestra microbiológica"
        verbose_name_plural = "Muestras microbiológicas"

        ordering = [
            "-fecha_toma",
        ]

    def __str__(self):
        return f"{self.fecha_toma:%d/%m/%Y} - {self.tipo_muestra.descripcion}"


# ==========================================================
# AISLAMIENTOS MICROBIOLÓGICOS
# (se mantiene igual, no se toca)
# ==========================================================


class AislamientoMicrobiologico(ModeloBase):

    muestra = models.ForeignKey(
        MuestraMicrobiologica,
        on_delete=models.CASCADE,
        related_name="aislamientos",
        verbose_name="Muestra",
    )

    germen = models.ForeignKey(
        Catalogo,
        on_delete=models.PROTECT,
        related_name="aislamientos_germen",
        limit_choices_to={"tipo__codigo": "GERMEN", "activo": True},
        verbose_name="Germen",
    )

    significativo = models.BooleanField(default=True, verbose_name="Significativo")

    class Meta:
        verbose_name = "Aislamiento microbiológico"
        verbose_name_plural = "Aislamientos microbiológicos"

        ordering = [
            "muestra",
            "germen",
        ]
        
    def __str__(self):
        return f"{self.germen.descripcion}"


# ==========================================================
# SENSIBILIDAD MICROBIOLÓGICA
# (se mantiene igual, no se toca)
# ==========================================================


class SensibilidadMicrobiologica(ModeloBase):

    class Resultado(models.TextChoices):
        SENSIBLE = "S", "Sensible"
        INTERMEDIO = "I", "Intermedio"
        RESISTENTE = "R", "Resistente"

    aislamiento = models.ForeignKey(
        AislamientoMicrobiologico,
        on_delete=models.CASCADE,
        related_name="sensibilidades",
        verbose_name="Aislamiento",
    )

    antibiotico = models.ForeignKey(
        Catalogo,
        on_delete=models.PROTECT,
        related_name="sensibilidades_antibiotico",
        limit_choices_to={"tipo__codigo": "ANTIMICROBIANO", "activo": True},
        verbose_name="Antibiótico",
    )

    resultado = models.CharField(
        max_length=1, choices=Resultado.choices, verbose_name="Resultado"
    )

    class Meta:
        verbose_name = "Sensibilidad microbiológica"
        verbose_name_plural = "Sensibilidades microbiológicas"

        ordering = [
            "aislamiento",
            "antibiotico",
        ]

    def __str__(self):
        return f"{self.antibiotico.descripcion} ({self.resultado})"
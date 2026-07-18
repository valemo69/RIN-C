from django import forms

from core.forms import BootstrapFormMixin

from .models import (
    Paciente,
    Internacion,
    InternacionCatalogo,
    Catalogo,
    InternacionTratamientoAntimicrobiano,
    MuestraMicrobiologica,
    AislamientoMicrobiologico,
    SensibilidadMicrobiologica,
)

# ==========================================================
# BÚSQUEDA DE PACIENTES
# ==========================================================

class BusquedaPacienteForm(BootstrapFormMixin, forms.Form):

    numero_documento = forms.CharField(
        label="Documento",
        required=False,
        max_length=20,
    )

    apellido = forms.CharField(
        label="Apellido",
        required=False,
        max_length=100,
    )

    def clean(self):

        cleaned_data = super().clean()

        numero_documento = cleaned_data.get("numero_documento", "").strip()
        apellido = cleaned_data.get("apellido", "").strip()

        if not numero_documento and not apellido:
            raise forms.ValidationError(
                "Debe ingresar un documento, un apellido o ambos."
            )

        if numero_documento:
            if not numero_documento.isdigit():
                self.add_error(
                    "numero_documento",
                    "El documento debe contener únicamente números."
                )
            elif len(numero_documento) not in (7, 8):
                self.add_error(
                    "numero_documento",
                    "El documento debe tener 7 u 8 dígitos."
                )

        return cleaned_data

# ==========================================================
# PACIENTES
# ==========================================================

class PacienteForm(BootstrapFormMixin, forms.ModelForm):

    class Meta:
        model = Paciente
        fields = (
            "tipo_documento",
            "numero_documento",
            "apellido",
            "nombre",
            "sexo",
            "fecha_nacimiento",
            "cobertura",
            "numero_afiliado",
            "estado_vital",
            "fecha_fallecimiento",
        )
        widgets = {
            "fecha_nacimiento": forms.DateInput(attrs={"type": "date"}),
            "fecha_fallecimiento": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        estado_vital = cleaned_data.get("estado_vital")
        fecha_fallecimiento = cleaned_data.get("fecha_fallecimiento")

        if estado_vital:
            if estado_vital.codigo == "F" and not fecha_fallecimiento:
                self.add_error(
                    "fecha_fallecimiento",
                    "Debe indicar la fecha de fallecimiento.",
                )
            if estado_vital.codigo == "A":
                cleaned_data["fecha_fallecimiento"] = None

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Catalogo

        self.fields["tipo_documento"].queryset = Catalogo.objects.filter(
            tipo__codigo="TIPO_DOCUMENTO",
            codigo__in=["DNI", "OTRO"],
        ).order_by("orden")

        self.fields["cobertura"].queryset = Catalogo.objects.filter(
            tipo__codigo="COBERTURA"
        ).order_by("descripcion")

# ==========================================================
# INTERNACIÓN
# ==========================================================

class InternacionForm(BootstrapFormMixin, forms.ModelForm):
    # Motivos (ForeignKey -> select)
    motivo_infeccioso = forms.ModelChoiceField(
        queryset=Catalogo.objects.filter(tipo__codigo="MOTIVO_INFECCIOSO", activo=True),
        required=False,
        empty_label="Sin motivo infeccioso",
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    motivo_obstructivo = forms.ModelChoiceField(
        queryset=Catalogo.objects.filter(tipo__codigo="MOTIVO_OBSTRUCTIVO", activo=True),
        required=False,
        empty_label="Sin motivo obstructivo",
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    motivo_intersticial = forms.ModelChoiceField(
        queryset=Catalogo.objects.filter(tipo__codigo="MOTIVO_INTERSTICIAL", activo=True),
        required=False,
        empty_label="Sin motivo intersticial",
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    motivo_pleural = forms.ModelChoiceField(
        queryset=Catalogo.objects.filter(tipo__codigo="MOTIVO_PLEURAL", activo=True),
        required=False,
        empty_label="Sin patología pleural",
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    motivo_vascular = forms.ModelChoiceField(
        queryset=Catalogo.objects.filter(tipo__codigo="MOTIVO_VASCULAR", activo=True),
        required=False,
        empty_label="Sin patología vascular",
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    motivo_oncologico = forms.ModelChoiceField(
        queryset=Catalogo.objects.filter(tipo__codigo="MOTIVO_ONCOLOGICO", activo=True),
        required=False,
        empty_label="Sin patología oncológica",
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    motivo_otro = forms.ModelChoiceField(
        queryset=Catalogo.objects.filter(tipo__codigo="MOTIVO_OTRO", activo=True),
        required=False,
        empty_label="Sin otros motivos",
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    # Antecedentes (ManyToMany -> checkboxes)
    antecedentes_respiratorios = forms.ModelMultipleChoiceField(
        queryset=Catalogo.objects.filter(tipo__codigo="ANTECEDENTE_RESPIRATORIO", activo=True),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
    )

    # Soporte respiratorio (ManyToMany -> checkboxes)
    soporte_respiratorio = forms.ModelMultipleChoiceField(
        queryset=Catalogo.objects.filter(tipo__codigo="SOPORTE_RESPIRATORIO", activo=True),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
    )

    # Exposición pasiva (ManyToMany -> checkboxes)
    exposicion_pasiva = forms.ModelMultipleChoiceField(
        queryset=Catalogo.objects.filter(tipo__codigo="EXPOSICION_PASIVA", activo=True),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
    )

    # Otros hábitos (ManyToMany -> checkboxes)
    otros_habitos = forms.ModelMultipleChoiceField(
        queryset=Catalogo.objects.filter(tipo__codigo="HABITO_INHALATORIO", activo=True),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
    )

    # Exposiciones laborales (ManyToMany -> checkboxes)
    exposiciones_laborales = forms.ModelMultipleChoiceField(
        queryset=Catalogo.objects.filter(tipo__codigo="EXPOSICION_LABORAL", activo=True),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
    )

    class Meta:
        model = Internacion
        fields = (
            "fecha_ingreso",
            "fecha_egreso",
            "procedencia",
            "destino_egreso",
            "insuficiencia_respiratoria",
            "motivo_infeccioso",
            "motivo_obstructivo",
            "motivo_intersticial",
            "motivo_pleural",
            "motivo_vascular",
            "motivo_oncologico",
            "motivo_otro",
            "antecedentes_respiratorios",
            "soporte_respiratorio",
            "tabaquismo",
            "exposicion_pasiva",
            "otros_habitos",
            "exposiciones_laborales",
        )
        widgets = {
            "fecha_ingreso": forms.DateInput(attrs={"type": "date"}),
            "fecha_egreso": forms.DateInput(attrs={"type": "date"}),
            "tabaquismo": forms.RadioSelect(attrs={'class': 'form-check-input'}),
        }

# ==========================================================
# COMORBILIDADES E INMUNIZACIONES
# ==========================================================

class ComorbilidadesForm(BootstrapFormMixin, forms.Form):
    comorbilidades = forms.ModelMultipleChoiceField(
        queryset=Catalogo.objects.filter(tipo__codigo="COMORBILIDAD", activo=True),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    inmunizaciones = forms.ModelMultipleChoiceField(
        queryset=Catalogo.objects.filter(tipo__codigo="INMUNIZACION", activo=True),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

# ==========================================================
# ELEMENTOS DE LA INTERNACIÓN
# ==========================================================

class InternacionCatalogoForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = InternacionCatalogo
        fields = ("internacion", "catalogo")

# ==========================================================
# TRATAMIENTOS ANTIMICROBIANOS
# ==========================================================

class InternacionTratamientoAntimicrobianoForm(BootstrapFormMixin, forms.ModelForm):

    class Meta:
        model = InternacionTratamientoAntimicrobiano
        fields = (
            "antimicrobiano",
            "indicacion",
            "via",
            "fecha_desde",
            "fecha_hasta",
            "dosis",
            "observaciones",
        )
        widgets = {
            "fecha_desde": forms.DateInput(attrs={"type": "date"}),
            "fecha_hasta": forms.DateInput(attrs={"type": "date"}),
            "observaciones": forms.Textarea(attrs={"rows": 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        desde = cleaned_data.get("fecha_desde")
        hasta = cleaned_data.get("fecha_hasta")

        if desde and hasta and hasta < desde:
            self.add_error(
                "fecha_hasta",
                "La fecha hasta no puede ser anterior a la fecha desde."
            )

        return cleaned_data

# ==========================================================
# MUESTRAS MICROBIOLÓGICAS
# ==========================================================

class MuestraMicrobiologicaForm(BootstrapFormMixin, forms.ModelForm):

    class Meta:
        model = MuestraMicrobiologica
        fields = (
            "fecha_toma",
            "tipo_muestra",
            "resultado",
            "mtb_detectado",
            "resistencia_rifampicina",
        )
        widgets = {
            "fecha_toma": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["mtb_detectado"].required = False
        self.fields["resistencia_rifampicina"].required = False

# ==========================================================
# AISLAMIENTOS
# ==========================================================

class AislamientoMicrobiologicoForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = AislamientoMicrobiologico
        fields = ("germen", "significativo")

# ==========================================================
# SENSIBILIDAD
# ==========================================================

class SensibilidadMicrobiologicaForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = SensibilidadMicrobiologica
        fields = ("antibiotico", "resultado")
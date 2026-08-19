from django.db import models

class CatalogoManager(models.Manager):
    def por_tipo(self, tipo_codigo):
        return self.filter(tipo__codigo=tipo_codigo, activo=True).order_by('orden', 'descripcion')

    def motivos_infecciosos(self):
        return self.por_tipo('MOTIVO_INFECCIOSO')

    def motivos_obstructivos(self):
        return self.por_tipo('MOTIVO_OBSTRUCTIVO')

    def motivos_intersticiales(self):
        return self.por_tipo('MOTIVO_INTERSTICIAL')

    def motivos_pleurales(self):
        return self.por_tipo('MOTIVO_PLEURAL')

    def motivos_vasculares(self):
        return self.por_tipo('MOTIVO_VASCULAR')

    def motivos_oncologicos(self):
        return self.por_tipo('MOTIVO_ONCOLOGICO')

    def motivos_otros(self):
        return self.por_tipo('MOTIVO_OTROS')

    def otros_habitos_inhalatorios(self):
        return self.por_tipo('OTROS_HABITOS_INHALATORIOS')

    def exposiciones_laborales(self):
        return self.por_tipo('EXPOSICION_OCUPACIONAL')

    def exposiciones_ambientales(self):
        return self.por_tipo('EXPOSICION_AMBIENTAL')

    def soporte_respiratorio(self):
        return self.por_tipo('SOPORTE_RESPIRATORIO')

    def antecedentes_respiratorios(self):
        return self.filter(tipo__codigo='ANTECEDENTE_RESPIRATORIO', activo=True).order_by('grupo', 'orden', 'descripcion')

    def comorbilidades(self):
        return self.por_tipo('COMORBILIDAD')

    def comorbilidades_agrupadas(self):
        vasculitis_codigos = ['GPA', 'MPA', 'EGPA', 'ANCA_OTRA',
                              'PAN', 'GOODPASTURE', 'BEHCET', 'CRIOGLOBULINEMIA',
                              'IGA', 'NO_ANCA_OTRA']
        qs = self.comorbilidades().order_by('grupo', 'orden', 'descripcion')
        agrupado = {}
        for item in qs:
            if item.codigo in vasculitis_codigos:
                continue
            grupo = item.grupo or 'Sin grupo'
            agrupado.setdefault(grupo, []).append(item)
        return agrupado

    def vasculitis_anca(self):
        codigos = ['GPA', 'MPA', 'EGPA', 'ANCA_OTRA']
        return self.filter(tipo__codigo='COMORBILIDAD', codigo__in=codigos, activo=True).order_by('orden', 'descripcion')

    def vasculitis_no_anca(self):
        codigos = ['PAN', 'GOODPASTURE', 'BEHCET', 'CRIOGLOBULINEMIA', 'IGA', 'NO_ANCA_OTRA']
        return self.filter(tipo__codigo='COMORBILIDAD', codigo__in=codigos, activo=True).order_by('orden', 'descripcion')

    def reumatologicas_excluyendo_vasculitis(self):
        vasculitis_codigos = ['GPA', 'MPA', 'EGPA', 'ANCA_OTRA',
                              'PAN', 'GOODPASTURE', 'BEHCET', 'CRIOGLOBULINEMIA',
                              'IGA', 'NO_ANCA_OTRA']
        return self.filter(
            tipo__codigo='COMORBILIDAD',
            grupo='Reumatológicas',
            activo=True
        ).exclude(codigo__in=vasculitis_codigos).order_by('orden', 'descripcion')

    def inmunizaciones(self):
        return self.por_tipo('INMUNIZACION')

    def germenes(self):
        return self.por_tipo('GERMEN')

    def germenes_bacterias(self):
        return self.filter(tipo__codigo='GERMEN', activo=True, tipo_microorganismo='bacteria').order_by('orden', 'descripcion')

    def germenes_hongos(self):
        return self.filter(tipo__codigo='GERMEN', activo=True, tipo_microorganismo='hongo').order_by('orden', 'descripcion')

    def germenes_virus(self):
        return self.filter(tipo__codigo='GERMEN', activo=True, tipo_microorganismo='virus').order_by('orden', 'descripcion')

    def germenes_parasitos(self):
        return self.filter(tipo__codigo='GERMEN', activo=True, tipo_microorganismo='parasito').order_by('orden', 'descripcion')
    
       
    def germenes_por_destino(self, destino_codigo):
        if destino_codigo == 'BAC':
            return self.germenes_bacterias().exclude(descripcion__icontains='Mycobacterium')
        elif destino_codigo == 'MTB':
            return self.filter(tipo__codigo='GERMEN', codigo__in=['MTB_TBC', 'MTB_NONTB'], activo=True).order_by('orden', 'descripcion')
        elif destino_codigo == 'MIC':
            return self.germenes_hongos()
        elif destino_codigo == 'VIR':
            return self.germenes_virus()
        elif destino_codigo == 'PAR':
            return self.germenes_parasitos()
        elif destino_codigo == 'PAT':
            return self.germenes()
        else:
            return self.germenes()
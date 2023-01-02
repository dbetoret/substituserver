from django.db import models

# Create your models here.

class Centre (models.Model):
    centre = models.CharField(max_length=200)
    auth_key = models.CharField("Clau d'autorització", max_length=200)
    def __str__(self):
        return self.centre

class Usuari (models.Model):
    centre = models.ForeignKey(Centre, on_delete=models.SET_NULL, null=True, blank=True)
    login = models.CharField(max_length=200, blank=True)
    email = models.CharField(max_length=200, blank=True)
    nom = models.CharField(max_length=200)
    password = models.CharField(max_length=200, blank=True)
    auth_key = models.CharField(max_length=200, blank=True)
    def __str__(self):
        return self.nom

class Espai (models.Model):
    centre = models.ForeignKey(Centre, on_delete=models.CASCADE)
    codi_aula = models.CharField("Codi d'aula", max_length=10)
    def __str__(self):
        return self.codi_aula

class Grup (models.Model):
    centre = models.ForeignKey(Centre, on_delete=models.CASCADE)
    grup = models.CharField(max_length=10)
    def __str__(self):
        return self.grup

class Materia (models.Model):
    centre = models.ForeignKey(Centre, on_delete=models.CASCADE)
    materia = models.CharField('Matèria', max_length=200)
    def __str__(self):
        return self.materia

class Franja_horaria (models.Model):
    centre = models.ForeignKey(Centre, on_delete=models.CASCADE)
    dia_setmana = models.CharField('Dia de la setmana', max_length=2)
    ndia_setmana = models.IntegerField(default=0)
    hinici = models.TimeField("Hora d'inici")
    hfinal = models.TimeField("Hora d'acabament")
    es_pati = models.BooleanField("És hora d'esplai?")
    def __str__(self):
        return self.dia_setmana+' '+str(self.hinici)

class Horari (models.Model):
    usuari = models.ForeignKey(Usuari, on_delete=models.CASCADE)
    hora = models.ForeignKey(Franja_horaria, on_delete=models.CASCADE)
    espai = models.ForeignKey(Espai, on_delete=models.SET_NULL, null=True, blank=True)
    grup = models.ForeignKey(Grup, on_delete=models.SET_NULL, null=True, blank=True)
    materia = models.ForeignKey(Materia, on_delete=models.SET_NULL, null=True, blank=True)
    es_guardia = models.BooleanField("És una guàrdia?")
    def __str__(self):
        return self.usuari.nom+' '+str(self.hora)[:8]

class Absencia (models.Model):
    usuari = models.ForeignKey(Usuari, on_delete=models.CASCADE)
    data = models.DateField("Data d'inici")
    data_fi = models.DateField("Data d'acabament", null=True, blank=True)
    hora_ini = models.TimeField("Hora d'inici", null=True, blank=True)
    hora_fi = models.TimeField("Hora d'acabament", null=True, blank=True)
    dia_complet = models.BooleanField("És absència de tota la jornada?")
    extraescolar = models.BooleanField("Es deu a una activitat extraescolar?")
    justificada = models.BooleanField("S'ha justificat l'absència?")
    def __str__(self):
        return self.usuari.nom+' '+str(self.data)


class Guardia (models.Model):
    horari = models.ForeignKey(Horari, on_delete=models.CASCADE)
    absencia = models.ForeignKey(Absencia, on_delete=models.CASCADE)
    data = models.DateField('Data')
    substitut = models.ForeignKey(Usuari, on_delete=models.CASCADE, null=True, blank=True)
    feina = models.CharField('Feina deixada pel professor titular',max_length=200)
    def __str__(self):
        return str(self.data)+' '+str(self.horari.hora)[:5]+' '+self.horari.usuari.nom

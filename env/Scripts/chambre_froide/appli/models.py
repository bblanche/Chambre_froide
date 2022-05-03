from django.db import models

class ChargeExternes(models.Model):
    longueur = models.FloatField(max_length = 999999)
    largeur = models.FloatField(max_length = 999999)
    hauteur = models.FloatField(max_length = 999999)
    degre = models.FloatField(max_length = 999999)
    typeIsolant = models.FloatField(max_length = 999999)
    typeEntrepot = models.CharField(max_length = 999999)
    region = models.CharField(max_length = 999999)
    chargeExterneMurNordEtSud = models.FloatField(max_length = 999999)
    chargeExterneMurOuestEtEst = models.FloatField(max_length = 999999)
    chargeExternePlafond = models.FloatField(max_length = 999999)
    chargeExternePlancher = models.FloatField(max_length = 999999)
    surfaceNordEtSud = models.FloatField(max_length = 999999)
    surfaceOuestEtEst = models.FloatField(max_length = 999999)
    surfacePlancherEtPlafond = models.FloatField(max_length = 999999)
    temperatureInterieure = models.FloatField(max_length = 999999)
    KmurEtPlafond = models.FloatField(max_length = 999999)
    Kplancher = models.FloatField(max_length = 999999)
    temperatureExterieure = models.FloatField(max_length = 999999)
    coeffConductivite = models.FloatField(max_length = 999999)
    epaisseurIsolant = models.FloatField(max_length = 999999)
    apportParTransmissionATraversLesParois = models.FloatField(max_length = 999999)
    volume = models.FloatField(max_length = 999999)
    apportParRenouvellementDAir = models.FloatField(max_length = 999999)
    nombreRenouvellementDAir = models.FloatField(max_length = 999999)
    totalChargeExternes = models.FloatField(max_length = 9999999999999)

class ChargeInternes(models.Model):
    chargeExternes = models.ForeignKey(ChargeExternes, on_delete = models.CASCADE)
    dureeMoyenneDOccupationParLePersonnel = models.FloatField(max_length = 999999)
    nombrePersonnesPresentesCF = models.FloatField(max_length = 999999)
    qteChaleurDegageeParUnePersonne = models.FloatField(max_length = 999999)
    masseDenree = models.FloatField(max_length = 999999)
    temperatureIntroductionDenree = models.FloatField(max_length = 999999)
    apportRespirationDenrees = models.FloatField(max_length = 999999)
    chargesDuEclairage = models.FloatField(max_length = 999999)
    chargesDuPersonnes = models.FloatField(max_length = 999999)
    apportDuDenreesEntrantes = models.FloatField(max_length = 999999)
    totalChargeInternes = models.FloatField(max_length = 999999)

class PuissanceFrigorifique(models.Model):
    chargeInternes = models.ForeignKey(ChargeInternes, on_delete = models.CASCADE)
    chargeFrigorifiqueIntermediaire = models.FloatField(max_length = 999999)
    dureeJournaliereFonctionnementInstallation = models.FloatField(max_length = 999999)
    puissanceFrigorifiqueIntermediaireEvaporateur = models.FloatField(max_length = 999999)
    puissanceEffectiveEvaporateur = models.FloatField(max_length = 999999)

 #   isolant = models.FloatField()
  #  coefConductivité = models.IntegerField()
    
   # def __str__(self):
    #    return f"{self.pk} {self.patient}"
    
    #def get_absolute_url(self):
     #   return reverse('management:payment_receipt_cashier', kwargs={
      #      'pk': self.pk
       # })
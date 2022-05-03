from cmath import e, sqrt
from django.shortcuts import render
from django.db import transaction, IntegrityError
import math

from appli.models import ChargeExternes, ChargeInternes, PuissanceFrigorifique

coefConductivites = [0.044, 0.025, 0.029, 0.035, 0.03, 0.093, 0.031, 0.054, 0.032] 
temperatureExterieures = [
    [29, 69, 'Adamaoua'],
    [27, 76, 'Centre'],
    [33, 60, 'Est'],
    [36, 46, 'Extreme-Nord'],
    [31, 83, 'Littoral'],
    [35, 56, 'Nord'],
    [31, 76, 'Nord-Ouest'],
    [27, 74, 'Ouest'],
    [29, 85, 'Sud'],
    [30, 82, 'Sud-Est']
]
regions = ['Adamaoua', 'Centre', 'Est', 'Extreme-Nord', 'Littoral', 'Nord', 'Nord-Ouest', 'Ouest', 'Sud', 'Sud-Est']

# Create your views here.
def index(request):
    puissanceFrigorifiques = PuissanceFrigorifique.objects.all()
    chargesInternes = ChargeInternes.objects.all()
    chargesExternes = ChargeExternes.objects.all()
    context = {
        'chargesInternes':chargesInternes,
        'chargesExternes':chargesExternes,
        'puissancesFrigorifiques':puissanceFrigorifiques
    }
    if request.method == 'POST':
        chargeExternesForm=request.POST.get("chargeExternes")
        chargeInternesForm=request.POST.get("chargeInternes")
        puissanceFrigorifiqueForm=request.POST.get("pFrigorifique")
        context = {'chargeExternesForm':chargeExternesForm}
        if chargeExternesForm == "True" :
            try:
                with transaction.atomic():
                    region = request.POST.get('region')
                    temperatureInt = request.POST.get('temperatureInterieure')
                    degre = request.POST.get('degre')
                    typeIsolant = request.POST.get('typeIsolant')
                    long = request.POST.get('longueur')
                    larg = request.POST.get('largeur')
                    haut = request.POST.get('hauteur')
                    typeEntrepot = request.POST.get('TypeEntrepot')

                    longueur = int(long)
                    largeur = int(larg)
                    hauteur = int(haut)
                    volume = longueur * largeur * hauteur
                    surfaceNordEtSud = hauteur * longueur
                    surfaceOuestEtEst = hauteur * largeur
                    surfacePlancherEtPlafond = largeur * longueur
                    temperatureInterieure = int(temperatureInt)
                    temperatureExterieure = temperatureExterieures[int(region) - 1][0]
                    lamdaIsolant = coefConductivites[int(typeIsolant) - 1]
                    
                    diffTemperature = temperatureExterieure - temperatureInterieure
                    e = lamdaIsolant * diffTemperature / 8
                    KmurEtPlafond = 1 / (0.09 + e / lamdaIsolant)
                    Kplancher = 1 / (0.06 + e / lamdaIsolant)

                    chargeExterneMurNordEtSud = KmurEtPlafond * surfaceNordEtSud * diffTemperature
                    chargeExterneMurOuestEtEst = KmurEtPlafond * surfaceOuestEtEst * diffTemperature
                    chargeExternePlafond = KmurEtPlafond * surfacePlancherEtPlafond * diffTemperature
                    if typeEntrepot == "entrepotAvecSousSol":
                        chargeExternePlancher = Kplancher * surfacePlancherEtPlafond * diffTemperature
                    else:
                        chargeExternePlancher = Kplancher * surfacePlancherEtPlafond * (15 - temperatureInterieure)
                    
                    apportParTransmissionATraversLesParois = chargeExterneMurNordEtSud + chargeExterneMurOuestEtEst + chargeExternePlafond + chargeExternePlancher
                    apportParRenouvellementDAir = 20.55 * math.sqrt(volume) / (273 + temperatureInterieure)
                    nombreRenouvellementDAir = 70 / math.sqrt(volume)
                    totalChargeExternes = apportParTransmissionATraversLesParois + apportParRenouvellementDAir
                    ChargeExternes.objects.create(
                            
                        longueur = longueur,
                        largeur = largeur,
                        hauteur = hauteur,
                        degre = degre,
                        typeIsolant = typeIsolant,
                        typeEntrepot = typeEntrepot,
                        region = regions[int(region) - 1],
                        chargeExterneMurNordEtSud = chargeExterneMurNordEtSud,
                        chargeExterneMurOuestEtEst = chargeExterneMurOuestEtEst,
                        chargeExternePlafond = chargeExternePlafond,
                        chargeExternePlancher = chargeExternePlancher,
                        surfaceNordEtSud = surfaceNordEtSud,
                        surfaceOuestEtEst = surfaceOuestEtEst,
                        surfacePlancherEtPlafond = surfacePlancherEtPlafond,
                        temperatureInterieure = temperatureInterieure,
                        KmurEtPlafond = KmurEtPlafond,
                        Kplancher = Kplancher,
                        temperatureExterieure = temperatureExterieure,
                        coeffConductivite = lamdaIsolant,
                        epaisseurIsolant = e,
                        apportParTransmissionATraversLesParois = apportParTransmissionATraversLesParois,
                        apportParRenouvellementDAir = apportParRenouvellementDAir,
                        volume = volume,
                        nombreRenouvellementDAir = nombreRenouvellementDAir, 
                        totalChargeExternes = totalChargeExternes
                    )

                    chargeExternes = ChargeExternes.objects.last()
                    context = {
                        'chargeExternes':chargeExternes,
                        'chargesInternes':chargesInternes,
                        'chargesExternes':chargesExternes,
                        'puissancesFrigorifiques':puissanceFrigorifiques
                    }
            except Exception as e :
                print (e)
                print ('charges externes')
                context = {
                        'error':e,
                        'chargesInternes':chargesInternes,
                        'chargesExternes':chargesExternes,
                        'puissancesFrigorifiques':puissanceFrigorifiques
                    }
            return render(request, 'appli/index.html', context)


        if chargeInternesForm == "True" :
            
                    
                    dureeMoyenneDOccupationParLePersonnel = request.POST.get('DureeMoyenneDOccupationParLePersonnel')
                    nombrePersonnesPresentesCF = request.POST.get('nombrePersonnesPresentesCF')
                    
                    masseDenree = request.POST.get('masseDenree')
                    temperatureIntroductionDenree = request.POST.get('temperatureIntroductionDenree')

                    dureeMoyenneDOccupationParLePersonnel = int(dureeMoyenneDOccupationParLePersonnel)
                    nombrePersonnesPresentesCF = int(nombrePersonnesPresentesCF)
                    qteChaleurDegageeParUnePersonne = 420
                    masseDenree = int(masseDenree)
                    temperatureIntroductionDenree = int(temperatureIntroductionDenree)

                    chargeExternes = ChargeExternes.objects.last()
                    surfacePlancher = chargeExternes.surfacePlancherEtPlafond
                    surfacePlancher = float(surfacePlancher)
                    temperatureInterieure = chargeExternes.temperatureInterieure
                    temperatureInterieure = float(temperatureInterieure)

                    chargesDuPersonnes = nombrePersonnesPresentesCF * dureeMoyenneDOccupationParLePersonnel * qteChaleurDegageeParUnePersonne / 24
                    chargesDuEclairage = (0.6 + 0.225 * dureeMoyenneDOccupationParLePersonnel) * surfacePlancher
                    apportDuDenreesEntrantes = 0.0116 * masseDenree * (268.5 - 1.74 * (2.2 + temperatureInterieure))
                    totalChargeInternes = chargesDuPersonnes + chargesDuEclairage + apportDuDenreesEntrantes

                    ChargeInternes.objects.create(
                        chargeExternes = chargeExternes,
                        dureeMoyenneDOccupationParLePersonnel = dureeMoyenneDOccupationParLePersonnel,
                        nombrePersonnesPresentesCF = nombrePersonnesPresentesCF,
                        qteChaleurDegageeParUnePersonne = qteChaleurDegageeParUnePersonne,
                        masseDenree = masseDenree,
                        temperatureIntroductionDenree = temperatureIntroductionDenree,
                        apportRespirationDenrees = 0,
                        chargesDuEclairage = chargesDuEclairage,
                        chargesDuPersonnes = chargesDuPersonnes,
                        apportDuDenreesEntrantes = apportDuDenreesEntrantes,
                        totalChargeInternes = totalChargeInternes
                    )
                    chargeInternes = ChargeInternes.objects.last()
                    
                    context = {
                        'chargeInternes':chargeInternes,
                        'chargeExternes':chargeExternes,
                        'chargesInternes':chargesInternes,
                        'chargesExternes':chargesExternes,
                        'puissancesFrigorifiques':puissanceFrigorifiques
                    }
            
                    return render(request, 'appli/index.html', context)

   
        if puissanceFrigorifiqueForm == "True" :
            try:
                with transaction.atomic():
                    dureeJournaliereFonctionnementInstallation = request.POST.get('dureeJournaliereFonctionnementInstallation')
                    dureeJournaliereFonctionnementInstallation = float(dureeJournaliereFonctionnementInstallation)

                    chargeInternes = ChargeInternes.objects.last()
                    chargeExternes = chargeInternes.chargeExternes
                    
                    totalChargeExternes = chargeExternes.totalChargeExternes
                    totalChargeInternes =  chargeInternes.totalChargeInternes
                    

                    chargeFrigorifiqueIntermediaire = float(totalChargeExternes) + float(totalChargeInternes)
                    puissanceFrigorifiqueIntermediaireEvaporateur = chargeFrigorifiqueIntermediaire * 24 / dureeJournaliereFonctionnementInstallation
                    puissanceEffectiveEvaporateur = 1.2 * puissanceFrigorifiqueIntermediaireEvaporateur

                    PuissanceFrigorifique.objects.create(
                        chargeInternes = chargeInternes,
                        chargeFrigorifiqueIntermediaire = chargeFrigorifiqueIntermediaire,
                        dureeJournaliereFonctionnementInstallation = dureeJournaliereFonctionnementInstallation,
                        puissanceFrigorifiqueIntermediaireEvaporateur = puissanceFrigorifiqueIntermediaireEvaporateur,
                        puissanceEffectiveEvaporateur = puissanceEffectiveEvaporateur,
                    )

                    puissanceFrigorifique = PuissanceFrigorifique.objects.last()
                    context = {
                        'chargeInternes':chargeInternes,
                        'chargeExternes':chargeExternes,
                        'puissanceFrigorifique':puissanceFrigorifique,
                        'chargesInternes':chargesInternes,
                        'chargesExternes':chargesExternes,
                        'puissancesFrigorifiques':puissanceFrigorifiques
                    }
            except Exception as e :
                print (e)
                print ('charges internes')
                context = {
                        'error':e,
                        'chargesInternes':chargesInternes,
                        'chargesExternes':chargesExternes,
                        'puissancesFrigorifiques':puissanceFrigorifiques
                    }
            return render(request, 'appli/index.html', context)
            
    return render(request, 'appli/index.html', context)
               

def liste(request):
    puissanceFrigorifiques = PuissanceFrigorifique.objects.all()
    chargesInternes = ChargeInternes.objects.all()
    chargesExternes = ChargeExternes.objects.all()
    context = {
        'chargeInternes':chargesInternes,
        'chargeExternes':chargesExternes,
        'puissanceFrigorifiques':puissanceFrigorifiques
    }
    return render(request, 'appli/details.html', context)
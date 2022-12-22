from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta, date
import json

from .models import Usuari, Espai, Grup, Materia, Horari, Absencia, Guardia, Franja_horaria, Centre

# Create your views here.

def index(request):
    return HttpResponse("Hola, index!!")

@csrf_exempt
def login(request):
    # input: usuari
    # output: espais, grups, materies, horari
    print ('Petició', request)
    print ('Petició de login: ', request.body)
    print (' Petició del usuari: ',request.headers['Authorization'])
    # a_put = json.loads(request.body)
    # if request.method == 'POST':
    #     insert_usuari(request)
    # if request.method == 'GET':
    return dades_mestres(request)


@csrf_exempt
def insert_usuari(request):
    print (' Petició del usuari: ',request.headers['Authorization'])
    put_param = json.loads(request.body)
    u = Usuari()
    u.nom = put_param["name"]
    # u.password
    # u.email
    u.centre = Centre.objects.filter(id=1)
    u.save()
    resposta = {}
    return JsonResponse(resposta)

@csrf_exempt
def dades_mestres(request):
    print (' Petició del usuari: ',request.headers['Authorization'])
    #put_param = json.loads(request.body)
    # u = Usuari.objects.get(email=request.GET["user"])
    u = Usuari.objects.get(id=request.headers["authorization"])
    if 0: # put_param["password"] != u.password:
        print ("no")
        return False
    else:
        espais = {}
        for e in Espai.objects.filter(centre_id=u.centre.id):
            espais[e.id] = e.codi_aula
        grups = {}
        for g in Grup.objects.filter(centre_id=u.centre.id):
            grups[g.id] = g.grup
        materies = {}
        for m in Materia.objects.filter(centre_id=u.centre.id):
            materies[m.id] = m.materia
        franges_horaries = {}
        for fh in Franja_horaria.objects.filter(centre_id=u.centre.id):
            franges_horaries[fh.id] = {
                'id': fh.id,
                'dia_setmana': fh.dia_setmana,
                'ndia_setmana': fh.ndia_setmana,
                'hinici': str(fh.hinici)[:5],
                'hfinal': str(fh.hfinal)[:5],
                'es_pati': fh.es_pati
            }
        horari = {}
        for h in Horari.objects.filter(usuari_id=u.id):
            horari[h.id] = {
                'id_franja': h.hora.id,
                'dia_setmana': h.hora.dia_setmana,
                'hora': str(h.hora.hinici)[:5],
                'espai_id': h.espai_id,
                'grup_id': h.grup_id,
                'materia_id': h.materia_id,
                'es_guardia': h.es_guardia
            }
        resposta = {
            'usuari_id': u.id,
            'usuari_nom': u.nom,
            'centre_id': u.centre_id,
            'centre_nom': u.centre.centre,
            'espais': espais, 
            'grups': grups, 
            'materies': materies, 
            'franges_horaries': franges_horaries,
            'horari': horari
        }
        return JsonResponse(resposta)


@csrf_exempt
def Absencies(request):
    print (' Petició del usuari: ',request.headers['Authorization'])
    print(request.method)
    if request.method == 'GET':
        return getAbsencies(request)
    if request.method == 'POST' or request.method == 'PUT':
        return putAbsencia(request)

@csrf_exempt
def getAbsencies(request):
    print (' Petició del usuari: ',request.headers['Authorization'])
    # input: usuari
    # output: absencies "propies", guardies "propies" i "del dia"
    ds = ['NO','DI','DM','DC','DJ','DV','DS','DG']
    absencies = []
    for a in Absencia.objects.filter(usuari_id=request.headers['Authorization']):
        classes = []
        for g in Guardia.objects.filter(absencia_id=a.id):
            classes.append( {
                'data': g.data.strftime("%Y-%m-%d"),
                'hinici': str(g.horari.hora.hinici)[:5],
                'dia_setmana': g.horari.hora.dia_setmana,
                'espai': g.horari.espai.codi_aula,
                'grup': g.horari.grup.grup,
                'materia': g.horari.materia.materia,
                'substitut': g.substitut_id,
                'feina': g.feina
            } )            
        absencies.append( {
            'id': a.id,
            'data': a.data.strftime("%Y-%m-%d"),
            'data_fi': a.data_fi.strftime("%Y-%m-%d"),
            'hora_ini': str(a.hora_ini)[:5],
            'hora_fi': str(a.hora_fi)[:5],
            'dia_complet': a.dia_complet,
            'extraescolar': a.extraescolar,
            'justificada': a.justificada,
            'guardies': classes
        } )
        # if a.dia_complet:
        #     data = a.data
        #     while data <= a.data_fi:
        #         if a.data.weekday() in range(1,6):
        #             dia_sem = ds[a.data.weekday()]

        #         data = data + 1
        # else:
        #     asdf
        

    return JsonResponse(absencies, safe=False)

@csrf_exempt
def putAbsencia(request):
    print (' Petició del usuari: ',request.headers['Authorization'])
    a_put = json.loads(request.body)
    print(request.body)
    d_ini = datetime.strptime(a_put["data"], "%Y-%m-%d").date()
    d_fi = datetime.strptime(a_put["data_fi"], "%Y-%m-%d").date()
    if a_put["id"] == -1:
        a_bd = Absencia()
        a_bd.justificada = False
        a_bd.usuari_id = request.headers['Authorization']
    else:
        # por usuario_id + fecha sólo tiene que haber 1 registro.
        a_bd = Absencia.objects.filter(usuari_id = request.headers['Authorization'], id = a_put["id"])[0]
    a_bd.data = d_ini
    a_bd.data_fi = d_fi
    if d_ini != a_bd.data and a_bd.data > date.today() and d_ini > date.today():
        # no podemos modificar ausencias pasadas.
        a_bd.data = d_ini
    if d_fi > d_ini and d_fi > date.today():
        a_bd.data_fi = d_fi
    a_bd.dia_complet = a_put["dia_complet"]
    a_bd.extraescolar = a_put["extraescolar"]
    a_bd.save()

    # Recalculem les guàrdies. No podem borrar i re-generar perquè podrien haver tasques assignades
    # o professors assignats o guàrdies fetes.

    (to_insert, to_delete) = inserta_guardies(a_bd.id)

    return JsonResponse({'id': a_bd.id, 'to_insert': to_insert, 'to_delete': to_delete }, safe=False, content_type='application/json')

@csrf_exempt
def guards(request):
    print (' Petició del usuari: ',request.headers['Authorization'])
    guardies = []
    if request.method == 'GET':
        # hg: hores en les que l'usuari té guàrdia.
        # g: guàrdies del centre que coincideixen amb l'hora de guàrdia hg.
        for hg in Horari.objects.filter(usuari_id=request.headers['Authorization'], es_guardia=True):
            print ("hora de guardia: ")
            for g in Guardia.objects.filter( horari__hora_id=hg.hora_id):
                print ("premi. guàrdia el ", g.data.strftime("%Y-%m-%d"), ' a les ',str(hg.hora.hinici))
                guardies.append( {
                    'data': g.data.strftime("%Y-%m-%d"),
                    'dia': str(hg.hora.dia_setmana),
                    'hora': str(hg.hora.hinici),
                    'professor': g.horari.usuari.nom,
                    'espai': g.horari.espai.codi_aula,
                    'grup': g.horari.grup.grup,
                    'materia': g.horari.materia.materia,
                    'es_guardia': g.horari.es_guardia,
                    'substitut': g.substitut,
                    'feina': g.feina
                } )
    else:
        pass
    print('vaig a retornar guardies ',guardies)
    return JsonResponse(guardies, safe=False)

def guards_by_id(request):
    # Permet carregar les guàrdies d'una absència determinada.
    pass

def guards_by_date(request):
    # Permte carregar les guàrdies d'una data determinada.
    # En futur, esta funció carregarà les d'avui.
    pass

@csrf_exempt
def updateGrups(request):
    print (' Petició del usuari: ',request.headers['Authorization'])
    gput = json.loads(request.body)
    print (str(gput))
    centre = Centre.objects.get(id = 1)
    meus_grups = Grup.objects.filter(centre_id = 1)
    for g in gput:
        print (g)
        if g[0][0] == '-':
            ngrup = Grup(centre=centre, grup=g[1])
            print ('creat el grup ', g[1])
            ngrup.save()
        else:
            try:
                wgrup = meus_grups.get(id=g[0])
                if wgrup.grup != g[1]:
                    wgrup.grup = g[1]
                    wgrup.save()
                    print ('canviat nom de gurp a ', g[1])
            except:
                print ('error en carregar el grup amb id ', g[0], ' i nom ', g[1])
    response_data = {}
    response_data['result'] = 'ok'
    response_data['message'] = 'everything is gonna be ok.'
    return JsonResponse(response_data, content_type='application/json')

@csrf_exempt
def updateEspais(request):
    print (' Petició del usuari: ',request.headers['Authorization'])
    vput = json.loads(request.body)
    # print (str(gput))
    centre = Centre.objects.get(id = 1)
    meus_elem = Espai.objects.filter(centre_id = 1)
    for g in vput:
        print (g)
        if g[0][0] == '-':
            nou = Espai(centre=centre, codi_aula=g[1])
            print ('creat lespai ', g[1])
            nou.save()
        else:
            try:
                welem = meus_elem.get(id=g[0])
                if welem.codi_aula != g[1]:
                    welem.codi_aula = g[1]
                    welem.save()
                    print ('canviat nom de espai a ', g[1])
            except:
                print ('error en carregar lespai amb id ', g[0], ' i nom ', g[1])
    response_data = {}
    response_data['result'] = 'ok'
    response_data['message'] = 'everything is gonna be ok.'
    return JsonResponse(response_data, content_type='application/json')

@csrf_exempt
def updateMateries(request):
    print (' Petició del usuari: ',request.headers['Authorization'])
    vput = json.loads(request.body)
    # print (str(gput))
    centre = Centre.objects.get(id = 1)
    meus_elem = Materia.objects.filter(centre_id = 1)
    for g in vput:
        print (g)
        if g[0][0] == '-':
            nou = Materia(centre=centre, materia=g[1])
            print ('creada la materia ', g[1])
            nou.save()
        else:
            try:
                welem = meus_elem.get(id=g[0])
                if welem.materia != g[1]:
                    welem.materia = g[1]
                    welem.save()
                    print ('canviat nom de materia a ', g[1])
            except:
                print ('error en carregar la materia amb id ', g[0], ' i nom ', g[1])
    response_data = {}
    response_data['result'] = 'ok'
    response_data['message'] = 'everything is gonna be ok.'
    return JsonResponse(response_data, content_type='application/json')

@csrf_exempt
def updateHorari(request, id_horari):
    print (' Petició del usuari: ',request.headers['Authorization'])
    valors = json.loads(request.body)
    print(valors, ' per al horari ', id_horari)
    try:
        horari = Horari.objects.get(usuari_id=request.headers['Authorization'], hora_id=id_horari)
    except Horari.DoesNotExist:
        print ('L horari ', id_horari, ' no existeix')
        horari = Horari(
            usuari = Usuari.objects.get(id=request.headers['Authorization']),
            hora = Franja_horaria.objects.get(id=id_horari)
        )
    except:
        print ('errors amb horari')
        return
    
    horari.es_guardia = valors['es_guardia']
    if horari.es_guardia == False:
        horari.espai = Espai.objects.get(id=valors['espai_id'])
        horari.grup = Grup.objects.get(id=valors['grup_id'])
        horari.materia = Materia.objects.get(id=valors['materia_id'])
    else:
        horari.espai = None
        horari.grup = None
        horari.materia = None
    horari.save()
    response_data = {}
    response_data['result'] = 'ok'
    response_data['message'] = 'everything is gonna be ok.'
    return JsonResponse(response_data, content_type='application/json')


def edit(request):
    print (' Petició del usuari: ',request.headers['Authorization'])
    # tipus: inserció, modificació, esborrat
    # taula: franja_horaria, materia, usuari, espai, grup, 
    # absència s'insertarà amb funció diferent, 
    # guardia no s'hauria de gestionar per se.
    usuari_id = request.headers['Authorization']
    
    return JsonResponse()

def inserta_absència(usuari ):
    # Comprova l'horari de l'usuari.
    # Comprova els dies de la setmana de l'absència.
    # Inserta totes les guàrdies corresponents
    pass

def inserta_guardies(abs_id):
    to_insert = {}
    to_delete = [] # llista de id_guardia a eliminar
    dies_setmana = ['DL','DM','DC','DJ','DV','DS','DG']
    # Comprovem les guardies que hi ha
    guardies = Guardia.objects.filter(absencia_id = abs_id)
    les_que_hi_ha = {}
    for g in guardies:
        les_que_hi_ha[g.data.strftime("%Y-%m-%d")+str(g.horari_id)] = False
    # Comprovem les que deuria haver. Si ja estàn, les marquem "true"
    # Si no estan, les insertem.
    abs = Absencia.objects.filter(id = abs_id)[0]
    if abs.data_fi < abs.data:
        return
    for delta in range((abs.data_fi-abs.data).days+1):
        d = abs.data+timedelta(days=delta)
        for h in Horari.objects.filter(hora__dia_setmana=dies_setmana[d.weekday()], usuari=abs.usuari, es_guardia=False ):
            if str(d)+str(h.id) not in les_que_hi_ha:
                ng = Guardia(horari=h, absencia=abs, data=d, feina='')
                ng.save()
                to_insert[ng.id]={horari: h, id_absencia: abs.id, data: d, feina: ''}
    for g in guardies:
        if not les_que_hi_ha[g.data.strftime("%Y-%m-%d")+str(g.horari_id)]:
            to_delete.append[g.id]
            g.delete()
    return (to_insert, to_delete)
    

# Obsoletes

def getGuardiesDICT(request):
    guardies = {}
    for hg in Horari.objects.filter(usuari_id=1, es_guardia=True):
        for g in Guardia.objects.filter(horari__hora_id=hg.hora_id):
            if str(g.data) not in guardies:
                guardies[str(g.data)]={}
            if str(hg.hora.hinici) not in guardies[str(g.data)]:
                guardies[str(g.data)][str(hg.hora.hinici)] = {}
            if g.horari.usuari.nom not in guardies[str(g.data)][str(hg.hora.hinici)]:
                guardies[str(g.data)][str(hg.hora.hinici)][g.horari.usuari.nom] = {}
            guardies[str(g.data)][str(hg.hora.hinici)][g.horari.usuari.nom] = {
                'data': str(g.data)+'1',
                'dia_setmana': str(hg.hora.dia_setmana),
                'hora': str(hg.hora.hinici),
                'professor': g.horari.usuari.nom,
                'espai': g.horari.espai_id,
                'grup': g.horari.grup_id,
                'materia': g.horari.materia_id,
                'substitut': g.substitut_id,
                'feina': g.feina
            }
    return JsonResponse({'data': guardies})


def getAbsenciesDICT(request):
    # input: usuari
    # output: absencies "propies", guardies "propies" i "del dia"
    ds = ['NO','DI','DM','DC','DJ','DV','DS','DG']
    absencies = {}
    for a in Absencia.objects.filter(usuari_id=1):
        absencies[str(a.data)] = {
            'data': str(a.data),
            'data_fi': str(a.data_fi),
            'hora_ini': str(a.hora_ini),
            'hora_fi': str(a.hora_fi),
            'dia_complet': a.dia_complet,
            'extraescolar': a.extraescolar,
            'justificada': a.justificada,
            'classes': {}
        }
        # if a.dia_complet:
        #     data = a.data
        #     while data <= a.data_fi:
        #         if a.data.weekday() in range(1,6):
        #             dia_sem = ds[a.data.weekday()]

        #         data = data + 1
        # else:
        #     asdf
        for g in Guardia.objects.filter(absencia_id=a.id):
            if str(g.data) not in absencies[str(a.data)]['classes']:
                absencies[str(a.data)]['classes'][str(g.data)] = {}
            absencies[str(a.data)]['classes'][str(g.data)][str(g.horari.hora.hinici)] = {
                'hinici': str(g.horari.hora.hinici),
                'dia_setmana': g.horari.hora.dia_setmana,
                'espai': g.horari.espai_id,
                'grup': g.horari.grup_id,
                'materia': g.horari.materia_id,
                'substitut': g.substitut_id,
                'feina': g.feina
            }

    return JsonResponse([absencies], safe=False)
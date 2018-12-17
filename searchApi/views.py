# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.views.generic import View

from  .models import Uf, Dolar, Tmc

import json
import datetime
import requests

API_BASE = 'https://api.sbif.cl/api-sbifv3/recursos_api/'
API_KEY = '98122fe900c9221a9a085b7ca16cc123bbd9f6c7'
FORMAT = 'json'

class ApiConsulta(View):

    def dispatch(self, request, *args, **kwargs):
        return super(ApiConsulta, self).dispatch(request, *args, **kwargs)
    
    def get_api(self, request):
        context = {}
        response = requests.get(API_BASE+'uf/?apikey='+API_KEY+'&formato='+FORMAT).json()
        response_dolar = requests.get(API_BASE+'dolar?apikey='+API_KEY+'&formato='+FORMAT).json()
        data = response
        data_dolar = response_dolar
        context['uf'] = data['UFs']
        context['dolarDia'] = data_dolar['Mensaje'] if data_dolar['CodigoError'] else data_dolar['Dolares']
        context['time'] =  datetime.datetime.now()
        context['desde'] = datetime.datetime.now().strftime('%d/%m/%Y')
        context['hasta'] = datetime.datetime.now().strftime('%d/%m/%Y')
        return context

    def get(self, request, *args, **kwargs):
        return render(request, 'searchApi/detalles.html', self.get_api(request))

    def post(self, request, *args, **kwargs):
        context=self.get_api(request)
        data = request.POST
        filter_ = request.POST.get('filter',None)
        desde = request.POST.get('desde',None)
        desde_ = datetime.datetime.strptime(desde, "%Y-%m-%d") if desde else None
        hasta = request.POST.get('hasta',None)
        hasta_ = datetime.datetime.strptime(hasta, "%Y-%m-%d") if hasta else None
        context['desde'] = desde_
        context['hasta'] = hasta_

        if filter_ == 'uf':
            if desde and hasta:
                consulta = Uf.objects.filter(date__gte = desde_, date__lte = hasta_)
                if consulta:
                    context['uf_bd'] = consulta
                else:
                    self.get_uf_range(desde_, hasta_, context, filter_)
                    if context['ufs']:
                        for uf in context['uf']['UFs']:
                            nueva_uf = Uf()
                            nueva_uf.uf = uf['Valor']
                            nueva_uf.date = uf['Fecha']
                            nueva_uf.save()
                
                
            elif desde:
                print('desde_', desde)
                self.get_uf_from(filter_,desde_, context)

            elif hasta:
                print('hasta_', hasta)
                self.get_uf_to(filter_,hasta_, context)
            
    
        return render(request, 'SearchApi/detalles.html', context)

    def max_uf(self,uf_list):
        max_val = max(uf_list,key=lambda item:item['Valor'])
        return max_val
    
    def min_uf(self,uf_list):
        min_val = min(uf_list,key=lambda item:item['Valor'])
        return min_val

    def promedio_uf(self,uf_list):
        valores_uf_list = [x['Valor'].replace(".", '').replace(',','.') for x in uf_list]
        sumatoria = sum([float(x) for x in valores_uf_list])
        media = (sumatoria/len(valores_uf_list))
        return "{0:.2f}".format(media)

    def max_dolar(self,dolar_list):
        max_val = max(dolar_list,key=lambda item:item['Valor'])
        return max_val
    
    def min_dolar(self,dolar_list):
        min_val = min(dolar_list,key=lambda item:item['Valor'])
        return min_val

    def promedio_dolar(self,dolar_list):
        valores_dolar = [x['Valor'].replace(".", '').replace(',','.') for x in dolar_list]
        sumatoria = sum([float(x) for x in valores_dolar])
        media = (sumatoria/len(valores_dolar))
        return "{0:.2f}".format(media)

    def get_dolar(self, fecha):
        fecha_ = datetime.datetime.strptime(fecha, "%Y-%m-%d") if fecha else None
        if fecha_:
            try:
                response = requests.get(API_BASE+'dolar/'+str(fecha_.year)+"/"+str(fecha_.month)+"/dias/"+str(fecha_.day)+"?apikey="+API_KEY+"&formato="+ FORMAT)
                if response:
                    dolar =response.json()
                    return dolar['Dolares'][0]
                else:
                    return {'Valor':'No Disponible', 'Fecha': 'No Disponible'}
            except Exception as e:
                print(e)


    def get_uf_to(self,filter_, hasta_, context):
        try:
            response = requests.get(API_BASE+filter_+"/anteriores/"+str(hasta_.year)+"/"+str(hasta_.month)+"/dias/"+str(hasta_.day)+"?apikey="+API_KEY+"&formato="+ FORMAT)
            if response:
                if response:
                    uf_list =response.json()
                    max_uf = self.max_uf(uf_list['UFs'])
                    context['max_uf'] = max_uf
                    min_uf = self.min_uf(uf_list['UFs'])
                    context['min_uf'] = min_uf
                    context['uf'] = uf_list
                    dolar= requests.get(API_BASE+"dolar/anteriores/"+str(hasta_.year)+"/"+str(hasta_.month)+"/"+str(hasta_.day)+"?apikey="+API_KEY+"&formato="+ FORMAT).json()
                    
                    max_dolar = self.max_dolar(dolar['Dolares'])
                    context['max_dolar'] = max_dolar
                    min_dolar = self.min_dolar(dolar['Dolares'])
                    context['min_dolar'] = min_dolar
                    context['dol'] = dolar
                    dolares = [self.get_dolar(x['Fecha']) for x in uf_list['UFs']]
                    context['dolares'] = json.dumps(dolares,ensure_ascii=False) if dolares else {}
            context['ufs'] = json.dumps(response.json()['UFs'],ensure_ascii=False)
        except Exception as e:
            print(e)
        
    def get_uf_from(self,filter_,desde_, context):
        try:
            response = requests.get(API_BASE+filter_+"/posteriores/"+str(desde_.year)+"/"+str(desde_.month)+"/dias/"+str(desde_.day)+"?apikey="+API_KEY+"&formato="+ FORMAT)
            if response:
                uf_list =response.json()
                max_uf = self.max_uf(uf_list['UFs'])
                context['max_uf'] = max_uf
                min_uf = self.min_uf(uf_list['UFs'])
                context['min_uf'] = min_uf
                context['uf'] = uf_list
                dolar= requests.get(API_BASE+"dolar/posteriores/"+str(desde_.year)+"/"+str(desde_.month)+"/"+str(desde_.day)+"?apikey="+API_KEY+"&formato="+ FORMAT).json()
                    
                max_dolar = self.max_dolar(dolar['Dolares'])
                context['max_dolar'] = max_dolar
                min_dolar = self.min_dolar(dolar['Dolares'])
                context['min_dolar'] = min_dolar
                context['dol'] = dolar
                dolares = [self.get_dolar(x['Fecha']) for x in uf_list['UFs']]
                context['dolares'] = json.dumps(dolares,ensure_ascii=False) if dolares else {}
            context['ufs'] = json.dumps(response.json()['UFs'],ensure_ascii=False)
        except Exception as e:
            print(e)

    def get_uf_range(self, desde_, hasta_, context, filter_):
        try:
            response = requests.get(API_BASE+filter_+"/periodo/"+str(desde_.year)+"/"+str(desde_.month)+"/"+str(hasta_.year)+"/"+str(hasta_.month)+"?apikey="+API_KEY+"&formato="+ FORMAT)
            if response:
                uf_list =response.json()
                max_val = self.max_uf(uf_list['UFs'])
                context['max_uf'] = max_val
                min_val = self.min_uf(uf_list['UFs'])
                context['min_uf'] = min_val
                media = self.promedio_uf(uf_list['UFs'])
                context['media_uf'] = media
                context['uf'] = uf_list

                dolar= requests.get(API_BASE+"dolar/periodo/"+str(desde_.year)+"/"+str(desde_.month)+"/dias_i/"+str(desde_.day)+"/"+str(hasta_.year)+"/"+str(hasta_.month)+"/dias_f/"+str(hasta_.day)+"?apikey="+API_KEY+"&formato="+ FORMAT).json()
                
                max_dolar = self.max_dolar(dolar['Dolares'])
                context['max_dolar'] = max_dolar
                min_dolar = self.min_dolar(dolar['Dolares'])
                context['min_dolar'] = min_dolar
                media = self.promedio_dolar(dolar['Dolares'])
                context['media_dolar'] = media
                context['dol'] = dolar

                dolares = [self.get_dolar(x['Fecha']) for x in uf_list['UFs']]
                context['dolares'] = json.dumps(dolares,ensure_ascii=False) if dolares else {}
            context['ufs'] = json.dumps(response.json()['UFs'],ensure_ascii=False)
        except Exception as e:
            print(e)

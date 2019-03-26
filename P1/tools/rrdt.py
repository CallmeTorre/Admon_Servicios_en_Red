import datetime
import rrdtool
import tempfile
import notify as mail

begin_aberration = 0
new_aberration = 0
number_of_beginning_aberrations = 0 
number_of_end_aberrations = 0

def createPredictionDatabase(path):
    rrdtool.create( path + "/trafico.rrd",
                    "--start",'N',
                    "--step",'60',
                    "DS:CPUload:GAUGE:600:U:U",
                    "RRA:AVERAGE:0.5:1:24")

#TODO Fix the Average last digit and the steps
def createRRDDatabase(path):
    rrdtool.create( path + "/trafico.rrd",
                    "--start", 'N',
                    "--step", '10',
                    "DS:inoctets:COUNTER:60:U:U",
                    "DS:outoctets:COUNTER:60:U:U",
                    "RRA:AVERAGE:0.5:6:10",
                    "RRA:AVERAGE:0.5:1:10")

def createAberrationDatabase(path):
    rrdtool.create( path + "/trafico.rrd",
                    "--start",'N',
                    "--step",'60',
                    "DS:inoctets:COUNTER:300:U:U",
                    #"RRA:AVERAGE:0.5:1:2016",
                    #The last digit says the numbers that youre gonna remember
                    "RRA:AVERAGE:0.5:1:2000",
                    #RRA:HWPREDICT:rows:alpha:beta:seasonal period[:rra - num]
                    "RRA:HWPREDICT:2000:0.1:0.0035:4:3",
                    #RRA:SEASONAL:seasonal period:gamma:rra-num
                    "RRA:SEASONAL:4:0.1:2",
                    #RRA:DEVSEASONAL:seasonal period:gamma:rra-num
                    "RRA:DEVSEASONAL:4:0.1:2",
                    #RRA:DEVPREDICT:rows:rra-num
                    "RRA:DEVPREDICT:2000:4",
                    #RRA:FAILURES:rows:threshold:window length:rra-num
                    #"RRA:FAILURES:12:7:9:4")
                    "RRA:FAILURES:2000:2:4:4")

def createRRDImage(path, initial_time, name):
    rrdtool.graph(  path + "/trafico.png",
                    "--start", initial_time,
                    "--title=" + name,
                    "--vertical-label=Entrantes",
                    "DEF:inoctets=" + path + "/trafico.rrd:inoctets:AVERAGE",
                    "DEF:outoctets=" + path + "/trafico.rrd:outoctets:AVERAGE",
                    "AREA:inoctets#00FF00:In traffic",
                    "LINE1:outoctets#0000FF:Out Salientes\r")

def createRRDPredictionImage(path, initial_time, type_data, u1, u2, u3):
    initial_time = int(initial_time) - 3600
    rg = rrdtool.graphv(  path + "/trafico.png",
                    "--start", str(initial_time),
                    "--end", '+3600s',
                    "--vertical-label=Porcentaje",
                    '--lower-limit', '0',
                    '--upper-limit', '100',
                    "DEF:carga=" + path + "/trafico.rrd:CPUload:AVERAGE",
                    "DEF:cargaCPUl=" + path + "/trafico.rrd:CPUload:AVERAGE",
                    "DEF:cargaCPUm=" + path + "/trafico.rrd:CPUload:AVERAGE",
                    "DEF:cargaCPUh=" + path + "/trafico.rrd:CPUload:AVERAGE",

                    "CDEF:umbral25=cargaCPUl,"+ u1 +",LT,0,carga,IF",
                    "CDEF:umbral50=cargaCPUl,"+ u2 +",LT,0,carga,IF",
                    "CDEF:umbral75=cargaCPUl,"+ u3 +",LT,0,carga,IF",

                    "VDEF:cargaMAX=carga,MAXIMUM",
                    "VDEF:cargaMIN=carga,MINIMUM",
                    "VDEF:cargaLAST=carga,LAST",
                    "VDEF:m=carga,LSLSLOPE",
                    "VDEF:b=carga,LSLINT",
                    'CDEF:predline=carga,POP,m,COUNT,*,b,+',
                    'CDEF:maxlimit=predline,90,100,LIMIT',
                    'CDEF:minlimit=predline,0,10,LIMIT',
                    'VDEF:upperminpoint=maxlimit,FIRST',
                    'VDEF:uppermaxpoint=maxlimit,LAST',
                    'VDEF:lowerminpoint=minlimit,FIRST',
                    'VDEF:lowermaxpoint=minlimit,LAST',

                    "GPRINT:upperminpoint:Reach 100% @ %c \\n:strftime",
                    "GPRINT:uppermaxpoint:Reach 90% @ %c \\n:strftime",
                    "GPRINT:lowerminpoint:Reach  10% @ %c \\n:strftime",
                    "GPRINT:lowermaxpoint:Reach 0% @ %c \\n:strftime",

                    "AREA:carga#3f51b5:Carga de " + type_data,
                    "AREA:umbral25#4caf50:Tráfico de carga mayor que " + u1,
                    "AREA:umbral50#ffc107:Tráfico de carga mayor que " + u2,
                    "AREA:umbral75#f44336:Tráfico de carga mayor que " + u3,
                    "HRULE:25#1a237e:Umbral 1 - "+ u1 +"%",
                    "HRULE:50#1b5e20:Umbral 2 - "+ u2 +"%",
                    "HRULE:75#ff6f00:Umbral 3 - "+ u3 +"%",

                    "LINE2:predline#ef0078:dashes=5",
                    "AREA:maxlimit#8b00dd77",
                    "LINE2:maxlimit#8b00dd",
                    "AREA:minlimit#8b00dd77",
                    "LINE2:minlimit#8b00dd",
                    #"PRINT:cargaMAX:%6.2lf %SMAX",
                    #"PRINT:cargaMIN:%6.2lf %SMIN",
                    #"PRINT:cargaLAST:%6.2lf %SLAST",
                    "PRINT:cargaLAST:%6.2lf")

    try:
        ultimo_valor=float(rg['print[0]'])
    except ValueError:
        ultimo_valor = 0

    if type_data == "CPU":
        u = None
        if ultimo_valor >= int(u1) and ultimo_valor < int(u2):
            u = u1
        elif ultimo_valor >= int(u2) and ultimo_valor < int(u3):
            u = u2
        elif ultimo_valor >= int(u3):
            u = u3

        if u:
            mail.asyncsend(type_data, u, path + "/trafico.png")

#TODO Refactor this method
def createAberrationImage(path):
    begin_date = rrdtool.last(path + '/trafico.rrd') - 1000
    end_date = rrdtool.last(path + '/trafico.rrd')
    ret = rrdtool.graph(path + "/trafico.png",
                        '--start', str(begin_date),
                        '--end', str(end_date),
                        '--title= Equipo 10 Fallas',
                        "--vertical-label=Bytes/s",
                        '--slope-mode',
                        "DEF:obs=" + path + "/trafico.rrd:inoctets:AVERAGE",
                        "DEF:pred=" + path + "/trafico.rrd:inoctets:HWPREDICT",
                        "DEF:dev=" + path + "/trafico.rrd:inoctets:DEVPREDICT",
                        "DEF:fail=" + path + "/trafico.rrd:inoctets:FAILURES",

                        "CDEF:scaledobs=obs,8,*",
                        #"CDEF:predict=120,-1,900,scaledobs,PREDICT",
                        "CDEF:upper=pred,dev,2,*,+",
                        "CDEF:lower=pred,dev,2,*,-",
                        "CDEF:scaledupper=upper,8,*",
                        "CDEF:scaledlower=lower,8,*",
                        "CDEF:scaledpred=pred,8,*",
                        "TICK:fail#FDD017:1.0:Fallas\\n",
                        "LINE3:scaledobs#00FF00:In traffic\\n",
                        "LINE1:scaledpred#FF00FF:Current Prediccion\\n",
                        #"LINE1:predict#FF00FF:Future Prediction\\n:dashes=3",
                        "LINE1:scaledupper#ff0000:Upper Bound Average bits in\\n",
                        "LINE1:scaledlower#0000FF:Lower Bound Average bits in")

    global begin_aberration
    global number_of_beginning_aberrations
    global number_of_end_aberrations

    isAberration = 0

    graphtmpfile = tempfile.NamedTemporaryFile()
    values = rrdtool.graph(graphtmpfile.name+'F',
                           "DEF:f0=" + path + '/trafico.rrd' + ":inoctets:FAILURES",
                           'PRINT:f0:LAST:%1.0lf')
    try:
        isAberration = int(values[2][0])
    except ValueError:
        pass

    if isAberration:
        begin_aberration = 1
        if not number_of_beginning_aberrations:
            #print(f"Aberration finded at {datetime.datetime.now().time()}")
            number_of_beginning_aberrations += 1
            mail.asyncsendAb(path + "/trafico.png", datetime.datetime.now().time())

    if begin_aberration and not isAberration:
        begin_aberration = 0
        if not number_of_end_aberrations:
            #print(f"Enden aberration at {datetime.datetime.now().time()}")
            number_of_end_aberrations += 1
            mail.asyncsendAb(path + "/trafico.png", datetime.datetime.now().time())


def updateAndDumpRRDDatabase(path, value):
    rrdtool.update(path + '/trafico.rrd', value)
    rrdtool.dump(path + '/trafico.rrd', path + '/trafico.xml')
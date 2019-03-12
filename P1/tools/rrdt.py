import rrdtool
import notify as mail

def createPredictionDatabase(path):
    rrdtool.create( path + "/trafico.rrd",
                    "--start",'N',
                    "--step",'60',
                    "DS:CPUload:GAUGE:600:U:U",
                    "RRA:AVERAGE:0.5:1:24")

def createRRDDatabase(path):
    rrdtool.create( path + "/trafico.rrd",
                    "--start", 'N',
                    "--step", '10',
                    "DS:inoctets:COUNTER:60:U:U",
                    "DS:outoctets:COUNTER:60:U:U",
                    "RRA:AVERAGE:0.5:6:10",
                    "RRA:AVERAGE:0.5:1:10")

def createRRDImage(path, initial_time, name):
    rrdtool.graph(  path + "/trafico.png",
                    "--start", initial_time,
                    "--title=" + name,
                    "--vertical-label=Entrantes",
                    "DEF:inoctets=" + path + "/trafico.rrd:inoctets:AVERAGE",
                    "DEF:outoctets=" + path + "/trafico.rrd:outoctets:AVERAGE",
                    "AREA:inoctets#00FF00:In traffic",
                    "LINE1:outoctets#0000FF:Out Salientes\r")

def createRRDCPUImage(path, initial_time):
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

                    "CDEF:umbral25=cargaCPUl,25,LT,0,carga,IF",
                    "CDEF:umbral50=cargaCPUl,50,LT,0,carga,IF",
                    "CDEF:umbral75=cargaCPUl,75,LT,0,carga,IF",

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

                    "AREA:carga#3f51b5:Carga del CPU",
                    "AREA:umbral25#4caf50:Tráfico de carga mayor que 25",
                    "AREA:umbral50#ffc107:Tráfico de carga mayor que 50",
                    "AREA:umbral75#f44336:Tráfico de carga mayor que 75",
                    "HRULE:25#1a237e:Umbral 1 - 25%",
                    "HRULE:50#1b5e20:Umbral 2 - 50%",
                    "HRULE:75#ff6f00:Umbral 3 - 75%",

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

def updateAndDumpRRDDatabase(path, value):
    rrdtool.update(path + '/trafico.rrd', value)
    rrdtool.dump(path + '/trafico.rrd', path + '/trafico.xml')
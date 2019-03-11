import rrdtool

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
    rrdtool.graph(  path + "/trafico.png",
                    "--start",str(initial_time),
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
                    "AREA:carga#3f51b5:Carga del CPU",
                    "AREA:umbral25#4caf50:Tráfico de carga mayor que 25",
                    "AREA:umbral50#ffc107:Tráfico de carga mayor que 50",
                    "AREA:umbral75#f44336:Tráfico de carga mayor que 75",
                    "HRULE:25#1a237e:Umbral 1 - 25%",
                    "HRULE:50#1b5e20:Umbral 2 - 50%",
                    "HRULE:75#ff6f00:Umbral 3 - 75%",
                    "PRINT:cargaMAX:%6.2lf %SMAX",
                    "PRINT:cargaMIN:%6.2lf %SMIN",
                    "PRINT:cargaLAST:%6.2lf %SLAST" )

def updateAndDumpRRDDatabase(path, value):
    rrdtool.update(path + '/trafico.rrd', value)
    rrdtool.dump(path + '/trafico.rrd', path + '/trafico.xml')
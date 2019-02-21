import rrdtool

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

def updateAndDumpRRDDatabase(path, value):
    rrdtool.update(path + '/trafico.rrd', value)
    rrdtool.dump(path + '/trafico.rrd', path + '/trafico.xml')

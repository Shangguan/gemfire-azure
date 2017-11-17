def get_total_mem_megs():
	with open('/proc/meminfo','r') as f:
		meminfo = f.read()

    lines = meminfo.splitlines()
	theline = [l for l in lines if l.find('MemTotal') >= 0][0]
	memstr = theline.split()[1]
    megs = int(memstr)/1000
    return megs

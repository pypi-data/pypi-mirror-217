def w(filenameloc, filewrite):
    filesimfwp = open(filenameloc, "w")
    filesimfwp.write(filewrite)
    filesimfwp.close()

def r(filenamelocr):
    simfwpread = open(filenamelocr, "r")
    simfwpread.close()

def a(filenameloca, fileadd):
    filesimfwpa = open(filenameloca, "a")
    filesimfwpa.write(fileadd)
    filesimfwpa.close()
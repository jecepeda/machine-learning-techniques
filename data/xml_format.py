import lxml.etree as etree

x = etree.parse("datos2007.xml")
x = etree.tostring(x, pretty_print = True)
x = x.replace("  ","\t")
print (x)

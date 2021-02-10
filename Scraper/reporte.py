def reporte(formato="", datos="", option="", end=False, start=False):
    if start == True:
        reporte = "<!DOCTYPE html>\n<html>\n<body>\n" if formato == "html" else ""
        reporte = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<scrapper>\n" if formato == "xml" else ""
    else:
        reporte = ""
    if formato == "xml":
        if option == "header" and start == True:
            reporte += "\t<query nombre=\"" + datos + "\">"
        elif option == "header":
            reporte += "\t</query>\n\t<query nombre=\"" + datos + "\">"
        elif option == "section":
            reporte += "\t\t<url direccion=" + datos + ">"
        elif option == "parrafo":
            reporte += "\t\t\t" + datos + "\n\t\t</url>"
    elif formato == "html":
        if option == "header":
            reporte += "<h1>" + datos + "</h1>"
        elif option == "parrafo":
            reporte += "<p>" + datos + "</p>"
        elif option == "section":
            reporte += "<h3><a href=" + datos + ">" + datos + "</a></h3>"
    elif formato == "txt":
        if option == "header":
            reporte += datos.upper()
        elif option == "section":
            reporte += "\t" + datos
        elif option == "parrafo":
            reporte += "\t\t" + datos
    else:
        print("Formato seleccionado incorrecto!\n\tFomatos permitidos: xml, html, txt\n\tNo se crea el archivo")
        exit
    reporte += "\n" if reporte != "" else ""
    if end == False:
        return reporte
    else:
        reporte += datos
        if formato == "xml":
            reporte += "\t</query>\n</scrapper>"
            crea_archivo(reporte, formato)
        elif formato == "html":
            reporte += "</body>\n</html>"
            crea_archivo(reporte, formato)
        else:
            crea_archivo(reporte, formato)

def crea_archivo(datos=str, formato=str):
    nombre = "scrapper_report." + formato
    with open(nombre, "w") as f:
        f.writelines(datos)

if __name__ == '__main__':
    formato = "xml"
    r = ""
    r += reporte(formato, "Hola", "header", start=True)
    r += reporte(formato, "Primer Programa en reporte", "section")
    r += reporte(formato, "Se puede agregar cuanta información sea necesaria", "parrafo")
    r += reporte(formato, "Se pueden crear varios headers con contenido", "header")
    r += reporte(formato, "Se puede agregar un descriptor por cada header", "section")
    r += reporte(formato, "Una explicación breve de lo que sucede", "parrafo")
    r += reporte(formato, "Se puede agregar otro header", "header")
    r += reporte(formato, "Más información dentro del header", "section")
    r += reporte(formato, "O vacío", "parrafo")
    reporte(formato, r, "", end=True)

def entrada_actividades():
    print("\nRUTA CRITICA")
    print(" ___________               ___________ ")
    print("|   |   |   |             |   |   |   |")
    print("|¯¯¯¯¯¯¯¯¯¯¯|             |¯¯¯¯¯¯¯¯¯¯¯|")
    print("|     1     | ----------> |     2     |")
    print("|___________|             |___________|")
    print("|   |   |   |             |   |   |   |")
    print(" ¯¯¯¯¯¯¯¯¯¯¯               ¯¯¯¯¯¯¯¯¯¯¯")
    print("SECCIÓN: Agregar actividades")
    control = None
    dias = 0
    actividades = {}
    arregloActividades = []
    while(control!="N"):
        control = None
        dias=0
        print("")
        nombre = input("  Proporcione el nombre de la actividad que se desea agregar:")
        for i in arregloActividades:
            while nombre == i:
                print("   Error: La actividad que se intenta añadir ya ha sido previamente registrada en el sistema")
                nombre = input("\n  Por favor, proporciona el nombre de la actividad que deseas añadir\n")
                
        arregloActividades.append(nombre)
        while(dias == 0):
            try:
                dias = int(input("  Ingresa la cantidad de dias tomará completar la actividad: "))
                while(dias <= 0):
                    print("   Error: Por favor, ingrese un numero mayor a 0.")
                    dias = int(input("  Ingresa la cantidad de dias tomará completar la actividad: "))
            except:
                print("   Error: Por favor, ingrese un numero mayor a 0.")
                print("\n")

        numeroPresesoresControl = False
        while numeroPresesoresControl == False:
            try:
                numeroPresesores = int(input("  ¿Cuántos predecesores tiene la actividad?: "))
                while numeroPresesores < 0 or numeroPresesores > len(actividades):
                    numeroPresesores = int(input("  Error: Ingrese un dato valido\n  ¿Cuántos predecesores tiene la actividad?\n"))
                numeroPresesoresControl = True
            except:
                numeroPresesoresControl = False
                print("\n   Error: Ha introducido un dato invalido!\n")


        predecesores = []
        for i in range(numeroPresesores):
            predecesorControl = False
            while not predecesorControl:
                print("Lista de los predecesores que se encuentran cargadas:")
                for j in range(1, len(actividades)+1):
                    actividad = list(actividades.keys())[j-1]
                    print(f"  {j}. {actividad}")
                pre = input("Escriba el número del predecesor: ")
                if pre in predecesores or not pre.isdigit() or int(pre) < 1 or int(pre) > len(actividades):
                    print("\nError: Parece que la opción que ha ingresado no es válida.\n")
                    predecesorControl = False
                else:
                    predecesorControl = True
                    predecesores.append(list(actividades.keys())[int(pre)-1])
        actividades[nombre] = {"dias": dias, "predecesores":predecesores, "ES":0, "EF": 0, "LS":0, "LF":0, "holgura":0}
        while(control!="S" and control!="N"):
            try:
                control = input("\n ¿Desea cargar otra actividad? (S/N): ").upper()
                if(control!="S" and control!="N"):
                    print("   Error: Escriba solo S para Si o N para No.")
            except:
                print("\n   Error: Escriba solo S para Si o N para No.\n")
    return actividades

def calcular_fechas(actividades):
    dependientes = []

    for actividad, info in actividades.items():
        for k in info["predecesores"]:
            if k not in dependientes:
                dependientes.append(k)
            if actividades[k]["EF"] > actividades[actividad]["ES"]:
                actividades[actividad]["ES"] = actividades[k]["EF"]
        actividades[actividad]["EF"] = actividades[actividad]["ES"] + info["dias"]

    for actividad in reversed(actividades.keys()):
        if actividad not in dependientes:
            actividades[actividad]["LS"] = actividades[actividad]["EF"] - actividades[actividad]["dias"]
            actividades[actividad]["LF"] = actividades[actividad]["EF"]

        for predecesor in actividades[actividad]["predecesores"]:
            if actividades[predecesor]["LF"] == 0:
                actividades[predecesor]["LF"] = actividades[actividad]["ES"]
            actividades[predecesor]["LS"] = actividades[predecesor]["LF"] - actividades[predecesor]["dias"]
            actividades[predecesor]["holgura"] = actividades[predecesor]["LS"] - actividades[predecesor]["ES"]

    return actividades

def imprimir_resultados(actividades):
    print("\n\n SECCIÓN: Mostrar resultados")
    ruta_critica = ""
    for actividad, info in actividades.items():
        print("\n  Holgura de la actividad "+actividad+" es: " +str(info['holgura'])+"")
        print("  ___________ ")
        print(" |"+str(info["ES"]).ljust(3)+"|"+str(info["dias"]).ljust(3)+"|"+str(info["EF"]).ljust(3)+"|")
        print(" |¯¯¯¯¯¯¯¯¯¯¯|")
        print(" |" + actividad.ljust(11) + "|")
        print(" |___________|")
        print(" |"+str(info["LS"]).ljust(3)+"|"+str(info["dias"]).ljust(3)+"|"+str(info["LF"]).ljust(3)+"|")
        print("  ¯¯¯¯¯¯¯¯¯¯¯ ")
        if info['holgura'] == 0:
            ruta_critica = ruta_critica + (actividad+"---->")
    ruta_critica = ruta_critica[:-5]
    print("\n     RUTA CRITICA: " + ruta_critica) 

def main():
    actividades = entrada_actividades()
    actividades = calcular_fechas(actividades)
    imprimir_resultados(actividades)

if __name__ == "__main__":
    main()
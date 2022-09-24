from io import open

def leerArchivo(archivo,lista): #Función que lee toda la información del archivo.
	lectura=archivo.readlines() #Lee todo el archivo y guarda línea por línea en una lista que llamaremos lectura.
	numVertices=lectura[0]
	numVertices=int(numVertices)
	n=0			#Contador que usaremos para recorrer la lista obtenida con todos los datos del archivo.
	caracteres=0   #Este es el contador de los caracteres del archivo, que luego usaremos para colocar el puntero de lectura del mismo en donde queramos.
	numeros=['0','1','2','3','4','5','6','7','8','9']  #Como en la lista, todos los números están en string, y la lectura se hace caracter a caracter, necesitaremos identificar los caracteres o números que vamos a necesitar.
	while (n<len(lectura)):  #Como la lista extrajo puros datos de tipo string, tenemos que pasarlos a tipo entero.
		k=0
		sublista=[]      #Para ello, usaremos listas anidadas.
		cantVertices=1
		for i in lectura[n]:
			if i in numeros:
				k+=1	#Contamos la cantidad de digitos que tendrá un dígito para poder agregarlo luego como un solo número, ya que la lectura del archivo se hace caracter a caracter.
			elif ((((i!="-") and (i!="\n")) or (cantVertices==2) or (n==0)) or ((cantVertices==1) and ((i=="\n") or (i=='')))):   #Verifica que el número no sea negativo.
					archivo.seek(caracteres-k) #Cuando ya sabemos la cantidad de dígitos que posee el número, nos volvemos al principio del mismo.
					num=archivo.read(k)   #Y leemos dicho número completo como una sola unidad.
					if num!='':
						num=int(num)
						cantVertices+=1
						if (num<=numVertices):  #Verifica que el número del vértice este dentro del número de vértices del grafo, dados al principio.
							sublista.append(num)  #Pasamos los números de tipo string a tipo integer.
					k=0
			caracteres+=1   
		caracteres+=1  #Se vuelve a contar un caracter luego de leer una lína, porque el puntero de los archivos toma los saltos de línea como otro caracter.
		if (n==len(lectura)-1):
			archivo.seek(caracteres-1-k) #Cuando ya sabemos la cantidad de dígitos que posee el número, nos volvemos al principio del mismo.			
			num=archivo.read(k)   #Y leemos dicho número completo como una sola unidad.
			if num!='':
				num=int(num)
				if (num<=numVertices):  #Verifica que el número del vértice este dentro del número de vértices del grafo, dados al principio.
					sublista.append(num)

		if (len(sublista)!=0):
			if (len(sublista)==1):  #En caso de que sea un vértice aislado.
				lista.append(sublista) 
			if (len(sublista)==2):	
				izq=sublista[0]
				der=sublista[1]
				if (not [der,izq] in lista) and (not [izq,der] in lista) and (der!=izq):  #Verifica que la arista no sea repetida y que no sea un lazo o bucle tampoco.
					lista.append(sublista)    #Se va formando la nueva lista anidada con puros datos de tipo integer mucho más fáciles de utilizar ahora.
		n+=1

	
	archivo.close()  #Cerramos el archivo ya que no trabajaremos más con él.

	return lista    #Devuelve la lista en donde se encuentra toda la información del archivo. En lista[0] está otra lisat con la cantidad de 
			#vértices que posee el grafo, y de ahí en adelante están almacenadas las listas con las aristas o en su decto, un vértice aislado.


def gradosVertices(lista,gradosV): #Indica el grado de todos los vértices del grafo.
	n=lista[0]
	n=n[0]
	for i in range (n):   #Sabemos el número de vértices del grafo, así que procedemos a crear un diccionario en donde las claves serán los vértices, y sus respectivos valores será el número de aristas que inciden en él, es decir, el grado.
		gradosV[i+1]=0

	for sublista in lista:   #Como es una lista anidada, para obtener los valores, tenemos que usar for anidados.
		val1=0
		val2=0
		for i in sublista:
				if val1==0:	#Todas las sublitas tienen solo uno o dos valores, así que hay que ver en cuál variable se almacena.
					val1=i
				else: 
					val2=i

		if val2!=0:		#Una arista debe incidir sobre dos vértices, y si val2=0 quiere decir que se trata de un vértice aislado, por lo cual no sumaría al grado del mismo, sin embargo si tanto val1 como val2 tienen valores distintos a 0, si hay arita entre ellos por lo cual se le suma 1 al contador de grado de cada vértice.
			n=gradosV[val1]
			gradosV[val1]=n+1
			n=gradosV[val2]
			gradosV[val2]=n+1	

	
	return gradosV 	#Devolvemos el diccionario que posee el grado de todos los vértices del grafo.


def visitarBP(vertices,pila,lista,numVertices):  #Esta función es el algoritmo de Búsqueda en Profundidad aplicado en Python.
	while ((len(pila))!=0):  #Mientras la pila no este vacía, ejecutar el while.
		tope=len(pila)
		tope=pila[tope-1]  #El tope de la pila
		existe=False

		for i in range (1,numVertices+1):
			if ((([tope,i] in lista) or ([i,tope] in lista)) and ((vertices[i])==0)): #Si existe una arista que vaya de tope hasta otro vértice del grafo, tal que este último vértice este en Blanco o en 0, hacer...
				vertices[i]=1
				pila.append(i)  #Se apila el siguiente vértice.
				existe=True
				break;  #Puede existir más de una arista que vaya desde el vértice que es tope de la pila, hacia otro vértice en blanco o en 0, pero como solo necesitamos el primero que encontremos, ya no necesitamos seguir en el for.
		
		if existe==False:  #Si no existe más ninguna arista entre el tope y otro vértice en blanco o en 0, es decir, que ya se visitaron todas sus adyacencias, entonces se elimina el tope y continuamos con el algoritmo.
			pila.pop()  #Desapila.


def esGrafoConexo(lista):  #Determina si un grafo es conexo o no
	pila=[]   #Pila que usaremos en la Búsqueda en Profundidad, la cual trabajaremos con una lista, pero con las reglas de una pila.
	n=lista[0]
	n=n[0]
	vertices={}
	for i in range (n):  #Se crea un diccionario con el fin de identificar los vértices del grafo con unos colores para realizar el Algoritmo de Búsqueda en Profundidad. EL 0 será el color blanco y el 1 será el gris.
		vertices[i+1]=0

	numConexas=0  #Almacena el número de componentes conexas que tiene el grafo según la cantidad de veces que se llama a la función visitarBP().
	for v in vertices:
		if vertices[v]==0:  #Para todo vértice del grafo que este en 0 o blanco, llamar a la función del recorrido de Búsqueda en Profundidad.
			vertices[v]=1	#Se pinta de gris, que es el 1.
			pila.append(v)
			visitarBP(vertices,pila,lista,n)
			numConexas+=1

	if numConexas==1:   #Si el grafo posee una sola componente conexa, quiere decir que el mismo es conexo, sino, es disconexo.
		return True
	else:
		return False

def sonVerticesVisitables(lista):
	verticesVisitables={}  #Diccionario que contiene el número de los vértices con los cuales cada vértice tiene una arista en común, y que por ende es visitable.
	numVertices=lista[0]
	numVertices=numVertices[0]

	for i in range(1,numVertices+1):
		verticesVisitables[i]=[]
		for j in range(1,numVertices+1):
			if (([i,j] in lista) or ([j,i] in lista)):
				vertices=verticesVisitables[i]
				vertices.append(j)
				verticesVisitables[i]=vertices

	return verticesVisitables

def esGrafoEuleriano(gradosV,lista,aristasRecorridas):  #Verifica si el grafo es Euleriano o no.
	for i in gradosV:
		if (((gradosV[i])%2)!=0): #Según el Teorema de Euler, una condición necesaria y suficiente para que un grafo simple conexo sea un grafo euleriano, es que todos sus vértices tengan grado par.
			return False

	verticesVisitables=sonVerticesVisitables(lista)
	inicio=verticesVisitables[1]
	ultimaArista=inicio[0]
	numAristas=0
	verticeActual=1
	while numAristas<(len(lista)-1):
		inicio=verticesVisitables[verticeActual]
		if verticeActual==ultimaArista and numAristas!=(len(lista)-1):
			n=1
			while True:
				proximoVertice=inicio[len(inicio)-n]
				if proximoVertice!=ultimaArista:
					break;
				n+=1
		else:
			proximoVertice=inicio[len(inicio)-1]

		subArista=[verticeActual,proximoVertice]
		aristasRecorridas.append(subArista)
		inicio.remove(proximoVertice)
		verticesVisitables[verticeActual]=inicio
		final=verticesVisitables[proximoVertice]
		final.remove(verticeActual)
		verticesVisitables[proximoVertice]=final
		verticeActual=proximoVertice
		numAristas+=1
	return True

def esGrafoHamiltoneano(gradosV,lista,verticesRecorridos): 
	verticesVisitables=sonVerticesVisitables(lista)
	aristasProhibidas=[]
	numVertices=lista[0]
	numVertices=numVertices[0]
	gradoMenor=numVertices
	for i in gradosV:
		if gradosV[i]==1:
			#print("El grafo no es Hamiltoneano porque no todos sus vértices tienen grado mayor o igual a 2")
			return False
		if gradosV[i]<gradoMenor:
			gradoMenor=gradosV[i]
			verticeMenor=i
			verticesRecorridos[0]=verticeMenor

	divisionPrincipal=False
	opcionDivision=0
	verticeDivision=verticeMenor
	while True:
		verticeActual=verticesRecorridos[len(verticesRecorridos)-1]
		opciones=verticesVisitables[verticeActual]	
		cambio=False
		mejorOpcion=[]

		for i in opciones:
			if ((not i in verticesRecorridos) and (not [verticeActual,i] in aristasProhibidas)):
				mejorOpcion.append(i)

		if ((len(mejorOpcion))!=0):
			caminoMenor=numVertices
			for i in mejorOpcion:
				if gradosV[i]<caminoMenor:
					caminoMenor=gradosV[i]
					proximoVertice=i

			cont=0
			for i in mejorOpcion:
				if (gradosV[i]==caminoMenor):
					cont+=1

			if (cont>1) and (divisionPrincipal==False): #Para identificar el vértice de la primera división o división principal.
				verticeDivision=verticeActual
				divisionPrincipal=True
				opcionDivision=0


			puede=True
			if (verticeActual==verticeDivision):
				puede=False
				if opcionDivision==0:
					ListaDivision=mejorOpcion
					maxDivision=len(mejorOpcion)
					verticesRecorridos.append(ListaDivision[opcionDivision])
					opcionDivision+=1
				else:
					if opcionDivision==maxDivision:
						return False
					else: 
						verticesRecorridos.append(ListaDivision[opcionDivision])
						opcionDivision+=1
						aristasProhibidas=[]

			if(cont>1) and (divisionPrincipal==True) and (puede==True):
				verticesRecorridos.append(proximoVertice)

			if (cont==1) and (puede==True):
				verticesRecorridos.append(proximoVertice)

		else:
			if (len(verticesRecorridos)==numVertices):
				if verticeMenor in opciones:
					verticesRecorridos.append(verticeMenor)
					return True
				else:
					n=verticesRecorridos.pop()
					previo=verticesRecorridos[len(verticesRecorridos)-1]
					aristasProhibidas.append([previo,n])

			else:
				n=verticesRecorridos.pop()
				previo=verticesRecorridos[len(verticesRecorridos)-1]
				aristasProhibidas.append([previo,n])


#------------------PROGRAMA-----------------------
lista=[]
gradosV={}
archivo=open("grafos.txt","r")  #Se abre el archivo.
lista=leerArchivo(archivo,lista)
gradosV=gradosVertices(lista,gradosV)
verticesRecorridos=[0]
aristasRecorridas=[]
verticesVisitables=sonVerticesVisitables(lista)

print("\n\n                             ¿Qué desea saber del siguiente grafo?\n")
print(lista)

respuesta=0
while (respuesta<=0) or (respuesta>3):
	print("\n\n     ____________________________________.:M E N U:.____________________________________")
	print("\n                          1. Deseo saber si el grafo es Euleriano.")
	print("\n                         2. Deseo saber si el grafo es Hamiltoneano.")
	print("\n              3. Deseo saber si el grafo es tanto Euleriano como Hamiltoneano.")
	print("\n     ____________________________________________________________________________________")
	respuesta=int(input("\n                 Por favor indique el número de la opción que desea ingresar: "))

if (respuesta==1):
	if esGrafoConexo(lista): #Evaluamos primero si es conexo o no, para ver si vale la pena analizar si es euleriano o hamiltoneano.
		euleriano=esGrafoEuleriano(gradosV,lista,aristasRecorridas)
		if euleriano: #Verifica la condición de si el grafo es Euleriano o no.
			print("\n\n                  El grafo es Euleriano, y su ciclo Euleriano es: ")
			print(aristasRecorridas)
		else:
			print("\n                    El grafo no es Euleriano.")
	else:
		print("\n\n                  Como el grafo no es conexo, no es un grafo Euleriano.")

elif respuesta==2:
	if esGrafoConexo(lista): #Evaluamos primero si es conexo o no, para ver si vale la pena analizar si es euleriano o hamiltoneano.
		hamiltoneano=esGrafoHamiltoneano(gradosV,lista,verticesRecorridos)
		if hamiltoneano:
			print("\n\n                   El grafo es Hamiltoneano, y su ciclo Hamiltoneano es: ")
			print(verticesRecorridos)
		else:
			print("\n                     El grafo no es Hamiltoneano.")
	else:
		print("\n\n                   Como el grafo no es conexo, no es un grafo Hamiltoneano.")


elif respuesta==3:
	if esGrafoConexo(lista): #Evaluamos primero si es conexo o no, para ver si vale la pena analizar si es euleriano o hamiltoneano.
		if esGrafoEuleriano(gradosV,lista,aristasRecorridas) and esGrafoHamiltoneano(gradosV,lista,verticesRecorridos):
			print("\n\n                 El grafo es Euleriano y Hamiltoneano al mismo tiempo.")
			print("\n                   Su ciclo Euleriano es: ")
			print(aristasRecorridas)
			print("\n                   Su ciclo Hamiltoneano es: ")
			print(verticesRecorridos)
		elif esGrafoEuleriano(gradosV,lista,aristasRecorridas):
			print("\n\n                 El grafo es Euleriano pero no es Hamiltoneano.")
			print("\n                   Su ciclo Euleriano es: ")
			print(aristasRecorridas)
		elif esGrafoHamiltoneano(gradosV,lista,verticesRecorridos):
			print("\n\n                 El grafo es Hamiltoneano pero no es Euleriano.")
			print("\n                   Su ciclo Hamiltoneano es: ")
			print(verticesRecorridos)
		else:
			print("\n\n                 El grafo no es ni Euleriano ni Hamiltoneano.")

	else:
		print("\n\n             Como el grafo no es conexo, no es ni un grafo Euleriano ni un grafo Hamiltoneano.")
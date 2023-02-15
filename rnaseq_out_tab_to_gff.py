import pandas #Para los dataframes
import argparse #Para el parseador de argumentos

#Crear al parseador
parser = argparse.ArgumentParser() 

#Añadir argumentos
parser.add_argument("--file", type = str, required = True, help = "The input file produced by blast with output format 6 (tabular).")
#parser.add_argument("--bitscore", type = float, required = True, help = "Bitscore obtained by blast. Used to add a level of filter to the result. If 0, all results will be maintained.")
parser.add_argument("--source", type = str, required = True, help = "The mode in which blast was performed, e.g. blastn, blastp, tblastx, ...")

#Parsear argumentos hacia una variable de almacenamiento
args = parser.parse_args()

#Renombrar variables o modificarlas si es necesario.
file = str(args.file)
outname = str(args.file.replace("_SJ.out.tab", "") + ".gff") #Cambiar nombre de salida
source = str(args.source)
#bitscore = float(args.bitscore)

df = pandas.DataFrame(columns = ["seqid", "source", "type", "start", "end", "score", "strand", "phase", "attributes"]) # Iniciar un df vacio pero con nombres de columnas

with open(file) as filehandler: #Abrir archivo
	for line in filehandler: #Para cada linea
		line = line.rstrip() #.replace("|", "; ") #Corta el trailing y remplaza | con ;
		line_elements = line.split("\t") #Separa por tabulaciones. Se crea una lista
		new_line = line_elements[0] + "\t" + source + "\t" + "splice_junction" + "\t" + line_elements[1] + "\t" + line_elements[2] + "\t.\t" + line_elements[3] + "\t.\t" + 'Query=' + line_elements[0] 
		new_line = new_line.split("\t")
		if new_line[6] == "1":
			new_line[6] = "+"
		if new_line[6] == "2":
			new_line[6] = "-"
		#print(new_line)
		df_list = pandas.DataFrame.from_dict({"seqid": [new_line[0]], "source": [new_line[1]], "type": [new_line[2]], "start": [new_line[3]], "end": [new_line[4]], \
                "score": [new_line[5]], "strand": [new_line[6]], "phase": [new_line[7]], "attributes": [new_line[8]] } ) #Crea un df de un dicc, a partir de new line y asignando nombres de columnas respectivos.
		df = pandas.concat([df, df_list]) #Unir df que tienen los mismo nombres de columnas
df.to_csv(outname , sep = "\t", header = False,  index = False) #Guardar df, por tabs, sin indice ni encabezado.

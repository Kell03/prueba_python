import mysql.connector
import PyPDF4
from datetime import datetime
# Establecer la conexión a la base de datos
conn = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="",
    database="pruebapy"
)
cursor = conn.cursor()

# Ejecutar la consulta
selectquery = "SELECT * FROM pruebadb"
cursor.execute(selectquery)

# Obtener los resultados
records = cursor.fetchall()

if len(records) == 0:
    print('No se encontraron personas')
else:
    for row in records:
        campos_llenar = {
            'Fecha': row[1],
            'Nombre establecimiento': row[2],
            'Dirección': row[3],
            'Localidad': row[4],
            'Provincia': row[5],
            'Persona contacto': row[6],
            'Teléfono contacto': row[7],
            'email': row[8],
            'CP': row[9],
            'comisión': row[10],
            'porcentaje retorno': row[11],
            'Sector actividad': row[12],
            'Fondo inicial': row[13],
            'Nombre empresa': row[14],
            'CIF': row[15],
            'CP 2': row[16],
            'Dirección Fiscal': row[17],
            'Localidad 2': row[18],
            'Provincia 2': row[19],
            'Nombre administrador': row[20],
            'DNI administrador': row[21],
            'Check Cajero': 1
        }
        fecha_hora_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
        input_pdf_path = 'pdf/formulario.pdf'

        with open(input_pdf_path, 'rb') as file:
            pdf_reader = PyPDF4.PdfFileReader(file)
            pdf_writer = PyPDF4.PdfFileWriter()

            for i in range(pdf_reader.getNumPages()):
                page = pdf_reader.getPage(i)
                annotations = page['/Annots']

                if annotations:
                    for annotation in annotations:
                        annotation_obj = annotation.getObject()  # Obtiene el objeto de anotación

                        if '/T' in annotation_obj:
                            field_name = annotation_obj['/T']
                            if field_name in campos_llenar:
                                annotation_obj.update({
                                    PyPDF4.generic.NameObject("/V"): PyPDF4.generic.createStringObject(
                                        str(campos_llenar[field_name])),
                                    PyPDF4.generic.NameObject("/Ff"): PyPDF4.generic.NumberObject(1)
                                })

                pdf_writer.addPage(page)

            output_pdf_path = 'pdf_fill/formulario_lleno' + str(row[0]) + '.pdf'.format( fecha_hora_actual)
            with open(output_pdf_path, 'wb') as output_file:
                pdf_writer.write(output_file)

            print("Campos llenados correctamente. El archivo PDF se ha guardado en:", output_pdf_path)

# Cerrar el cursor y la conexión a la base de datos
cursor.close()
conn.close()




"""

input_pdf_path = 'pdf/formulario.pdf'

with open(input_pdf_path, 'rb') as file:
    pdf_reader = PyPDF4.PdfFileReader(file)
    fields = pdf_reader.getFields()

    for field_name, field_value in fields.items():
        print(field_name)

        """
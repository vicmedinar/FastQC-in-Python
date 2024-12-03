Analisis de calidad fastaqc en python
import subprocess
import zipfile
import os
import webbrowser
import tempfile
import shutil

# Ruta a Java (asegúrate de que Java esté instalado en esa ruta)
java_path = r"C:\Program Files (x86)\Common Files\Oracle\Java\javapath\java.exe"

# Ruta al directorio donde está FastQC, se ejecuta de manera local
fastqc_path = r"C:\Users\Vistor\Desktop\victor\maestria Nacional\proyecto maestria\programas\FastQC"

# Archivos JAR necesarios para la ejecución
sam_jar = r"C:\Users\Vistor\Desktop\victor\maestria Nacional\proyecto maestria\programas\FastQC\sam-1.103.jar"
jbzip2_jar = r"C:\Users\Vistor\Desktop\victor\maestria Nacional\proyecto maestria\programas\FastQC\jbzip2-0.9.jar"

# Ruta al archivo de entrada, debe estar en la carpeta local de fastqc
input_file = r"C:\Users\Vistor\Desktop\victor\maestria Nacional\proyecto maestria\programas\FastQC\SRR10832365.fastq"

# Comando para ejecutar FastQC con los parámetros correctos
command = [
    java_path,
    "-Xmx250m",  # Limitar la memoria de Java
    "-classpath", f".;{sam_jar};{jbzip2_jar}",  # Clases necesarias
    "uk.ac.babraham.FastQC.FastQCApplication",  # Clase principal de FastQC
    input_file  # El archivo de entrada que deseas analizar
]

# Ejecutar el comando
try:
    subprocess.run(command, cwd=fastqc_path, check=True)
    print("FastQC se ejecutó correctamente.")
except subprocess.CalledProcessError as e:
    print(f"Hubo un error al ejecutar FastQC: {e}")

#mover resultados del analisis a la carpeta de final
# Ruta del archivo de origen
archivo_origen = r"C:\Users\Vistor\Desktop\victor\maestria Nacional\proyecto maestria\programas\FastQC\SRR10832365_fastqc.zip"

# Ruta de destino
directorio_destino = r"C:\Users\Vistor\Desktop\victor\maestria Nacional\programacion para biologos\ensayo\tareas\entregable #1\SRA"

# Mover el archivo
try:
    shutil.move(archivo_origen, directorio_destino)
    print(f"El archivo ha sido movido a: {directorio_destino}")
except Exception as e:
    print(f"Hubo un error al mover el archivo: {e}")

#Visualizar resultados
#descomprimir .ZIP

def read_specific_lines_from_zip(zip_path, txt_filename, line_numbers):
    """
    Lee líneas específicas de un archivo de texto dentro de un ZIP.
    """
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Busca el archivo txt_filename en el ZIP
            txt_path = None
            for item in zip_ref.namelist():
                if item.endswith(txt_filename):
                    txt_path = item
                    break

            if txt_path is None:
                raise FileNotFoundError(f"No se encontró {txt_filename} en el archivo ZIP")

            # Lee el archivo de texto desde el ZIP
            with zip_ref.open(txt_path) as txt_file:
                lines = txt_file.read().decode('utf-8').splitlines()

                print(f"\nResumen del analisis FastQC:")
                print("-" * 50)
                for line_num in line_numbers:
                    if 1 <= line_num <= len(lines):
                        print(f"{lines[line_num - 1]}")
                    # print(f"Linea {line_num}: {lines[line_num-1]}")
                    else:
                        print(f"Linea {line_num}: Fuera de rango - el archivo tiene {len(lines)} lineas")

    except zipfile.BadZipFile:
        print("Error: El archivo ZIP está corrupto o no es un archivo ZIP válido")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo ZIP en la ruta especificada: {zip_path}")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")


def extract_and_open_html(zip_path):
    """
    Extrae y abre el archivo HTML del ZIP en el navegador predeterminado.
    """
    try:
        # Crear un directorio temporal
        temp_dir = tempfile.mkdtemp()

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Buscar el archivo HTML
            html_file = None
            for file in zip_ref.namelist():
                if file.endswith('.html'):
                    html_file = file
                    break

            if html_file is None:
                raise FileNotFoundError("No se encontró ningún archivo HTML en el ZIP")

            # Extraer todo el contenido al directorio temporal
            print(f"Extrayendo archivos...")
            zip_ref.extractall(temp_dir)

            # Construir la ruta completa al archivo HTML
            html_path = os.path.join(temp_dir, html_file)

            # Abrir el archivo HTML en el navegador predeterminado
            print(f"Abriendo {html_file} en el navegador...")
            webbrowser.open(f'file://{os.path.abspath(html_path)}')

            # Esperar un momento antes de limpiar
            print("\nEl archivo HTML se ha abierto en tu navegador.")
            print("Los archivos temporales se eliminarán al cerrar el programa.")

    except zipfile.BadZipFile:
        print("Error: El archivo ZIP está corrupto o no es un archivo ZIP válido")
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        if 'temp_dir' in locals():
            shutil.rmtree(temp_dir)


if __name__ == "__main__":
    # Ruta al archivo ZIP
    zip_path = r"C:\Users\Vistor\Desktop\victor\maestria Nacional\programacion para biologos\ensayo\tareas\entregable #1\SRA\SRR10832365_fastqc.zip"

    # Leer las líneas específicas del archivo TXT
    txt_filename = "fastqc_data.txt"
    lines_to_read = [4, 6, 7, 8, 10, 11]
    read_specific_lines_from_zip(zip_path, txt_filename, lines_to_read)

    # Abrir el archivo HTML
    extract_and_open_html(zip_path)

    # Mantener el programa abierto hasta que el usuario presione Enter
    input("\nPresiona Enter para cerrar el programa y limpiar los archivos temporales...")

from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

DB_HOST = '192.168.96.8'
DB_USER = 'web_gimnasio'
DB_PASS = 'Web123!'
DB_NAME = 'gimnasio_db'

def conectar_db():
    return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME, cursorclass=pymysql.cursors.DictCursor)

# Mostrar la lista de socios y el buscador
@app.route('/')
def index():
    busqueda = request.args.get('q')
    
    conexion = conectar_db()
    socios = []
    try:
        with conexion.cursor() as cursor:
            if busqueda:
                sql = "SELECT * FROM Socios WHERE Nombre LIKE %s OR Apellido LIKE %s"
                valor_busqueda = f"%{busqueda}%"
                cursor.execute(sql, (valor_busqueda, valor_busqueda))
            else:
                cursor.execute("SELECT * FROM Socios")
            
            socios = cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conexion.close()
        
    return render_template('index.html', socios=socios, busqueda=busqueda)

# Creación de nuevo socio
@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo_socio():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        telefono = request.form['telefono']
        id_plan = request.form['id_plan']

        conexion = conectar_db()
        try:
            with conexion.cursor() as cursor:
                sql = "INSERT INTO Socios (Nombre, Apellido, Email, Telefono, ID_Plan) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (nombre, apellido, email, telefono, id_plan))
            conexion.commit()
        except Exception as e:
            print(f"Error al guardar: {e}")
        finally:
            conexion.close()

        return redirect(url_for('index'))

    return render_template('nuevo_socio.html')

# Modificación de socio existente
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_socio(id):
    conexion = conectar_db()
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        telefono = request.form['telefono']
        id_plan = request.form['id_plan']

        try:
            with conexion.cursor() as cursor:
                sql = "UPDATE Socios SET Nombre=%s, Apellido=%s, Email=%s, Telefono=%s, ID_Plan=%s WHERE ID_Socio=%s"
                cursor.execute(sql, (nombre, apellido, email, telefono, id_plan, id))
            conexion.commit()
        except Exception as e:
            print(f"Error al actualizar: {e}")
        finally:
            conexion.close()
        return redirect(url_for('index'))

    else:
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM Socios WHERE ID_Socio = %s", (id,))
                socio = cursor.fetchone()
        finally:
            conexion.close()
        return render_template('editar_socio.html', socio=socio)

# Eliminación de socio
@app.route('/eliminar/<int:id>')
def eliminar_socio(id):
    conexion = conectar_db()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM Socios WHERE ID_Socio = %s", (id,))
        conexion.commit()
    except Exception as e:
        print(f"Error al eliminar: {e}")
    finally:
        conexion.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

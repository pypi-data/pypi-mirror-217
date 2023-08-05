### Autores:

- MC. Rodolfo Lopez
- Dr. Oscar de la Torre
- Dr. Felipe Andoni

### Descripcion:

- Libreria para la extraccion de precios de granos, frutas y hortalizas del SNIIM.

### Requerimientos:

- pip install pymongo

### Uso:

- import sniimapp

Los parametros obligatorios para hacer una busqueda son el tipo de mecado **granos**, **fyh**, **fecha inicial** y **fecha final**:
- sniim = sniimapp.SNIIM('granos', '01/01/2018', '22/01/2018')
- sniim = sniimapp.SNIIM('fyh', '01/01/2018', '22/01/2018')

Se pueden utilizar los parametros de **producto** y **origen** para afinar la busqueda:
- sniim = sniimapp.SNIIM('granos', '01/01/2018', '22/01/2018', 'Alubia')
- sniim = sniimapp.SNIIM('granos', '01/01/2018', '22/01/2018', 'Alubia', 'Durango')

Una vez creado el objeto, se utiliza la funcion **get_data()** para obtener los datos:
- data = sniim.get_data()

La funcion get_data() regresa un objeto cursor Mongo con el cual se puede interactur con los datos.
Para mas informaciion sobre cursor Mongo visite [Tools for iterating over MongoDB query results](https://pymongo.readthedocs.io/en/stable/api/pymongo/cursor.html#pymongo.cursor.Cursor.address)

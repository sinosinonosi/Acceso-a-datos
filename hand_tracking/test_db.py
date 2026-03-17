from dao.mongodb_dao import MongoDBDAO

print("Probando la conexión a la base de datos...")
db = MongoDBDAO()

if db.connected:
    print("¡Todo perfecto! El .env y la conexión a MongoDB Atlas funcionan.")
else:
    print("Hubo un problema. Revisa tu URI en el archivo .env.")
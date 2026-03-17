from pymongo import MongoClient
from config.settings import MONGODB_URI, DATABASE_NAME

class MongoDBDAO:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBDAO, cls).__new__(cls)
            cls._instance._connect()
        return cls._instance

    def _connect(self):
        try:
            self.client = MongoClient(MONGODB_URI)
            self.db = self.client[DATABASE_NAME]
            self.sessions_collection = self.db['sessions']
            self.events_collection = self.db['volume_events']
            
            self.client.admin.command('ping')
            self.connected = True
            print("Conexión a MongoDB Atlas exitosa.")
        except Exception as e:
            self.connected = False
            print(f"Error al conectar a MongoDB: {e}")

    def insert_session(self, session_data):
        """Inserta una sesión y devuelve el ID generado por Mongo"""
        if self.connected:
            result = self.sessions_collection.insert_one(session_data)
            return result.inserted_id
        return None

    def update_session(self, session_id, session_data):
        """Actualiza la sesión (para añadir la fecha de fin y la duración)"""
        if self.connected and session_id:
            self.sessions_collection.update_one(
                {'_id': session_id},
                {'$set': session_data}
            )

    def insert_volume_event(self, event_data, session_id):
        """Inserta un evento de volumen vinculándolo a la sesión actual"""
        if self.connected:
            event_data['session_id'] = session_id
            self.events_collection.insert_one(event_data)
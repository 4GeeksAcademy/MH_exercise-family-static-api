from random import randint
class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._next_id = 1
        self._members = [
            {"id": 1, 
             "name": "John", 
             "age": 33, 
             "lucky_numbers": [7, 13, 22]
             },
            {"id": 2, 
             "name": "Jane", 
             "age": 35, 
             "lucky_numbers": [10, 14, 3]
             },
            {"id": 3, 
             "name": "Jimmy", 
             "age": 5, 
             "lucky_numbers": [1]
             }
        ]

    def _generateId(self):
        """Genera un nuevo ID único para un miembro."""
        current_id = self._next_id
        self._next_id += 1
        return current_id

    def add_member(self, member):
        """Agrega un nuevo miembro a la familia."""
        member['id'] = member.get('id', self._generateId())
        member['last_name'] = self.last_name
        self._members.append(member)

    def delete_member(self, id):
        """Elimina un miembro de la familia por su ID."""
        self._members = [member for member in self._members if member['id'] != id]

    def get_member(self, id):
        """Obtiene un miembro de la familia por su ID."""
        return next((member for member in self._members if member['id'] == id), None)

    def get_all_members(self):
        """Devuelve todos los miembros de la familia."""
        return self._members
class StudentsModel:
    def __init__(self, id, nip, apprentice, ine, username, last_name, first_name, email, isadmin,td_id,
                td_name,tp_id, tp_name,promotion_id ,promotion_year, promotion_level, 
                 degree_id, degree_name, role_id, role_name):
        self.id = id
        self.nip = nip
        self.apprentice = apprentice
        self.ine = ine
        self.username = username
        self.last_name = last_name
        self.first_name = first_name
        self.email = email
        self.isadmin = isadmin
        self.td_id= td_id
        self.tp_id= tp_id
        self.td_name = td_name
        self.tp_name = tp_name
        self.promotion_id= promotion_id
        self.promotion_year = promotion_year
        self.promotion_level = promotion_level
        self.degree_id = degree_id
        self.degree_name = degree_name
        self.role_id = role_id
        self.role_name = role_name

    def jsonify(self):
        return {
            "personal_info": {
                "id": self.id,
                "nip": self.nip,
                "apprentice": self.apprentice,
                "ine": self.ine
            },
            "user_info": {
                "username": self.username,
                "last_name": self.last_name,
                "first_name": self.first_name,
                "email": self.email,
                "isadmin": self.isadmin,
                "role": {
                    "id": self.role_id,
                    "name": self.role_name
                }
            },
            "academic_info": {
                "td": {
                    "id"   : self.td_id,
                    "name": self.td_name
                },
                "tp": {
                    "id"   : self.tp_id,
                    "name": self.tp_name
                },
                "promotion": {
                    "id": self.promotion_id,
                    "year": self.promotion_year,
                    "level": self.promotion_level
                },
                "degree": {
                    "id": self.degree_id,
                    "name": self.degree_name
                }
            }
        }

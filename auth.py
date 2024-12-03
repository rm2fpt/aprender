from flask_login import UserMixin
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

# Configuração do Supabase
supabase = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_KEY')
)

class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data.get('id')
        self.email = user_data.get('email')
        self.name = user_data.get('name')
        self.picture = user_data.get('picture')

    @staticmethod
    def get(user_id):
        try:
            response = supabase.table('users').select('*').eq('id', user_id).execute()
            if response.data:
                return User(response.data[0])
        except Exception as e:
            print(f"Erro ao buscar usuário: {e}")
        return None

    @staticmethod
    def create_or_update_user(user_info):
        try:
            # Verifica se o usuário já existe
            response = supabase.table('users').select('*').eq('email', user_info['email']).execute()
            
            user_data = {
                'email': user_info['email'],
                'name': user_info.get('name', ''),
                'picture': user_info.get('picture', '')
            }

            if not response.data:
                # Cria novo usuário
                response = supabase.table('users').insert(user_data).execute()
            else:
                # Atualiza usuário existente
                user_id = response.data[0]['id']
                response = supabase.table('users').update(user_data).eq('id', user_id).execute()

            return User(response.data[0])
        except Exception as e:
            print(f"Erro ao criar/atualizar usuário: {e}")
            return None

from app.extensions import get_db


class TokenRepository:

    # AÑADIR EL TOKEN A LA LISTA NEGRA
    @staticmethod
    def add_to_blacklist(token, user_id):
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO token_blacklist (token, user_id) VALUES (%s, %s)",
                (token, user_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error Blacklist: {e}")
            return False
        finally:
            cursor.close()


    # VALIDACIÓN DEL TOKEN
    @staticmethod
    def is_blacklisted(token):
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM token_blacklist WHERE token = %s", (token,))
            result = cursor.fetchone()
            return result is not None
        finally:
            cursor.close()
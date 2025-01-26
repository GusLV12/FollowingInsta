from dotenv import load_dotenv
import os

# Obtener la ruta absoluta del archivo .env
dotenv_path = os.path.join(os.path.dirname(__file__), "..", "env", ".env")
print(f"Loading .env file from: {dotenv_path}")

# Cargar las variables desde el archivo .env
load_dotenv(dotenv_path)

# Obtener las variables del entorno
username = os.getenv("IG_NAME")
password = os.getenv("IG_PSSD")

print(f"Username: {username}")
print(f"Password: {password}")


print("Variables loaded successfully!")

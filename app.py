from src import app

if __name__ == '__main__':
  try:
    app.run(host='127.0.0.1', port=5000, debug=True)
  except Exception as e:
    print(f"Error al iniciar la aplicación: {e}")

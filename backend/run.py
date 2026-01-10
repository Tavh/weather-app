from app import create_app
from app.core.database import init_db

connexion_app = create_app()
app = connexion_app.app

if __name__ == '__main__':
    print("Initializing database...")
    init_db()
    
    # Run using the standard Flask development server
    # With Connexion 2.x, routes are registered on 'app'
    app.run(host="127.0.0.1", port=8080, debug=True)

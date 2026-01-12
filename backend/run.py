from app import create_app
from app.core.database import init_db

connexion_app = create_app()
app = connexion_app.app

if __name__ == '__main__':
    from app.core.logging import setup_logging
    setup_logging()
    
    print("Initializing database...")
    init_db()
    
    # Run using the standard Flask development server
    # With Connexion 2.x, routes are registered on 'app'
    # Use 0.0.0.0 to bind to all interfaces, making it accessible from outside the container
    app.run(host="0.0.0.0", port=8080, debug=False)

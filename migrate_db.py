from app import app, db
from models import User
from datetime import datetime

def migrate_database():
    with app.app_context():
        # Get the current table info
        inspector = db.inspect(db.engine)
        columns = inspector.get_columns('user')
        column_names = [col['name'] for col in columns]
        
        print("Current columns:", column_names)
        
        # Check if we need to migrate
        if 'created_at' not in column_names:
            print("Migrating database...")
            
            # Create a temporary table with new schema
            db.session.execute('''
                CREATE TABLE user_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    created_at DATETIME,
                    last_login DATETIME
                )
            ''')
            
            # Copy data from old table
            db.session.execute('''
                INSERT INTO user_new (id, username, password, created_at, last_login)
                SELECT id, username, password, datetime('now'), NULL FROM user
            ''')
            
            # Drop old table and rename new one
            db.session.execute('DROP TABLE user')
            db.session.execute('ALTER TABLE user_new RENAME TO user')
            
            db.session.commit()
            print("Migration completed successfully!")
        else:
            print("Database is already up to date.")

if __name__ == '__main__':
    migrate_database()
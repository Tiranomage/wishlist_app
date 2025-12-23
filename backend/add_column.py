from db import engine
from sqlalchemy import text

with engine.connect() as conn:
    trans = conn.begin()
    try:
        conn.execute(text('ALTER TABLE gifts ADD COLUMN selected BOOLEAN DEFAULT FALSE'))
        trans.commit()
        print('Column added successfully')
    except Exception as e:
        if "duplicate column name" in str(e).lower():
            print('Column already exists')
            trans.commit()
        else:
            print(f'Error: {e}')
            trans.rollback()
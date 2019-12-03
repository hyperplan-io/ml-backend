import sqlite3
from uuid import uuid4
from io import BytesIO 
import json
from functools import partial
import numpy as np
from typing import Callable

def insert_prediction(conn, features, metadata, labels):
    serializedFeatures = BytesIO()
    np.save(serializedFeatures, features)
    serializedFeatures.seek(0)
    serializedX = json.dumps(serializedFeatures.read().decode('latin-1'))

    serializedLabels = BytesIO()
    np.save(serializedLabels, labels)
    serializedLabels.seek(0)
    serializedY = json.dumps(serializedLabels.read().decode('latin-1'))
    prediction_id = str(uuid4())
    conn.execute(
        '''
        INSERT INTO predictions(id, features, labels) VALUES(?,?,?)
        ''', (prediction_id, serializedX, serializedY)
    )
    print(metadata)
    conn.executemany(
        '''
        INSERT INTO entities(prediction_id, key, value) VALUES(?,?,?)
        ''', list(map(lambda kv: (prediction_id, kv[0], kv[1]), metadata))
    )
    conn.commit()

def sqlite_hook(filename) -> Callable[[np.ndarray], None]:
    conn = sqlite3.connect(filename)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS predictions(
            id BLOB,
            features BLOB,
            labels BLOB,
            examples BLOB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP 
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS entities(
            prediction_id BLOB,
            key TEXT,
            VALUE TEXT
        )
    ''')
    return partial(insert_prediction, conn)

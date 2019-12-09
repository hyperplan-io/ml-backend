import sqlite3
from uuid import uuid4
from io import BytesIO 
import json
from functools import partial
import numpy as np
from typing import Callable, Dict

def insert_prediction(conn, features, labels, metadata):
    serializedFeatures = BytesIO()
    np.save(serializedFeatures, features)
    serializedFeatures.seek(0)
    serializedX = json.dumps(serializedFeatures.read().decode('latin-1'))

    serializedLabels = BytesIO()
    np.save(serializedLabels, labels)
    serializedLabels.seek(0)
    serializedY = json.dumps(serializedLabels.read().decode('latin-1'))

    serializedExamples= BytesIO()
    np.save(serializedExamples, np.array([]))
    serializedExamples.seek(0)
    serializedExamples = json.dumps(serializedExamples.read().decode('latin-1'))

    prediction_id = str(uuid4())
    conn.execute(
        '''
        INSERT INTO predictions(id, features, labels, examples) VALUES(?,?,?,?)
        ''', (prediction_id, serializedX, serializedY, serializedExamples)
    )
    conn.executemany(
        '''
        INSERT INTO entities(prediction_id, key, value) VALUES(?,?,?)
        ''', list(map(lambda kv: (prediction_id, kv[0], kv[1]),  [[key, value] for key,value in metadata.items()]))
    )
    conn.commit()
    return prediction_id

def read_predictions(conn):
    cursor = conn.execute('SELECT id, features, labels, examples, created_at, updated_at, key, value FROM predictions LEFT JOIN entities ON entities.prediction_id = predictions.id').fetchall()
    data = {}
    for row in cursor:
        prediction_id = row[0]
        features = row[1]
        labels = row[2]
        examples = row[3]
        created_at = row[4]
        updated_at = row[5]
        key = row[6]
        value = row[7]

        featureMemfile = BytesIO()
        featureMemfile.write(json.loads(features).encode('latin-1'))
        featureMemfile.seek(0)

        labelMemfile = BytesIO()
        labelMemfile.write(json.loads(labels).encode('latin-1'))
        labelMemfile.seek(0)

        exampleMemfile = BytesIO()
        exampleMemfile.write(json.loads(examples).encode('latin-1'))
        exampleMemfile.seek(0)

        metadata = {}
        if key is not None:
            metadata[key] = value

        if prediction_id in data:
            prediction = data[prediction_id]
            data[prediction_id] = (prediction_id, prediction[1], prediction[2], prediction[3], prediction[4], prediction[5], reduce(lambda x,y: dict(x, **y), (prediction[6], metadata)))
        else:
            data[prediction_id] = (prediction_id, np.load(featureMemfile), np.load(labelMemfile), np.load(exampleMemfile), created_at, updated_at, metadata)
    return list(data.values())

def sqlite_hook(filename) -> Callable[[np.ndarray, np.ndarray, Dict], None]:
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
    conn.commit()
    return partial(insert_prediction, conn)

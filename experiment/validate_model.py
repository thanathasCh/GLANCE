import backend
import config
import cv2
import numpy as np

(x_train, y_train), (x_test, y_test) = backend.load_data()
embedding_model, model = backend.create_siamese_network()
model.load_weights(config.checkpoint_path)

database = []

for i in range(10):
    indice_pos = np.squeeze(np.where(y_train == i))
    database.append(x_train[indice_pos[0]])

database = np.array(database)
database = embedding_model.predict(database)

example_index = 111
example_x, example_y = np.expand_dims(x_train[example_index], axis=0), y_test[example_index]
example_emb = embedding_model.predict(example_x)[0]

distances = np.linalg.norm(database - example_emb, axis=1)
for i, label in enumerate(distances):
    print(i, label)
import backend
import config

backend.clear_logs(True)

(x_train, y_train), (x_test, y_test) = backend.load_data()
steps_per_epoch = int(x_train.shape[0]/config.batch_size)

embedding_model, net = backend.create_siamese_network(config.describe_model)
callbacks = backend.get_callbacks()
net.compile(loss=backend.triplet_loss, optimizer='adam')


_ = net.fit( 
    backend.data_generator(x_train, y_train),
    steps_per_epoch=steps_per_epoch,
    epochs=config.epochs,
    verbose=True,
    callbacks=callbacks
)
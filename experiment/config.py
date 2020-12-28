emb_size = 128
alpha = 0.2
batch_size = 64
epochs = 500
image_shape=(56, 56)
describe_model = False
checkpoint_path = 'checkpoints/weights-00000010.h5'
data_file = 'products.data'

input_shape=(image_shape[0], image_shape[1], 3)
batch_input_shape=(batch_size, input_shape[0], input_shape[1], input_shape[2])
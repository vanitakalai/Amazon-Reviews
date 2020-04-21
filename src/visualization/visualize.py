import matplotlib.pyplot as plt

def plot_model_resutls(history):
  fig, ax = plt.subplots(1, 2, figsize=(12, 6))

  loss = history.history['loss']
  val_loss = history.history['val_loss']
  epochs = range(1, len(loss) + 1)

  ax[0].plot(epochs, loss, 'bo', label='Training loss')
  ax[0].plot(epochs, val_loss, 'b', label='Validation loss')
  ax[0].set_title('Training and validation loss')
  ax[0].set_xlabel('Epochs')
  ax[0].set_ylabel('Loss')
  ax[0].legend()

  acc = history.history['accuracy']
  val_acc = history.history['val_accuracy']

  ax[1].plot(epochs, acc, 'bo', label='Training acc')
  ax[1].plot(epochs, val_acc, 'b', label='Validation acc')
  ax[1].set_title('Training and validation accuracy')
  ax[1].set_xlabel('Epochs')
  ax[1].set_ylabel('Accuracy')
  ax[1].legend()

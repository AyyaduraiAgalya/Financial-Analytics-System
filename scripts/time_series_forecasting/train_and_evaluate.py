from data_preparation import main as prepare_data
from lstm_model import create_lstm_model
from evaluate_model import evaluate_model
from tensorflow.keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt

def plot_training_history(history):
    """
    Plots training and validation loss over epochs.

    Args:
        history: History object from model training.
    """
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

def train_and_evaluate():
    """
    Full pipeline to train and evaluate the LSTM model.
    """
    # Step 1: Prepare data
    X_train, X_test, y_train, y_test, scaler = prepare_data()

    # Step 2: Build LSTM model
    input_shape = (X_train.shape[1], X_train.shape[2])
    model = create_lstm_model(input_shape)

    # Step 3: Train model with early stopping
    early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    history = model.fit(
        X_train, y_train,
        validation_data=(X_test, y_test),
        epochs=50,
        batch_size=32,
        callbacks=[early_stopping],
        verbose=1
    )

    # Step 4: Plot training history
    plot_training_history(history)

    # Step 5: Evaluate the model
    evaluation_metrics = evaluate_model(model, X_test, y_test, scaler)

    # Save the model
    model.save("models/lstm_model.h5")
    print("Model saved as 'models/lstm_model.h5'")

    return evaluation_metrics

if __name__ == "__main__":
    train_and_evaluate()
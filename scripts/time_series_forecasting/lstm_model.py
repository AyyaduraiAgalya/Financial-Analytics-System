from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

def create_lstm_model(input_shape, dropout_rate=0.2):
    """
    Builds and compiles an LSTM model for time series forecasting.

    Args:
        input_shape (tuple): Shape of the input data (timesteps, features).
        dropout_rate (float): Dropout rate to prevent overfitting.

    Returns:
        model: Compiled LSTM model.
    """
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=input_shape, return_sequences=True))
    model.add(Dropout(dropout_rate))
    model.add(LSTM(50, activation='relu'))
    model.add(Dropout(dropout_rate))
    model.add(Dense(1))

    model.compile(optimizer='adam', loss='mse')
    return model

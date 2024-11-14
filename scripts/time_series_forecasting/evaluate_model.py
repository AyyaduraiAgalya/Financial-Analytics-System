from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np


def evaluate_model(model, X_test, y_test, scaler):
    """
    Evaluates the LSTM model on test data and computes evaluation metrics.

    Args:
        model: Trained LSTM model.
        X_test (np.array): Test data features.
        y_test (np.array): True values for the test data.
        scaler: Scaler used to inverse transform predictions.

    Returns:
        dict: Dictionary containing RMSE and MAE scores.
    """
    # Make predictions
    y_pred_scaled = model.predict(X_test)

    # Inverse scale the predictions and true values
    y_pred = scaler.inverse_transform(y_pred_scaled)
    y_true = scaler.inverse_transform(y_test.reshape(-1, 1))

    # Calculate metrics
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)

    print(f"RMSE: {rmse:.4f}")
    print(f"MAE: {mae:.4f}")

    return {"RMSE": rmse, "MAE": mae}
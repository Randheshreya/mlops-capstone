import os
import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib


# Ensure MLflow points to the local server UI (optional but safe)
mlflow.set_tracking_uri("http://127.0.0.1:5000")

EXPERIMENT_NAME = "mlops-capstone"


def main():
    mlflow.set_experiment(EXPERIMENT_NAME)

    # Start an MLflow run
    with mlflow.start_run() as run:
        # Load data
        df = pd.read_csv("data/housing.csv")
        X = df[["area"]]
        y = df["price"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Example hyperparameters (log even if model doesn't use them directly)
        learning_rate = 0.01
        epochs = 10
        mlflow.log_param("learning_rate", learning_rate)
        mlflow.log_param("epochs", epochs)
        mlflow.log_param("model_type", "LinearRegression")

        # Train model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Predict + metrics
        preds = model.predict(X_test)
        mse = mean_squared_error(y_test, preds)
        r2 = r2_score(y_test, preds)

        mlflow.log_metric("mse", float(mse))
        mlflow.log_metric("r2", float(r2))

        # Save a local copy (optional)
        os.makedirs("models", exist_ok=True)
        joblib.dump(model, "models/model.pkl")

        # Infer signature & input example for MLflow
        signature = infer_signature(X_train, model.predict(X_train))
        input_example = X_test.head(5)

        # Log model artifact (will appear under Artifacts in MLflow UI)
        mlflow.sklearn.log_model(
            sk_model=model,
            name="linear_regression_model",
            signature=signature,
            input_example=input_example,
        )

        run_id = run.info.run_id
        exp_id = run.info.experiment_id
        print(f"Run completed. experiment_id={exp_id}, run_id={run_id}")


if __name__ == "__main__":
    main()

from azureml.core import Workspace, Experiment, Dataset, Datastore, Run
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib
import os

def main(args):
    # Verbind met je AML Workspace
    ws = Workspace.from_config(path="../config/config.json")

    # Verbind met je datastore (Blob Storage)
    datastore = Datastore.get(ws, datastore_name='ehbdatabase')

    # Maak een TabularDataset aan vanuit je Blob Storage container
    dataset = Dataset.Tabular.from_delimited_files(path=(datastore, '/*.txt'))

    # Registreer de dataset in je workspace
    dataset = dataset.register(workspace=ws, name='processed_data')

    # Start een run
    experiment = Experiment(ws, name='train-logistic-regression')
    run = experiment.start_logging()

    try:
        # Laad de data
        data = pd.read_csv(args.data_path, delimiter='\t')  # Pas dit aan naar je eigen dataformaat

        # Verwerk je data (voorbeeld)
        X = data['text']  # Pas dit aan naar je eigen features
        y = data['label']  # Pas dit aan naar je eigen labels

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train het model
        model = LogisticRegression()
        model.fit(X_train, y_train)

        # Voorspel en evalueer het model
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f"Accuracy: {accuracy}")

        # Log de metrics
        run.log('accuracy', accuracy)

        # Sla het model op
        os.makedirs('outputs', exist_ok=True)
        joblib.dump(value=model, filename='outputs/model.pkl')

        # Registreer het model
        run.upload_file(name='outputs/model.pkl', path_or_stream='outputs/model.pkl')
        run.complete()

        model = run.register_model(model_name='logistic_regression_model',
                                   model_path='outputs/model.pkl',
                                   tags={'Training context': 'AzureML'},
                                   description='A logistic regression model')
    except Exception as e:
        run.fail(str(e))
    finally:
        run.complete()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', type=str, help='Path to the training data')
    args = parser.parse_args()
    main(args)

# imports
import feather
import pandas


def predict_model(upstream, product, lang, model_name, split_type, n_folds=10, quantile_intervals=None):
    # format variable
    upstream = dict(upstream)

    # import model class
    if lang == 'Python':
        import models
    elif lang == 'R':
        import rpy2.robjects as robjects
        from rpy2.robjects import pandas2ri
        import rpy2_r6.r6b as r6b
        r = robjects.r
        r['source']('models.R')

    if split_type == 'train_test':
        # load test data
        X_test = feather.read_dataframe(upstream['split_data']['test_X_data'])
        del upstream['split_data']

        # load model
        if lang == 'Python':
            model = load_python_model(
                models,
                model_name,
                next(iter(upstream.values()))['model']
            )
        elif lang == 'R':
            model = load_r_model(
                r6b,
                r,
                model_name,
                str(next(iter(upstream.values()))['model'])
            )
            # convert pandas dataframe to R dataframe
            pandas2ri.activate()
            X_test = pandas2ri.py2rpy_pandasdataframe(
                X_test
            )
            pandas2ri.deactivate()

        # predict
        preds = model.predict(X_test, quantile_intervals)

        if lang == 'R':
        # convert to pandas dataframe
            pandas2ri.activate()
            preds = robjects.conversion.rpy2py(preds)
            pandas2ri.deactivate()

        # save data for next process
        feather.write_dataframe(preds, product['predictions'])
    elif split_type == 'k_fold':
        # allocate memory for predictions
        predictions = []
        # for each fold
        for i in range(1, n_folds+1):
            # load test data
            X_test = feather.read_dataframe(
                upstream['split_data'][f'fold_{i}_X_data']
            )

            # load model
            if lang == 'Python':
                model = load_python_model(
                    models,
                    model_name,
                    upstream[f'{model_name}_fit'][f'model_{i}']
                )
            elif lang == 'R':
                model = load_r_model(
                    r6b,
                    r,
                    model_name,
                    str(upstream[f'{model_name}_fit'][f'model_{i}'])
                )
                # convert pandas dataframe to R dataframe
                pandas2ri.activate()
                X_test = pandas2ri.py2rpy_pandasdataframe(
                    X_test
                )
                pandas2ri.deactivate()

            # predict
            preds = model.predict(X_test, quantile_intervals)

            if lang == 'R':
            # convert to pandas dataframe
                pandas2ri.activate()
                preds = robjects.conversion.rpy2py(preds)
                pandas2ri.deactivate()

            # append fold predictions to predictions set
            predictions.append(preds)
        # save data for next process
        feather.write_dataframe(
            pandas.concat(predictions),
            product['predictions']
        )
        

def load_python_model(models, model_name, path):
    model_class = getattr(models, model_name)
    model = model_class()
    model.load(path)
    return model


def load_r_model(r6b, r, model_name, path):
    model_class = r6b.R6DynamicClassGenerator(r[model_name])
    model = model_class.new()
    model.load(path)
    return model
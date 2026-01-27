"""
# Encapsulate ML logic so it’s reusable and isolated.

CLASS LogisticModel:
    INITIALIZE:
        IF saved model exists:
            LOAD model
        ELSE:
            CREATE new logistic regression model

    FUNCTION train(features, labels):
        FIT model using training data

    FUNCTION predict(features):
        RETURN predictions from model

"""
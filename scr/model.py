from catboost import CatBoostClassifier


def load_model(session_state):
    model = CatBoostClassifier()
    session_state.model = model.load_model('model/multibank_hasedo_false')

from common import config
from annoy import AnnoyIndex

def _get_base_model():
    return AnnoyIndex(config.EMB_SIZE, config.DIS_ALG)


def _load_model(locationId):
    path = config.ANNOY_DB_PATH(locationId)
    annoyModel = _get_base_model()
    annoyModel.load(path)

    return annoyModel

def create_model(ids, features, locationId):
    model = _get_base_model()

    for product_id, feature in zip(ids, features):
        model.add_item(product_id, feature)

    model.build(config.BUILD_NUM)
    _save_model(model, locationId)
    _del_model(model)


def find_annoy(feature, locationId):
    model = _load_model(locationId)
    ids = model.get_nns_by_vector(feature, config.K_NUM)
    _del_model(model)

    return ids


def _save_model(model, locationId):
    path = config.ANNOY_DB_PATH(locationId)
    print(path)
    model.save(path)


def _del_model(model):
    del model
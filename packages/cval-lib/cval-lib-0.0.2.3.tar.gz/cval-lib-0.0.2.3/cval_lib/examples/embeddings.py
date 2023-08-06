if __name__ == '__main__':
    from random import random
    import uuid

    from cval_lib.connection import CVALConnection
    from cval_lib.models.embedding import ImageEmbeddingModel

    img_id_1 = str(uuid.uuid4().hex)
    img_id_2 = str(uuid.uuid4().hex)

    embeddings = [
        ImageEmbeddingModel(id=img_id_1, image_embedding=list(map(lambda x: random(), range(1000)))),
        ImageEmbeddingModel(id=img_id_2, image_embedding=list(map(lambda x: random(), range(1000)))),
    ]

    print(embeddings)
    user_api_key = 'USER_API_KEY'
    cval = CVALConnection(user_api_key)
    ds = cval.dataset()
    ds.create()
    emb = cval.embedding("d5b49f6b-f34b-4688-bef3-ae8209040041", 'training')
    emb.upload_many(embeddings)
    ds.embedding(type_of_dataset='training').get_many()
    print(emb.get_many())

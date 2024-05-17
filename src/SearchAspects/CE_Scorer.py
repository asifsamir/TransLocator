from sentence_transformers import CrossEncoder

class CrossEncoderScorer:
    def __init__(self, model_path, init_model=True):

        if init_model:
            self.model = CrossEncoder(model_path)
        else:
            self.model = None
        # self.model.to(device)


    def score(self, method_body, query):

        if self.model is None:
            raise Exception('Model not initialized. Please provide a valid model path.')

        score = self.model.predict([[method_body, query]])

        return score[0]





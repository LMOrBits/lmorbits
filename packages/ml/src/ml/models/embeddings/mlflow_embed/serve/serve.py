import os
import yaml
from pathlib import Path

from sentence_transformers import SentenceTransformer
import litserve as ls
from pathlib import Path
from fastapi.responses import JSONResponse

from fastembed import TextEmbedding

class EmbeddingAPI(ls.LitAPI):

    def __init__(self, params):
        super().__init__()
        self.params = params

    def setup(self,device):
        self.instruction = "Represent this sentence for searching relevant passages: "
        self.model =  TextEmbedding()

    def decode_request(self, request):
        return request["input"]

    def predict(self, query):
        return self.model.embed(query)

    def encode_response(self, output):
        list_of_numpy = list(output)
        return JSONResponse({"result": [d.tolist() for d in list_of_numpy]})  # Convert first ndarray to list



if __name__ == "__main__":
    params_file = Path(os.environ.get('PARAMS_FILE', 'params.yaml'))
    with open(params_file) as f:
        params = yaml.safe_load(f)

    api = EmbeddingAPI(params)
    server = ls.LitServer(api)
    server.run(port=1111)

   
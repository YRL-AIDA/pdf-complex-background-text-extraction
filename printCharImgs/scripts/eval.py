from cnn_model import Model
from config import DefaultModel
from font_recognition import FontRecognizer
# p1 = "../data/models_and_classnames/rus"
# p2 = "../data/models_and_classnames/eng"
# p3 = "../data/models_and_classnames/rus_eng"
model_re = Model.load_default_model()
model_r = Model.load_default_model(DefaultModel.Russian)
model_e = Model.load_default_model(DefaultModel.English)

m = FontRecognizer.load_model("../data/models_and_classnames/rus")
print("R+E", model_re.weights.get_metrics_result())

from speechbrain.inference.interfaces import foreign_class

classifier = foreign_class(source="speechbrain/emotion-recognition-wav2vec2-IEMOCAP", pymodule_file="custom_interface.py", classname="CustomEncoderWav2vec2Classifier")
out_prob, score, index, text_lab = classifier.classify_file("./anger.wav")
print(out_prob, score, index, text_lab)

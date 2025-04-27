import pandas
import random
data = pandas.read_csv("./data/Words_to_learn.csv")
to_learn = data.to_dict(orient="records")
fr_words = random.choice(to_learn)
print(fr_words)
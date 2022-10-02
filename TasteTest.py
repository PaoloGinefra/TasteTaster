import gradio as gr
import numpy as np
from imageDownloader import getUrl

import pandas as pd
import numpy as np

OBJECTS_NUMBER = 50

# Imports, shuffles and selects the food names
data = pd.read_csv('./foods.csv')
names = np.array(data.name)
np.random.shuffle(names)

Objects = names[:OBJECTS_NUMBER]


def analyze(*argv):
    pos = 0
    zero = 0
    total = 0
    Len = 0

    for i in range(len(argv) // 2):
        if not argv[2*i + 1]:
            v = argv[2*i]
            pos += v > 0
            zero += v == 0

            total += v
            Len += 1

    return pos, zero, Len - pos - zero, total/Len, len(argv)//2 - Len


with open('./index.css') as css:
    with gr.Blocks(css=css.read()) as demo:

        gr.Markdown('# Tastes Test')
        gr.Markdown('Express your taste on various food where:')
        gr.Markdown('- **-10** = I absolutely hate this')
        gr.Markdown('- **0** = Neutral')
        gr.Markdown('- **10** = This is my favourite food')

        with gr.Tab("Tastes"):
            inputs = []

            for i, obj in enumerate(Objects):
                with gr.Row():
                    url = getUrl(obj)
                    with gr.Column(scale=0.25):
                        image = gr.Image(url, shape=(100, None))

                    with gr.Column():
                        gr.Markdown(f'## {i+1}-' + obj)

                        input = gr.Slider(-10, 10, 0, step=1,
                                          label='To my tastes it\'s a', elem_id='slider')

                        checkBox = gr.Checkbox(False, label='Skip')

                        inputs.append(input)
                        inputs.append(checkBox)

        with gr.Tab("Results"):
            Liked = gr.Number(0, label="Liked")
            Neutral = gr.Number(0, label="Neutral")
            Disliked = gr.Number(0, label="Disliked")

            Average = gr.Number(0, label="Average")

            Skipped = gr.Number(0, label="Skipped")

            outputs = [Liked, Neutral, Disliked, Average, Skipped]

            for i in inputs:
                i.change(analyze, inputs, outputs)

    demo.launch()

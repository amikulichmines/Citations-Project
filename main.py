from bokeh.models.widgets import FileInput, TextAreaInput, Button
from bokeh.models import CustomJS
from pybase64 import b64decode
import io
from bokeh.io import curdoc
from bokeh.layouts import row, column, layout
from bokeh.models import HoverTool, ColumnDataSource, Div, MultiSelect, Select, Slider, TextInput, ColorBar, \
    LinearColorMapper, LinearAxis, Range1d, Toggle, Paragraph, Span, BoxZoomTool
from bokeh.plotting import figure, output_file, show, save
from bokeh.palettes import Inferno256
from bokeh.transform import linear_cmap, transform
from bokeh.models.widgets import Panel, Tabs
from bokeh.io import show
from bokeh.models import CustomJS, TextInput
from model_class import model

abstract_input = TextAreaInput(value="", title="Paste abstract here:", height=250)
abstract_input.js_on_change("value", CustomJS(code="""
    console.log('text_input: value=' + this.value, this.toString())
"""))

title_input = TextInput(value="", title="Enter paper title here")
title_input.js_on_change("value", CustomJS(code="""
    console.log('text_input: value=' + this.value, this.toString())
"""))

author_number = Select(title="Enter the number of authors:", value="0",
                       options=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], width=60)
author_number.js_on_change("value", CustomJS(code="""
    console.log('select: value=' + this.value, this.toString())
"""))
error_message = Div(text="")

p = Paragraph(text="Based on the information you entered, your paper is expected to garner:")

y1 = Paragraph(text="-")
y1text = Paragraph(text=" citations after 1 year")
y5 = Paragraph(text="-")
y5text = Paragraph(text=" citations after 5 years")
y10 = Paragraph(text="-")
y10text = Paragraph(text=" citations after 10 years")
grid = row(column([y1, y5, y10]), column([y1text, y5text, y10text]))


def calculate(title, authors, abstract, paper, ):
    print(title)
    print(authors)
    print(abstract)
    print(paper)
    # SVM
    # kNN
    model.fit()
    model.predict()
    return (5, 10, 15)


def get_paper_string():
    data = str(b64decode(file_input.value))
    return data


y1.text = " - "


def update_output():
    title = title_input.value
    authors = author_number.value
    abstract = abstract_input.value
    paper = get_paper_string()
    if check_for_errors():
        y1.text = "-"
        y5.text = "-"
        y10.text = "-"
    else:
        y1.text = str(calculate(title, authors, abstract, paper)[0])
        y5.text = str(calculate(title, authors, abstract, paper)[1])
        y10.text = str(calculate(title, authors, abstract, paper)[2])
    print("clicked")

def check_for_errors():
    errors = False
    error_message.text = "<p style='color:red;'>"
    print(file_input.value)
    if file_input.value == "":
        errors=True
        error_message.text+="<br>Error: No file uploaded!"
    if author_number.value == "0":
        errors=True
        error_message.text+="<br>Error: Number of authors must be greater than 0"
    if title_input.value == "":
        errors=True
        error_message.text+="<br>Error: Title cannot be empty"
    if len(title_input.value) > 4000:
        errors=True
        error_message.text+="<br>Error: Title is too long!"
    if title_input.value == "":
        errors=True
        error_message.text+="<br>Error: Abstract cannot be empty"
    if len(abstract_input.value) > 10000:
        errors=True
        error_message.text += "<br>Error: Abstract is too long!"
    return errors


button = Button(label='Predict citations', button_type='success', aspect_ratio=3)
# button.js_on_click(CustomJS(code="console.log('button: click!', this.toString())"))
button.on_click(update_output)


file_input = FileInput(accept=".txt,.pdf", name="Import paper here")

controls = [file_input, title_input, author_number, abstract_input, button, error_message]
displays = [p, grid]

inputs = column(controls, width=500, height=1000)
outputs = column(displays, width=500, height=100)

inputs2 = column(Div(text="<h1>Inputs</h1>"), inputs)
outputs2 = column(Div(text="<h1>Outputs</h1>"), outputs)
final_row = row(inputs2, outputs2)
pan_oi = Panel(child=final_row, title="Citations")

tabs = Tabs(tabs=[pan_oi])
curdoc().add_root(tabs)

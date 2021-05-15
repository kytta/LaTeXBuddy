from jinja2 import Environment, PackageLoader


env = Environment(loader=PackageLoader("latexbuddy"))


def render_html(file_name, file_text, errors):
    err_values = sorted(errors.values(), key=lambda e: int(e.start))
    template = env.get_template("result.html")
    highlighted_file_text = highlight_code(file_text, errors)
    return template.render(
        file_name=file_name, highlighted_file_text=highlighted_file_text, errors=errors
    )


def highlight_code(file_text, errors):
    # offset = 0
    # for error in sorted(errors.values(), key=lambda e: int(e.start)):
    #     start_index = int(error.start) + offset
    #     end_index = start_index + int(error.length)
    #     file_text = (
    #         file_text[:start_index]
    #         + "<u>"
    #         + file_text[start_index:end_index]
    #         + "</u>"
    #         + file_text[end_index:]
    #     )
    #     offset += len("<u></u>")

    return file_text

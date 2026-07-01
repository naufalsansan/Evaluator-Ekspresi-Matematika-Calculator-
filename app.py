from flask import Flask, render_template, request, redirect, url_for

from calculator import (
    validate_expression,
    infix_to_postfix_steps,
    evaluate_postfix_steps
)

app = Flask(__name__)

# Riwayat Perhitungan
history = []


@app.route("/", methods=["GET", "POST"])
def index():

    result = None
    postfix = None
    error = None

    steps_convert = []
    steps_evaluate = []

    if request.method == "POST":

        expression = request.form["expression"].strip()

        if expression == "":
            error = "Masukkan ekspresi terlebih dahulu."

        else:

            valid, message = validate_expression(expression)

            if not valid:
                error = message

            else:

                try:

                    postfix, steps_convert = infix_to_postfix_steps(expression)

                    result, steps_evaluate = evaluate_postfix_steps(postfix)

                    history.insert(0, {
                        "expression": expression,
                        "postfix": " ".join(postfix),
                        "result": result
                    })

                except ZeroDivisionError:

                    error = "Tidak boleh membagi dengan nol."

                except Exception as e:

                    error = str(e)

    return render_template(
        "index.html",

        result=result,
        postfix=postfix,
        error=error,

        history=history,

        steps_convert=steps_convert,
        steps_evaluate=steps_evaluate
    )


@app.route("/clear", methods=["POST"])
def clear():

    history.clear()

    return redirect(url_for("index"))


if __name__ == "__main__":

    app.run(debug=True, use_reloader=False)
from flask import Flask, render_template, request, session
from googletrans import Translator
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.permanent_session_lifetime = timedelta(days=7)

translator = Translator()

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session:
        session['history'] = []

    translation = None
    detected_lang = None
    dest_lang = None
    text = ""

    if request.method == 'POST':
        text = request.form.get('text', '')
        dest_lang = request.form.get('language', '')
        if text.strip() and dest_lang:
            try:
                result = translator.translate(text, dest=dest_lang)
                translation = result.text
                detected_lang = result.src

                session['history'].insert(0, {
                    'original': text,
                    'translated': translation,
                    'from': detected_lang,
                    'to': dest_lang
                })
                session.modified = True
            except Exception as e:
                translation = f"Error: {str(e)}"

    return render_template(
        'index.html',
        translation=translation,
        detected_lang=detected_lang,
        dest_lang=dest_lang,
        history=session['history'],
        text=text
    )

if __name__ == '__main__':
    app.run(debug=True)

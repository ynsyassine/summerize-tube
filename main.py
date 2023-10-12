from UTILS import *
from flask import Flask, request, render_template_string

app = Flask(__name__)
template = '''
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <title>Video Summarizer</title>
  </head>
  <body>
    <div class="container">
      <h1 class="mt-5">Video Summarizer</h1>
      <form method="post">
        <div class="mb-3">
          <label for="video_url" class="form-label">Video URL</label>
          <input type="text" class="form-control" id="video_url" name="video_url" required>
        </div>
        <button type="submit" class="btn btn-primary">Summarize</button>
      </form>
      {% if summary %}
      <h2 class="mt-5">Summary</h2>
      <p>{{ summary }}</p>
      {% endif %}
    </div>
    <!-- Optional JavaScript; choose one of the two! -->
    <!-- Option 1: Bootstrap Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"></script>
  </body>
</html>
'''
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form['video_url']
        audio_file = get_audio(video_url)
        audio_chunks = return_chunks(audio_file)
        full_script = transcript_chunk(audio_chunks)
        summary = final_summarize(full_script)
        return render_template_string(template, summary=summary)
    return render_template_string(template)


if __name__ == '__main__':
    app.run(debug=True)

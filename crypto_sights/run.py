from app import create_app
import subprocess
import os

app = create_app()

if __name__ == "__main__":

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    EVAL_BACKEND_PATH = os.path.join(
        BASE_DIR, "evaluation", "evalbackend.py"
    )

    print("Eval backend path:", EVAL_BACKEND_PATH)

    subprocess.Popen(["python", EVAL_BACKEND_PATH])

    app.run(host="0.0.0.0", port=7860, debug=False)

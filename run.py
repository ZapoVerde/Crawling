# run.py


def run_console():
    from console_ui import main as console_main
    console_main()


def run_web():
    from web_ui import app
    app.run(debug=True)


if __name__ == "__main__":
    # Choose which UI layer to use
    run_console()
    # To launch the web interface instead, just comment this out and use:
    # run_web()

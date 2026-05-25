.PHONY: compile refresh-installer

compile: main.py
	pyinstaller --noconsole --onefile --add-data="data/help_dialog_subject.json:data" --name "AudLooper" ./main.py

refresh-installer:
	pip uninstall pyinstaller
	pip install pyinstaller

from kaggle.api.kaggle_api_extended import KaggleApi

api = KaggleApi()
api.authenticate()
# Save kaggle.json to the file path displayed in the OSError message given when attempting to import kaggle
api.kaggle competitions submit -c titanic -f submission.csv -m "Message"

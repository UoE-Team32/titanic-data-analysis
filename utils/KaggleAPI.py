from kaggle.api.kaggle_api_extended import KaggleApi

api = KaggleApi()
api.authenticate()
api.kaggle competitions submit -c titanic -f submission.csv -m "Message"

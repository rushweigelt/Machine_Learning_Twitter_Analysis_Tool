import json
twitter_cred = dict()


twitter_cred['CONSUMER_KEY'] = 'XLuTfzcgjUtlZs4dzGM3W2tq6'
twitter_cred['CONSUMER_SECRET'] = 'FfTFPxwhiI97wuy9TOe6Lq8Sgl8phJRFQNaukQbEXg6oblyuzJ'
twitter_cred['ACCESS_KEY'] = '1179141952794583042-IPNL6nE2SdzZnG26p3Ld5TgpBSNfA9'
twitter_cred['ACCESS_SECRET'] = 'ptuUKpOGbUZIg8alVapQdXg3ibPdoBMwGT5LBDW4DRcgK'

with open('twitter_credentials.json', 'w') as secret_info:
    json.dump(twitter_cred, secret_info, indent=4, sort_keys=True)

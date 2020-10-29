import tweepy


def status(message):
    # personal details
    consumer_key = "0eA3X2uuhNrss1YXTHHxde1qg"
    consumer_secret = "frcj79NinQOBGyhfhwMHNGGapD401JHyuQEAqo19B284ksk5ek"
    access_token = "845034311581601796-RoXubf5sNCxYkb4Wgb2gxZv6hfagycp"
    access_token_secret = "NUe3foY5ANduJMGILjlIT64NP1XF53TqhphO6I0V2l73N"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    api.update_status(status=message)

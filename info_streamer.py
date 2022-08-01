import tweepy
import os
from os.path import expanduser
from dotenv import load_dotenv
env_path = expanduser("~/.env2") # use .env for production
load_dotenv(dotenv_path=env_path, override=True)


def twitter_setup():
    # Authenticate and access using keys:
    auth = tweepy.OAuthHandler(os.getenv("CONSUMER_KEY"), os.getenv("CONSUMER_SECRET"))
    auth.set_access_token(os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_SECRET"))

    # Return API access:
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api

api = twitter_setup()

subst_list = ['mdma', 'lsd', 'amphetamine']

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):

        if hasattr(status, "retweeted_status"):  # Check if Retweet
            print(f" check if retweet:, {status['retweeted_status']['text']}")
        else:
            try:
                ## catch nesting
                replied_to=status.in_reply_to_screen_name
                answer_user=status.user.screen_name
                first_user=status.user.id
                answer_id=status.id
                answer_user_id = status.user.id
                ## ignore replies that by default contain mention
                reply_to_status_id=status.in_reply_to_status_id
                reply_to_user_id=status.in_reply_to_user_id
                status_text = status.text.lower()

#                 telegram_bot_sendtext(f"{replied_to}, 'nesting', {in_reply_to_user_id}, 'replied to', {replied_to}, 'message', {status.text}")

            except AttributeError:

                replied_to=status.in_reply_to_screen_name
                answer_user=status.user.screen_name
                answer_user_id = status.user.id
                answer_id=status.id
                reply_to_status_id=status.in_reply_to_status_id
                reply_to_user_id=status.in_reply_to_user_id

                # telegram_bot_sendtext(f"ATRIB ERROR: {replied_to}, 'nesting', {in_reply_to_user_id}, 'replied to', {replied_to}, 'message', {status.text}")

            update_status = f"""Thanks for calling me!
Please reply to this tweet with  - and the name of one of these substances to get safer use information: {subst_list}
for example -MDMA or -LSD. Alternatively, you can tweet: @ViewsOnDrugsBot -[substance name] or -help
"""

            # Warning: don't reply infinite times to yourself!!
            self_ids=[1319577341056733184, 1118874276961116162]
            print(status_text)
            if status.user.id not in self_ids and '-' in status_text:

                info_subs=status_text.split("-")[1]

                if info_subs in subst_list:
                    api.update_status(f"Here comes a safer use thread to {info_subs}", in_reply_to_status_id=answer_id,
                    auto_populate_reply_metadata=True)

                elif "help" in info_subs:

                    api.update_status(update_status, in_reply_to_status_id=answer_id,
                    auto_populate_reply_metadata=True)
                    print(answer_id, "help")
                else:
                    print(answer_id, subst_list)
                    pass


    def on_error(self, status):
        # telegram_bot_sendtext(f"ERROR with: {status}")
        print(f"ERROR with: {status}")



def listen_stream_and_rt(keyword):
    myStreamListener = MyStreamListener()
    try:
        myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
        myStream.filter(track=[keyword])
    except Exception as ex:
        # telegram_bot_sendtext(f"ERROR {ex} with: {status}")
        print(f"ERROR {ex}")

        pass

#listen to every mention of the bot but only interact with those having
# - and one of the substances on ´subst_list´ or -help
listen_stream_and_rt('ViewsOnDrugsBot')

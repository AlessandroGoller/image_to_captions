import csv
import json
from datetime import datetime
from itertools import dropwhile, takewhile

import instaloader
from tqdm import tqdm


class GetInstagramProfile:
    """
    Class to load a profile and download its data.
    """

    def __init__(self) -> None:
        self.L = instaloader.Instaloader()

    def download_users_profile_picture(self, username):
        """
        Download a user's profile picture.
        """
        self.L.download_profile(username, profile_pic_only=True)

    def download_users_posts_with_periods(self, username):
        """
        Download posts from a user within a specified period of time.
        """
        posts = instaloader.Profile.from_username(self.L.context, username).get_posts()
        SINCE = datetime(2021, 8, 28)
        UNTIL = datetime(2021, 9, 30)

        for post in takewhile(
            lambda p: p.date > SINCE, dropwhile(lambda p: p.date > UNTIL, posts)
        ):
            self.L.download_post(post, username)

    def download_hastag_posts(self, hashtag):
        """
        Download posts that contains a certain hashtag.
        """
        for post in instaloader.Hashtag.from_name(self.L.context, hashtag).get_posts():
            self.L.download_post(post, target="#" + hashtag)

    def get_users_followers(self, user_name):
        """
        Function to get a profile's followers.
        Note: login required to get a profile's followers.
        """
        self.L.login(input("input your username: "), input("input your password: "))
        profile = instaloader.Profile.from_username(self.L.context, user_name)
        file = open("follower_names.txt", "a+")
        for followee in profile.get_followers():
            username = followee.username
            file.write(username + "\n")
            print(username)

    def get_users_followings(self, user_name):
        """
        Function to get a profile's followings.
        Note: login required to get a profile's followings.
        """
        self.L.login(input("input your username: "), input("input your password: "))
        profile = instaloader.Profile.from_username(self.L.context, user_name)
        file = open("following_names.txt", "a+")
        for followee in profile.get_followees():
            username = followee.username
            file.write(username + "\n")
            print(username)

    def get_post_comments(self, username):
        """
        Function to get a post's comments and print them at screen.
        """
        posts = instaloader.Profile.from_username(self.L.context, username).get_posts()
        for post in posts:
            for comment in post.get_comments():
                print("comment.id  : " + str(comment.id))
                print("comment.owner.username  : " + comment.owner.username)
                print("comment.text  : " + comment.text)
                print("comment.created_at_utc  : " + str(comment.created_at_utc))
                print("************************************************")

    def get_post_info_csv(self, username):
        """
        Function to get info from every post of a user and store them in a csv file.
        """
        with open(username + ".csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            posts = instaloader.Profile.from_username(
                self.L.context, username
            ).get_posts()
            for post in posts:
                print("post date: " + str(post.date))
                print("post profile: " + post.profile)
                print("post caption: " + post.caption)
                print("post location: " + str(post.location))

                posturl = "https://www.instagram.com/p/" + post.shortcode
                print("post url: " + posturl)
                writer.writerow(
                    [
                        "post",
                        post.mediaid,
                        post.profile,
                        post.caption,
                        post.date,
                        post.location,
                        posturl,
                        post.typename,
                        post.mediacount,
                        post.caption_hashtags,
                        post.caption_mentions,
                        post.tagged_users,
                        post.likes,
                        post.comments,
                        post.title,
                        post.url,
                    ]
                )

                for comment in post.get_comments():
                    writer.writerow(
                        [
                            "comment",
                            comment.id,
                            comment.owner.username,
                            comment.text,
                            comment.created_at_utc,
                        ]
                    )
                    print("comment username: " + comment.owner.username)
                    print("comment text: " + comment.text)
                    print("comment date : " + str(comment.created_at_utc))
                print("\n\n")

    def get_post_info_json(self, username, last_n_posts=100):
        """
        Function to get info from every post of a user and store them in a json file (dictionary style).
        """
        data = {}
        posts = instaloader.Profile.from_username(self.L.context, username).get_posts()
        print(
            "Downloading last " + str(last_n_posts) + " posts from " + username + "..."
        )
        for _i in tqdm(range(last_n_posts)):
            post = posts.__next__()
            shortcode = post.mediaid_to_shortcode(post.mediaid)
            data[shortcode] = {}
            # Store the post info
            data[shortcode]["post"] = post.caption
            data[shortcode]["hashtags"] = post.caption_hashtags
            data[shortcode]["mentions"] = post.caption_mentions
            data[shortcode]["tagged_users"] = post.tagged_users
            data[shortcode]["likes"] = post.likes
            data[shortcode]["comments"] = post.comments
            data[shortcode]["date"] = str(post.date)
            data[shortcode]["location"] = post.location
            data[shortcode]["typename"] = post.typename
            data[shortcode]["mediacount"] = post.mediacount
            data[shortcode]["title"] = post.title
            data[shortcode]["posturl"] = "https://www.instagram.com/p/" + shortcode

        return data


def load_post_captions_from_json(json_file: str, shortcodes: list = None) -> list:
    """
    Function to load post captions from a json file. The post loaded are the one specified by the shortcodes list.
    This to allow compatibility with eventual search functions on the specific post.
    """
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    captions = []
    if shortcodes is None:
        # Load the complete file
        shortcodes = list(data.keys())
        for shortcode in shortcodes:
            captions.append(data[shortcode]["post"])
    else:
        for shortcode in shortcodes:
            captions.append(data[shortcode]["post"])

    return captions


if __name__ == "__main__":
    username = "dulacetduparc"
    client = GetInstagramProfile()
    data = client.get_post_info_json(username)
    # Save as json file
    with open(username + ".json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

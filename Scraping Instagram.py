import instaloader
from datetime import datetime
from itertools import dropwhile, takewhile


# creating an Instaloader() object
ig=instaloader.Instaloader()


username = input("Enter Instagram Username : ")

profile = instaloader.Profile.from_username(ig.context, username)

#Functions that helps to Extract Information
def get_followers():
    print(username," has ",profile.followers," Followers")


def get_followees():
    print(username," Following ",profile.followees," Members")

def get_dp():
    ig.download_profile(username,profile_pic_only=True)
    print("DP Downloaded Successfully Checkout ",username," Folder")

def get_bio():
    print("Heres the Bio: ")
    print("\"",profile.biography,"\"")


def post_count():
    print(username," Uploaded ",profile.mediacount," Posts")

def get_posts(n):

    posts = profile.get_posts()
    #no post condition
    for c,post in enumerate(posts, 1):
        if(c!=n+1):
            ig.download_post(post, target=f"{profile.username}")
        else:
            break
    print(n," Posts downloaded.")

def download_users_posts_with_periods():

    posts = instaloader.Profile.from_username(ig.context, username).get_posts()
    print(" From YEAR MONTH DATE: ")
    a,b,c=map(int,input().split())
    print(" To YEAR MONTH DATE: ")
    d,e,f=map(int,input().split())
    SINCE = datetime(a, b, c)
    UNTIL = datetime(d, e, f)
    ct=0
    for post in takewhile(lambda p: p.date > SINCE, dropwhile(lambda p: p.date > UNTIL, posts)):
        ig.download_post(post, username)
        ct+=1
    print("We found ",ct, " Posts. From ",a,b,c," To ",d,e,f)
    print(ct," Posts downloaded ")

def download_hastag_posts():
    hashtag=input("Please type hashtag: ")
    c=0
    for post in instaloader.Hashtag.from_name(ig.context, hashtag).get_posts():
        ig.download_post(post, target='#'+hashtag)
        c+=1
    if c==0:
        print(" No posts found with hashtag #",hashtag)
    elif c==1:
        print("Only 1 post found ")
    else:
        print("We found ",c, " posts")

def get_posts_info():
    cn=int(input("How many recent posts info do you need? "))
    posts = instaloader.Profile.from_username(ig.context, username).get_posts()
    for c,post in enumerate(posts, 0):
        if(c!=cn):
            print("POST-",c+1)
            print("Post Date: "+str(post.date))
            print("Post Profile: "+post.profile)
            print("Post Caption: "+post.caption)


            posturl = "https://www.instagram.com/p/"+post.shortcode
            print("Post url: "+posturl)
            print("\n")
        else:
            break



while True:
    print("\n")
    print("---> What you want to know about this profile")
    print("1. Followers")
    print("2. Followees")
    print("3. Download Profile Picture")
    print("4. Posts Count")
    print("5. Download Posts")
    print("6. Bio")
    print("7. Download Posts in Specific period")
    print("8. Download Posts with specific Hashtag")
    print("9. Full details of Posts")
    print("10. Exit")

    choice = int(input("Enter your choice: "))
    if choice == 1:
        get_followers()

    elif choice == 2:
        get_followees()

    elif choice == 3:
        get_dp()

    elif choice == 4:
        post_count()

    elif choice == 5:
        if(profile.is_private):
            print(username," is in Private")
        else:
            n=int(input("How many posts you want to download: "))
            if(n<=profile.mediacount):
                get_posts(n)
            else:
                print("User has only ",profile.mediacount," Posts")
                n=int(input("How many posts you want to download: "))
                if(n<=profile.mediacount):
                    get_posts(n)
                else:
                    print("I can't Help You")

    elif choice == 6:
        get_bio()
    elif choice==7:
        download_users_posts_with_periods()
    elif choice==8:
        download_hastag_posts()
    elif choice==9:
        get_posts_info()
    elif choice==10:
        break

import praw
import quoraCrawler
import AccountDetails
import time

if __name__ == "__main__":
    already_done  = []
    #Initaize the crawler
    quoraCrawler.initalize()
    r = praw.Reddit(user_agent = "quorabot")
    #add your account details into a seperate AccountDetails.py file
    r.login(AccountDetails.account_user, AccountDetails.account_pass)
    subreddit = r.get_subreddit(AccountDetails.account_subreddit)
    while True: 
        #Scan the specified subreddit for 100 seconds and add your comment 
        for submission in subreddit.get_new(limit = 10):
            if submission.domain == 'quora.com' and submission.id not in already_done:
                finalcomment = quoraCrawler.getFinalComments(submission.url)
                submission.add_comment(finalcomment)
                already_done.append(submission.id)
                print "Submitted to : " + submission.id            
                # sleep so that quora does not ban us
                time.sleep(10)
        #sleep for some time
        time.sleep(100)
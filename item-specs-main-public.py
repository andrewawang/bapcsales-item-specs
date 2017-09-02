import praw
import time
import sqlite3

reddit = praw.Reddit(client_id='___________',
                     client_secret="____________",
                     refresh_token="____________",
                     password="__________",
                     user_agent="__________",
                     username="__________")

subreddit = reddit.subreddit('buildapcsales')

#CURRENT VERSION ONLY SUPPORTS FREESYNC MONITOR SPECS
conn=sqlite3.connect('specs.db')
c=conn.cursor()

def executeScriptsFromFile(filename):
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    for command in sqlCommands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        #try:
        c.execute(command)
        #except OperationalError, msg:
            #print("Command skipped: " + msg)


executeScriptsFromFile('freesync_monitors.sql')

#freesync_monitors_table=open('freesync_monitors.sql' , 'r')
#freesync_monitors_table=freesync_monitors_table.read()
"""
for row in c.execute('SELECT * FROM FreeSync_Monitors'):
        print(row)
"""
old_posts=[]

def specs(post):
    """
    main spec scraper
    """
    #post_model=item_model(post.title)
    type,brand,model=title_scrape(post.title)

def title_scrape(title):
    """
    returns type of item, brand, and model name
    """
    #CURRENTLY ONLY ITENTIFIES MONITORS
    #PARTIAL GPU AND CASE SUPPORT
    title=title.lower()
    type, brand, model = "","",""
    type=type_scrape(title)
    if type=='monitor':
        brand=monitor_brand(title)
        model=monitor_model(title,brand)
    return type,brand,model

def type_scrape(title):
    """
    returns type, title assumed lowercase
    """
    types=['monitor','gpu', 'case'] #currently only itentifies types in list
    for k in types:
        if k in title:
            return k

def monitor_brand(title):
    """
    returns brand of monitor, assumes title lowercase
    """
    #todo: change to sql query
    brands=['aoc','asus','acer','ago','benq','dell','eizo','hp','i-odata','iiyama','lg','lenovo','nixeus','philips','samsung','viewsonic','pixio']
    for k in brands:
        if k in title:
            return k

def monitor_model(title,brand):
    """
    returns sku of model, assumes title lowercase
    """
    b = (brand,)
    #CURRENTLY HERE
    c.execute('SELECT MODEL FROM FreeSync_Monitors WHERE MANUFACTURER=?', b)
    model=str(c.fetchone())

    #sanitize model string
    return model
    


def comment(post):
    """
    comments the specs of the item
    """
    #need to scrape from sql file
    specs= " "

    post.add_comment(specs)

"""
MAIN
Always on loop that scans for new posts
"""
while True:
    new_post=next(subreddit.new())
    if new_post not in old_posts:
        old_posts.append(new_post)
        specs(new_post)
    time.sleep(20) #wait x seconds before checking for new post


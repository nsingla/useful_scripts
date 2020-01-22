import pandas as pd
import twitter
import time
import random



api = twitter.Api(consumer_key='xxxxxxx',
                      consumer_secret='xxxxxxx',
                      access_token_key='xxxxxxx',
                      access_token_secret='xxxxxxx',
                      sleep_on_rate_limit=True)


def get_target_followers(target_screen_name):
    followers = api.GetFollowerIDs(screen_name=target_screen_name)
    stats_list = []
    for follower in followers:
        user = api.GetUser(follower)
        stats_list.append([user.id, user.screen_name, user.location, user.verified, 
                           user.email, user.followers_count, user.friends_count, 
                           user.description])
    df = pd.DataFrame(stats_list, columns=['id', 'screen_name', 'location', 'verified', 'email',
                                           'num_followers', 'num_following', 'description'])
    df = df.sort_values(by='num_followers', ascending=False)
    return df


def filterc(x, keywords):
	'''
		Filters if keyword is found in location or description of the account
	'''
	for kw in keywords:
		if kw in x['location'].lower() or kw in x['description'].lower():
			return True
	return False


def get_filtered_followers(df, keywords):    
    df['filter'] = df.apply(lambda x: filterc(x, keywords), axis=1)
    fdf = df[df['filter']]
    fdf.reset_index(inplace=True)
    return fdf


def save_followers_to_csv(target_screen_name, keywords):
    df = get_target_followers(target_screen_name)
    fdf = get_filtered_followers(df, keywords)
    fdf.to_csv(target_screen_name + '_filtered_followers.csv')
    df.to_csv(target_screen_name + '_followers.csv')


def follow_users(filename, start_idx, end_idx):
    myfriends = api.GetFriendIDs()
    data = pd.read_csv(filename)
    for idx, row in data.iterrows():
        sname = row['screen_name']
        if idx < start_idx:
            continue
        if row['id'] not in myfriends:
        	try:
        		print(str.format('Following[{}]: {}', str(idx), sname))
        		api.CreateFriendship(screen_name=sname)
        		api.CreateMute(screen_name=sname)
        	except Exception as e:
        		print('Error: ' + str(e))
        	time.sleep((random.random() * 2) + 4)
        if idx > end_idx:
        	print('Done.')
        	break



# STEP 1:
# set your own account's api keys (top of the script, api = ...)

# STEP 2 :
# make sure you run this for an account that has only upto couple thousand followers
# because of sleep_on_rate_limint = True, it can take a really long time
# change target_screen_name and keywords accordingly (screen name is without @ sign)
target_screen_name = 'xyz_aus'
keywords = ['sydney', 'australia', 'melbourne', 'brisbane', 'south wales',
            'gold coast', 'victoria', 'vic', 'perth', 'canberra', 'adelaide', ' aus ']

# STEP 3:
# run save followers one time to save list of followers, uncomment below
# save_followers_to_csv(target_screen_name, keywords)


# STEP 4:
# run follow users for 100-200 users max at a time, 
# filename = 'xyz_aus_filtered_followers.csv'
# follow_users(filename, 0, 100)








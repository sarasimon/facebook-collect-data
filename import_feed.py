import urllib3
import facebook
import requests

# # Parameters of your app and the id of the profile you want to mess with.
# FACEBOOK_APP_ID = '128493641147023'
# FACEBOOK_APP_SECRET = '5a516ee5e97ed7515c9ace63ceb468e1'
# FACEBOOK_PROFILE_ID = '1471676833'

token = "EAAB03UHWIo8BAA8ZCtqmkR1z9ZBo0x1lNw9G49OmwzkPvBGtkT0JOGBEAqgPkquumBWbY3sXOsOazgsdmLWGlRyZB5EEAAMS3rJoDRxnXivCqeOwBJne15IAwwdQIYma2kVGvNHI7csNNqlAee13JtR9wfWxuMZD"
graph = facebook.GraphAPI(access_token=token, version=2.7)
page_id = '693720023971471'


def add_user_name(comments_list, user_id):
    if user_id in comments_list.keys():
        comments_list[user_id] += 1
    else:
        comments_list[user_id] = 1


def search_for_comments(comment_id, comments_list):
    try:
        # comments = graph.get_object(id=comment_id, fields='comments{from,comment_count}')
        comments = graph.get_connections(id=comment_id, connection_name='comments')
        count_single_users_comments(comments, comments_list)
    except KeyError:
        return


def count_single_users_comments(comments_dict, comments_list):
    # for comment in comments_dict:
    #     print comment
    #
    # add_user_name(comments_list, comments_dict['from']['name'])

    if 'comments' in comments_dict.keys():
        for comment in comments_dict['comments']['data']:
            user_id = comment['from']['name']
            add_user_name(comments_list, user_id)
            search_for_comments(comment['id'], comments_list)
            count_single_users_likes(comment['id'], comments_list)


def count_single_users_likes(message_id, comments_list):
    try:
        likes = graph.get_all_connections(id=message_id, connection_name='likes')
        for like in likes:
            add_user_name(comments_list, like['name'])
    except KeyError:
        return


def count_members():
    members = graph.get_all_connections(id=page_id, connection_name='members')
    return list(members)


def search_active_users(since, until):
    feed = graph.get_all_connections(id=page_id, connection_name='feed',
                                     fields='id,comments{id,from,likes},from,likes,created_time',
                                     since=since, until=until)
    active_users_list = {}
    for post in feed:
        message_id = post['id']
        user_id = post['from']['name']
        add_user_name(active_users_list, user_id)
        count_single_users_likes(message_id, active_users_list)
        count_single_users_comments(post, active_users_list)

    print(active_users_list)
    return active_users_list

    # print('Active users: ' + str(len(active_users_list)))

search_active_users('2017-10-29', '2017-10-30')

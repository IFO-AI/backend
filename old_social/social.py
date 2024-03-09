from mastodon import Mastodon

from mastodon import Mastodon
SCOPES_TO_REQUEST = ['read', 'write', 'follow', 'push']

mastodon = Mastodon(client_id = 'BJCDDO2Wd0Xx_9IGfvwWWRuVEw57b2cx3fVt5mGod9k', client_secret="6K1hlKrMSSoyuioTD8LSLW4p2YRBrL6pHrkVoB6_AXU", api_base_url ="https://mastodon.social", access_token="hSr_ylX-hXLaDYDipc07a06wGorDop4fzbRnkOwzFN0")

# mastodon.log_in(
#     'jubel8180@gmail.com',
#     'incrediblygoodpassword',
#     to_file = 'pytooter_usercred.secret'
# )


# mastodon = Mastodon(access_token = 'hSr_ylX-hXLaDYDipc07a06wGorDop4fzbRnkOwzFN0')
data = mastodon.toot('Tooting from Python using #mastodonpy !')
# print(data)
# mastodon.timeline_home()

       